#!/usr/bin/env python3
"""Fetch a Natas level page with HTTP Basic auth.

Usage: otw_natas.py <level> <password> [path] [--data 'k=v&k2=v2']
"""
import sys
import requests


def main():
    level = int(sys.argv[1])
    password = sys.argv[2]
    args = sys.argv[3:]
    data = None
    if '--data' in args:
        i = args.index('--data')
        from urllib.parse import parse_qs
        data = {k: v[0] for k, v in parse_qs(args[i + 1]).items()}
        args = args[:i] + args[i + 2:]
    path = args[0] if args else ''
    url = f'http://natas{level}.natas.labs.overthewire.org/{path}'
    if data:
        r = requests.post(url, auth=(f'natas{level}', password),
                          data=data, timeout=30, allow_redirects=False)
    else:
        r = requests.get(url, auth=(f'natas{level}', password),
                         timeout=30, allow_redirects=False)
    print(f'STATUS {r.status_code} URL {r.url}')
    print('HEADERS', dict(r.headers))
    print('--- BODY ---')
    print(r.text)


if __name__ == '__main__':
    main()
