#!/usr/bin/env python3
"""GIT_SSH wrapper: run git-over-SSH through paramiko (no sshpass needed).

Git invokes this as:  wrapper [-o OPT VAL] [-p PORT] user@host 'git-upload-pack ...'
Credentials come from OTW_GIT_PASS; port from -p or OTW_GIT_PORT (default 2220).
"""
import os
import socket
import sys
import threading

import paramiko


def main():
    args = sys.argv[1:]
    dbg_on = bool(os.environ.get('OTW_GIT_DEBUG'))

    def dbg(msg):
        if dbg_on:
            print('[git-ssh] ' + msg, file=sys.stderr, flush=True)

    if dbg_on:
        dbg('argv=' + repr(sys.argv))
    port = int(os.environ.get('OTW_GIT_PORT', '2220'))
    cleaned = []
    i = 0
    while i < len(args):
        if args[i] == '-o' and i + 1 < len(args):
            i += 2
            continue
        if args[i] == '-p' and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
            continue
        cleaned.append(args[i])
        i += 1
    args = cleaned
    if len(args) < 2:
        dbg('bad args')
        return 2
    target, command = args[0], ' '.join(args[1:])
    user, host = target.rsplit('@', 1) if '@' in target else (None, target)
    dbg(f'connect {user}@{host}:{port} cmd={command}')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port, username=user,
                       password=os.environ.get('OTW_GIT_PASS', ''),
                       timeout=30, allow_agent=False, look_for_keys=False)
        stdin, stdout, stderr = client.exec_command(command, timeout=300)
    except Exception as exc:
        print(f'[git-ssh] {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1
    chan = stdout.channel
    chan.settimeout(15)
    dbg('connected; entering read loop')

    def pump_in():
        try:
            while True:
                data = os.read(0, 4096)
                if not data:
                    break
                dbg(f'stdin -> remote {len(data)} bytes')
                stdin.write(data)
                stdin.flush()
            dbg('stdin EOF; shutdown_write')
            stdin.channel.shutdown_write()
        except Exception as exc:
            dbg(f'pump_in error {type(exc).__name__}: {exc}')

    threading.Thread(target=pump_in, daemon=True).start()

    while True:
        try:
            data = chan.recv(65536)
            if not data:
                dbg('recv EOF')
                break
            dbg(f'recv {len(data)} bytes')
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except socket.timeout:
            if chan.exit_status_ready():
                dbg('timeout + exit ready')
                break
            continue
        except Exception as exc:
            dbg(f'recv error {type(exc).__name__}: {exc}')
            break

    rc = chan.recv_exit_status()
    dbg(f'exit {rc}')
    client.close()
    return rc


if __name__ == '__main__':
    sys.exit(main())
