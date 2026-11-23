# Self-Learning Memory — `~/cyber-lessons/`

A durable reference of what actually cost effort, so a future session does not pay for it twice.
This is **not** a diary. It stores only things that changed how you would attack the *next*
challenge.

## The rule that matters

Log a lesson when **any** of these is true:

1. A solve took **>= 3 failed attempts** or **> 20 minutes**.
2. A tool behaved unexpectedly — wrong path, wrong flag, silent no-op, output that lied.
3. You **discarded an assumption**. This is the highest-value case and the most often skipped.
4. You verified whether a host/URL/API is **live or dead** and it was not obvious.
5. A technique worked that is **not already in the playbook**.

Do **not** log: routine wins, anything the tool's `--help` or `man` page already states, or
one-line fixes. A log nobody reads is worthless; noise trains you to skip the file.

## Files

| Path | Role |
|---|---|
| `INDEX.md` | **Auto-generated** map of every entry. Read this first. Never hand-edit. |
| `lessons/L*.md` | One record per hard-won solve. `note.sh` allocates IDs. |
| `mistakes.md` | Append-only log of assumptions that turned out wrong, each with its correction. |
| `playbook.md` | Verified command patterns that were **run and confirmed**. |

`note.sh` rebuilds `INDEX.md` on every write, so the index cannot drift from reality.

## Usage

```bash
~/cyber-lessons/note.sh lesson "<title>" \
  --area <web|crypto|forensics|stego|rev|osint|misc|tooling> \
  --context "<challenge id / site / situation>" \
  --trigger  "<why it was hard: attempts, time, what failed>" \
  --wrong    "<assumptions you had to discard>" \
  --fix      "<the actual root cause or technique that worked>" \
  --verify   "<the command that proves it>" \
  --transfer "<when to reuse this in a DIFFERENT challenge>" \
  [--tags a,b,c]

~/cyber-lessons/note.sh mistake "<assumption that was wrong>" \
  [--area <a>] [--context <c>] [--correction "<what was actually true>"]

~/cyber-lessons/note.sh technique "<name>" --area <a> --cmd "<verified command>" [--note <n>]

~/cyber-lessons/note.sh search <term>     # grep lessons + mistakes + playbook
~/cyber-lessons/note.sh index             # rebuild INDEX.md
```

`note.sh` **rejects** a lesson that is missing `--trigger`, `--fix`, or `--transfer`. That is
deliberate: a lesson nobody can transfer to a new problem is a story, not a reference.

## Why `--transfer` is mandatory

A record of *what happened* does not help on a different challenge. A record of *when this
pattern applies* does. The trigger and transfer fields are what turn this directory from a
log into a reference — keep them concrete, and prefer the shape of the problem over the
shape of one instance:

- Bad transfer: "Used foremost on c5 and it worked."
- Good transfer: "Any challenge where a file's reported size is not a multiple of the
  block device size — carve before analyzing containers."

## At the start of a session

Read `INDEX.md`. When a new challenge's shape resembles something in the index, open the
matching `lessons/L*.md` before reaching for a tool.
