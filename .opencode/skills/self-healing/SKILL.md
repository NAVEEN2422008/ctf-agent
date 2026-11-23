---
name: self-healing
description: Self-healing protocol for detecting, diagnosing, and fixing broken tools, dependencies, and configurations automatically.
---

# SELF-HEALING SKILL

When ANY tool fails, follow this protocol:

## 1. DIAGNOSE
```bash
# Check if tool exists
which <tool>
# Check version
<tool> --version
# Check PATH
echo $PATH
# Check error output
<tool> 2>&1 | tail -20
```

## 2. REMEDIATE
```bash
# Go tools (ProjectDiscovery, ffuf, etc.)
go install -v github.com/projectdiscovery/<tool>/cmd/<tool>@latest
go install -v github.com/ffuf/ffuf/v2@latest

# Python tools
pip3 install --break-system-packages <tool>

# Ruby gems
gem install <tool>

# System tools
sudo apt install -y <tool>

# Rust tools
cargo install <tool>
```

## 3. VERIFY
```bash
# Check binary exists
which <tool>
# Check version works
<tool> --version
# Test basic functionality
<tool> -h 2>&1 | head -5
```

## 4. LOG
```bash
# Record the self-heal event
echo "[$(date)] Self-healed: <tool> - <action>" >> ~/.config/opencode/self-heal.log
```

## 5. CONTINUE
Resume the original task with the fixed tool.

## COMMON FIXES

### Go tools not found
```bash
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
# Add to ~/.zshrc permanently
echo 'export GOPATH=$HOME/go' >> ~/.zshrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc
```

### Python tools not found
```bash
# Kali uses PEP 668, need --break-system-packages
pip3 install --break-system-packages <tool>
# Or check ~/.local/bin
ls ~/.local/bin/
export PATH=$PATH:$HOME/.local/bin
```

### Ruby gems not found
```bash
# Gems install to ~/.local/share/gem/ruby/X.Y.0/bin
export PATH=$PATH:$HOME/.local/share/gem/ruby/3.3.0/bin
```

### Nuclei templates missing
```bash
nuclei -update-templates
# Or manually
git clone https://github.com/projectdiscovery/nuclei-templates.git ~/.local/nuclei-templates/
```

### Wordlists missing
```bash
# SecLists
git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists/
# RockYou
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

### MCP server not working
```bash
# Check if npx can find it
npx -y <package> --help
# Check node version
node --version
# Check npm registry
npm view <package>
```

### Permission denied
```bash
chmod +x <file>
# Or run with sudo if system-level
```

## VERIFICATION MATRIX

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| Tool exists | `which <tool>` | Exit code 0 |
| Tool works | `<tool> --version` | Version output |
| PATH correct | `echo $PATH` | Contains ~/go/bin, ~/.local/bin |
| Templates | `ls ~/.local/nuclei-templates/` | Directory exists |
| Wordlists | `ls /usr/share/wordlists/` | Files exist |
| MCP works | `npx -y <pkg> --help` | Help output |

## OUTPUT FORMAT
```
[SELF-HEAL] Tool name
[ISSUE] What broke
[FIX] What was done
[VERIFY] Proof it works
[STATUS] Complete
```