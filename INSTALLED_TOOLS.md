# INSTALLED TOOLS & SKILLS DOCUMENTATION
# CTF Multi-Agent System - OpenCode Environment
# Generated: Sun Nov 22 2026

## System Overview
- **Controller**: Linux, Intel i5 2nd Gen, 4GB RAM
- **API**: NVIDIA NIM Free Tier (~40 RPM)
- **Shell**: zsh
- **Python**: 3.13.12

## Pre-Installed CLI Tools (verified working)
| Tool | Path | Notes |
|------|------|-------|
| python3 | /usr/bin/python3 | 3.13.12 |
| pip | /usr/bin/pip | 26.1.1 |
| tailscale | /usr/sbin/tailscale | VPN/funnel |
| nmap | /usr/bin/nmap | Network scanner |
| binwalk | /usr/bin/binwalk | Firmware analysis |
| exiftool | /usr/bin/exiftool | Metadata extraction |
| r2 | /usr/bin/r2 | Radare2 framework |
| objdump | /usr/bin/objdump | Binary analysis |
| strings | /usr/bin/strings | String extraction |
| tshark | /usr/bin/tshark | Packet analysis |
| gdb | /usr/bin/gdb | Debugger |

## Installed Python Libraries
| Package | Version | Purpose |
|---------|---------|---------|
| pwntools | 4.15.0 | CTF exploitation framework |
| pycryptodome | 3.23.0 | Cryptography operations |
| z3-solver | 5.4.1.0 | SMT solver |
| requests | 2.32.5 | HTTP client |
| beautifulsoup4 | 4.14.3 | HTML parsing |
| scapy | 2.7.1 | Packet manipulation |

## OpenCode Skills (24 total)
| Skill | Category | Description |
|-------|----------|-------------|
| 0day-research | Research | Zero-day vulnerability research methodology |
| ad-attacks | Active Directory | AD attack paths & privilege escalation |
| anti-forensics | Anti-Forensics | Log evasion, timestomping, evidence destruction |
| api-audit | API Security | REST/GraphQL API security testing |
| c2-operations | C2 | Command & Control infrastructure |
| cloud-escape | Cloud | Container escape & K8s attack paths |
| cloud-pentest | Cloud | Cloud security assessment (AWS/Azure/GCP) |
| cyber-memory | Memory | Persistent cross-session memory loop |
| cybersec | General | General cybersecurity analysis |
| data-exfil | Exfiltration | Covert channels & data theft prevention |
| forensics-workflow | Forensics | DFIR workflow & evidence handling |
| hardening | Hardening | Security hardening techniques |
| lateral-movement | Pivoting | Cross-segment lateral movement |
| malware-analysis | Malware | Static/dynamic malware analysis |
| mcp-autopilot | MCP | Automatic MCP tool routing |
| opsec-evasion | OPSEC | Anti-detection techniques |
| pivoting-mastery | Pivoting | Multi-hop network penetration |
| self-healing | Self-Heal | Auto-diagnose & fix broken tools |
| threat-intel | OSINT | Threat intelligence collection |
| tool-mastery | Reference | Complete tool reference/usage |
| web3-security | Web3 | Smart contract auditing |
| wireless-pentest | Wireless | WPA/WPA2 attacks & rogue APs |
| zero-trust-bypass | Network | Zero-trust network bypass |

## MCP Servers (5 connected)
| Server | Purpose | Tools |
|--------|---------|-------|
| `security-tools` | 81 hacking tools | ffuf, nuclei, nmap, sqlmap, hydra, john, hashcat, etc. |
| `ghost-intel` | CVE/OSINT | cve_lookup, exploitdb_search, hash_identify, whois_lookup |
| `ghost-web` | Web analysis | Header analysis, tech detect, SSL, WAF, robots, sitemap |
| `ghost-network` | Network recon | Port scan, DNS, subdomains, traceroute, CIDR expand |
| `cve-search` | CVE database | CIRCL CVE queries |

## Zero-RAM Remote Worker System (IN PROGRESS)
- **Broker**: `.opencode/scripts/worker_broker.py` - ThreadingHTTPServer on 127.0.0.1:8765
- **Manager**: `.opencode/scripts/worker_manager.py` - start/generate-worker commands
- **Funnel**: Tailscale `funnel --bg 8765` → `https://*.ts.net`
- **Token**: 32-char random session token, `X-Worker-Tree` header auth

## Pending Installations (Phase 2-3)
- Tailscale Funnel configuration
- Worker broker/manager scripts
- NVIDIA NIM model routing configuration
- Cyber-memory persistent loop setup

## Security Gates Passed
- [x] No Docker installed (4GB RAM constraint)
- [x] No Java/JVM tools installed
- [x] No Playwright/Chromium installed locally
- [x] LSPs disabled/configured for low RAM
- [x] Only 1 background MCP server (security-tools)
- [x] Python libs installed without heavy dependencies

## Model Routing Priority (NVIDIA NIM)
1. `ctf-lead` (Orchestrator): `nvidia/nemotron-3-ultra-550b-a55b`
2. `ctf-triage` (Fast Recon): `nvidia/nemotron-3.5-lightning-30b-a3b`
3. `ctf-forensics` (Multimodal/Stego): `nvidia/nemotron-3.5-super-vl-120b-a12b`
4. `ctf-web`, `ctf-pwn-rev`, `ctf-crypto`, `ctf-worker-dispatch`: `minimaxai/minimax-m3.1-flash`
5. Fallbacks: `deepseek-ai/deepseek-v4.1-flash`, `nvidia/nemotron-3.5-super-120b-a12b`

## RAM Usage Notes
- Local background MCP servers: 1 max (security-tools)
- Python libs: all pure CLI, <200MB combined
- No Docker, no Ghidra, no Java, no Playwright locally
- Worker funnel offloads heavy tasks to remote machine