---
description: Resume the OverTheWire campaign from the exact next unsolved level
---

# /otw-continue

Resume the full OverTheWire autonomous campaign from the durable checkpoint.

## Steps (do these first, in order)

1. Read `.opencode/memory/otw_campaign_state.json`. It is gitignored and contains live credentials — never print it wholesale into chat, never commit it.
2. Read `notes/overthewire_recon_report.md` for host/port and tool posture.
3. Read `notes/overthewire_self_evaluation.md` for the current honest scorecard.
4. Search `.opencode/memory/research_notes/` and `playbooks/` for a note covering the next level's concept before attempting it.
5. Read the **official** level page at `https://overthewire.org/wargames/<game>/<game><n>.html`. Never fetch walkthroughs, writeups, solution repos, or leaked passwords.
6. Continue from `state.next` (wargame, level, username, password).

## Transport

- SSH games: `python3 .opencode/memory/otw_ssh.py <host> <port> <user> <pass> '<command>'`
- Natas: `requests` / `curl` with HTTP Basic auth.

## After EVERY level

- Update the state file: status, attempts, commands used, and the next level's credential.
- Append a winning technique to `.opencode/memory/patterns/solved_techniques.jsonl`.
- If stuck after 2 attempts: research the **general concept**, write `.opencode/memory/research_notes/<topic>.md`, retry.
- After 3 distinct researched approaches: mark `NEEDS_RETRY` with the exact blocker, append to `.opencode/memory/patterns/dead_ends.jsonl`, and move on; revisit later.
- Update the self-evaluation scorecard after each wargame.

## Memory

Orient with `~/cyber-lessons/note.sh relevant "overthewire <game> level <n>"` at the start of each wargame. Log lessons for discarded assumptions, tool surprises, and techniques that worked.
