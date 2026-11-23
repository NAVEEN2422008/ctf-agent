---
description: Recall prior hard-won lessons before starting work. Run this FIRST, every session.
agent: ghost-operator
---

# /recall — orient in the memory store before working

Most "new" problems are already recorded. Read the store **before** picking a tool, not after
failing three times.

## Ranked recall for the task at hand
```bash
~/cyber-lessons/note.sh relevant "<one-line description of the task>" 5
```
Prints the top lessons by score, each with its `--transfer` line — the reusable part.

## Other lookups
```bash
~/cyber-lessons/note.sh search "<term>"          # literal, no mid-word truncation
~/cyber-lessons/note.sh list --area forensics   # real filter (area taxonomy is validated)
~/cyber-lessons/note.sh list --grep nuclei       # real filter over titles
~/cyber-lessons/note.sh brief                   # one-screen counts
```

## On any surprise — re-check before you vary the approach
```bash
~/cyber-lessons/note.sh search "<tool or symptom>"
```
A tool failure, an empty result set, or output that looks like success is the moment to search.
Do not start improvising variants of something already documented.

## Track the engagement while you work
```bash
~/cyber-lessons/eng.sh open  "<slug>" --area <a> --goal "<goal>"   # ctf-cybercom-5, pentest-example.com
~/cyber-lessons/eng.sh try   "<slug>" "<hypothesis>" "<command>" "<result>"
~/cyber-lessons/eng.sh verdict "<slug>" solved|dead
```
The on-disk counter — not recollection — decides whether a lesson is owed. At 3+ attempts the
tracker tells you a lesson is mandatory. A dead end is evidence too: `note.sh negative`.
