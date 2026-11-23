---
description: Directory and content fuzzing with ffuf
agent: webapp
---

Execute directory fuzzing against: $ARGUMENTS

## Common Directories
```bash
ffuf -u $ARGUMENTS/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403 -o ffuf_common.json -of json
```

## Large Directories
```bash
ffuf -u $ARGUMENTS/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-directories.txt -mc 200,301,302,403 -o ffuf_raft.json -of json
```

## File Extensions
```bash
ffuf -u $ARGUMENTS/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-files.txt -mc 200 -o ffuf_files.json -of json
```

## Parameter Discovery
```bash
ffuf -u $ARGUMENTS -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -mc 200 -o ffuf_params.json -of json
```

## Virtual Host Discovery
```bash
DOMAIN=$(echo $ARGUMENTS | sed 's|https\?://||' | cut -d/ -f1)
ffuf -u $ARGUMENTS -H "Host: FUZZ.$DOMAIN" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200 -o ffuf_vhosts.json -of json
```

## Recursion
```bash
ffuf -u $ARGUMENTS/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-directories.txt -mc 200 -recursion -recursion-depth 2 -o ffuf_recursive.json -of json
```

## Results Analysis
```bash
cat ffuf_common.json | jq '.results[] | {url: .url, status: .status, length: .length}'
```
