#!/usr/bin/env python3
"""
GHOST-NETWORK MCP SERVER
Network analysis: port scanning, service detection, DNS enumeration,
subdomain discovery, and network range analysis.
"""
import json
import shutil
import subprocess
import sys
import socket
from typing import Any


def run_cmd(cmd: list[str], timeout: int = 60) -> dict[str, Any]:
    """Run a command and return output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "command": " ".join(cmd),
            "exit_code": result.returncode,
            "stdout": result.stdout[-6000:],
            "stderr": result.stderr[-2000:],
        }
    except subprocess.TimeoutExpired:
        return {"command": " ".join(cmd), "error": f"Timed out after {timeout}s"}
    except Exception as e:
        return {"command": " ".join(cmd), "error": str(e)}


def quick_port_scan(host: str, ports: str = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443,9000,9200") -> dict[str, Any]:
    """Quick TCP port scan using Python sockets."""
    open_ports = []
    for port_str in ports.split(","):
        port = int(port_str.strip())
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    return {"host": host, "open_ports": open_ports, "scanned": len(ports.split(","))}


def nmap_scan(target: str, args: str = "-sC -sV -T4") -> dict[str, Any]:
    """Run nmap scan."""
    binary = shutil.which("nmap")
    if not binary:
        return {"error": "nmap not found. Install: sudo apt install -y nmap"}
    cmd = [binary] + args.split() + [target]
    return run_cmd(cmd, timeout=300)


def naabu_scan(target: str, ports: str = "top-1000") -> dict[str, Any]:
    """Run naabu port scan."""
    binary = shutil.which("naabu")
    if not binary:
        return {"error": "naabu not found. Install: go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"}
    cmd = [binary, "-host", target, "-p", ports, "-silent"]
    return run_cmd(cmd, timeout=180)


def dns_enum(domain: str) -> dict[str, Any]:
    """DNS enumeration with dnsrecon."""
    binary = shutil.which("dnsrecon")
    if not binary:
        return {"error": "dnsrecon not found. Install: sudo apt install -y dnsrecon"}
    cmd = [binary, "-d", domain, "-t", "std"]
    return run_cmd(cmd, timeout=120)


def subdomain_enum(domain: str) -> dict[str, Any]:
    """Subdomain enumeration with subfinder."""
    binary = shutil.which("subfinder")
    if not binary:
        return {"error": "subfinder not found. Install: go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"}
    cmd = [binary, "-d", domain, "-silent"]
    return run_cmd(cmd, timeout=180)


def reverse_dns(ip: str) -> dict[str, Any]:
    """Reverse DNS lookup."""
    try:
        hostname = socket.gethostbyaddr(ip)
        return {"ip": ip, "hostname": hostname[0], "aliases": hostname[1]}
    except Exception as e:
        return {"ip": ip, "error": str(e)}


def traceroute(target: str) -> dict[str, Any]:
    """Traceroute to target."""
    binary = shutil.which("traceroute")
    if not binary:
        return {"error": "traceroute not found"}
    return run_cmd([binary, "-n", "-m", "20", target], timeout=60)


def cidr_expand(cidr: str) -> dict[str, Any]:
    """Expand CIDR range using mapcidr."""
    binary = shutil.which("mapcidr")
    if not binary:
        return {"error": "mapcidr not found. Install: go install -v github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest"}
    cmd = [binary, "-cidr", cidr, "-silent"]
    result = run_cmd(cmd, timeout=30)
    if "stdout" in result:
        ips = [l.strip() for l in result["stdout"].splitlines() if l.strip()]
        result["ip_count"] = len(ips)
        result["ips"] = ips[:100]
    return result


TOOLS = {
    "quick_port_scan": (quick_port_scan, {"host": {"type": "string"}, "ports": {"type": "string", "description": "Comma-separated ports", "default": "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443,9000,9200"}}),
    "nmap_scan": (nmap_scan, {"target": {"type": "string"}, "args": {"type": "string", "default": "-sC -sV -T4"}}),
    "naabu_scan": (naabu_scan, {"target": {"type": "string"}, "ports": {"type": "string", "default": "top-1000"}}),
    "dns_enum": (dns_enum, {"domain": {"type": "string"}}),
    "subdomain_enum": (subdomain_enum, {"domain": {"type": "string"}}),
    "reverse_dns": (reverse_dns, {"ip": {"type": "string"}}),
    "traceroute": (traceroute, {"target": {"type": "string"}}),
    "cidr_expand": (cidr_expand, {"cidr": {"type": "string"}}),
}


def handle_initialize() -> dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "ghost-network", "version": "1.0.0"},
    }


def handle_list_tools() -> dict[str, Any]:
    tools = []
    for name, (_, schema) in TOOLS.items():
        tools.append({
            "name": name,
            "description": name.replace("_", " ").title(),
            "inputSchema": {"type": "object", "properties": schema},
        })
    return {"tools": tools}


def handle_call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name not in TOOLS:
        return {"content": [{"type": "text", "text": json.dumps({"error": f"Unknown tool: {name}"})}]}
    func, _ = TOOLS[name]
    try:
        result = func(**arguments)
    except TypeError as e:
        result = {"error": f"Invalid arguments: {e}"}
    except Exception as e:
        result = {"error": str(e)}
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]}


def main() -> None:
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