---
description: Secret-scan, stage, commit and push all new skills, research notes, playbooks and config changes to the private ctf-agent repo
---

# /backup-github

One-command backup of this OpenCode CTF agent to the **private** `ctf-agent`
GitHub repository. Run it after learning something new, adding a skill, or
changing config.

## Hard rules

- Never stage or push `.opencode/.worker_session.json`,
  `.opencode/.worker_specs.json`, `.opencode/memory/otw_campaign_state.json`,
  `notes/.otw_session_creds.tmp`, `.env`, `*.key`, `*.pem`, `*auth*`,
  `*secret*`, `*token*`, or `auth.jar`. `.gitignore` enforces this — verify it.
- Never print a secret's value into chat. Report file + line + pattern only.
- If the secret scan finds anything, STOP. Redact it (replace with an env var
  placeholder such as `${NVIDIA_API_KEY}`), re-scan to 0, then continue.
- The repo must be private. Never call `gh repo create` without `--private`.

## Step 1 — Re-run the secret scan

```bash
cd ~/ctf
python3 - <<'PY'
import subprocess, os, re
files = subprocess.check_output(
    ['git','ls-files','--cached','--others','--exclude-standard'], text=True
).splitlines()
pats = [
 ('nvidia', r'nvapi-[A-Za-z0-9_\-]{8,}'),
 ('google', r'AIza[A-Za-z0-9_\-]{10,}'),
 ('openai', r'\bsk-[A-Za-z0-9_\-]{12,}'),
 ('github', r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}'),
 ('aws', r'\bAKIA[0-9A-Z]{16}\b'),
 ('privkey', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
 ('bearer', r'Bearer\s+[A-Za-z0-9_\-\.]{20,}'),
 ('urlcred', r'https?://[^/\s:@]+:[^/\s@]+@'),
 ('assigned_secret', r'(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token|client[_-]?secret)\b\s*[:=]\s*["\']([^"\']{8,})["\']'),
 ('worker_token_literal', r'X-Worker-Token["\']?\s*[:=]\s*["\'][A-Za-z0-9_\-]{12,}["\']'),
]
placeholder = re.compile(r'^\s*(\$\{|\$\(|<|\{ENV|os\.environ|getenv|changeme|CHANGE|example|placeholder|REDACTED|your_)', re.I)
hits = []
for f in files:
    if not os.path.isfile(f): continue
    raw = open(f,'rb').read()
    if b'\0' in raw[:4096]: continue
    for i, line in enumerate(raw.decode('utf-8','ignore').splitlines(), 1):
        for name, p in pats:
            m = re.search(p, line)
            if not m: continue
            if name == 'assigned_secret' and placeholder.match(m.group(2)): continue
            hits.append((f, i, name))
print('files scanned:', len(files), '| secret hits:', len(hits))
for h in hits: print(f'  {h[0]}:{h[1]} [{h[2]}]')
PY
```

Also confirm the forbidden paths are ignored:

```bash
git check-ignore -v .opencode/.worker_session.json \
  .opencode/.worker_specs.json .opencode/memory/otw_campaign_state.json \
  notes/.otw_session_creds.tmp .env auth.jar
```

Proceed only when the scan reports **0 secret hits** and every path above is
reported as ignored.

## Step 2 — Summarize what was newly learned

Compare the working tree against `HEAD` and write a short bullet list of new
skills, research notes, playbooks, patterns, lessons, and config changes:

```bash
git status --short
git diff --stat HEAD
```

## Step 3 — Stage, commit, push

```bash
git add -A
git diff --cached --name-only          # final eyeball: no secrets, no auth.jar
git commit -m "backup: opencode ctf-agent config, skills, and memory snapshot ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
git branch -M main
git push origin main
```

If `origin` is missing, create/attach the private repo first:

```bash
gh auth status                         # must be logged in
gh repo view ctf-agent >/dev/null 2>&1 \
  && git remote add origin git@github.com:$(gh api user --jq .login)/ctf-agent.git \
  || gh repo create ctf-agent --private --source=. --remote=origin
```

## Step 4 — Report

Print the repo URL, the list of pushed files, and an explicit confirmation of
the secret-scan result (e.g. "0 secrets or credentials uploaded").
