#!/usr/bin/env python3
"""Run a batch of SSH commands across successive wargame levels.

Usage:
  python3 otw_batch.py '[{"host":"bandit.labs.overthewire.org","port":2220,
      "user":"bandit1","pass":"...","cmd":"cat ./-","label":"bandit-1"}, ...]'

Each item is independent (own connection). Prints labelled stdout/stderr blocks.
"""
import json
import sys
import paramiko

def main():
    items = json.loads(sys.argv[1])
    for item in items:
        label = item.get('label', item.get('user', '?'))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(item['host'], int(item.get('port', 2220)),
                           username=item['user'], password=item['pass'],
                           timeout=20, allow_agent=False, look_for_keys=False)
            _, stdout, stderr = client.exec_command(item['cmd'], timeout=25)
            out = stdout.read().decode('utf-8', 'replace').strip()
            err = stderr.read().decode('utf-8', 'replace').strip()
            print(f'=== {label} :: {item["cmd"]} ===')
            if out:
                print(out)
            if err:
                print('[stderr] ' + err.replace('\n', '\n[stderr] '))
        except Exception as exc:
            print(f'=== {label} ERROR {type(exc).__name__}: {exc} ===')
        finally:
            client.close()

if __name__ == '__main__':
    main()
