---
name: forensics-workflow
description: Digital forensics and incident response workflow for evidence collection, analysis, and reporting.
---

# Forensics Workflow Skill

## When to Use
Use this skill when performing digital forensics investigations, incident response, or evidence collection during authorized engagements.

## Evidence Collection

### Disk Imaging
```bash
# Create forensic image
dd if=/dev/sda of=/evidence/disk_image.img bs=4M status=progress

# Verify integrity
sha256sum /evidence/disk_image.img > /evidence/disk_image.img.sha256

# Mount read-only
mount -o loop,ro /evidence/disk_image.img /mnt/evidence
```

### Memory Collection
```bash
# Linux
dd if=/dev/mem of=/evidence/memory.dump

# Windows (using WinPmem)
winpmem_mini_x64.exe /evidence/memory.dump
```

### Network Capture
```bash
# Capture traffic
tcpdump -i any -w /evidence/capture.pcap -c 100000

# Filter by host
tcpdump -i any host <target> -w /evidence/target_traffic.pcap
```

## Analysis

### Volatility (Memory)
```bash
# Image info
volatility -f /evidence/memory.dump imageinfo

# Process list
volatility -f /evidence/memory.dump --profile=<profile> pslist

# Network connections
volatility -f /evidence/memory.dump --profile=<profile> netscan

# Command history
volatility -f /evidence/memory.dump --profile=<profile> cmdline

# Extract files
volatility -f /evidence/memory.dump --profile=<profile> filescan
volatility -f /evidence/memory.dump --profile=<profile> dumpfiles -D /evidence/extracted
```

### Sleuth Kit (Disk)
```bash
# List files
fls -r /mnt/evidence

# Recover deleted files
icat -r /mnt/evidence <inode>

# Timeline
fls -r -m "/" /mnt/evidence > /evidence/bodyfile.txt
mactime -b /evidence/bodyfile.txt > /evidence/timeline.csv

# Search strings
grep -r "password" /mnt/evidence/
```

### Wireshark (Network)
```bash
# HTTP requests
tshark -r /evidence/capture.pcap -Y "http.request" -T fields -e ip.src -e http.host -e http.request.uri

# DNS queries
tshark -r /evidence/capture.pcap -Y "dns" -T fields -e dns.qry.name

# Credentials
tshark -r /evidence/capture.pcap -Y "http.authorization" -T fields -e http.authorization

# TLS analysis
tshark -r /evidence/capture.pcap -Y "tls.handshake" -T fields -e tls.handshake.extensions_server_name
```

## Output Format
```
[EVIDENCE] Description
[SOURCE] Memory/Disk/Network/Log
[ANALYSIS] Findings
[INDICATOR] IOC/TTP
[TIMELINE] Event sequence
[IMPACT] Assessment
```
