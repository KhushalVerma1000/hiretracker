# Security audit: landing site, trial form, Neon + Prisma + Resend
Date: 24 Oct 2026. Scope: the code in this folder only. Not covered: your Neon project, Resend account, DNS or hosting settings, the main app, or a live penetration test.

## What was run
- `npm audit` on dependencies; static checks on the built site (inline handlers, `javascript:` links, `target=_blank`, external links without `rel=noopener`, inline scripts, committed secrets); 5 automated tests on the validator and the API handler (method, origin, content-type, invalid input, fill-time check, honeypot).
- Not run here (network blocked): `prisma generate`, a real database write, a real Resend send. Test these once on a preview deployment.

## Findings
| # | Severity | Finding | Status |
|---|---|---|---|
| 1 | High (dependency) | `zod` < 4.6.6 memory-exhaustion advisory | **Fixed**: removed zod, replaced by a small hand-written validator with strict length and type limits |
| 2 | High (advisory, dev-time) | `deepmerge-ts` via Prisma CLI 6.x (`@prisma/config`): stack exhaustion when merging recursive objects | **Open, low real risk**: runs only in the Prisma CLI at build time on your own schema, never on user input. The fix is Prisma 7 (breaking: driver adapter + `prisma.config.ts`). Plan the upgrade; re-run `npm audit` |
| 3 | Medium | Form could overwrite another person's lead by re-submitting their email | **Fixed**: repeat emails get the same success reply but change and send nothing |
| 4 | Medium | Form could be used to mail-bomb a third party's address | **Mitigated**: confirmation email is sent only on the first entry per address, plus per-IP rate limit (5 per 10 min). **Recommended**: add Cloudflare Turnstile and/or a confirm-by-link step before trusting the address |
| 5 | Medium | HTML / header injection through form fields into emails | **Fixed**: all fields HTML-escaped in emails; control characters and newlines stripped from names and subjects; no user text in headers |
| 6 | Medium | Cross-site posting to `/api/lead` | **Fixed**: exact `Origin` match against `SITE_ORIGIN`, JSON content-type required, 8 KB body cap, POST only |
| 7 | Medium | Bots | **Mitigated**: hidden honeypot field (fake success, nothing stored) and a minimum fill-time check |
| 8 | Medium | Missing browser protections | **Fixed**: `vercel.json` sets a strict CSP (the one inline script is pinned by hash; no `unsafe-inline` for scripts), HSTS, nosniff, frame denial, referrer policy, permissions policy, COOP; API responses are `no-store` |
| 9 | Low | Personal data minimisation | Raw IPs are never stored (salted SHA-256 for rate limiting only, pruned after 24 h); no request data in logs; no cookies |
| 10 | Low | Secrets | None committed; `.env` is git-ignored; `.env.example` has placeholders only. Use a Resend key with sending access only |
| 11 | Info | SQL injection | Prisma parameterises all queries; no raw SQL |
| 12 | Info | Rate-limit trust | Uses the first `x-forwarded-for` value, which is correct behind Vercel; if you host elsewhere, review it |

## Before launch
1. Set all env vars in the host; rotate any key that was ever pasted in chat or committed.
2. Verify your sending domain in Resend and publish SPF, DKIM and DMARC records.
3. In Neon, use a role with only the privileges the app needs, and keep `DIRECT_URL` out of the runtime environment if your host allows it.
4. Run `npx prisma migrate dev --name init` once locally, commit `prisma/migrations`, and deploy with `npx prisma migrate deploy`.
5. Send a test submission on a preview URL; confirm the row, both emails, and a 429 after 6 quick tries.
6. 3-months-free offer: it is a discretionary selection, not a draw. Publish the selection criteria in the offer terms (filled from `CONFIG`), apply them consistently, record the reason in `Lead.reviewNote`, and avoid wording that implies a random draw. Have a lawyer glance over the terms and any ads.
