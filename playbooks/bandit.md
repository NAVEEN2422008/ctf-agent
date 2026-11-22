# Bandit playbook — verified techniques (34/34 solved)

## SSH access pattern
```python
import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('bandit.labs.overthewire.org', 2220,
          username=f'bandit{n}', password=PASSWORD,
          timeout=30, allow_agent=False, look_for_keys=False)
_, o, e = c.exec_command('command', timeout=45)
```
`sshpass` is not installed; paramiko is the reliable path.

## Forced-shell escapes
- **L25 → L26** (`showtext` → `more`): open PTY with `height=5`, send `v`, then vi
  `:e /etc/bandit_pass/bandit26`, `:set shell=/bin/bash`, `:shell`.
- **L26 → L27**: from the escaped bash, `./bandit27-do cat /etc/bandit_pass/bandit27`.
  `exec_command` directly on bandit26 times out because the forced `showtext` shell
  does not handle non-interactive commands.
- **L32 → L33** (uppercase shell): send `$0` — no letters to uppercase, so `sh -c '$0'`
  spawns a real shell. Then `cat /etc/bandit_pass/bandit33`.

## Decompression loop (L12)
- `xxd -r` (NOT `xxd -r -p`) to turn hex text back into binary.
- Reset `f=f` after each gzip/bzip2 stage; the file variable must point at the
  newly decompressed output.

## Network levels
- **L16**: TLS service on localhost:31790 returns an SSH private key for bandit17.
- **L20**: local listener thread + `./suconnect 54321`.
- **L24**: brute-force 4-digit PIN on localhost:30002 using one persistent socket.

## Git levels (27–31)
Use the paramiko `GIT_SSH` wrapper at `.opencode/memory/otw_git_ssh.py`:
```bash
OTW_GIT_PASS='<password>' \
GIT_SSH=/home/naveenkumar/ctf/.opencode/memory/otw_git_ssh.py \
GIT_SSH_VARIANT=ssh \
git clone ssh://bandit<N>-git@bandit.labs.overthewire.org:2220/home/bandit<N>-git/repo /tmp/repo<N>
```
- L27: password in deleted commit / current README.
- L28: `git log -p --all` — password removed in HEAD, present in earlier commit.
- L29: `git branch -a` — password only in `origin/dev`.
- L30: `git tag -l` + `git show <tag>` — password in annotated tag object.
- L31: create `key.txt` with `May I come in?`, `git add -f` (blocked by `*.txt` in
  `.gitignore`), commit, push. Pre-receive hook prints the password then rejects
  the push — the rejection is expected.

## Checkpoint discipline
After every level:
```bash
python3 .opencode/memory/otw_checkpoint.py '{"wargame":"bandit","level":N,"status":"solved","password":"<next>","attempts":N,"commands":[...],"notes":"..."}'
```
The helper auto-advances `current_wargame/current_level` and recomputes stats.
