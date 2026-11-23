---
name: offensive-recon
description: Execute structured network reconnaissance, service enumeration, and attack surface mapping for authorized penetration testing engagements.
---

# Offensive Reconnaissance Skill

## When to Use
Use this skill when performing reconnaissance against authorized targets during penetration testing engagements. This includes passive OSINT, active enumeration, and attack surface mapping.

## Execution Phases

### Phase 1: Passive Reconnaissance
```bash
# Subdomain enumeration
subfinder -d <target> -silent -o subs_passive.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%25.<target>&output=json" | jq -r '.[].name_value' | sort -u > subs_ct.txt

# Combine results
cat subs_passive.txt subs_ct.txt | sort -u > subs_all.txt
```

### Phase 2: Active Enumeration
```bash
# Live host detection
cat subs_all.txt | httpx -silent -status-code -title > live_hosts.txt

# Port scanning
naabu -list subs_all.txt -top-ports 1000 -silent > ports.txt

# Service detection
nmap -sC -sV -iL <hosts_file> -oN services.txt
```

### Phase 3: Attack Surface Mapping
```bash
# Web technology detection
httpx -list live_hosts.txt -tech-detect -status-code

# Directory fuzzing
ffuf -u <target>/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403

# Subdomain takeover check
subfinder -d <target> -silent | httpx -silent -status-code | grep -E "200|404|NXDOMAIN"
```

### Phase 4: Vulnerability Discovery
```bash
# Nuclei scan
nuclei -list live_hosts.txt -t ~/nuclei-templates/ -severity critical,high

# Wayback URLs
cat subs_all.txt | waybackurls | sort -u > wayback.txt

# JavaScript analysis
katana -u <target> -d 3 -jc
```

## Output Format
```
[RECON] Target: <domain>
[SUBDOMAINS] Count: X
[LIVE_HOSTS] Count: X
[PORTS] Open: X
[VULNS] Critical: X, High: X, Medium: X
[RISK] Overall risk assessment
```

## Verification Steps
1. Verify subdomain count matches expected scope
2. Validate live hosts respond correctly
3. Confirm port scan covers all expected services
4. Review vulnerability findings for false positives
