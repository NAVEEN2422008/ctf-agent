# AGENTS.md — CyberCom CTF workspace (`~/ctf`)

Live CTF workspace for **Noctivus 2026** on `https://infra.cybercomctf.com`. This file covers the
workspace conventions; environment/tooling facts live in `~/AGENTS.md` (read that too — it has the
`~/go/bin` and `~/.local/nuclei-templates` traps).

## Platform facts

- CTFd-compatible REST API at `https://infra.cybercomctf.com/api/v1/*`. The frontend is **Next.js
  (App Router / RSC) behind Cloudflare** — `x-powered-by: Next.js`, `vary: ... rsc, next-router-*`.
  `rsc.txt` here is the React Server Component flight payload, and `js/`+`jsl/` are the
  `/_next/static/chunks/*.js` bundles pulled from it. `headers.txt` holds the raw response headers.
- Flag format: `NOCT{...}`. Record every solve in `flags/solved.txt` as `<challenge_id> <FLAG>`.
- Auth is a cookie jar: `auth.jar` (gitignore-worthy secret, mode 600). Both scripts depend on it —
  if downloads return `NO URL`, the jar expired; re-auth in a browser and refresh it.

## Commands (non-obvious, workspace-specific)

```bash
./dl.sh <file_id> <out_name>     # resolve file id -> presigned URL -> download
./sub.sh <challenge_id> <flag>   # POST to /api/v1/challenges/attempt
./login.sh                       # INTERACTIVE ONLY - refreshes auth.jar
```

- **`login.sh` must be run by the human, never by you.** It prompts for the password with hidden
  input and writes only `$HOME/ctf/auth.jar` at mode 600, so the password never enters the transcript.
  Its own last line is an instruction: report only the HTTP status + cookie count, and never paste the
  password or the jar's contents. Do not `cat auth.jar`, do not hand-roll a login `curl`, and do not
  ask the user to paste credentials into chat — tell them to run `./login.sh` in their terminal instead.
- `filelist.txt` is the `<file_id> <challenge_id> <original_filename>` index. Challenge IDs are the
  *second* column; the file IDs are **not** the challenge IDs — `chal.json` maps them.
- When saving a download, keep the `dl/c<challenge_id>_<original_name>` prefix convention already used
  in `dl/`. It is what makes artifacts greppable back to `chal.json`.
- `chal.json` is the challenge inventory snapshot: `challenges[]` with `id`, `category`, `value`,
  `solve_count`, `is_solved`, `files[]`, `hints[]`, `first_blood_team_name`, and `total_teams`.
  Re-fetch it rather than assuming it is current — solve counts and lock state change live.

## Log what you learn (non-optional)

This event is mostly forensics/stego/crypto, so technique carry-over matters more than speed.
Two rules for this workspace:

1. **Read `~/cyber-lessons/INDEX.md` before starting a challenge.** Prior lessons on LSB
   channel splitting, `file`-magic carving, and this platform's id space are already recorded.
2. **After any challenge that took more than ~3 attempts, or where you had to throw away an
   assumption, log it** via `~/cyber-lessons/note.sh lesson ...` with `--transfer` describing the
   *general* pattern, not just this challenge. See `~/cyber-lessons/README.md`.

Record progress in two places, for two different reasons: `flags/solved.txt` is what has been
accepted by the platform, a lesson is what made it possible — a solve with no lesson is a repeat of
the same cost for whoever reads this next.

## Directory ownership

| Path | Contents |
|---|---|
| `dl/` | Downloaded + carved challenge artifacts (`c<id>_*` prefix) |
| `flags/solved.txt` | One `<challenge_id> <FLAG>` line per solve — the source of truth for progress |
| `js/`, `jsl/` | Next.js chunk bundles from platform recon (`jsl/` is the later/merged pass) |
| `rsc.txt`, `headers.txt` | Platform recon output (RSC flight payload, HTTP headers) |
| `*.html` | `login.html`, `reg.html`, `challenges.html` — saved platform pages |

Not a git repo. There is no build, test, or lint step — verification is *submit the flag* via
`./sub.sh` and see it accepted.

## Challenge profile (from the `chal.json` snapshot)

28 challenges / 42 teams, heavy on forensics and OSINT — not a web-heavy event:

`FORENSICS` 10, `OSINT` 5, `CRYPTO` 4, `WEB` 4, `MISC` 3, `REVERSE ENGINEEIRNG` 1 (sic — the typo is
in the platform data, do not "fix" it in queries), `WELCOME` 1.

- **WEB challenges (31-34) have no files** — they are live instances, so `dl.sh` is a no-op and you
  must drive them in a browser (the `playwright` MCP server is available) or via HTTP.
- Watch for challenge files referenced only in the description (e.g. id 23 "After the Wipe" points at
  a Google Drive link, not a platform file). `files: []` does not mean "no artifact".
- Point values are inverted vs. difficulty intuition: the 500-600pt WEB challenges already have
  solves, while several 100-200pt forensics challenges have **zero** solves. Solve count is the better
  difficulty signal than points.
- `afterimage_tail.bin` (~16MB) and `c6_challenge.img` (exactly 33554432 B = 32MiB) are large binary
  artifacts — carve and inspect out-of-band rather than reading them into context.
- `comb_*.png` / `lsb_*.png` in `dl/` are intermediate work products from stego on `c29_qqqqqrrrrrrrr.png`
  (classic RGB-channel LSB extraction → `lsb_R/B/G.png` → per-channel channel analysis). These are
  reusable technique artifacts, not downloads.

## Toolchain notes for this event

- `zsteg` and `steghide` are **not installed** — install before starting LSB-stego challenges rather
  than burning time on hand-rolled Python. `binwalk`, `exiftool`, `foremost`, `testdisk` are available.
- `~/go/bin` must be on `PATH` for `subfinder`/`naabu`; the `/recon` and `/scan` slash commands are
  written for a real target and are overkill here — go straight at the artifact.
- `c21_challenge` is an executable (`-rwxr-xr-x`); check it with `file`, `strings`, `readelf`/`objdump`,
  `gdb`, and the `binary` subagent.
- The RE agent is spelled `REVERSE ENGINEEIRNG` in the platform data; `chal.json` is the place to read
  category names from, not your own spelling.
