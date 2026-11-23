#!/usr/bin/env bash
# eng.sh — engagement/thread attempt tracker for GHOST OPERATOR.
# Keys on a generic slug, so the same mechanism covers CTF challenges
# (ctf-cybercom-5), pentest targets (pentest-example.com) and CVE repros (cve-2024-3400).
# The on-disk attempt counter — not recollection — decides whether a lesson is owed.
set -uo pipefail

BASE="$HOME/cyber-lessons/threads"
AREAS="web crypto forensics stego rev pwn osint recon ad cloud ir mal c2 tooling misc"
mkdir -p "$BASE"

today() { date -u +%Y-%m-%d; }
now()   { date -u +%H:%M; }
die()   { printf 'eng.sh: %s\n' "$1" >&2; exit 1; }
one_line() { printf '%s' "${1:-}" | tr '\n' ' ' | tr -s ' ' | sed -E 's/^ +| +$//g' | awk '{ if (length($0)<=140) print; else { s=substr($0,1,140); sub(/ [^ ]*$/,"",s); print s " ~" } }'; }
field() { sed -nE "s/^$2: *(.*)$/\1/p" "$1" 2>/dev/null | head -1; }

safe_slug() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//' | cut -c1-60; }
thread_path() { printf '%s/%s.md' "$BASE" "$(safe_slug "$1")"; }
attempts() { field "$(thread_path "$1")" attempts; }

AREA=""; GOAL=""
parse_pairs() { while [[ $# -gt 0 ]]; do case "$1" in
  --area) AREA="$2"; shift 2 ;; --goal) GOAL="$2"; shift 2 ;; *) die "unknown flag '$1'" ;; esac; done; }

case "${1:-}" in
  open)
    [[ $# -ge 2 ]] || die "usage: eng.sh open \"<slug>\" [--area a] [--goal g]"
    shift; SLUG="$1"; shift; parse_pairs "$@"
    AREA="${AREA:-misc}"; valid=0; for a in $AREAS; do [[ "$a" == "$AREA" ]] && valid=1; done
    [[ $valid -eq 1 ]] || die "--area '$AREA' not in taxonomy. Use one of: $AREAS"
    F="$(thread_path "$SLUG")"
    [[ -e "$F" ]] && die "thread already open: $(safe_slug "$SLUG") (use eng.sh try, or a new slug)"
    { echo "slug: $(safe_slug "$SLUG")"; echo "opened: $(today) $(now)"; echo "area: $AREA"
      echo "goal: $(one_line "$GOAL")"; echo "attempts: 0"; echo "verdict: open"; echo "---"; } > "$F"
    printf 'opened thread %s (attempts=0). Log every try with eng.sh try.\n' "$(safe_slug "$SLUG")"
    ;;

  try)
    [[ $# -ge 5 ]] || die "usage: eng.sh try \"<slug>\" \"<hypothesis>\" \"<command>\" \"<result>\""
    shift; SLUG="$1"; H="$2"; CMD="$3"; RES="$4"
    F="$(thread_path "$SLUG")"; [[ -e "$F" ]] || die "no such thread: $(safe_slug "$SLUG") (eng.sh open first)"
    n=$(attempts "$SLUG"); n=${n:-0}; n=$((n+1))
    sed -i -E "s/^attempts: .*/attempts: $n/" "$F"
    { echo; echo "### attempt $n — $(today) $(now)"; echo "hypothesis: $(one_line "$H")"
      echo "command: $(one_line "$CMD")"; echo "result: $(one_line "$RES")"; } >> "$F"
    printf 'attempt %s logged. %s\n' "$n" "$([[ $n -ge 3 ]] && echo '>>> 3+ attempts: a lesson is OWED (note.sh lesson).' || echo '(lesson owed at 3)')"
    ;;

  verdict)
    [[ $# -ge 3 ]] || die "usage: eng.sh verdict \"<slug>\" solved|dead"
    shift; SLUG="$1"; V="$2"
    case "$V" in solved|dead) ;; *) die "verdict must be solved or dead" ;; esac
    F="$(thread_path "$SLUG")"; [[ -e "$F" ]] || die "no such thread: $(safe_slug "$SLUG")"
    sed -i -E "s/^verdict: .*/verdict: $V/" "$F"
    sed -i -E "s/^closed: .*/closed: $(today) $(now)/" "$F" 2>/dev/null || printf 'closed: %s %s\n' "$(today)" "$(now)" >> "$F"
    n=$(attempts "$SLUG"); n=${n:-0}
    if [[ "$V" == "solved" && $n -ge 3 ]]; then echo "SOLVED after $n attempts -> MANDATORY: note.sh lesson (--trigger/--fix/--transfer). This is the high-value case."
    elif [[ "$V" == "solved" ]]; then echo "solved in $n attempt(s) -> quick win? note.sh quick \"<what>\" --do-not \"<what not to over-engineer>\""
    elif [[ $n -ge 3 ]]; then echo "dead after $n attempts -> note.sh negative \"<approach>\" --because \"<the condition that ruled it out>\" (a dead end is evidence too)"
    else echo "dead in $n attempt(s) -> too few to generalize; consider note.sh negative if a technique misled you"; fi
    ;;

  show) [[ $# -ge 2 ]] || die "usage: eng.sh show \"<slug>\""; cat "$(thread_path "$2")" 2>/dev/null || die "no such thread" ;;
  list)
    for f in "$BASE"/*.md; do [[ -e "$f" ]] || continue
      printf '%-28s attempts=%-3s verdict=%-6s %s\n' "$(field "$f" slug)" "$(field "$f" attempts)" "$(field "$f" verdict)" "$(one_line "$(field "$f" goal)")"
    done
    ;;
  *) printf 'eng.sh — attempt tracker. Subcommands: open | try | verdict | show | list\n'; exit 1 ;;
esac
