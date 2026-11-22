#!/usr/bin/env python3
"""Reusable paramiko SSH command runner for OverTheWire shell games.

Usage:
  python3 otw_ssh.py <host> <port> <user> <password> '<remote command>' [timeout]

Prints stdout, then stderr prefixed with '[stderr]'. Exits with the remote exit code.
No sshpass needed. Credentials are passed as argv (avoid shell history by using the
campaign state file as the source in automation).
"""
import sys
import paramiko

def main():
    if len(sys.argv) < 6:
        print(__doc__, file=sys.stderr)
        return 2
    host, port, user, password, command = sys.argv[1:6]
    timeout = int(sys.argv[6]) if len(sys.argv) > 6 else 20
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, int(port), username=user, password=password,
                       timeout=timeout, allow_agent=False, look_for_keys=False,
                       compress=False)
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode('utf-8', 'replace')
        err = stderr.read().decode('utf-8', 'replace')
        rc = stdout.channel.recv_exit_status()
        if out:
            sys.stdout.write(out)
        if err:
            sys.stdout.write('[stderr] ' + err.replace('\n', '\n[stderr] '))
        return rc
    except Exception as exc:
        print(f'[ssh-error] {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1
    finally:
        client.close()

if __name__ == '__main__':
    sys.exit(main())
