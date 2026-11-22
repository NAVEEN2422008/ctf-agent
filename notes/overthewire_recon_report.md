# OverTheWire — Full-Website Autonomous Campaign: Recon Report

Generated: 2026-11-22T18:00:59Z
Source: official pages only (`https://overthewire.org/wargames/` and each game's own pages).
No walkthroughs, writeups, solution blogs, or leaked passwords were consulted.

## 1. Inventory of active wargames

| Wargame | Category | Host & Port / URL | Levels (target) | Difficulty (official) | Order |
|---|---|---|---|---|---|
| Bandit | Linux / CLI basics | `bandit.labs.overthewire.org:2220` (SSH) | 0–33 (34) | beginner | 1 |
| Natas | Server-side web security | `http://natasX.natas.labs.overthewire.org` (HTTP Basic) | 0–34 (35) | beginner→advanced | 2a |
| Krypton | Cryptography | `krypton.labs.overthewire.org:2231` (SSH) | 0–6 (7) | beginner | 2b |
| Leviathan | Reverse engineering / dynamic analysis | `leviathan.labs.overthewire.org:2223` (SSH) | 0–7 (8) | 1/10 | 2c |
| Narnia | Binary exploitation intro | `narnia.labs.overthewire.org:2226` (SSH) | 0–9 (10) | 2/10 | 3 |
| Behemoth | Binary exploitation | `behemoth.labs.overthewire.org:2221` (SSH) | 0–8 (9) | 3/10 | 4 |
| Utumno | Binary exploitation | `utumno.labs.overthewire.org:2227` (SSH) | 0–8 (9)¹ | 4/10 | 5 |
| Maze | Binary exploitation / RE | `maze.labs.overthewire.org:2225` (SSH) | 0–9 (10)² | 5/10 | 6 |
| Vortex | Advanced exploitation | `vortex.labs.overthewire.org:2222` (SSH), `:5842` (level 0) | 0–26 (27) | advanced | 7 |
| Manpage | Linux C programming misconceptions | `manpage.labs.overthewire.org:2224` (SSH) | 0–6 (7) | x/10 | side |
| Drifter | Encrypted remote syscall proxy | `drifter.labs.overthewire.org:2230` (SSH), `:1111` (level 0) | TBD | advanced | side |
| FormulaOne | Reverse engineering | `formulaone.labs.overthewire.org:2232` (SSH) | TBD | advanced | side |

¹ Official Utumno page says "Levels: 10"; campaign target follows the user-specified 0–8. Discrepancy noted, not silently "fixed".
² Official Maze page says "Levels: 9"; campaign target follows the user-specified 0–9. Discrepancy noted.

Skipped per instructions: **Semtex** (Offline); **HES2010, Abraxas, Monxla, Kishi** (Released, not active).

Official suggested order: Bandit → (one of Natas / Krypton / Leviathan) → Narnia → Behemoth → Utumno → Maze → …
Campaign order follows the user's explicit sequence: Bandit → Natas → Krypton → Leviathan → Narnia → Behemoth → Utumno → Maze → Vortex → Manpage / Drifter / FormulaOne.

## 2. Local tool readiness

| Tool | Status | Path / note |
|---|---|---|
| `ssh` | OK | `/usr/bin/ssh` |
| `sshpass` | **MISSING** | Use `paramiko` (installed) via `.opencode/memory/otw_ssh.py` |
| `curl` | OK | `/usr/bin/curl` |
| `python3` | OK | `/usr/bin/python3` |
| `pwntools` (`pwn`) | OK | importable |
| `paramiko` | OK | importable — SSH transport for all shell games |
| `requests` | OK | importable — Natas HTTP |
| `z3` | OK | importable — constraint solving |
| `pycryptodome` (`Crypto`) | OK | importable — Krypton / crypto |
| `gdb` | OK | `/usr/bin/gdb` |
| `radare2` / `r2` | OK | `/usr/bin/radare2` |
| `objdump`, `readelf`, `strings` | OK | binutils present |
| `strace` | OK | `/usr/bin/strace` |
| `ltrace` | **MISSING** | Self-heal before Leviathan (`apt install ltrace`) |
| `nc` | OK | `/usr/bin/nc` |
| `nmap` | OK | `/usr/bin/nmap` |
| `john`, `hashcat` | OK | password tooling available |

Self-heal actions queued: install `ltrace` before Leviathan. `sshpass` intentionally not installed — paramiko helper is the chosen transport.

## 3. Reachability probe (2026-11-22T18:00Z)

| Target | Result |
|---|---|
| bandit:2220 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| natas0 HTTP:80 | OPEN |
| krypton:2231 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| leviathan:2223 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| narnia:2226 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| behemoth:2221 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| utumno:2227 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| maze:2225 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| vortex:2222 | **TIMEOUT** — revisit; do not declare dead (lesson L0001) |
| manpage:2224 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| drifter:2230 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |
| formulaone:2232 | OPEN — `SSH-2.0-OpenSSH_10.2p1` |

Authentication smoke test: `bandit0@bandit:2220` → **AUTH_OK** (`uid=11000(bandit0)`, home `/home/bandit0`, `readme` present). The campaign can start immediately.

## 4. Anti-cheat posture

- Allowed: official overthewire.org level pages, `man`/`--help`, language/library docs, general concept research (ciphers, x86, format strings, RC4, syscall ABIs, etc.).
- Forbidden and not used: walkthroughs, writeups, solution repos, hint blogs, leaked password lists.
- Every concept researched gets a reusable note in `.opencode/memory/research_notes/<topic>.md`.

## 5. Artifacts created

- `.opencode/memory/otw_campaign_state.json` — resumable checkpoint (gitignored, contains credentials)
- `.opencode/memory/otw_ssh.py` — paramiko-based SSH command helper
- `.opencode/commands/otw-continue.md` — `/otw-continue` resume command
- `.opencode/memory/research_notes/` — concept reference notes
- `.opencode/memory/patterns/solved_techniques.jsonl`, `dead_ends.jsonl` — learning logs
- `notes/overthewire_self_evaluation.md` — live honest scorecard
