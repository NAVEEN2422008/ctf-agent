# ctf-agent

A portable, self-learning OpenCode CTF/offensive-security agent setup. This
repository is the **sanitized** snapshot of the controller configuration, custom
agents, slash commands, skills, worker scripts, and accumulated learning memory.
No credentials, session state, or API keys are stored here.

## What this setup includes

### Architecture

- **Controller** — lightweight Linux box (Intel i5 2nd Gen, **4 GB RAM**), zsh,
  Python 3.13, running OpenCode with a small-model-first routing strategy
  (NVIDIA NIM free tier, ~40 RPM) to stay within the memory/CPU budget.
- **Windows worker over Tailscale Funnel** — a reverse-pull job broker
  (`worker_broker.py`, bound to `127.0.0.1:8765`) plus a session/payload manager
  (`worker_manager.py`). The controller opens a Tailscale Funnel, generates a
  base64-encoded in-memory Python one-liner for the Windows host, and the worker
  long-polls `/next-job`, executes inside `tempfile.TemporaryDirectory()`, and
  POSTs results to `/result`. No `.py` file is ever written on Windows; all
  endpoints require an `X-Worker-Token` header that is generated at runtime.
- **Self-learning memory** — two complementary stores:
  - `cyber-lessons/` — ranked lessons, mistakes, negatives, quick wins, and a
    transfer-oriented playbook (`note.sh`, `eng.sh`, `INDEX.md`).
  - `.opencode/memory/` — solved-technique and dead-end patterns, research
    notes, playbooks, templates, and benchmark reports.

### Contents

| Path | What it is |
|---|---|
| `opencode.json` | Sanitized OpenCode config (agents, commands, MCP servers, permissions) |
| `backup/global_opencode.json` | Sanitized copy of `~/.config/opencode/opencode.json` |
| `backup/global_AGENTS.md` | Global environment/instructions file |
| `backup/mcp/` | Local MCP server sources (filesystem, memory, sequential-thinking, playwright, security-tools, ghost-intel, ghost-web, ghost-network, cve-search) |
| `.opencode/agent/` | 13 custom agent definitions |
| `.opencode/commands/` | 12 slash commands (incl. `/backup-github`, `/otw-continue`, recon/scan/fuzz/vuln/exploit) |
| `.opencode/skills/` | 20 specialized skills |
| `.opencode/scripts/` | Worker broker/manager and benchmark scripts |
| `.opencode/memory/` | Patterns, research notes, playbooks, templates, benchmark reports, OTW helpers |
| `playbooks/` | Campaign playbooks (e.g. Bandit) |
| `cyber-lessons/` | Durable cross-session lesson store |
| `notes/` | OverTheWire recon, self-evaluation, and self-improvement reports |
| `AGENTS.md`, `INSTALLED_TOOLS.md` | Workspace conventions and verified tool inventory |

## Restore on a fresh machine

1. **Clone the private repo**

   ```bash
   git clone git@github.com:<your-username>/ctf-agent.git ~/ctf-agent
   cd ~/ctf-agent
   ```

2. **Install OpenCode** (follow the official installer for your platform), then
   put the config in place:

   ```bash
   mkdir -p ~/.config/opencode
   cp opencode.json ~/.config/opencode/opencode.json
   cp -a .opencode/agent ~/.config/opencode/
   cp -a .opencode/skills ~/.config/opencode/
   cp -a .opencode/commands ~/.config/opencode/command/
   cp -a .opencode/scripts ~/.opencode/scripts/
   cp -a .opencode/memory ~/.opencode/memory/
   cp -a cyber-lessons ~/cyber-lessons
   ```

   The MCP command paths in `opencode.json` are absolute
   (`/home/naveenkumar/...`). Update them to your `$HOME` before use.

3. **Set API keys via `/connect`** — do **not** paste keys into config files or
   commit them. Prefer environment variables (`${NVIDIA_API_KEY}`, etc.). This
   repository intentionally contains zero key material.

4. **Install the lightweight Python packages** used by the memory/worker
   scripts (all pure-Python or small wheels; no heavy build step):

   ```bash
   pip install --user paramiko requests beautifulsoup4 pwntools \
       pycryptodome z3-solver scapy
   ```

   The worker one-liner additionally uses `requests` on the Windows host.

5. **Verify**

   ```bash
   python3 -m py_compile .opencode/scripts/*.py .opencode/memory/*.py
   git check-ignore -v .opencode/memory/otw_campaign_state.json auth.jar
   ```

6. **Authenticate GitHub** for future `/backup-github` runs:

   ```bash
   gh auth login          # or use an SSH key with push access
   ```

## Backing up future learning

Run `/backup-github`. It re-runs the secret scan, stages new skills/research
notes/playbooks/config changes, commits a timestamped snapshot, and pushes to
`ctf-agent`. See `.opencode/commands/backup-github.md`.

## Current learning stats

| Metric | Count |
|---|---|
| Custom agents | 13 |
| Slash commands | 12 |
| Skills | 20 |
| Worker/benchmark scripts | 5 |
| Research notes & reports | 4 |
| Playbooks | 2 |
| Pattern files / entries | 2 / 8 |
| Solved techniques logged | 31 |
| Durable lessons (`cyber-lessons`) | 10 |
| Memory files total | 15 |

## Security posture

- `.gitignore` strictly excludes `.opencode/.worker_session.json`,
  `.opencode/.worker_specs.json`, `.opencode/memory/otw_campaign_state.json`,
  `notes/.otw_session_creds.tmp`, `.env`, `*.key`, `*.pem`, `*auth*`, `*secret*`,
  `*token*`, and `auth.jar`.
- The last full scan of all staged files reported **0 secrets / 0 credentials**.
- Worker tokens are generated at runtime (`secrets.token_hex(16)`), never stored.
- The repository is **private**.
