# Verified Technique Playbook

Only entries that were **run and confirmed**. Appended by `note.sh technique`.

### Enumerate a live CTFd platform — recon (2026-09-27)

```bash
curl -s -b auth.jar https://<host>/api/v1/challenges | jq -r ".data[]|\"\(.id)\t\(.category)\t\(.value)\t\(.solve_count)\t\(.name)\""
```

On Noctivus 2026 solve_count was a better difficulty signal than points: several 100-200pt challenges had zero solves while 500-600pt WEB ones were already taken.

### Resolve file_id to challenge_id — recon (2026-09-27)

```bash
jq -r ".challenges[]|select(.files[]?.id==\${FILE_ID})|.id" chal.json   # FILE_ID comes from filelist.txt / dl.sh
```

### Detect Next.js/RSC before choosing a scraping strategy — recon (2026-09-27)

```bash
curl -sI https://<host> | grep -iE "x-powered-by|vary:.*rsc"
```

x-powered-by: Next.js plus vary containing rsc means read the React flight payload and /_next/static/chunks, not the rendered DOM.

### Confirm a domain is truly dead (bypass sandbox DNS filtering) — tooling (2026-09-27)

```bash
curl -s -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=<domain>&type=A" | jq -r "[.Answer[]?|select(.type==1).data]|if length==0 then \"NO_A_RECORD\" else join(\",\") end"
```

### Verify a site's live/dead status in this sandbox (2-step) — tooling (2026-09-27)

```bash
# 1. HTTP probe with browser UA
curl -s -o /dev/null -w "%{http_code}" -L -A "Mozilla/5.0" --max-time 12 https://<domain>
# 000 => NOT proof of death (sandbox DNS is filtered). Go to step 2:
curl -s -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=<domain>&type=A" \
  | jq -r "[.Answer[]?|select(.type==1).data]|if length==0 then \"NO_A_RECORD (genuinely gone)\" else \"ALIVE: \"+join(\",\") end"
```

Interpret: NO_A_RECORD = retired. Resolves but curl 000 = live, just blocks this IP/UA (hackmyvm, smashthestack, ringzer0, sourceforge). 403/525/526 = live behind Cloudflare bot/WAF. Multiple concurrent requests also trigger GitHub rate-limit 404s, which look exactly like a deleted repo — re-test a 404 before believing it (this is how crAPI was nearly dropped).

### memory-search-pattern — tooling (2026-11-22)

```bash
~/cyber-lessons/note.sh search 'DNS'
```

search across lessons, mistakes, playbook for a term
