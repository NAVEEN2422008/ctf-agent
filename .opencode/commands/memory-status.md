---
description: Health-check the memory store — coverage, staleness, and AGENTS.md duplication.
agent: ghost-operator
---

# /memory-status — is the store trustworthy right now?

```bash
~/cyber-lessons/note.sh status       # counts, last update, areas with NO coverage
~/cyber-lessons/note.sh brief        # one-screen digest
~/cyber-lessons/note.sh synthesize   # lessons-per-area + top tags (what themes exist)
~/cyber-lessons/note.sh recheck      # lessons whose --verify tool is no longer on PATH
~/cyber-lessons/note.sh check-sync   # WARN-ONLY duplicate scan vs ~/AGENTS.md
~/cyber-lessons/note.sh index        # regenerate INDEX.md (auto-run on every write)
~/cyber-lessons/eng.sh list          # open/closed engagement threads
```

## How to read it
- **An area with no coverage is a blind spot**, not a clean bill of health. It means nothing has
  been logged there yet — likely because the area is unfamiliar, not because it is easy.
- **`recheck` output means an environment fact went stale.** A lesson citing a tool that is no
  longer installed is a lesson that will now mislead you. Fix it: log a `negative` if the technique
  no longer applies, or a new `lesson` with the current path.
- **`check-sync` never writes.** `~/AGENTS.md` owns the toolchain facts; a lesson should carry the
  *reasoning*, not a second copy of the path. When it reports a DUP, keep the lesson and let
  AGENTS.md remain the single source of the fact.
- **`INDEX.md` is generated — never hand-edit it.** Append via `note.sh`.
