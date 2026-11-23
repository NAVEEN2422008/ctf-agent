#!/usr/bin/env python3
"""
GHOST-WEB MCP SERVER
Web application analysis: HTTP header inspection, technology fingerprinting,
SSL/TLS certificate analysis, WAF detection, and robots/sitemap parsing.
"""
import json
import os
import shutil
import socket
import ssl
import subprocess
import sys
import urllib.request
import urllib.parse
from typing import Any

# Ensure Go tools and local bins are in PATH
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + os.path.expanduser("~/go/bin") + os.pathsep + os.path.expanduser("~/.local/bin")


def http_get(url: str, timeout: int = 20) -> dict[str, Any]:
    """Fetch URL and return headers/status/body preview."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (GhostOperator)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode(errors="replace")
            return {
                "url": url,
                "status": resp.status,
                "headers": dict(resp.headers),
                "body_preview": body[:2000],
                "body_length": len(body),
            }
    except urllib.error.HTTPError as e:
        return {
            "url": url,
            "status": e.code,
            "headers": dict(e.headers),
            "error": str(e.reason),
        }
    except Exception as e:
        return {"url": url, "error": str(e)}


def analyze_headers(url: str) -> dict[str, Any]:
    """Analyze HTTP security headers."""
    result = http_get(url)
    if "error" in result and "headers" not in result:
        return result
    headers = result.get("headers", {})
    security_headers = {
        "Strict-Transport-Security": "HSTS",
        "Content-Security-Policy": "CSP",
        "X-Frame-Options": "Clickjacking protection",
        "X-Content-Type-Options": "MIME sniffing protection",
        "X-XSS-Protection": "XSS filter",
        "Referrer-Policy": "Referrer leakage control",
        "Permissions-Policy": "Browser feature control",
        "Access-Control-Allow-Origin": "CORS policy",
    }
    findings = []
    for header, purpose in security_headers.items():
        value = headers.get(header)
        findings.append({
            "header": header,
            "purpose": purpose,
            "present": value is not None,
            "value": value,
            "status": "GOOD" if value else "MISSING",
        })
    # Server info
    server = headers.get("Server", "Unknown")
    powered_by = headers.get("X-Powered-By", "Unknown")
    return {
        "url": url,
        "status": result.get("status"),
        "server": server,
        "x_powered_by": powered_by,
        "security_headers": findings,
        "missing_count": sum(1 for f in findings if not f["present"]),
    }


def detect_tech(url: str) -> dict[str, Any]:
    """Detect web technologies using whatweb."""
    binary = shutil.which("whatweb")
    if not binary:
        return {"error": "whatweb not found. Install: sudo apt install -y whatweb"}
    try:
        result = subprocess.run(
            [binary, "--no-errors", "--color=never", url],
            capture_output=True, text=True, timeout=60,
        )
        return {"url": url, "detection": result.stdout.strip()[:3000]}
    except Exception as e:
        return {"error": str(e)}


def ssl_analyze(host: str, port: int = 443) -> dict[str, Any]:
    """Analyze SSL/TLS certificate."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=15) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
        return {
            "host": host,
            "port": port,
            "tls_version": version,
            "cipher": cipher[0] if cipher else None,
            "subject": cert.get("subject"),
            "issuer": cert.get("issuer"),
            "not_before": cert.get("notBefore"),
            "not_after": cert.get("notAfter"),
            "serial": cert.get("serialNumber"),
            "san": cert.get("subjectAltName"),
        }
    except Exception as e:
        return {"host": host, "error": str(e)}


def waf_detect(url: str) -> dict[str, Any]:
    """Detect WAF using wafw00f."""
    binary = shutil.which("wafw00f")
    if not binary:
        return {"error": "wafw00f not found. Install: sudo apt install -y wafw00f"}
    try:
        result = subprocess.run(
            [binary, url, "-o", "-"],
            capture_output=True, text=True, timeout=60,
        )
        return {"url": url, "waf_detection": result.stdout.strip()[:2000]}
    except Exception as e:
        return {"error": str(e)}


def robots_parse(url: str) -> dict[str, Any]:
    """Fetch and parse robots.txt."""
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    result = http_get(robots_url)
    if "error" in result:
        return result
    body = result.get("body_preview", "")
    disallowed = [l.split(":", 1)[1].strip() for l in body.splitlines() if l.lower().startswith("disallow")]
    allowed = [l.split(":", 1)[1].strip() for l in body.splitlines() if l.lower().startswith("allow")]
    sitemaps = [l.split(":", 1)[1].strip() for l in body.splitlines() if l.lower().startswith("sitemap")]
    return {
        "url": robots_url,
        "status": result.get("status"),
        "disallowed_paths": disallowed,
        "allowed_paths": allowed,
        "sitemaps": sitemaps,
        "raw": body[:1500],
    }


def sitemap_parse(url: str) -> dict[str, Any]:
    """Fetch and parse sitemap.xml."""
    parsed = urllib.parse.urlparse(url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    result = http_get(sitemap_url)
    if "error" in result:
        return result
    body = result.get("body_preview", "")
    import re
    urls = re.findall(r"<loc>(.*?)</loc>", body)
    return {
        "url": sitemap_url,
        "status": result.get("status"),
        "url_count": len(urls),
        "urls": urls[:50],
    }


TOOLS = {
    "analyze_headers": (analyze_headers, {"url": {"type": "string", "description": "Target URL"}}),
    "detect_tech": (detect_tech, {"url": {"type": "string"}}),
    "ssl_analyze": (ssl_analyze, {"host": {"type": "string"}, "port": {"type": "integer", "default": 443}}),
    "waf_detect": (waf_detect, {"url": {"type": "string"}}),
    "robots_parse": (robots_parse, {"url": {"type": "string"}}),
    "sitemap_parse": (sitemap_parse, {"url": {"type": "string"}}),
}


def handle_initialize() -> dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "ghost-web", "version": "1.0.0"},
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