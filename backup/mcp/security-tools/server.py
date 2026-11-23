#!/usr/bin/env python3
"""
GHOST SECURITY TOOLS MCP SERVER
Wraps all installed hacking tools into MCP tools for the ghost-operator agent.
Self-healing: auto-detects missing tools and reports install commands.
"""
import json
import os
import shutil
import subprocess
import sys
import shlex
from typing import Any

# Ensure Go tools and local bins are in PATH
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.expanduser("~/go/bin") + os.pathsep + os.path.expanduser("~/.local/bin")

# ─── Tool registry: name → (binary, description) ───────────────────────────
TOOLS = {
    # Reconnaissance
    "subfinder": ("subfinder", "Subdomain enumeration"),
    "amass": ("amass", "Attack surface enumeration"),
    "assetfinder": ("assetfinder", "Subdomain discovery"),
    "httpx": ("httpx", "HTTP probing and tech detection"),
    "naabu": ("naabu", "Fast port scanner"),
    "nmap": ("nmap", "Network mapper"),
    "masscan": ("masscan", "Mass port scanner"),
    "dnsx": ("dnsx", "DNS resolver and probing"),
    "katana": ("katana", "Web crawler"),
    "gau": ("gau", "Get all URLs from wayback"),
    "waybackurls": ("waybackurls", "Wayback machine URLs"),
    "hakrawler": ("hakrawler", "Web crawler"),
    "hakrevdns": ("hakrevdns", "Reverse DNS lookup"),
    "gowitness": ("gowitness", "Web screenshot tool"),
    "uncover": ("uncover", "Search engine API discovery"),
    "mapcidr": ("mapcidr", "CIDR expansion"),
    "asnmap": ("asnmap", "ASN mapping"),
    "tlsx": ("tlsx", "TLS/SSL certificate grabber"),
    "urlfinder": ("urlfinder", "URL discovery"),
    "alterx": ("alterx", "Subdomain permutation"),
    "shuffledns": ("shuffledns", "Mass DNS resolver"),
    "cdncheck": ("cdncheck", "CDN detection"),
    "dnsrecon": ("dnsrecon", "DNS enumeration"),
    "fierce": ("fierce", "DNS reconnaissance"),
    "theHarvester": ("theHarvester", "OSINT email/subdomain harvesting"),
    "sherlock": ("sherlock", "Username enumeration across social networks"),
    "dnsgen": ("dnsgen", "DNS wordlist generator"),
    "puredns": ("puredns", "Fast DNS resolver"),

    # Web application
    "ffuf": ("ffuf", "Web fuzzer"),
    "gobuster": ("gobuster", "Directory/file/DNS busting"),
    "feroxbuster": ("feroxbuster", "Content discovery"),
    "dirb": ("dirb", "Directory brute forcer"),
    "nuclei": ("nuclei", "Vulnerability scanner"),
    "nikto": ("nikto", "Web server scanner"),
    "sqlmap": ("sqlmap", "SQL injection tool"),
    "dalfox": ("dalfox", "XSS scanner"),
    "wpscan": ("wpscan", "WordPress scanner"),
    "whatweb": ("whatweb", "Web technology fingerprinting"),
    "wafw00f": ("wafw00f", "WAF detection"),
    "gf": ("gf", "Grep patterns for web vulns"),
    "qsreplace": ("qsreplace", "Query string replacement"),
    "httprobe": ("httprobe", "HTTP probing"),

    # Network / AD
    "netexec": ("netexec", "Network exploitation (SMB/LDAP/WinRM)"),
    "responder": ("responder", "LLMNR/NBT-NS poisoning"),
    "mitm6": ("mitm6", "IPv6 MITM for AD"),
    "enum4linux": ("enum4linux", "SMB enumeration"),
    "smbclient": ("smbclient", "SMB client"),
    "hydra": ("hydra", "Password brute forcer"),
    "john": ("john", "John the Ripper password cracker"),
    "hashcat": ("hashcat", "GPU password cracker"),
    "kerbrute": ("kerbrute", "Kerberos brute force"),
    "ldapdomaindump": ("ldapdomaindump", "LDAP domain dump"),
    "pypykatz": ("pypykatz", "Mimikatz in Python"),
    "ldeep": ("ldeep", "LDAP enumeration"),
    "impacket-secretsdump": ("impacket-secretsdump", "Dump secrets from AD"),
    "chisel": ("chisel", "TCP tunnel"),
    "ligolo-agent": ("ligolo-agent", "Ligolo agent"),
    "ligolo-proxy": ("ligolo-proxy", "Ligolo proxy"),
    "proxify": ("proxify", "HTTP proxy"),
    "arpscan": ("arp-scan", "ARP scanner"),

    # Exploitation
    "msfconsole": ("msfconsole", "Metasploit framework"),
    "searchsploit": ("searchsploit", "ExploitDB search"),
    "sqlmap": ("sqlmap", "SQL injection"),
    "dalfox": ("dalfox", "XSS scanner"),
    "gdb": ("gdb", "GNU debugger"),
    "radare2": ("r2", "Reverse engineering framework"),
    "ROPgadget": ("ROPgadget", "ROP gadget finder"),
    "one_gadget": ("one_gadget", "One gadget RCE finder"),
    "strace": ("strace", "System call tracer"),
    "objdump": ("objdump", "Binary analysis"),
    "readelf": ("readelf", "ELF analysis"),
    "strings": ("strings", "Extract strings from binaries"),
    "exiftool": ("exiftool", "Metadata extraction"),
    "binwalk": ("binwalk", "Firmware analysis"),

    # Forensics / Blue team
    "tshark": ("tshark", "Network protocol analyzer"),
    "tcpdump": ("tcpdump", "Packet capture"),
    "volatility3": ("vol", "Memory forensics"),
    "yara": ("yara", "Malware pattern matching"),
    "gitleaks": ("gitleaks", "Secret scanning"),
    "notify": ("notify", "Notification tool"),
    "interactsh-client": ("interactsh-client", "OOB interaction client"),
}

INSTALL_HINTS = {
    "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    "amass": "go install -v github.com/owasp-amass/amass/v4/...@master",
    "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
    "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
    "ffuf": "go install -v github.com/ffuf/ffuf/v2@latest",
    "nmap": "sudo apt install -y nmap",
    "sqlmap": "sudo apt install -y sqlmap",
    "netexec": "pip3 install --break-system-packages netexec",
    "msfconsole": "sudo apt install -y metasploit-framework",
    "volatility3": "pip3 install --break-system-packages volatility3",
    "yara": "sudo apt install -y yara",
    "one_gadget": "gem install one_gadget",
    "sherlock": "pip3 install --break-system-packages sherlock",
    "dnsgen": "pip3 install --break-system-packages dnsgen",
    "puredns": "go install -v github.com/d3mondev/puredns/v2@latest",
}


def tool_status() -> dict[str, Any]:
    """Check which tools are installed and which are missing."""
    installed, missing = [], []
    for name, (binary, desc) in TOOLS.items():
        if shutil.which(binary):
            installed.append(name)
        else:
            missing.append(name)
    return {"installed": sorted(installed), "missing": sorted(missing), "total": len(TOOLS)}


def run_tool(name: str, args: list[str], timeout: int = 180) -> dict[str, Any]:
    """Run a tool by name with args."""
    if name not in TOOLS:
        return {"error": f"Unknown tool: {name}. Available: {', '.join(sorted(TOOLS))}"}
    binary, desc = TOOLS[name]
    path = shutil.which(binary)
    if not path:
        hint = INSTALL_HINTS.get(name, f"Install '{binary}' manually")
        return {"error": f"Tool '{name}' ({binary}) not found. Install with: {hint}"}
    try:
        result = subprocess.run(
            [path] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "tool": name,
            "command": f"{binary} {' '.join(shlex.quote(a) for a in args)}",
            "exit_code": result.returncode,
            "stdout": result.stdout[-8000:],
            "stderr": result.stderr[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"tool": name, "error": f"Timed out after {timeout}s"}
    except Exception as e:
        return {"tool": name, "error": str(e)}


def self_heal() -> dict[str, Any]:
    """Report missing tools and their install commands."""
    status = tool_status()
    fixes = []
    for name in status["missing"]:
        hint = INSTALL_HINTS.get(name, f"# {name}: no auto-install hint")
        fixes.append({"tool": name, "install": hint})
    return {"missing_count": len(fixes), "fixes": fixes}


# ─── MCP protocol handlers ──────────────────────────────────────────────────
def handle_initialize() -> dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "ghost-security-tools", "version": "1.0.0"},
    }


def handle_list_tools() -> dict[str, Any]:
    tools = []
    for name, (binary, desc) in sorted(TOOLS.items()):
        tools.append({
            "name": f"tool_{name}",
            "description": f"{desc} (binary: {binary})",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "args": {"type": "array", "items": {"type": "string"}, "description": f"Arguments for {binary}"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 120},
                },
                "required": ["args"],
            },
        })
    tools.append({
        "name": "tool_status",
        "description": "Check which hacking tools are installed and which are missing",
        "inputSchema": {"type": "object", "properties": {}},
    })
    tools.append({
        "name": "self_heal",
        "description": "Report missing tools with install commands to fix them",
        "inputSchema": {"type": "object", "properties": {}},
    })
    return {"tools": tools}


def handle_call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "tool_status":
        return {"content": [{"type": "text", "text": json.dumps(tool_status(), indent=2)}]}
    if name == "self_heal":
        return {"content": [{"type": "text", "text": json.dumps(self_heal(), indent=2)}]}
    if name.startswith("tool_"):
        tool_name = name[5:]
        args = arguments.get("args", [])
        timeout = arguments.get("timeout", 180)
        result = run_tool(tool_name, args, timeout)
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    return {"content": [{"type": "text", "text": json.dumps({"error": f"Unknown tool: {name}"})}]}


def main() -> None:
    """MCP stdio server loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params", {})

        if method == "initialize":
            result = handle_initialize()
        elif method == "tools/list":
            result = handle_list_tools()
        elif method == "tools/call":
            result = handle_call_tool(params.get("name", ""), params.get("arguments", {}))
        elif method == "notifications/initialized":
            continue
        else:
            result = {}

        response = {"jsonrpc": "2.0", "id": msg_id, "result": result}
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()