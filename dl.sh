#!/usr/bin/env bash
UA='Mozilla/5.0 (X11; Linux x86_64) Chrome/140.0'
URL=$(curl -s -b auth.jar -H "User-Agent: $UA" "https://infra.cybercomctf.com/api/v1/files/$1" \
      | python3 -c 'import sys,json;print(json.load(sys.stdin).get("url",""))')
[ -z "$URL" ] && { echo "NO URL file $1"; exit 1; }
curl -s -L -H "User-Agent: $UA" "$URL" -o "$2" && echo "OK $2 $(stat -c%s "$2")B" || echo "FAIL $2"
