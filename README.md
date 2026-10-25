# Landing site
Static site generator. Edit `CONFIG` at the top of `build.py`, run `python3 build.py`, deploy the `site/` folder on your own domain.
- Product name: `NAME` / `ACCENT` (also renames the product screens inside the SVGs).
- Yellow `[placeholders]` on /privacy, /terms and /contact are owner decisions; fill them in CONFIG.
- Preview: `cd site && python3 -m http.server 8000`.
- Have a lawyer review the Privacy Policy and Terms before publishing. Keep every claim true of the code.

## Trial form, database and email
- Form -> `POST /api/lead` (`api/lead.js`) -> Neon via Prisma (`prisma/schema.prisma`) -> Resend (`lib/emails.js`).
- Setup: `cp .env.example .env`, fill it in, `npm install`, `npx prisma migrate dev --name init`, then deploy (Vercel reads `vercel.json`, serves `site/`, runs the API).
- Rebuild pages after editing `CONFIG`: `python3 build.py` (also rewrites `vercel.json`). Commit `site/`.
- Tests: `npm test`. See `SECURITY_AUDIT.md` before launch.
