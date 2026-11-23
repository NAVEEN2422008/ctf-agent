id: L0006
date: 2026-09-27
area: recon
tags: credentials,secrets,hygiene
title: Credential refresh is human-only
context: ~/ctf/login.sh and auth.jar
trigger: Downloads begin returning 'NO URL' as the cookie jar expires, which tempts you to fix auth yourself.
fix: Ask the user to run ./login.sh in their own terminal; report only the HTTP status and cookie count. Never cat or echo the jar.
verify: ls -l ~/ctf/auth.jar   # expect mode 600; check perms only, never contents
transfer: Any workspace with an interactive login helper. The credential-hygiene contract is a feature, not an obstacle to route around.
---

## Trigger — why this was hard
    Downloads begin returning 'NO URL' as the cookie jar expires, which tempts you to fix auth yourself.
## Wrong assumptions discarded
    Would hand-roll a login curl, or cat auth.jar to inspect it. Both are wrong: login.sh exists so the password is read with hidden input and never enters the transcript, and the jar is a live session secret.
## Actual root cause / what worked
    Ask the user to run ./login.sh in their own terminal; report only the HTTP status and cookie count. Never cat or echo the jar.
## Verification (the command that proves it)
    ls -l ~/ctf/auth.jar   # expect mode 600; check perms only, never contents
## Transfer — reuse this when
    Any workspace with an interactive login helper. The credential-hygiene contract is a feature, not an obstacle to route around.
