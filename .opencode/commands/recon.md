---
description: Full reconnaissance pipeline: subdomain enumeration, live host detection, port scanning, screenshots, and vulnerability scanning
agent: recon
---

Execute a full reconnaissance pipeline against the target: $ARGUMENTS

## Phase 1: Subdomain Enumeration
```bash
# Passive subdomain discovery
subfinder -d $ARGUMENTS -silent -o subs_passive.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%25.$ARGUMENTS&output=json" | jq -r '.[].name_value' | sort -u > subs_ct.txt

# Combine and deduplicate
cat subs_passive.txt subs_ct.txt | sort -u > subs_all.txt
echo "[*] Found $(wc -l < subs_all.txt) subdomains"
```

## Phase 2: Live Host Detection
```bash
cat subs_all.txt | httpx -silent -status-code -title -tech-detect -follow-redirects > live_hosts.txt
echo "[*] $(wc -l < live_hosts.txt) live hosts found"
```

## Phase 3: Port Scanning
```bash
# Top 1000 ports
naabu -list subs_all.txt -top-ports 1000 -silent -o ports_top.txt

# Service detection on open ports
cat ports_top.txt | cut -d: -f1 | sort -u > hosts_open.txt
nmap -sC -sV -iL hosts_open.txt -oN nmap_services.txt
```

## Phase 4: Web Screenshots
```bash
cat live_hosts.txt | cut -d' ' -f1 > urls.txt
gowitness file -f urls.txt -P screenshots/ --timeout 30
```

## Phase 5: Vulnerability Scanning
```bash
nuclei -list urls.txt -t ~/nuclei-templates/ -severity critical,high,medium -o nuclei_results.txt
```

## Phase 6: Wayback URLs
```bash
cat subs_all.txt | waybackurls | sort -u > wayback_urls.txt
```

## Output Summary
```
[+] Recon Complete for $ARGUMENTS
    Subdomains: subs_all.txt
    Live Hosts: live_hosts.txt
    Ports: ports_top.txt
    Services: nmap_services.txt
    Screenshots: screenshots/
    Vulnerabilities: nuclei_results.txt
    Wayback URLs: wayback_urls.txt
```
