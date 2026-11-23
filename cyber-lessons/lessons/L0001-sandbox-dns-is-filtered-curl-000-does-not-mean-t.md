id: L0001
date: 2026-09-27
area: tooling
tags: dns,verification,false-negative
title: Sandbox DNS is filtered: curl 000 does NOT mean the site is dead
context: verifying practice/CTF sites for AGENTS.md
trigger: Nearly published 7 sites as 'dead' from curl exit 000. One was PortSwigger's own Web Security Academy.
fix: Confirm via DNS-over-HTTPS against a public resolver. Distinguish 'no A record' from 'connection refused'.
verify: curl -s -H 'accept: application/dns-json' "https://cloudflare-dns.com/dns-query?name=academy.portswigger.net&type=A" | jq -r '.Answer[]?|select(.type==1).data'
transfer: Before reporting any host/API/URL dead from this box. Also tells parked domains (0day.wtf -> 208.91.197.39) apart from dead ones.
---

## Trigger — why this was hard
    Nearly published 7 sites as 'dead' from curl exit 000. One was PortSwigger's own Web Security Academy.
## Wrong assumptions discarded
    Treated 'curl could not resolve host' as proof of decommissioning. It was this sandbox's resolver, not the sites.
## Actual root cause / what worked
    Confirm via DNS-over-HTTPS against a public resolver. Distinguish 'no A record' from 'connection refused'.
## Verification (the command that proves it)
    curl -s -H 'accept: application/dns-json' "https://cloudflare-dns.com/dns-query?name=academy.portswigger.net&type=A" | jq -r '.Answer[]?|select(.type==1).data'
## Transfer — reuse this when
    Before reporting any host/API/URL dead from this box. Also tells parked domains (0day.wtf -> 208.91.197.39) apart from dead ones.
