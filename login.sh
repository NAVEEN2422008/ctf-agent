#!/usr/bin/env bash
# Interactive login helper for CYBERCOM CTF.
# Reads credentials with hidden input IN YOUR TERMINAL and writes only a
# 0600 cookie jar. The password is never printed, never logged, never
# passed on the command line, and never reaches the assistant context.
set -euo pipefail

JAR="$HOME/ctf/auth.jar"
URL="https://infra.cybercomctf.com/api/v1/auth/login"

echo "CYBERCOM CTF - authenticated login"
echo "-----------------------------------"
printf "Username or email: "
IFS= read -r USER
printf "Password (hidden): "
IFS= read -rs PASS
echo

# Build JSON safely without shell interpolation issues.
BODY=$(python3 -c 'import json,sys; print(json.dumps({"email":sys.argv[1],"password":sys.argv[2]}))' "$USER" "$PASS")

# POST, keep cookies, discard body so no token/field is echoed.
CODE=$(curl -s -o /tmp/.cc_login_body -w '%{http_code}' -c "$JAR" \
  -X POST "$URL" \
  -H 'Content-Type: application/json' \
  --data-binary "$BODY")

unset BODY PASS USER
rm -f /tmp/.cc_login_body

chmod 600 "$JAR" 2>/dev/null || true
COOKIES=$(grep -c . "$JAR" 2>/dev/null || echo 0)

echo "-----------------------------------"
echo "HTTP status : $CODE"
if [ "$COOKIES" -gt 1 ]; then
  echo "Cookies set : $COOKIES"
fi
case "$CODE" in
  200) echo "RESULT      : SUCCESS" ;;
  401) echo "RESULT      : INVALID CREDENTIALS" ;;
  403) echo "RESULT      : FORBIDDEN" ;;
  *)   echo "RESULT      : UNEXPECTED" ;;
esac
echo "Cookie jar  : $JAR (perms $(stat -c %a "$JAR" 2>/dev/null || echo '?'))"
echo
echo ">> Report ONLY the status + cookie count to the assistant."
echo ">> Never paste the password or the jar contents."
