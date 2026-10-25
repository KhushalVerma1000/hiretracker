import test from "node:test";
import assert from "node:assert/strict";
import { validateLead, esc, oneLine } from "../lib/validate.js";

const ok = { name: "Asha Rao", email: "ASHA@Example.com ", phone: "+91 98765 43210", company: "Acme Staffing", role: "Founder",
  companyType: "Staffing / placement agency", teamSize: "6-20 recruiters", consent: true, ts: Date.now() - 5000 };
test("accepts and normalises a valid lead", () => {
  const r = validateLead(ok); assert.ok(r.ok); assert.equal(r.data.email, "asha@example.com");
});
test("rejects missing consent, bad phone, bad enum, long text", () => {
  for (const bad of [{ consent: false }, { phone: "abc" }, { companyType: "x" }, { challenge: "a".repeat(601) }, { email: "nope" }])
    assert.ok(!validateLead({ ...ok, ...bad }).ok);
});
test("escapes HTML and strips newlines for subjects", () => {
  assert.equal(esc('<img onerror="x">'), "&lt;img onerror=&quot;x&quot;&gt;");
  assert.equal(oneLine("a\r\nBcc: evil@x.com"), "a Bcc: evil@x.com");
});
