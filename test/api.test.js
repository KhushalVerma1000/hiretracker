import test from "node:test";
import assert from "node:assert/strict";
process.env.SITE_ORIGIN = "https://site.test";
const { default: handler } = await import("../api/lead.js");
const run = async (req) => { let out; const res = { headers: {}, setHeader(k, v) { this.headers[k] = v; }, status(c) { this.code = c; return this; }, json(b) { out = b; return this; } };
  await handler({ method: "POST", headers: { origin: "https://site.test", "content-type": "application/json" }, body: {}, socket: {}, ...req }, res); return { code: res.code, out }; };
const ok = { name: "Asha Rao", email: "a@b.co", phone: "+91 98765 43210", company: "Acme", role: "CEO", companyType: "Other", teamSize: "1-5 recruiters", consent: true };
test("rejects wrong method, origin and content-type", async () => {
  assert.equal((await run({ method: "GET" })).code, 405);
  assert.equal((await run({ headers: { origin: "https://evil.test", "content-type": "application/json" } })).code, 403);
  assert.equal((await run({ headers: { origin: "https://site.test", "content-type": "text/plain" } })).code, 415);
});
test("rejects invalid input and short fill time; honeypot returns fake success without DB", async () => {
  assert.equal((await run({ body: { ...ok, email: "x", ts: Date.now() - 9000 } })).code, 400);
  assert.equal((await run({ body: { ...ok, ts: Date.now() } })).code, 400);
  const bot = await run({ body: { ...ok, ts: Date.now() - 9000, hp: "spam" } }); assert.equal(bot.code, 200);
});
