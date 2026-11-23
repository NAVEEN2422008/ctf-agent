---
name: cybersec
description: Cybersecurity analysis and penetration testing skill. Use when analyzing vulnerabilities, performing security assessments, penetration testing, or discussing offensive/defensive security techniques. Triggers on terms like pentest, exploit, vulnerability, scan, recon, hack, security audit.
---

# Cybersecurity Analysis Skill

## Operational Framework

### MITRE ATT&CK Mapping
Map all findings to MITRE ATT&CK techniques:
- **Reconnaissance**: T1595-T1599
- **Resource Development**: T1583-T1589
- **Initial Access**: T1189-T1199
- **Execution**: T1059-T1060
- **Persistence**: T1036-T1099
- **Privilege Escalation**: T1068-T1069
- **Defense Evasion**: T1027-T1140
- **Credential Access**: T1003-T1058
- **Discovery**: T1046-T1087
- **Lateral Movement**: T1021-T1080
- **Collection**: T1005-T1114
- **Exfiltration**: T1029-T1048

### OWASP Top 10 (2021) Mapping
- **A01**: Broken Access Control
- **A02**: Cryptographic Failures
- **A03**: Injection
- **A04**: Insecure Design
- **A05**: Security Misconfiguration
- **A06**: Vulnerable and Outdated Components
- **A07**: Identification and Authentication Failures
- **A08**: Software and Data Integrity Failures
- **A09**: Security Logging and Monitoring Failures
- **A10**: Server-Side Request Forgery

## Tool Reference

### Reconnaissance
| Tool | Purpose | Syntax |
|------|---------|--------|
| subfinder | Subdomain enum | `subfinder -d <domain> -silent` |
| httpx | HTTP probe | `cat subs.txt \| httpx -silent` |
| naabu | Port scan | `naabu -list hosts.txt -top-ports 1000` |
| nuclei | Vuln scan | `nuclei -u <url> -t templates/` |
| katana | Web crawler | `katana -u <url> -d 3` |
| gowitness | Screenshots | `cat urls.txt \| gowitness file -f` |

### Exploitation
| Tool | Purpose | Syntax |
|------|---------|--------|
| sqlmap | SQL injection | `sqlmap -u "url?id=1" --batch` |
| ffuf | Web fuzzer | `ffuf -u url/FUZZ -w wordlist.txt` |
| hydra | Brute force | `hydra -l user -P pass.txt target http-post-form` |
| netexec | AD attack | `netexec smb targets.txt -u user -p pass` |
| responder | LLMNR/NBT-NS | `responder -I eth0` |
| chisel | Pivoting | `chisel server --reverse` |

### Binary Exploitation
| Tool | Purpose | Syntax |
|------|---------|--------|
| ROPgadget | Find gadgets | `ROPgadget --binary <elf>` |
| one_gadget | One-shot gadgets | `one_gadget <libc>` |
| pwndbg | GDB plugin | `gdb -q <binary>` |
| checksec | Binary info | `checksec --file=<binary>` |

## Analysis Workflow

### 1. Scope Definition
```
[SCOPE] Authorized pentest / Code review / Hardening audit
[TARGET] IP range / Domain / Repository / Config
[OBJECTIVE] Full assessment / Specific vuln class / Compliance
[CONSTRAINTS] Rules of engagement / Timeframe / Exclusions
```

### 2. Reconnaissance Phase
```bash
# Passive
subfinder -d <target> -silent | httpx -silent

# Active
nmap -sC -sV -p- <target>
```

### 3. Vulnerability Analysis
```bash
# Web
ffuf -u <target>/FUZZ -w common.txt
nuclei -u <target> -severity critical,high

# Network
nmap --script vuln <target>
```

### 4. Exploitation (Authorized Only)
```bash
# Develop PoC
# Document impact
# Report findings
```

### 5. Post-Exploitation
```bash
# Privilege escalation
# Lateral movement
# Data access assessment
```

### 6. Reporting
```
[FINDING] Vulnerability description
[EVIDENCE] Steps to reproduce
[SEVERITY] CVSS score
[REMEDIATION] Fix recommendation
[MITRE] ATT&CK technique
```

## Output Format

Always structure findings as:
```
[VULN] Vulnerability Name
[OWASP/CWE] Classification
[SEVERITY] Critical/High/Medium/Low/Info
[EVIDENCE] Proof of concept
[REMEDIATION] Fix recommendation
[MITRE] ATT&CK technique mapping
```

## Rules of Engagement

1. **ALWAYS** obtain written authorization
2. Document all actions with timestamps
3. Minimize impact on production systems
4. Exfiltrate only authorized data
5. Clean up all artifacts after engagement
6. Report all findings including unintended access
