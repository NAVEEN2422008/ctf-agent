id: 
date: 2026-11-22
host: REI
area: tooling
tags: git,ssh,paramiko,overthewire,bandit
title: git-shell repos need paramiko GIT_SSH wrapper, not SFTP or shell commands
context: OverTheWire Bandit 27-31 git levels: git-shell rejects arbitrary commands, SFTP EOF during negotiation
trigger: Five sequential wrapper misconfigurations before clone worked: ssh variant, wrong host, -o parsing, recv_ready stall, read(4096) blocking
fix: paramiko GIT_SSH wrapper with GIT_SSH_VARIANT=ssh, real hostname, -o/-p arg parsing, blocking chan.recv with timeout, and os.read(0,4096) for stdin
verify: OTW_GIT_PASS=... GIT_SSH=... GIT_SSH_VARIANT=ssh git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo /tmp/otw_repo27
transfer: Any forced-command SSH account that only speaks a binary protocol (git-shell, cvs, etc.) can be driven from local tools via a paramiko-backed GIT_SSH/SSH ~
---

## Trigger — why this was hard
    Five sequential wrapper misconfigurations before clone worked: ssh variant, wrong host, -o parsing, recv_ready stall, read(4096) blocking
## Wrong assumptions discarded
    Assumed git-shell would allow ls/cat/git log via exec_command; assumed SFTP would work; assumed sys.stdin.buffer.read(4096) forwards small pkt-lines
## Actual root cause / what worked
    paramiko GIT_SSH wrapper with GIT_SSH_VARIANT=ssh, real hostname, -o/-p arg parsing, blocking chan.recv with timeout, and os.read(0,4096) for stdin
## Verification (the command that proves it)
    OTW_GIT_PASS=... GIT_SSH=... GIT_SSH_VARIANT=ssh git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo /tmp/otw_repo27
## Transfer — reuse this when
    Any forced-command SSH account that only speaks a binary protocol (git-shell, cvs, etc.) can be driven from local tools via a paramiko-backed GIT_SSH/SSH wrapper; inspect the exact argv the client passes before writing the parser
