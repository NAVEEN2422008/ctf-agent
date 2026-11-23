# Wrong-Assumption Log

Append-only. Every time an agent assumed something and was wrong, it lands here.
Format: `- **date** <assumption> — _correction:_ <what was actually true>`


- **2026-09-27** Treated 'curl could not resolve host' as proof of decommissioning. It was this sandbox's resolver, not the sites. — _correction:_ Confirm via DNS-over-HTTPS against a public resolver. Distinguish 'no A record' from 'connection refused'.

- **2026-09-27** Trusted the built-in command body, which passes -t ~/nuclei-templates/. That path does not exist; real templates are in ~/.local/nuclei-templates/. — _correction:_ Resolve the template dir once per session and pass -t explicitly, or omit -t so nuclei auto-resolves bundled templates.

- **2026-09-27** Assumed 'httpx' is unambiguous. There are two: /usr/bin/httpx (204 bytes, root-owned) and ~/go/bin/httpx (the real 69MB build). — _correction:_ Use ~/go/bin/httpx, or confirm PATH puts ~/go/bin ahead of /usr/bin. subfinder and naabu exist ONLY in ~/go/bin.

- **2026-09-27** Assumed the served page was the app. The API is CTFd-compatible at /api/v1/*, but the frontend is Next.js App Router/RSC behind Cloudflare, so the body is a ~ — _correction:_ Read the RSC flight payload (rsc.txt) and /_next/static/chunks for client-side routes. Drive /api/v1/* directly with the auth.jar cookie for data.

- **2026-09-27** Assumed the integer on a download is the integer to submit. filelist.txt column 1 is a file id; the real challenge id is column 2 / chal.json. — _correction:_ Map via chal.json (challenges[].files[].id -> parent challenge id), or read column 2 of filelist.txt.

- **2026-09-27** Would hand-roll a login curl, or cat auth.jar to inspect it. Both are wrong: login.sh exists so the password is read with hidden input and never enters the ~ — _correction:_ Ask the user to run ./login.sh in their own terminal; report only the HTTP status and cookie count. Never cat or echo the jar.

- **2026-09-27** Assumed one LSB plane held the flag and that a generic stego tool would find it. — _correction:_ Extract per-channel LSB planes to separate files (R,G,B), analyse each independently, then combine (xor/max/min/mean/sum-clip). The 'q'/'r'-heavy filename ~

- **2026-09-27** Local chal.json is authoritative for which challenges are already solved _(context: ~/ctf/chal.json snapshot vs flags/solved.txt)_ — _correction:_ They disagreed: chal.json marked 11/15/16/23/35 is_solved=true while flags/solved.txt held only 21, and chal.json marked 21 false. The snapshot was older. Both ~

- **2026-09-27** Tried to read a lesson by a guessed filename — _correction:_ Filenames are auto-slugged; use note.sh search <term> or list the directory.

- **2026-11-22** assumed memory would just work without configuration — _correction:_ configured note.sh, INDEX.md, lessons directory, and all required fields

- **2026-11-22** assumed all Python packages install without dependencies _(context: phase-4)_ — _correction:_ pip install --break-system-packages handles most missing deps

- **2026-11-22** assumed -p (plain) was right for a file that had offset columns; assumed the loop variable stayed valid after gunzip/bunzip2 rewrote the file as f — _correction:_ use 'xxd -r data.txt out' (no -p) for standard offset+hex+ASCII dumps; assign f=f after creating the file and again after every gzip/bzip2 branch because those ~

- **2026-11-22** Assumed git-shell would allow ls/cat/git log via exec_command; assumed SFTP would work; assumed sys.stdin.buffer.read(4096) forwards small pkt-lines — _correction:_ paramiko GIT_SSH wrapper with GIT_SSH_VARIANT=ssh, real hostname, -o/-p arg parsing, blocking chan.recv with timeout, and os.read(0,4096) for stdin
