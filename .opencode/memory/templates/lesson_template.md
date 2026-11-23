# Lesson template

Copy this into a new file under `cyber-lessons/lessons/` (or pass the fields to
`~/cyber-lessons/note.sh lesson`) when a problem cost more than ~3 attempts,
required discarding an assumption, or exposed a tooling lie.

```markdown
## <short title> — L<NNNN>

- **Area**: <ctf | tooling | recon | forensics | crypto | web | ...>
- **Trigger**: <what made this hard — the specific surprise>
- **Wrong assumption**: <what you believed that turned out to be false>
- **Fix / root cause**: <what actually worked and why>
- **Verify**: <exact command that proves it>
- **Transfer**: <the general SHAPE of the problem — when to reuse this elsewhere>
- **Tags**: <comma,separated,tags>
```

Rules:

- `--trigger`, `--fix`, and `--transfer` are mandatory. A lesson without a
  transfer is a story, not a reference.
- State the shape of the problem, not the instance. "Any Next.js target with
  `x-powered-by: Next.js`" transfers; "challenge 23 on infra.cybercomctf.com"
  does not.
- Log negative evidence too: a technique that did NOT apply is as valuable as
  one that worked. Use `note.sh negative`.
- Never put live credentials, session state, or campaign passwords in a lesson.
