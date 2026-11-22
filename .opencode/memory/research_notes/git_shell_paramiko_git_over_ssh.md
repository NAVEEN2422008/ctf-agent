# git-shell over paramiko (no sshpass, no SFTP)

## Context
OverTheWire Bandit git levels (27–31) expose repos to users whose login shell is
`git-shell`. Arbitrary commands (`ls`, `cat`, `git log`) are rejected with
`fatal: unrecognized command '...'`, and SFTP fails with `SSHException: EOF during negotiation`.

## Working approach
Use a `GIT_SSH` wrapper backed by paramiko so local `git clone`/`git push` speak
the git protocol through git-shell. Implementation: `.opencode/memory/otw_git_ssh.py`.

```bash
OTW_GIT_PASS='<password>' \
GIT_SSH=/home/naveenkumar/ctf/.opencode/memory/otw_git_ssh.py \
GIT_SSH_VARIANT=ssh \
git clone ssh://bandit<N>-git@bandit.labs.overthewire.org:2220/home/bandit<N>-git/repo /tmp/repo<N>
```

## Five traps hit while building the wrapper (all verified)
1. `GIT_SSH_VARIANT` defaults to `simple`, which refuses `-p PORT`:
   `fatal: ssh variant 'simple' does not support setting port`. Set `GIT_SSH_VARIANT=ssh`.
2. The URL host must be the real host (`bandit.labs.overthewire.org`), not `localhost`
   (the official page uses `localhost` because it assumes you are already on the box).
   Using `localhost` gives `gaierror: [Errno -2] Name or service not known` — actually it
   resolves locally but connects to the wrong machine.
3. Git invokes the wrapper with `-o SendEnv=GIT_PROTOCOL -p 2220 user@host 'git-upload-pack ...'`.
   A parser that only checks `argv[1] == '-p'` misparses the host. Skip `-o <val>` pairs.
4. Polling `chan.recv_ready()` stalled after receiving the 334-byte advertisement.
   Blocking `chan.recv(65536)` with `chan.settimeout(15)` works.
5. `sys.stdin.buffer.read(4096)` blocks until 4096 bytes; git sends tiny pkt-lines, so
   nothing was forwarded and the clone deadlocked. Use `os.read(0, 4096)` which returns
   available bytes immediately.

## Transfer
Any SSH account restricted to `git-shell` (or any forced command that only accepts a
specific protocol) can be driven from local git tools with a paramiko `GIT_SSH` wrapper,
provided credentials are available. The same wrapper handled `git-receive-pack` for the
level-31 push, where the pre-receive hook printed the next password and then rejected
the push (expected — do not treat the rejection as failure).
