id: L0002
date: 2026-09-27
area: tooling
tags: nuclei,false-negative,config
title: Nuclei templates are not where the shipped slash commands look
context: /recon and /vuln command bodies
trigger: Silent failure: scans nothing and still exits 0. A scan with no findings looks identical to a scan that never ran.
fix: Resolve the template dir once per session and pass -t explicitly, or omit -t so nuclei auto-resolves bundled templates.
verify: nuclei -tl | head -1 && ls -d ~/.local/nuclei-templates
transfer: Any 'my scan found nothing' result on this box. Treat an empty finding set as a config bug until proven otherwise.
---

## Trigger — why this was hard
    Silent failure: scans nothing and still exits 0. A scan with no findings looks identical to a scan that never ran.
## Wrong assumptions discarded
    Trusted the built-in command body, which passes -t ~/nuclei-templates/. That path does not exist; real templates are in ~/.local/nuclei-templates/.
## Actual root cause / what worked
    Resolve the template dir once per session and pass -t explicitly, or omit -t so nuclei auto-resolves bundled templates.
## Verification (the command that proves it)
    nuclei -tl | head -1 && ls -d ~/.local/nuclei-templates
## Transfer — reuse this when
    Any 'my scan found nothing' result on this box. Treat an empty finding set as a config bug until proven otherwise.
