id: L0004
date: 2026-09-27
area: recon
tags: nextjs,rsc,ctfd,recon
title: CTFd API behind a Next.js RSC frontend
context: infra.cybercomctf.com (Noctivus 2026)
trigger: Saved HTML looked like a flat SPA with no visible API surface, so grepping the markup for endpoints yields nothing.
fix: Read the RSC flight payload (rsc.txt) and /_next/static/chunks for client-side routes. Drive /api/v1/* directly with the auth.jar cookie for data.
verify: curl -s -b auth.jar https://infra.cybercomctf.com/api/v1/challenges | jq '.data[0]|{name,category}'
transfer: Any Next.js target: 'x-powered-by: Next.js' + 'vary: ...rsc...' instantly decides whether to read the flight payload or the DOM.
---

## Trigger — why this was hard
    Saved HTML looked like a flat SPA with no visible API surface, so grepping the markup for endpoints yields nothing.
## Wrong assumptions discarded
    Assumed the served page was the app. The API is CTFd-compatible at /api/v1/*, but the frontend is Next.js App Router/RSC behind Cloudflare, so the body is a React flight stream rather than readable markup.
## Actual root cause / what worked
    Read the RSC flight payload (rsc.txt) and /_next/static/chunks for client-side routes. Drive /api/v1/* directly with the auth.jar cookie for data.
## Verification (the command that proves it)
    curl -s -b auth.jar https://infra.cybercomctf.com/api/v1/challenges | jq '.data[0]|{name,category}'
## Transfer — reuse this when
    Any Next.js target: 'x-powered-by: Next.js' + 'vary: ...rsc...' instantly decides whether to read the flight payload or the DOM.
