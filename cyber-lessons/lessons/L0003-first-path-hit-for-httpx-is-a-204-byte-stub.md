id: L0003
date: 2026-09-27
area: tooling
tags: path,httpx,projectdiscovery
title: First PATH hit for httpx is a 204-byte stub
context: recon pipeline / httpx live-host detection
trigger: Same silent-failure class: a stub binary will not accept the expected flags.
fix: Use ~/go/bin/httpx, or confirm PATH puts ~/go/bin ahead of /usr/bin. subfinder and naabu exist ONLY in ~/go/bin.
verify: stat -c '%s %n' /usr/bin/httpx ~/go/bin/httpx; command -v subfinder naabu httpx ffuf
transfer: Any Go-installed ProjectDiscovery tool, especially in non-login shells where ~/go/bin may be missing from PATH.
---

## Trigger — why this was hard
    Same silent-failure class: a stub binary will not accept the expected flags.
## Wrong assumptions discarded
    Assumed 'httpx' is unambiguous. There are two: /usr/bin/httpx (204 bytes, root-owned) and ~/go/bin/httpx (the real 69MB build).
## Actual root cause / what worked
    Use ~/go/bin/httpx, or confirm PATH puts ~/go/bin ahead of /usr/bin. subfinder and naabu exist ONLY in ~/go/bin.
## Verification (the command that proves it)
    stat -c '%s %n' /usr/bin/httpx ~/go/bin/httpx; command -v subfinder naabu httpx ffuf
## Transfer — reuse this when
    Any Go-installed ProjectDiscovery tool, especially in non-login shells where ~/go/bin may be missing from PATH.
