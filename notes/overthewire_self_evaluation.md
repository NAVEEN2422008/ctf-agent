# OverTheWire — Brutally Honest Self-Evaluation

Live scorecard. Updated after every wargame. Rubric: 100 points total.

- Recon & Planning — 15
- Solve Rate — 35 (strictly proportional to solved / total)
- Research Quality & Note-Taking — 15
- Efficiency & Loop Discipline — 20 (deduct for wasted commands, syntax errors, dead ends)
- Self-Awareness & Honesty — 15

## Live table

| Wargame | Total Levels | Solved | Needs Retry | Honest Score |
|---|---|---|---|---|
| Bandit | 34 | 34 | 0 | 90/100 |
| Natas | 35 | 0 | 0 | — |
| Krypton | 7 | 0 | 0 | — |
| Leviathan | 8 | 0 | 0 | — |
| Narnia | 10 | 0 | 0 | — |
| Behemoth | 9 | 0 | 0 | — |
| Utumno | 9 | 0 | 0 | — |
| Maze | 10 | 0 | 0 | — |
| Vortex | 27 | 0 | 0 | — |
| Manpage | 7 | 0 | 0 | — |
| Drifter | TBD | 0 | 0 | — |
| FormulaOne | TBD | 0 | 0 | — |

## Bandit score breakdown (90/100)

- Recon & Planning: 15/15 — official pages fetched, tool/reachability audit done up front.
- Solve Rate: 35/35 — 34/34 levels solved, zero `NEEDS_RETRY`.
- Research Quality & Note-Taking: 14/15 — concept notes written for `xxd -r` and the
  git-shell/paramiko wrapper; one point off because the git-history pattern notes were
  only written after the fact, not before solving.
- Efficiency & Loop Discipline: 11/20 — nine recorded dead ends / wasted commands:
  `xxd -r -p` mistake (L12), decompression-loop `f=f` reset (L12), bandit26 `exec_command`
  timeout from forced `showtext` shell (L26), missing `json` import on checkpoint (L26),
  and five separate git-wrapper misconfigurations (ssh variant, wrong host, `-o` parsing,
  `recv_ready()` stall, `read(4096)` blocking). All were diagnosed and logged, but the
  deduction is real.
- Self-Awareness & Honesty: 15/15 — no walkthroughs used, all failures recorded, score
  reflects the wasted cycles rather than the clean final state.

## Deductions so far

- Bandit: −9 efficiency (nine dead ends listed above), −1 research quality.

## Top weaknesses (honest, live)

1. Tool-building under time pressure produced five sequential config errors in the git
   wrapper; should have inspected git's actual argv before writing the parser.
2. `ltrace` missing (needed for Leviathan); `sshpass` missing (mitigated by paramiko helper).
3. Vortex SSH endpoint timed out on first probe — unresolved reachability risk.
4. Campaign scope is very large (156+ levels); sustained efficiency across sessions is unproven.
