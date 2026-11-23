---
description: Log a hard-won lesson, mistake, negative, or quick win to the durable memory store.
agent: ghost-operator
---

# /note — log to the durable memory store

Store: `~/cyber-lessons/` (always absolute — works from any directory, CTF or pentest).

**First, read the task you just did.** Which of these is true?

| Trigger | Action |
|---|---|
| ≥3 attempts, or >20 min on one problem | `lesson` |
| You discarded an assumption | `lesson --wrong` **and** `mistake` |
| A tool lied (wrong path, silent no-op, fake success) | `lesson --area tooling` |
| You proved something live vs dead, not obviously | `lesson` |
| A technique worked that is not in `playbook.md` | `technique` |
| A technique did NOT apply (tried it, wrong context) | `negative` |
| Something was easy in a non-obvious way | `quick` |

Routine wins and anything in `man`/`--help` are **not** worth logging. Noise trains you to skip the file.

## Log a lesson (the high-value case)
```bash
~/cyber-lessons/note.sh lesson "<title>" --area <web|crypto|forensics|stego|rev|pwn|osint|recon|ad|cloud|ir|mal|c2|tooling|misc> \
  --context "<what you were doing>" \
  --trigger "<WHY this was hard: attempts, time, the assumption that misled you>" \
  --wrong  "<assumptions you discarded>" \
  --fix    "<actual root cause / what worked>" \
  --verify "<the command that proves it>" \
  --transfer "<when to reuse this on a DIFFERENT problem — the point of a reference>" \
  --tags a,b
```
`--trigger`, `--fix` and `--transfer` are **mandatory**; `note.sh` rejects the lesson without them.
A lesson that cannot transfer is a story, not a reference.

## Log the other record types
```bash
~/cyber-lessons/note.sh mistake "<assumption>" --context "<where>" --correction "<what was actually true>"
~/cyber-lessons/note.sh negative "<technique>" --because "<the distinguishing condition that ruled it out>"
~/cyber-lessons/note.sh quick "<what was easy>" --do-not "<what you nearly over-engineered>"
~/cyber-lessons/note.sh technique "<name>" --area <a> --cmd "<the command that actually worked>"
```

## Rules
- **`--transfer` is the highest-value field.** Describe the *shape* of the problem, not this instance.
- **Do not let a lesson stop you from looking.** Every technique you apply must be one you have
  evidence applies to *this* target. A store that only records successes makes you more confident
  while being wrong — that is what `negative` prevents.
- Near-duplicates are refused. Use `--force`, or record that it supersedes an earlier ID.
