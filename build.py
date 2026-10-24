#!/usr/bin/env python3
"""Builds the static site into ./site  ->  python3 build.py
Edit CONFIG, rebuild, commit. Empty values show as yellow [placeholders] on the legal pages."""
import os, re, shutil, html as H

COMPANY_TYPES = ["Staffing / placement agency", "Manpower / outsourcing firm", "In-house HR team", "Other"]
TEAM_SIZES = ["1-5 recruiters", "6-20 recruiters", "21-50 recruiters", "50+ recruiters"]

CONFIG = dict(
    NAME="HireTracker",            # product name (must match the OAuth consent screen exactly)
    ACCENT="Tracker",             # part of the logo shown in colour ("" for none)
    OLD_NAME="HireTrack",    # name baked into the source SVG screens (replaced at build)
    DOMAIN="https://hiretracker.in",  # PLACEHOLDER: set the domain you own
    EMAIL="",                # support / privacy contact on your own domain
    ENTITY="SUKRSH INFOTECH",               # legal entity that operates the product
    ADDRESS="C 229,KA-324, Pratap vihar,ghaziabad,201009",              # registered address (or city and country)
    LAW="India, courts at Ghaziabad",                  # governing law and courts, e.g. "India, courts at <city>"
    HOSTING="india,cloudflare",              # hosting country and provider, plus other sub-processors
    RETENTION="365 days",            # retention periods: account data, mail log, audit log, backups
    GRIEVANCE="codzentechnology@gmail.com",            # grievance / data-protection contact, if advised
    DATE="16 October 2026",  # policy effective / last-updated date
    VERSION="0.1",
    OFFER_ELIGIBILITY="Recruitment companies or companies with a minimum of 4 recruiters",    # who may apply (country, business users, one request per email)
    OFFER_CRITERIA="what match our internal checklist",       # how you select companies for the 3 free months (e.g. fit, team size, readiness)
    OFFER_DECISION="We will notify selected companies within 2 weeks of submission.",       # how many companies are selected and when you tell applicants
)
C = CONFIG
OUT = "site"
UNFILLED = set()

def v(key):
    if C[key]:
        return H.escape(C[key])
    UNFILLED.add(key)
    return f"<mark>[{key.title().replace('_', ' ')}]</mark>"

def sub(s):
    s = s.replace("mailto:%EMAIL%", "mailto:" + (C["EMAIL"] or "contact@example.com"))
    s = s.replace("%NAME%", H.escape(C["NAME"])).replace("%DOMAIN%", C["DOMAIN"])
    return re.sub(r"%([A-Z_]+)%", lambda m: v(m.group(1)) if m.group(1) in C else m.group(0), s)

def logo():
    n, a = C["NAME"], C["ACCENT"]
    return (H.escape(n[:-len(a)]) + f"<b>{H.escape(a)}</b>") if a and n.endswith(a) else H.escape(n)

def page(path, title, desc, body, extra_head="", index=True):
    url = C["DOMAIN"] + path
    robots = "" if index else '<meta name="robots" content="noindex">'
    mail = C["EMAIL"] or "contact@example.com"
    return sub(f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(title)}</title><meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{url}">{robots}<meta name="theme-color" content="#3D4FC4">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="%NAME%">
<meta property="og:title" content="{H.escape(title)}"><meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{C["DOMAIN"]}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css"><script>{BOOT}</script>{extra_head}</head><body>
<nav aria-label="Main"><div class="w"><a class="logo" href="/" style="text-decoration:none;color:inherit">{logo()}</a>
<div class="links"><a href="/#features">Features</a><a href="/#how">How it works</a><a href="/#faq">FAQ</a><a class="btn" href="/#trial">Start free trial</a></div></div></nav>
<main>{body}</main>
<footer><div class="w"><span>© %NAME% · %ENTITY%</span><div class="fl2"><a href="/privacy/">Privacy Policy</a><a href="/terms/">Terms of Service</a><a href="/contact/">Contact</a><a href="https://www.sukrshinfotech.com" rel="noopener">Sukrsh Infotech</a><a href="https://www.codzentechnology.com" rel="noopener">Codzen Technology</a></div></div></footer>
<script src="/assets/site.js" defer></script><script src="/assets/form.js" defer></script></body></html>''')

def img(name, alt, **kw):
    a = " ".join(f'{k}="{v_}"' for k, v_ in kw.items())
    return f'<img src="/assets/{name}.svg" data-restart="/assets/{name}.svg" alt="{alt}" {a}>'

def row(cls, eyebrow, h2, sub_, items, name, alt, d, zoom, ph=False):
    lis = "".join(f"<li>{i}</li>" for i in items)
    fr = f'<div class="frame{" ph" if ph else ""}" data-dir="{d}"><{"img"} src="/assets/{name}.svg" data-restart="/assets/{name}.svg" alt="{alt}" loading="lazy" width="{420 if ph else 960}" height="{760 if ph else 600}"></div>'
    if ph:
        fr = f'<div class="fl">{fr}</div>'
    return f'<div class="row {cls}"><div class="txt"><div class="eyebrow">{eyebrow}</div><h2>{h2}</h2><p class="sub">{sub_}</p><ul class="c">{lis}</ul></div>{fr}</div>'


BOOT = "document.documentElement.classList.add('js')"
def companies():
    return ('<section class="alt" aria-labelledby="co"><div class="w"><h2 id="co">The companies behind %NAME%</h2><div class="grid">'
    '<div class="card"><h3>Codzen Technology</h3><p>Builds B2B SaaS platforms, automation and custom web applications for business and corporate clients.</p><p><a href="https://www.codzentechnology.com" rel="noopener">www.codzentechnology.com</a></p></div>'
    '<div class="card"><h3>Sukrsh Infotech Private Limited</h3><p>A manpower outsourcing and placement company registered in Ghaziabad, Uttar Pradesh, serving organisations across Delhi NCR.</p><p><a href="https://www.sukrshinfotech.com" rel="noopener">www.sukrshinfotech.com</a></p></div></div></div></section>')

def form_html():
    opt = lambda xs: '<option value="">Select</option>' + "".join(f"<option>{H.escape(x)}</option>" for x in xs)
    def fld(n, label, typ="text", ac="", extra="", full=False):
        return f'<div class="f{" full" if full else ""}"><label for="f-{n}">{label}</label><input id="f-{n}" name="{n}" type="{typ}" autocomplete="{ac}" required {extra}><span class="err" data-err="{n}"></span></div>'
    sel = lambda n, label, xs: f'<div class="f"><label for="f-{n}">{label}</label><select id="f-{n}" name="{n}" required>{opt(xs)}</select><span class="err" data-err="{n}"></span></div>'
    return ('<form id="lead-form" class="form" method="post" action="/api/lead">'
      + fld("name", "Full name", ac="name", extra='maxlength="100"') + fld("email", "Work email", "email", "email", 'maxlength="254"')
      + fld("phone", "Phone / WhatsApp", "tel", "tel", 'maxlength="20"') + fld("company", "Company name", ac="organization", extra='maxlength="120"')
      + fld("role", "Your role", ac="organization-title", extra='maxlength="80"') + sel("companyType", "Company type", COMPANY_TYPES) + sel("teamSize", "Recruiters in your team", TEAM_SIZES)
      + '<div class="f full"><label for="f-challenge">Biggest hiring challenge (optional)</label><textarea id="f-challenge" name="challenge" maxlength="600"></textarea><span class="err" data-err="challenge"></span></div>'
      + '<div class="hp" aria-hidden="true"><label>Leave this empty<input name="hp" tabindex="-1" autocomplete="off"></label></div>'
      + '<div class="f full"><label class="chk"><input type="checkbox" name="consent" required><span>I agree to be contacted about my free trial, understand my request will be reviewed for the 3-months-free offer, and accept the <a href="/privacy/">Privacy Policy</a> and the <a href="/terms/#offer">offer terms</a>.</span></label><span class="err" data-err="consent"></span></div>'
      + '<div class="f full"><button class="btn" type="submit">Start free trial</button><p class="status" role="status" aria-live="polite"></p></div></form>')

def landing():
    faq = [
        ("What is %NAME%?", "%NAME% is recruitment tracking software for staffing, placement and manpower agencies and in-house HR teams. It brings resume parsing, the daily candidate line-up, client and role tracking, and recruiter performance reporting into one workspace."),
        ("Can I import resumes in bulk?", "Yes. Upload resumes as PDF, Word files or photos and %NAME% reads each one and fills in the candidate profile for you, so you are not retyping details."),
        ("Does %NAME% work for agencies with many clients?", "Yes. Track every client and open position side by side, give each recruiter their own line-up, and see performance per recruiter and per client."),
        ("Does %NAME% read my email?", "No. If you connect Gmail or Outlook, %NAME% asks for send-only permission. It sends a message only when you click Send, and it cannot read, list, search or delete anything in your mailbox. You can disconnect at any time."),
        ("How is candidate data handled?", "Your agency decides what candidate data to enter, and %NAME% processes it on your behalf. See our <a href=\"/privacy/\">Privacy Policy</a> for what we store, how it is protected and how to request deletion."),
    ]
    faqh = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    body = f'''<header class="hero"><div class="w"><span class="tag">Free trial · 3 months free for selected companies</span>
<h1>Track every candidate, from resume to joining</h1>
<p class="lead">%NAME% is the recruitment workbench for staffing and placement agencies: parse resumes in bulk, run your daily line-up, update clients and see which recruiters are really closing.</p>
<div class="cta"><a class="btn" href="#trial">Start free trial</a><a class="btn o" href="#features">See how it works</a></div><p class="offer">Request a free trial. We review every request and select companies for <b>3 months free</b>. <a href="/terms/#offer">Offer terms</a></p>
<div class="stage" id="stage"><div class="aurora"></div>
<div class="chip" style="left:1%;top:16%"><span><i></i>Resume parsed</span></div><div class="chip" style="right:0;top:36%"><span><i></i>Line-up ready</span></div><div class="chip" style="left:6%;bottom:9%"><span><i></i>Interview scheduled</span></div>
<div class="zw" id="hz"><div class="tl" id="ht"><div class="shot"><img src="/assets/product-view.svg" alt="%NAME% recruitment workbench showing today's candidate line-up" width="960" height="600" fetchpriority="high"></div></div></div></div></div></header>
<section id="features" aria-labelledby="ft"><div class="w"><h2 id="ft" style="text-align:center;max-width:720px;margin:0 auto 64px">Everything a recruitment team needs in one place</h2>
{row("", "Resume parser", "Parse resumes in bulk and skip the typing", "Drop in a batch of PDFs, Word files or phone photos. %NAME% reads each resume and builds the candidate profile, so your recruiters spend time calling, not copying.", ["Import up to 100 resumes at a time", "Works with PDF, Word and photos", "Candidates ready to call in minutes"], "resume-parser", "Resume parser importing several resumes into candidate profiles", 1, "")}
{row("r", "Stage automation", "Hiring stages that move on their own", "Set up your stages once. %NAME% keeps candidates flowing through screening, line-up and interview, and tells your team what needs attention next.", ["Configurable hiring stages", "Fewer manual status updates", "Consistent follow-up across every recruiter"], "automation", "Recruitment stage automation rules moving candidates through the pipeline", -1, "")}
{row("", "Recruiter analytics", "Know which recruiters and clients are delivering", "See placements, pipeline bottlenecks and recruiter performance in one dashboard instead of stitching spreadsheets together.", ["Recruiter-level performance tracking", "Pipeline bottlenecks at a glance", "Client-ready reporting"], "analytics", "Recruitment analytics dashboard showing placements and recruiter performance", 1, "")}
{row("r", "Mobile", "Your daily line-up, in your pocket", "Recruiters work from the phone. Mark candidates reached, schedule interviews and send updates wherever the day takes them.", ["Today's line-up with live counts", "One-tap status updates", "Schedule interviews on the go"], "mobile", "Mobile recruitment app showing today's candidate line-up", -1, "", True)}
</div></section>
<section class="alt" aria-labelledby="em"><div class="w"><div class="mail"><div class="eyebrow">Email</div><h2 id="em">Send client updates from your own Gmail or Outlook</h2>
<p class="sub">Connect your mailbox with send-only access. Clients see your familiar address and replies come straight to you. %NAME% sends only when you click Send and never reads your inbox. Disconnect whenever you like. Read the <a href="/privacy/">Privacy Policy</a>.</p></div></div></section>
<section id="how" aria-labelledby="hw"><div class="w"><h2 id="hw" style="text-align:center">How %NAME% works</h2>
<div class="steps"><div class="card"><h3>Add clients and roles</h3><p>Set up the clients you serve, their open positions and your hiring stages.</p></div>
<div class="card"><h3>Import resumes, build the line-up</h3><p>Parse resumes in bulk and plan each recruiter's daily line-up.</p></div>
<div class="card"><h3>Track, update, report</h3><p>Move candidates through stages, email clients and review performance.</p></div></div></div></section>
<section class="alt" aria-labelledby="who"><div class="w"><h2 id="who">Built for recruitment teams of every size</h2>
<div class="grid"><div class="card"><h3>Staffing and placement agencies</h3><p>Run many clients and roles with a clear view per recruiter.</p></div>
<div class="card"><h3>Manpower and outsourcing firms</h3><p>Keep candidate sourcing, line-ups and joinings organised.</p></div>
<div class="card"><h3>In-house HR teams</h3><p>Track hiring across departments without a spreadsheet maze.</p></div></div></div></section>
<section id="faq" aria-labelledby="fq"><div class="w" style="max-width:760px"><h2 id="fq">Frequently asked questions</h2>{faqh}</div></section>
<section id="trial" aria-labelledby="tr"><div class="w trial"><div><div class="eyebrow">Free trial</div><h2 id="tr">Start your free trial</h2><p class="sub">Tell us about your team and we will set you up. We review every request and select companies to receive <b>3 months free</b>.</p><ul class="c"><li>Parse resumes in bulk</li><li>Run your daily line-up</li><li>Track recruiter performance</li></ul><p class="offer"><a href="/terms/#offer">Offer terms apply</a>.</p></div>{form_html()}</div></section>
{companies()}'''
    ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"SoftwareApplication","name":"%NAME%","url":"%DOMAIN%/","applicationCategory":"BusinessApplication","operatingSystem":"Web","description":"Recruitment tracking software for staffing and placement agencies and HR teams: resume parsing, daily line-up, stage automation and recruiter analytics."},{"@type":"Organization","name":"%NAME%","url":"%DOMAIN%/","logo":"%DOMAIN%/assets/logo.svg"}]}</script>'''
    t = "%NAME% | Recruitment Tracking Software for Agencies"
    d = "%NAME% is recruitment tracking software for staffing and placement agencies. Request a free trial; selected companies get 3 months free. Parse resumes, run your daily line-up and track every candidate."
    return page("/", sub(t), sub(d), body, ld)

def doc(path, title, desc, inner):
    body = f'<article class="doc"><h1>{title}</h1><p class="meta">Effective %DATE% · Version %VERSION% · {{op}}</p>{inner}</article>'.replace("{op}", "%ENTITY%")
    return page(path, f"{title} | %NAME%", desc, body)

PRIVACY = '''
<h2>1. Who we are</h2><p>%NAME% is operated by %ENTITY%, %ADDRESS%. Contact: <a href="mailto:%EMAIL%">%EMAIL%</a>. Grievance / data-protection contact: %GRIEVANCE%.</p>
<h2>2. Who this policy covers</h2><p>(a) Staff users of the agencies and companies that use %NAME% ("customers"); (b) candidates whose details customers enter; (c) visitors to this website.</p>
<h2>3. Our role</h2><p>The customer decides what candidate and client data to enter and why. %NAME% processes that data on the customer's behalf and instructions. Candidates who want access, correction or deletion should contact the agency that holds their data first. If you cannot reach them, write to us at %EMAIL% and we will help.</p>
<h2>4. Data we collect</h2><ul><li><b>Account data:</b> name, work email, phone, role, organisation, and a password hash (never the password).</li>
<li><b>Customer-entered data:</b> candidate names, contact details, resumes, employment details, pipeline stage and notes; client contacts and open positions.</li>
<li><b>Trial requests and enquiries (website form):</b> name, work email, phone, company, role, company type, team size, an optional note, your consent, and campaign source if you arrived from a tracked link. We use it to contact you about your trial, review your request for the 3-months-free offer (our team reads each submission) and improve our marketing. Requests are stored in our database (Neon) and emailed through Resend. A hashed form of your IP address is kept briefly to stop abuse.</li>
<li><b>Usage and audit data:</b> login times, actions taken and IP address where logged.</li>
<li><b>Email-connection data</b> (only if you connect a mailbox): the connected email address, OAuth tokens, granted permissions, connection status, and a log of each message sent through the connection (time, recipients, subject, message ID; not the message body).</li></ul>
<p>We do not ask for, and customers should not enter without need, sensitive details such as caste, religion or health information.</p>
<h2>5. How we use data</h2><p>To provide and secure the service, give support and meet legal obligations. We do not sell personal data and we do not use it for advertising.</p>
<h2>6. Google user data</h2>
<p>If you choose to connect your Gmail account, %NAME% requests one mailbox permission, send-only: <code>https://www.googleapis.com/auth/gmail.send</code>. This lets %NAME% send an email from your Gmail address when you click Send. We do not request permission to read, list, search, modify or delete any email, draft, label, contact or attachment in your Gmail account. We also request the basic openid and email permissions, which only tell us which Gmail address you connected.</p>
<p><b>What we access and store.</b> When you connect, we store your Gmail address, the OAuth refresh token (encrypted at rest), the permissions you granted and the connection status. For each email you send through the connection we keep a record of the time, recipients, subject and message ID. We do not store the contents of your Gmail mailbox.</p>
<p><b>How we use it.</b> Only to send the emails you ask us to send, from your own address, when you click Send in %NAME%. Each send is a single message triggered by you. We never send mail automatically through your account.</p>
<p><b>Sharing.</b> We do not sell, rent or share Google user data. We do not transfer it to others except as necessary to provide the send feature you asked for, to comply with law, or for security. We do not use it for advertising, including retargeting or interest-based advertising.</p>
<p><b>Human access.</b> Our staff do not read your data. We access it only with your explicit consent for a specific item, where needed for security, or where the law requires it.</p>
<p><b>Disconnecting and deletion.</b> You can disconnect at any time in Settings, Email accounts. We then revoke the token with Google where possible and delete the stored connection. You can also remove %NAME%'s access at <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>. To have remaining records deleted, email %EMAIL%.</p>
<p>%NAME%'s use and transfer of information received from Google APIs will adhere to the <a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>, including the Limited Use requirements.</p>
<h2>7. Microsoft user data</h2><p>If you connect Outlook or Microsoft 365, %NAME% requests the delegated permissions <code>Mail.Send</code> and <code>offline_access</code>, plus basic openid and email permissions that only identify the connected mailbox. We do not request read access to your mailbox and do not use application permissions. We store the connected address, the granted permissions, the connection status and the latest refresh token (encrypted at rest; Microsoft rotates it on use). We keep the same send log as above and never the message body. Use is limited to sending messages you ask us to send; we do not sell or share this data or use it for advertising. You can disconnect in Settings, Email accounts, or remove access at <a href="https://myaccount.microsoft.com">myaccount.microsoft.com</a>.</p>
<h2>8. Sharing and sub-processors</h2><p>We share data only with providers that help us run the service: Resend (email), Neon (database) and %HOSTING%. We do not sell personal data.</p>
<h2>9. Storage, security and retention</h2><p>Data is encrypted in transit, OAuth refresh tokens are encrypted at rest, and access is controlled per organisation. Retention: %RETENTION%.</p>
<h2>10. Deleting data and disconnecting</h2><p>Disconnect a mailbox in Settings, Email accounts: the token is revoked with the provider where possible and then deleted. To request account or data deletion, email %EMAIL%.</p>
<h2>11. Your rights</h2><p>You may ask to access, correct or delete your personal data, withdraw consent, or complain about how it is handled. Email %EMAIL% and we will respond within a reasonable time, and within any period the law sets.</p>
<h2>12. International transfers</h2><p>Data is hosted in: %HOSTING%. Where hosting or a sub-processor is outside your country, we rely on appropriate safeguards.</p>
<h2>13. Children</h2><p>%NAME% is for business users aged 18 or over and does not support recruitment of minors.</p>
<h2>14. Cookies</h2><p>This website uses only essential cookies and similar technologies needed to run the service. We do not use advertising cookies.</p>
<h2>15. Changes to this policy</h2><p>We will update this page and the date above when this policy changes and notify account holders of material changes. If we begin using a new type of Google user data, we will update this policy and ask for your consent again before accessing it.</p>
<h2>16. Contact and grievances</h2><p>%ENTITY%, %ADDRESS%. <a href="mailto:%EMAIL%">%EMAIL%</a>. Grievance contact: %GRIEVANCE%.</p>'''

TERMS = '''
<h2>1. Agreement and eligibility</h2><p>These terms are between %ENTITY% ("we") and the business that uses %NAME% ("you"). By using the service you accept them. The service is for business users aged 18 or over.</p>
<h2>2. The service and beta</h2><p>%NAME% is recruitment tracking software. Features may change, and beta features carry no uptime commitment.</p>
<h2>3. Accounts</h2><p>Organisation admins are responsible for their users and for keeping credentials safe.</p>
<h2>4. Customer data and roles</h2><p>You own your data. You are responsible for having a lawful basis, and any required consent, to enter candidate data. We process it on your instructions as described in the <a href="/privacy/">Privacy Policy</a>.</p>
<h2>5. Acceptable use</h2><p>No spam, unsolicited bulk email, unlawful or discriminatory use, scraping, or attempts to breach security. The email feature sends one message per click; bulk sending through connected mailboxes is not allowed.</p>
<h2>6. Connected email accounts</h2><p>You authorise %NAME% to send from your own address when you click Send. You are responsible for what you send, you can disconnect at any time, and the provider's own terms (Google, Microsoft) also apply.</p>
<h2>7. Fees</h2><p>Free during beta unless we agree otherwise in writing. We will give notice before any charges begin.</p>
<h2>8. Intellectual property</h2><p>We own the service. You grant us a licence to use your data only to run the service for you.</p>
<h2>9. Confidentiality and security</h2><p>We protect your data as described in the <a href="/privacy/">Privacy Policy</a>.</p>
<h2>10. Suspension and termination</h2><p>Either party may end the agreement. We may suspend accounts that break these terms. After termination you may export your data for a limited period, after which we delete it.</p>
<h2>11. Disclaimers and liability</h2><p>The service is provided as is during beta. To the extent the law allows, our liability is limited and you indemnify us for your misuse of the service.</p>
<h2>12. Governing law and contact</h2><p>These terms are governed by the laws of %LAW%. We may update them and will post the new date here. Contact: <a href="mailto:%EMAIL%">%EMAIL%</a>.</p>
<h2 id="offer">13. Free trial and 3-months-free offer</h2><p>Anyone eligible may request a free trial. Separately, we review each request and select some companies to receive 3 months free use of %NAME%. This is a discretionary selection, not a draw or lottery. Eligibility: %OFFER_ELIGIBILITY%. How we select: %OFFER_CRITERIA%. Numbers and timing: %OFFER_DECISION%. Selected companies are told by email. Submitting a request does not guarantee selection, the offer has no cash value and is not transferable, and our decision is final. We may change or end the offer, and false, duplicate or automated requests are void. One request per business email address.</p>'''

def build():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/assets")
    for f in os.listdir("src"):
        p = "src/" + f
        if f.endswith(".svg"):
            s = open(p).read().replace(C["OLD_NAME"], C["NAME"])
            open(f"{OUT}/assets/{f.replace('hiretrack-', '')}", "w").write(s)
        else:
            shutil.copy(p, f"{OUT}/assets/{f}")
    n, a = C["NAME"], C["ACCENT"]
    logo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><rect width="120" height="120" rx="26" fill="#3D4FC4"/><text x="60" y="78" font-family="Arial,sans-serif" font-size="56" font-weight="700" fill="#fff" text-anchor="middle">{H.escape(n[0])}</text></svg>'
    open(f"{OUT}/assets/logo.svg", "w").write(logo_svg)
    og = f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#3D4FC4"/><text x="80" y="300" font-family="Arial,sans-serif" font-size="110" font-weight="700" fill="#fff">{H.escape(n)}</text><text x="80" y="380" font-family="Arial,sans-serif" font-size="40" fill="#DDE1FF">Recruitment tracking software for agencies</text></svg>'
    open("src_og.svg", "w").write(og)
    pages = {
        "index.html": landing(),
        "privacy/index.html": doc("/privacy/", "Privacy Policy", "How %NAME% collects, uses, stores and protects data, including Google and Microsoft user data.".replace("%NAME%", n), PRIVACY),
        "terms/index.html": doc("/terms/", "Terms of Service", "The terms for using %NAME% recruitment tracking software.".replace("%NAME%", n), TERMS),
        "contact/index.html": page("/contact/", f"Contact | {n}", f"Contact {n} for support, privacy requests and demos.", '<article class="doc"><h1>Contact</h1><p>For support, privacy requests or data deletion, email <a href="mailto:%EMAIL%">%EMAIL%</a>. To start a free trial, use the form below.</p><p>%ENTITY%<br>%ADDRESS%</p><p>Grievance contact: %GRIEVANCE%</p></article><div class="w" style="max-width:820px;padding-bottom:56px">' + form_html() + '</div>' + companies()),
    }
    for p, c in pages.items():
        os.makedirs(os.path.dirname(f"{OUT}/{p}") or OUT, exist_ok=True)
        open(f"{OUT}/{p}", "w").write(c)
    d = C["DOMAIN"]
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {d}/sitemap.xml\n")
    open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{d}{u}</loc></url>" for u in ["/", "/privacy/", "/terms/", "/contact/"]) + "</urlset>")
    import hashlib, base64, json
    h = base64.b64encode(hashlib.sha256(BOOT.encode()).digest()).decode()
    csp = f"default-src 'self'; script-src 'self' 'sha256-{h}'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests"
    hdr = lambda k, v: {"key": k, "value": v}
    cfg = {"outputDirectory": "site", "buildCommand": "prisma generate", "trailingSlash": True,
      "headers": [{"source": "/(.*)", "headers": [hdr("Content-Security-Policy", csp), hdr("Strict-Transport-Security", "max-age=31536000; includeSubDomains"), hdr("X-Content-Type-Options", "nosniff"), hdr("X-Frame-Options", "DENY"), hdr("Referrer-Policy", "strict-origin-when-cross-origin"), hdr("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()"), hdr("Cross-Origin-Opener-Policy", "same-origin")]},
                  {"source": "/api/(.*)", "headers": [hdr("Cache-Control", "no-store")]}]}
    open("vercel.json", "w").write(json.dumps(cfg, indent=2))
    print("Built ->", OUT, "| unfilled placeholders:", ", ".join(sorted(UNFILLED)) or "none")

build()
