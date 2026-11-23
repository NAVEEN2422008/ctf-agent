#!/usr/bin/env python3
"""
GHOST-INTEL MCP SERVER
Threat intelligence: CVE lookup (NVD API), ExploitDB search (local searchsploit),
OSINT enrichment, and hash identification.
"""
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.parse
from typing import Any

# Ensure Go tools and local bins are in PATH
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.expanduser("~/go/bin") + os.pathsep + os.path.expanduser("~/.local/bin")

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CIRCL_API = "https://cve.circl.lu/api/"


def http_get(url: str, timeout: int = 20) -> dict[str, Any]:
    """Safe HTTP GET returning JSON."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ghost-operator/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


# ─── CVE Lookup ─────────────────────────────────────────────────────────────
def cve_lookup(cve_id: str) -> dict[str, Any]:
    """Look up a specific CVE by ID."""
    if not cve_id.upper().startswith("CVE-"):
        return {"error": f"Invalid CVE ID: {cve_id}. Format: CVE-YYYY-NNNNN"}
    data = http_get(f"{CIRCL_API}cve/{cve_id.upper()}")
    if "error" in data:
        return data
    # Handle CVE 5.0 format (cveMetadata + containers)
    if "cveMetadata" in data:
        meta = data.get("cveMetadata", {})
        containers = data.get("containers", {}).get("cna", {})
        descriptions = containers.get("descriptions", [])
        metrics = containers.get("metrics", [])
        cvss = None
        for m in metrics:
            if "cvssV3_1" in m:
                cvss = m["cvssV3_1"].get("baseScore")
                break
            if "cvssV3_0" in m:
                cvss = m["cvssV3_0"].get("baseScore")
                break
        refs = [r.get("url") for r in containers.get("references", [])[:5]]
        return {
            "id": meta.get("cveId"),
            "summary": descriptions[0].get("value", "") if descriptions else "",
            "cvss": cvss,
            "published": meta.get("datePublished"),
            "modified": meta.get("dateUpdated"),
            "references": refs,
            "state": meta.get("state"),
        }
    # Legacy format fallback
    return {
        "id": data.get("id"),
        "summary": data.get("summary"),
        "cvss": data.get("cvss"),
        "cvss3": data.get("cvss3"),
        "published": data.get("Published"),
        "modified": data.get("Modified"),
        "references": data.get("references", [])[:5],
        "capec": data.get("capec", []),
        "cwe": data.get("cwe"),
    }


def cve_search(query: str, limit: int = 10) -> dict[str, Any]:
    """Search CVEs by keyword using NVD API."""
    params = urllib.parse.urlencode({"keywordSearch": query, "resultsPerPage": limit})
    data = http_get(f"{NVD_API}?{params}")
    if "error" in data:
        return data
    results = []
    for vuln in data.get("vulnerabilities", [])[:limit]:
        c = vuln.get("cve", {})
        results.append({
            "id": c.get("id"),
            "published": c.get("published"),
            "description": c.get("descriptions", [{}])[0].get("value", "")[:200],
            "severity": c.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "N/A"),
            "score": c.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", "N/A"),
        })
    return {"query": query, "count": len(results), "results": results}


def cve_by_vendor_product(vendor: str, product: str, limit: int = 10) -> dict[str, Any]:
    """Search CVEs for a specific vendor/product via CIRCL."""
    data = http_get(f"{CIRCL_API}search/{vendor}/{product}")
    if "error" in data:
        return data
    if not isinstance(data, list):
        return {"error": "Unexpected response"}
    results = []
    for c in data[:limit]:
        results.append({
            "id": c.get("id"),
            "summary": c.get("summary", "")[:150],
            "cvss": c.get("cvss"),
        })
    return {"vendor": vendor, "product": product, "count": len(results), "results": results}


def latest_cves(limit: int = 10) -> dict[str, Any]:
    """Get the latest CVEs."""
    data = http_get(f"{CIRCL_API}last")
    if "error" in data:
        return data
    if not isinstance(data, list):
        return {"error": "Unexpected response"}
    results = []
    for c in data[:limit]:
        results.append({
            "id": c.get("id"),
            "summary": c.get("summary", "")[:150],
            "cvss": c.get("cvss"),
            "published": c.get("Published"),
        })
    return {"count": len(results), "results": results}


# ─── ExploitDB Search ───────────────────────────────────────────────────────
def exploitdb_search(query: str, limit: int = 10) -> dict[str, Any]:
    """Search local ExploitDB via searchsploit."""
    binary = shutil.which("searchsploit")
    if not binary:
        return {"error": "searchsploit not found. Install: sudo apt install -y exploitdb"}
    try:
        result = subprocess.run(
            [binary, query, "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return {"error": result.stderr[:500]}
        data = json.loads(result.stdout)
        exploits = data.get("EXPLOITS", [])[:limit]
        return {"query": query, "count": len(exploits), "results": exploits}
    except Exception as e:
        return {"error": str(e)}


# ─── Hash Identification ────────────────────────────────────────────────────
def hash_identify(hash_value: str) -> dict[str, Any]:
    """Identify hash type using hashid."""
    binary = shutil.which("hashid")
    if not binary:
        return {"error": "hashid not found. Install: sudo apt install -y hashid"}
    try:
        result = subprocess.run(
            [binary, hash_value],
            capture_output=True, text=True, timeout=15,
        )
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return {"hash": hash_value[:32] + "...", "possible_types": lines[2:] if len(lines) > 2 else lines}
    except Exception as e:
        return {"error": str(e)}


# ─── OSINT Enrichment ───────────────────────────────────────────────────────
def whois_lookup(domain: str) -> dict[str, Any]:
    """WHOIS lookup for a domain."""
    binary = shutil.which("whois")
    if not binary:
        return {"error": "whois not found"}
    try:
        result = subprocess.run([binary, domain], capture_output=True, text=True, timeout=20)
        lines = [l for l in result.stdout.splitlines() if l.strip()][:40]
        return {"domain": domain, "whois": lines}
    except Exception as e:
        return {"error": str(e)}


def ip_info(ip: str) -> dict[str, Any]:
    """Get IP geolocation and ASN info."""
    data = http_get(f"http://ip-api.com/json/{ip}")
    if "error" in data:
        return data
    return {
        "ip": data.get("query"),
        "country": data.get("country"),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "as": data.get("as"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "timezone": data.get("timezone"),
    }


def dns_lookup(domain: str) -> dict[str, Any]:
    """DNS resolution for a domain."""
    binary = shutil.which("dig")
    if not binary:
        return {"error": "dig not found"}
    try:
        result = subprocess.run([binary, "+short", domain], capture_output=True, text=True, timeout=15)
        ips = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return {"domain": domain, "resolved_ips": ips}
    except Exception as e:
        return {"error": str(e)}


# ─── MCP handlers ───────────────────────────────────────────────────────────
TOOLS = {
    "cve_lookup": (cve_lookup, {"cve_id": {"type": "string", "description": "CVE ID e.g. CVE-2024-1234"}}),
    "cve_search": (cve_search, {"query": {"type": "string", "description": "Keyword to search"}, "limit": {"type": "integer", "description": "Max results", "default": 10}}),
    "cve_by_vendor_product": (cve_by_vendor_product, {"vendor": {"type": "string"}, "product": {"type": "string"}, "limit": {"type": "integer", "default": 10}}),
    "latest_cves": (latest_cves, {"limit": {"type": "integer", "default": 10}}),
    "exploitdb_search": (exploitdb_search, {"query": {"type": "string", "description": "Search term"}, "limit": {"type": "integer", "default": 10}}),
    "hash_identify": (hash_identify, {"hash_value": {"type": "string", "description": "Hash to identify"}}),
    "whois_lookup": (whois_lookup, {"domain": {"type": "string"}}),
    "ip_info": (ip_info, {"ip": {"type": "string"}}),
    "dns_lookup": (dns_lookup, {"domain": {"type": "string"}}),
}


def handle_initialize() -> dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "ghost-intel", "version": "1.0.0"},
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