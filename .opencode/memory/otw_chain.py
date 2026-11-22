#!/usr/bin/env python3
"""Chain sequential SSH levels (Bandit-style), auto-extracting each next password.

Usage:
  python3 otw_chain.py '{
    "host":"bandit.labs.overthewire.org","port":2220,
    "start_user":"bandit1","start_pass":"<password>",
    "steps":[{"level":1,"cmd":"cat ./-","notes":"dashed filename"}]
  }'

For each step: connect, run cmd, extract the 32-char password from output,
print it, and call otw_checkpoint.py to persist the level. Add
"checkpoint":false to a step to skip persistence (useful for probing).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import paramiko

HERE = Path(__file__).resolve().parent
CHECKPOINT = HERE / 'otw_checkpoint.py'


def extract_password(output):
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    for ln in reversed(lines):
        if 'password' in ln.lower():
            found = re.findall(r'[A-Za-z0-9]{32}', ln)
            if found:
                return found[-1]
    for ln in reversed(lines):
        found = re.findall(r'[A-Za-z0-9]{32}', ln)
        if found:
            return found[-1]
    return None


def main():
    cfg = json.loads(sys.argv[1])
    host = cfg['host']
    port = int(cfg.get('port', 2220))
    game = cfg.get('game', 'bandit')
    user = cfg['start_user']
    password = cfg['start_pass']

    for step in cfg['steps']:
        level = int(step['level'])
        cmd = step['cmd']
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host, port, username=user, password=password,
                           timeout=20, allow_agent=False, look_for_keys=False)
            _, stdout, stderr = client.exec_command(cmd, timeout=30)
            out = stdout.read().decode('utf-8', 'replace')
            err = stderr.read().decode('utf-8', 'replace')
        except Exception as exc:
            print(f'LEVEL {level} SSH_ERROR {type(exc).__name__}: {exc}')
            break
        finally:
            client.close()

        nxt = extract_password(out)
        print(f'=== LEVEL {level} ({user}) cmd={cmd!r} ===')
        print(out.strip()[:1200])
        if err.strip():
            print('[stderr] ' + err.strip()[:400])
        if not nxt:
            print(f'LEVEL {level} NO_PASSWORD_EXTRACTED — stopping chain')
            break

        if step.get('checkpoint', True):
            payload = {
                'wargame': game, 'level': level, 'status': 'solved',
                'password': nxt, 'attempts': int(step.get('attempts', 1)),
                'commands': [cmd], 'notes': step.get('notes', ''),
            }
            subprocess.run([sys.executable, str(CHECKPOINT), json.dumps(payload)],
                           check=True)

        password = nxt
        user = f'{game}{level + 1}'
        print(f'LEVEL {level} PASSWORD -> {password}')


if __name__ == '__main__':
    main()
