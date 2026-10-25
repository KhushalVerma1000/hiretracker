import crypto from "node:crypto";
import { db } from "../lib/db.js";
import { validateLead } from "../lib/validate.js";
import { sendLeadEmails } from "../lib/emails.js";

const WINDOW_MS = 10 * 60 * 1000, MAX_ATTEMPTS = 5;
const json = (res, code, body) => { res.setHeader("Cache-Control", "no-store"); res.status(code).json(body); };

function originOk(req) {
  const allowed = (process.env.SITE_ORIGIN || "").replace(/\/$/, "");
  const o = req.headers.origin;
  return Boolean(allowed) && o === allowed;
}

export default async function handler(req, res) {
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return json(res, 405, { ok: false }); }
  if (!originOk(req)) return json(res, 403, { ok: false });
  if (!String(req.headers["content-type"] || "").startsWith("application/json")) return json(res, 415, { ok: false });
  const raw = req.body;
  if (!raw || typeof raw !== "object" || JSON.stringify(raw).length > 8000) return json(res, 400, { ok: false });

  const ip = String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "").split(",")[0].trim();
  const ipHash = crypto.createHash("sha256").update(ip + (process.env.IP_HASH_SALT || "")).digest("hex");

  const parsed = validateLead(raw);
  if (!parsed.ok) return json(res, 400, { ok: false, errors: parsed.errors });
  const d = parsed.data;
  if (d.hp) return json(res, 200, { ok: true }); // bot: pretend success, store nothing
  const age = Date.now() - d.ts;
  if (age < 2500 || age > 24 * 3600 * 1000) return json(res, 400, { ok: false, errors: { form: "Please try again." } });

  try {
    const prisma = db();
    const recent = await prisma.attempt.count({ where: { ipHash, createdAt: { gt: new Date(Date.now() - WINDOW_MS) } } });
    if (recent >= MAX_ATTEMPTS) return json(res, 429, { ok: false, error: "Too many attempts. Please try again later." });
    await prisma.attempt.create({ data: { ipHash } });
    if (Math.random() < 0.02) await prisma.attempt.deleteMany({ where: { createdAt: { lt: new Date(Date.now() - 24 * 3600 * 1000) } } });

    const { ts, hp, consent, ...rest } = d;
    const data = { ...rest, consent: true, consentAt: new Date() };
    // Repeat submissions get the same success reply but change nothing and send nothing: this stops
    // anyone overwriting another person's record or using the form to mail-bomb an address.
    const existing = await prisma.lead.findUnique({ where: { email: d.email }, select: { id: true } });
    if (existing) return json(res, 200, { ok: true });
    const lead = await prisma.lead.create({ data });
    const sent = await sendLeadEmails(lead).catch(() => ({ notified: false, confirmed: false }));
    await prisma.lead.update({ where: { id: lead.id }, data: sent });
    return json(res, 200, { ok: true });
  } catch (e) {
    // Never log request data. Start-up errors carry no user data, so their (credential-redacted) message is safe to log.
    const detail = e?.name === "PrismaClientInitializationError"
      ? String(e.message || "").replace(/(postgres(?:ql)?:\/\/)[^@\s]+@/gi, "$1***@").replace(/\s+/g, " ").slice(0, 400) : "";
    console.error("lead handler failed:", e?.name, e?.errorCode || e?.code, detail);
    return json(res, 500, { ok: false, error: "Something went wrong. Please try again." });
  }
}
