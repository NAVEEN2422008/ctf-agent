slug: ctf-test-01
opened: 2026-09-27 20:30
area: forensics
goal: verify the attempt counter is real
attempts: 3
verdict: solved
---

### attempt 1 — 2026-09-27 20:30
hypothesis: hypothesis A
command: binwalk file
result: nothing found

### attempt 2 — 2026-09-27 20:30
hypothesis: hypothesis B
command: exiftool file
result: comment field had the data

### attempt 3 — 2026-09-27 20:30
hypothesis: hypothesis C
command: steghide extract
result: wrong passphrase
