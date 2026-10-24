export const COMPANY_TYPES = ["Staffing / placement agency", "Manpower / outsourcing firm", "In-house HR team", "Other"];
export const TEAM_SIZES = ["1-5 recruiters", "6-20 recruiters", "21-50 recruiters", "50+ recruiters"];

const clean = (s) => s.replace(/[\u0000-\u001f\u007f]+/g, " ").replace(/\s+/g, " ").trim();
const EMAIL = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[A-Za-z]{2,}$/;
const PHONE = /^\+?[0-9 ()\-]{7,20}$/;
const UTM = /^[\w.\-+ %]{0,100}$/;

/** Returns { ok, data, errors }. Only plain strings/numbers/booleans are accepted; unknown keys are dropped. */
export function validateLead(raw) {
  const e = {}, d = {};
  const str = (k, min, max, msg) => {
    const v = typeof raw[k] === "string" ? clean(raw[k]) : "";
    if (v.length < min || v.length > max) e[k] = msg; else d[k] = v;
  };
  str("name", 2, 100, "Enter your name");
  str("company", 2, 120, "Enter your company name");
  str("role", 2, 80, "Enter your role");
  const email = typeof raw.email === "string" ? raw.email.trim().toLowerCase() : "";
  if (email.length > 254 || !EMAIL.test(email)) e.email = "Enter a valid work email"; else d.email = email;
  const phone = typeof raw.phone === "string" ? raw.phone.trim() : "";
  if (!PHONE.test(phone)) e.phone = "Enter a valid phone number"; else d.phone = phone;
  if (!COMPANY_TYPES.includes(raw.companyType)) e.companyType = "Choose one"; else d.companyType = raw.companyType;
  if (!TEAM_SIZES.includes(raw.teamSize)) e.teamSize = "Choose one"; else d.teamSize = raw.teamSize;
  if (raw.challenge != null && raw.challenge !== "") {
    if (typeof raw.challenge !== "string" || raw.challenge.length > 600) e.challenge = "Keep this under 600 characters";
    else d.challenge = raw.challenge.replace(/\u0000/g, "").trim();
  }
  if (raw.consent !== true) e.consent = "Please tick the box to continue";
  for (const k of ["utmSource", "utmMedium", "utmCampaign"])
    if (typeof raw[k] === "string" && raw[k] !== "" && UTM.test(raw[k])) d[k] = raw[k];
  d.ts = Number.isInteger(raw.ts) ? raw.ts : 0;
  d.hp = typeof raw.hp === "string" ? raw.hp.slice(0, 200) : "";
  d.consent = raw.consent === true;
  return { ok: Object.keys(e).length === 0, data: d, errors: e };
}

export const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export const oneLine = (s) => String(s ?? "").replace(/[\r\n\u0000-\u001f]+/g, " ").slice(0, 100);
