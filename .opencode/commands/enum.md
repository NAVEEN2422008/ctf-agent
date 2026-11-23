---
description: Service enumeration: SMB, HTTP, DNS, SNMP, LDAP
agent: recon
---

Execute service enumeration against: $ARGUMENTS

## SMB Enumeration
```bash
# Shares
netexec smb $ARGUMENTS --shares -u '' -p ''
enum4linux -a $ARGUMENTS
smbclient -L //$ARGUMENTS/ -N

# Null session
netexec smb $ARGUMENTS -u guest -p '' --shares
```

## HTTP Enumeration
```bash
# Technology detection
httpx -u $ARGUMENTS -title -tech-detect -status-code

# Nikto
nikto -h $ARGUMENTS -o nikto_results.txt

# Whatweb
whatweb $ARGUMENTS
```

## DNS Enumeration
```bash
# Zone transfer attempt
dig axfr $ARGUMENTS @$(dig NS $ARGUMENTS +short)

# Record enumeration
dig any $ARGUMENTS
dnsrecon -d $ARGUMENTS -a
```

## SNMP Enumeration
```bash
# Community strings
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt $ARGUMENTS

# Walk
snmpwalk -v2c -c public $ARGUMENTS
snmp-check $ARGUMENTS
```

## LDAP Enumeration
```bash
# Anonymous bind
ldapsearch -x -H ldap://$ARGUMENTS -b ""

# User enumeration
ldapsearch -x -H ldap://$ARGUMENTS -b "DC=domain,DC=com" "(objectClass=user)" sAMAccountName
```

## RDP Enumeration
```bash
nmap -p 3389 --script rdp-enum-encryption $ARGUMENTS
rdp-sec-check $ARGUMENTS
```
