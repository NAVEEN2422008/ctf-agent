#!/usr/bin/env bash
# sub.sh <challenge_id> <flag>
curl -s -b auth.jar -H 'User-Agent: Mozilla/5.0' -H 'Content-Type: application/json' \
  -X POST https://infra.cybercomctf.com/api/v1/challenges/attempt \
  -d "{\"challenge_id\":$1,\"flag\":\"$2\"}"
