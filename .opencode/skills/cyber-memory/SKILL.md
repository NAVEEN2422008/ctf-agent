---
name: cyber-memory
description: Durable cross-session memory for hard-won security lessons, discarded assumptions, verified techniques, and negative evidence. Use at the START of any engagement to recall prior lessons, and at the END to log what was hard, what was assumed wrongly, and what actually worked.
---

# CYBER-MEMORY

A store of things that cost real effort, so they are paid for once. Lives at `~/cyber-lessons/` —
**always that absolute path, whatever the cwd.** Applies to CTF challenges, pentest engagements,
CVE repros, malware triage, and CTF alike.

## The anti-strutjacket rule — read this first

A store that only says "this worked" teaches you to repeat what worked, and makes you **more
certain while being wrong**. Cumulative-only memory is actively dangerous.

Two consequences you must honour:
1. **Never let a lesson stop you from looking.** Every technique you apply must be one you have
   evidence applies to *this* target. Prior success is a hypothesis, not a warrant.
2. **Log what did NOT work, and why.** `note.sh negative` records the distinguishing condition that
   ruled an approach out. This is what keeps the memory honest.

Also: if you *do* check the store and a technique still fails, that is the highest-value entry
you can make — you have proven the condition matters.

## ORIENT — first, every session
```bash
~/cyber-lessons/note.sh relevant "<one-line description of the task>" 5
```
Ranked by score, showing each `--transfer` line. Read before choosing a tool.
```bash
~/cyber-lessons/note.sh search "<term>"     # on any surprise, before improvising variants
```

## TRACK — while working
```bash
~/cyber-lessons/eng.sh open  "<slug>" --area <a> --goal "<goal>"   # ctf-cybercom-5, pentest-example.com, cve-2024-3400
~/cyber-lessons/eng.sh try   "<slug>" "<hypothesis>" "<command>" "<result>"
~/cyber-lessons/eng.sh verdict "<slug>" solved|dead
```
The counter is on disk. At 3+ attempts, `try` says a lesson is **owed**; `verdict solved` says it
is **mandatory**. `verdict dead` at 3+ means log a `negative`.

## LOG — the trigger table
| Trigger | Command |
|---|---|
| ≥3 attempts, or >20 min | `note.sh lesson` |
| Discarded an assumption | `note.sh lesson --wrong` + `note.sh mistake` |
| Tool lied: wrong path, silent no-op, fake success | `note.sh lesson --area tooling` |
| Proved live vs dead, not obviously | `note.sh lesson` |
| Technique worked, not in `playbook.md` | `note.sh technique` |
| Technique did NOT apply | `note.sh negative` |
| Easy in a non-obvious way | `note.sh quick` |

```bash
~/cyber-lessons/note.sh lesson "<title>" --area <a> --context "<c>" \
  --trigger "<why it was hard>" --wrong "<assumptions discarded>" \
  --fix "<root cause / what worked>" --verify "<command that proves it>" \
  --transfer "<when to reuse on a DIFFERENT problem>" --tags a,b
```
`--trigger`, `--fix`, `--transfer` are mandatory — a lesson that cannot transfer is a story, not
a reference. **Write `--transfer` as the shape of the problem, not the instance.**

```bash
~/cyber-lessons/note.sh negative "<technique>" --because "<distinguishing condition>"
~/cyber-lessons/note.sh quick "<what was easy>" --do-not "<what not to over-engineer>"
~/cyber-lessons/note.sh mistake "<assumption>" --correction "<what was true>"
```

**Do not log:** routine wins, anything already in `man`/`--help`. Noise trains you to skip the file.

## HARD-WON TRAPS ON THIS HOST (also in ~/AGENTS.md, which owns the facts)
- `subfinder`/`naabu` are in `~/go/bin` only. `/usr/bin/httpx` is a 204-byte stub.
- Nuclei templates are `~/.local/nuclei-templates/`. **An empty finding set is a config bug until
  proven otherwise** — a scan that found nothing is indistinguishable from a scan that never ran.
- Not installed: `zsteg`, `steghide`, `audacity`. `masscan` is MCP-only.
- Tor is **not** installed and nothing listens on 9050 — do not export proxy vars, and do not
  claim traffic is anonymized.

## OWNERSHIP
`~/AGENTS.md` owns **toolchain facts** (paths, what is installed). This store owns **reasoning**
(why it was hard, what was assumed, when it transfers). `note.sh check-sync` reports overlap and
**never writes** — when it flags a DUP, keep the lesson and leave the fact in AGENTS.md.
