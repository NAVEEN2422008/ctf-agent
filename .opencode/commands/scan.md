---
description: Nmap service scan with default scripts and version detection
agent: recon
---

Execute comprehensive Nmap scan against: $ARGUMENTS

## Quick Service Scan
```bash
nmap -sC -sV -oN scan_quick.txt $ARGUMENTS
```

## Full Port Scan
```bash
nmap -sC -sV -p- -T4 -oN scan_full.txt $ARGUMENTS
```

## UDP Top 100
```bash
nmap -sU --top-ports 100 -oN scan_udp.txt $ARGUMENTS
```

## Vulnerability Scan
```bash
nmap --script vuln -oN scan_vuln.txt $ARGUMENTS
```

## All Scans
```bash
echo "[*] Starting scans against $ARGUMENTS"
nmap -sC -sV -p- -T4 -oN scan_all.txt --script vuln $ARGUMENTS
echo "[+] Scan complete: scan_all.txt"
```
