# AGENTS.md — Cyber Ops Environment

Loaded via `instructions: ["AGENTS.md"]` in `~/.config/opencode/opencode.json`.
**That config is the source of truth** — read it before assuming an agent, command, or MCP server exists.

## Runtime facts (verified 2026-09-27)

- Default agent `ghost-operator`, shell `/bin/zsh`, model `anthropic/claude-sonnet-4-6`.
- Permissions are wide open: `bash {"*": "allow"}`, `edit: allow`, `external_directory {"*": "allow"}`.
  No approval prompt will appear — just run the command instead of asking.
- Agents: `ghost-operator`, `autonomous-hacker`, `security-auditor`, `recon`, `webapp`, `binary`,
  `exploit`, `cloud`, `api`, `forensics`, `malware`, `blue`, `opsec`. There is **no `security` agent**.
- Commands: `/recon /scan /fuzz /vuln /enum /exploit /pivot /privesc /hash /cloud /api /ad /forensics
  /malware /opsec /report /self-config /self-heal /verify /full-pentest /pivot-setup /ad-enum /cloud-enum`.
  Bodies live in `~/.config/opencode/command/` (7 files) plus the `command` block of `opencode.json`.
- MCP servers (9): `security-tools`, `ghost-intel`, `ghost-web`, `ghost-network`, `cve-search`,
  `playwright`, `sequential-thinking`, `filesystem`, `memory`. Prefer these over hand-rolled bash for
  CVE lookups, header/tech/WAF analysis, and port/DNS/subdomain work — they are already wired up.

## Toolchain gotchas (these will bite you)

- **Nuclei templates live at `~/.local/nuclei-templates/`, NOT `~/nuclei-templates/`.** The built-in
  `/vuln` and `/recon` command bodies still reference `~/nuclei-templates/` and will silently scan
  nothing. Override the `-t` path, or use bare `nuclei -severity critical,high` (auto-resolves).
- **ProjectDiscovery Go tools are in `~/go/bin`**: `subfinder`, `naabu`, `httpx`, `ffuf`.
  `subfinder` and `naabu` exist *only* there — not in `/usr/bin`. `~/go/bin` precedes `/usr/bin` here,
  but a login/non-interactive shell may not, so use the absolute path when it matters.
- **`/usr/bin/httpx` is a 204-byte stub, not the tool.** The real ProjectDiscovery httpx is
  `~/go/bin/httpx`. `/usr/bin/ffuf` and `~/go/bin/ffuf` are two different builds (`~/go/bin` wins).
- Wordlists confirmed: `/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt` and
  `.../burp-parameter-names.txt`. `rockyou` is gzipped: `/usr/share/wordlists/rockyou.txt.gz`.
- **Not installed** (matters for stego/DFIR): `zsteg`, `steghide`, `audacity`, `masscan` is in the MCP
  wrapper only. Installed and working: `binwalk`, `exiftool`, `foremost`, `testdisk`, `john`,
  `hashcat`, `sqlmap`, `nuclei`, `nmap`, `gdb`, `objdump`, `readelf`, `ROPgadget`, `radare2`.
- Don't guess at tool availability: `security-tools_tool_status` lists installed vs missing,
  `security-tools_self_heal` returns install commands.

## Self-learning memory (do this, every session)

`~/cyber-lessons/` is a durable reference of hard-won lessons, wrong assumptions, and verified
techniques. **Read `~/cyber-lessons/INDEX.md` at the start of any task** — it is the map of what
previously cost real effort. Append through the logger; never hand-edit `INDEX.md`, it is generated.

```bash
~/cyber-lessons/note.sh search <term>              # look up prior lessons before starting
~/cyber-lessons/note.sh lesson "<title>" --area <a> --context <c> --trigger <t> \
                    --wrong <w> --fix <f> --verify <v> --transfer <x> [--tags a,b]
~/cyber-lessons/note.sh mistake "<wrong assumption>" [--area <a>] [--correction <c>]
~/cyber-lessons/note.sh technique "<name>" --area <a> --cmd "<verified command>" [--note <n>]
```

**You MUST log a lesson when any of these happened** — this is the whole point of the directory:

- a solve took **>= 3 failed attempts** or **> 20 minutes**
- a tool surprised you: wrong path, wrong flag, silent no-op, or output that looked like success
- you **discarded an assumption** (highest value, most often skipped — log it even alone)
- you determined whether a host/URL/API is live vs dead and it was not obvious
- a technique worked that is not already in `playbook.md`

Do not log routine wins or anything already in `man`/`--help`; noise trains you to skip the file.
`note.sh` rejects a lesson missing `--trigger`, `--fix`, or `--transfer` on purpose — a lesson that
cannot be transferred to a different challenge is a story, not a reference. See
`~/cyber-lessons/README.md` for the full protocol.

## Practice targets — verified live 2026-09-27

Use these to test skill legally. All URLs below returned a live response on that date.

### Web / theory
| Site | URL | Notes |
|---|---|---|
| PortSwigger Web Security Academy | https://portswigger.net/web-security | Free, best web theory + labs |
| HackTricks | https://hacktricks.xyz | Free knowledge base; the best single reference |
| PentesterLab | https://pentesterlab.com | Web + code review, subscription |
| Hacker101 | https://hackerone.com/hacker101 | Free HackerOne web class + ongoing CTF |
| Intigriti | https://intigriti.com | Real bug-bounty programs + monthly XSS challenge |
| FIRST API Security | https://api.first.org | Free API security learning tracks |
| OWASP Juice Shop | https://owasp.org/www-project-juice-shop/ | Self-host, modern vulns |
| OWASP WebGoat | https://owasp.org/www-project-webgoat/ | Self-host, lesson-based |
| OWASP Mutillidae II | https://github.com/webpwnized/mutillidae | Dozens of vulns + built-in hints |
| OWASP crAPI | https://github.com/OWASP/crAPI | Vulnerable API (BOLA, BFLA, mass assignment) |
| bWAPP | https://sourceforge.net/projects/bwapp | 100+ vulns, classic PHP lab |
| DVWA | https://github.com/digininja/DVWA | Self-host, low/med/high |
| Metasploitable 3 | https://github.com/rapid7/metasploitable3 | Intentionally vulnerable VM images |
| Google XSS Game | https://xss-game.appspot.com | 6 XSS levels, browser-only |
| DefectDojo | https://defectdojo.com | Hosted web/API/mobile labs |

### CTF / wargame
| Site | URL | Notes |
|---|---|---|
| Hack The Box | https://www.hackthebox.com | Machines + CTF |
| HTB Academy | https://academy.hackthebox.com | Free structured paths |
| TryHackMe | https://tryhackme.com | Best for absolute beginners |
| picoCTF | https://picoctf.org | Free, gamified, beginner CTF |
| OverTheWire | https://overthewire.org | Bandit (Linux), Natas (web) |
| Hack This Site | https://hackthissite.com | Free, long-running, free level 1-12ish |
| CTFtime | https://ctftime.org | Event calendar + team play |
| CTFlearn | https://ctflearn.com | Free beginner challenges |
| VulnHub | https://www.vulnhub.com | Downloadable boot2root VMs |
| VulnWare | https://www.vulnware.com | Free boot2root VMs |
| HackMyVM | https://hackmyvm.com | Boot2root + online labs |
| exploit.education | https://exploit.education | 16-machine x86 wargame |
| RingZer0 | https://ringzer0.com | Jeopardy-style, many categories |
| EchoCTF | https://echoctf.com | Full virtual smart-city range |

### Pwn / reversing / crypto
| Site | URL | Notes |
|---|---|---|
| pwnable.kr | https://pwnable.kr | Best beginner pwn wargame |
| pwnable.tw | https://pwnable.tw | Harder, classic |
| pwnable.xyz | https://pwnable.xyz | Modern pwn wargame |
| reversing.kr | https://reversing.kr | RE practice |
| SmashTheStack | https://smashthestack.com | Multi-arch, classic (x86, ARM, MIPS) |
| CryptoHack | https://cryptohack.org | Free, modern crypto |
| Cryptopals | https://cryptopals.com | Free, the crypto standard |
| Crackmes.one | https://crackmes.one | RE downloads |
| cmdchallenge | https://cmdchallenge.com | Linux command fluency |
| webhacking.kr | https://webhacking.kr | Web exploitation, many levels |
| Microcorruption | https://microcorruption.com | ARM assembly + debugger |

### Blue team / cloud / knowledge
| Site | URL | Notes |
|---|---|---|
| CyberDefenders | https://cyberdefenders.com | Free SOC/forensics investigations |
| Blue Team Labs Online | https://blueteamlabs.online | Gamified IR + DFIR challenges |
| SEED Labs | https://seedsecuritylabs.org | Free academic labs, web+network+crypto |
| OWASP Cheat Sheet Series | https://github.com/OWASP/CheatSheetSeries | Concise secure-coding reference |
| OWASP ASVS | https://github.com/OWASP/ASVS | Verification standard to test against |
| Security StackExchange | https://security.stackexchange.com | Q&A, searchable |

**Retired — do not chase these:** `academy.portswigger.net` (use `portswigger.net/web-security`),
`root-me.com` (no DNS record), `xss.game` (no DNS record), `saltycrate.io` (no DNS),
`0day.wtf` (domain parked), `owasp.org/www-project-dvwa/` (404), `xss.pwnfunction.com`
(self-declared unmaintained), `ctf.csie.cnu.edu.tw` (no DNS), `security.club.sysu.edu.cn`
(no DNS), `linuxpwndiary.com` (no DNS), `ctf.buet.ac.bd` (no DNS), `ctfs.nitd.edu.in` (no DNS),
`webdevkaty/mutillidae` (404 — use `webpwnized/mutillidae`).

## Rules of engagement

1. Written authorization before testing anything not listed above as intentionally vulnerable.
2. Stay in scope; never access or modify data beyond it.
3. Minimize impact — no DoS, no data destruction, no persistence on real systems.
4. Report unintended findings, don't quietly exploit them.
5. Exfiltrate only what proves the finding; preserve evidence integrity.
6. Clean up artifacts (temp files, listeners, injected accounts) when the engagement ends.

## Finding output format

```
[VULN]  <name>
[OWASP/CWE] <classification>
[SEVERITY] Critical | High | Medium | Low | Info
[EVIDENCE] <repro steps + proof>
[REMEDIATION] <fix>
[MITRE] <ATT&CK technique id>
```

Map every finding to an OWASP Top 10 (2021) category and a MITRE ATT&CK technique. Use the `blue`
agent for defensive/IR work and `forensics` for evidence handling.
