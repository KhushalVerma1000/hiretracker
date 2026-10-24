import { Resend } from "resend";
import { esc, oneLine } from "./validate.js";

const brand = () => process.env.BRAND_NAME || "JopUP";
const site = () => process.env.SITE_ORIGIN || "";

export async function sendLeadEmails(lead) {
  const resend = new Resend(process.env.RESEND_API_KEY);
  const from = process.env.RESEND_FROM; // e.g. "JopUP <hello@yourdomain.com>" (domain verified in Resend)
  const to = process.env.LEAD_NOTIFY_TO;
  const rows = [["Name", lead.name], ["Email", lead.email], ["Phone", lead.phone], ["Company", lead.company], ["Role", lead.role],
    ["Company type", lead.companyType], ["Team size", lead.teamSize], ["Challenge", lead.challenge || "-"],
    ["Source", [lead.utmSource, lead.utmMedium, lead.utmCampaign].filter(Boolean).join(" / ") || "direct"]];
  const table = rows.map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0"><b>${esc(k)}</b></td><td>${esc(v)}</td></tr>`).join("");
  const owner = resend.emails.send({
    from, to: to.split(",").map((s) => s.trim()), replyTo: lead.email,
    subject: `New trial request: ${oneLine(lead.company)} (${oneLine(lead.name)})`,
    html: `<p>New free-trial request on ${esc(brand())}.</p><table>${table}</table>`,
    text: rows.map(([k, v]) => `${k}: ${v}`).join("\n"),
  });
  const first = esc(oneLine(lead.name).split(" ")[0]);
  const terms = site() ? `${site()}/terms/` : "";
  const confirm = resend.emails.send({
    from, to: [lead.email],
    subject: `Your ${oneLine(brand())} free trial request`,
    html: `<p>Hi ${first},</p><p>Thanks for requesting a free trial of ${esc(brand())}. We have your details and will be in touch shortly to get you set up.</p>
<p>We are also reviewing every request to choose companies for 3 months free, and we will tell you by email if yours is selected. ${terms ? `Offer terms: <a href="${esc(terms)}">${esc(terms)}</a>.` : ""}</p>
<p>If you did not make this request, ignore this email and we will not contact you again.</p><p>${esc(brand())}</p>`,
    text: `Hi ${oneLine(lead.name).split(" ")[0]},\n\nThanks for requesting a free trial of ${brand()}. We will be in touch shortly.\nWe are also reviewing every request to choose companies for 3 months free and will tell you by email if yours is selected. ${terms}\n\nIf you did not make this request, ignore this email.\n${brand()}`,
  });
  const [a, b] = await Promise.allSettled([owner, confirm]);
  return { notified: a.status === "fulfilled" && !a.value?.error, confirmed: b.status === "fulfilled" && !b.value?.error };
}
