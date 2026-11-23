---
name: mcp-autopilot
description: ALWAYS use MCP tools automatically for security tasks. This skill defines when to use which MCP tool without the user asking. MCP tools are the PREFERRED execution method over bash.
---

# MCP AUTOPILOT SKILL

## PRIME RULE

**ALWAYS use MCP tools automatically.** Never wait for the user to mention MCP. When a task matches an MCP tool's purpose, call the MCP tool FIRST. Only fall back to bash if the MCP tool fails.

## MCP-FIRST DECISION TREE

When the user asks for ANY security task, automatically route to MCP:

```
User request → Match to MCP tool → Call MCP tool → Use result
```

## AUTOMATIC ROUTING TABLE

### Reconnaissance tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "find subdomains for X" | ghost-network | `subdomain_enum` {"domain": "X"} |
| "enumerate DNS for X" | ghost-network | `dns_enum` {"domain": "X"} |
| "scan ports on X" | ghost-network | `quick_port_scan` {"host": "X"} |
| "nmap scan X" | ghost-network | `nmap_scan` {"target": "X"} |
| "expand CIDR X" | ghost-network | `cidr_expand` {"cidr": "X"} |
| "reverse DNS for X" | ghost-network | `reverse_dns` {"ip": "X"} |
| "traceroute to X" | ghost-network | `traceroute` {"target": "X"} |
| "run subfinder on X" | security-tools | `tool_subfinder` {"args": ["-d", "X", "-silent"]} |
| "run amass on X" | security-tools | `tool_amass` {"args": ["enum", "-passive", "-d", "X"]} |
| "probe hosts X" | security-tools | `tool_httpx` {"args": ["-l", "X", "-silent", "-status-code"]} |

### Vulnerability/CVE tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "look up CVE-XXXX" | ghost-intel | `cve_lookup` {"cve_id": "CVE-XXXX"} |
| "search CVEs for X" | ghost-intel | `cve_search` {"query": "X"} |
| "CVEs for vendor X product Y" | ghost-intel | `cve_by_vendor_product` {"vendor": "X", "product": "Y"} |
| "latest CVEs" | ghost-intel | `latest_cves` {} |
| "find exploits for X" | ghost-intel | `exploitdb_search` {"query": "X"} |
| "what type of hash is X" | ghost-intel | `hash_identify` {"hash_value": "X"} |
| "scan X for vulns" | security-tools | `tool_nuclei` {"args": ["-u", "X", "-severity", "critical,high"]} |
| "sqlmap X" | security-tools | `tool_sqlmap` {"args": ["-u", "X", "--batch"]} |
| "nikto X" | security-tools | `tool_nikto` {"args": ["-h", "X"]} |

### Web analysis tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "check headers on X" | ghost-web | `analyze_headers` {"url": "X"} |
| "what tech does X use" | ghost-web | `detect_tech` {"url": "X"} |
| "check SSL cert on X" | ghost-web | `ssl_analyze` {"host": "X"} |
| "is there a WAF on X" | ghost-web | `waf_detect` {"url": "X"} |
| "check robots.txt on X" | ghost-web | `robots_parse` {"url": "X"} |
| "check sitemap on X" | ghost-web | `sitemap_parse` {"url": "X"} |
| "fuzz X" | security-tools | `tool_ffuf` {"args": ["-u", "X/FUZZ", "-w", "wordlist"]} |
| "wordpress scan X" | security-tools | `tool_wpscan` {"args": ["--url", "X"]} |
| "xss scan X" | security-tools | `tool_dalfox` {"args": ["url", "X"]} |

### OSINT tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "whois for X" | ghost-intel | `whois_lookup` {"domain": "X"} |
| "IP info for X" | ghost-intel | `ip_info` {"ip": "X"} |
| "DNS lookup X" | ghost-intel | `dns_lookup` {"domain": "X"} |
| "osint on X" | security-tools | `tool_theHarvester` {"args": ["-d", "X", "-b", "all"]} |
| "find username X" | security-tools | `tool_sherlock` {"args": ["X"]} |

### Network/AD tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "enum4linux X" | security-tools | `tool_enum4linux` {"args": ["-a", "X"]} |
| "netexec smb X" | security-tools | `tool_netexec` {"args": ["smb", "X"]} |
| "crack hash X" | security-tools | `tool_hashcat` {"args": ["-m", "1000", "X", "wordlist"]} |
| "hydra X" | security-tools | `tool_hydra` {"args": ["-l", "admin", "-P", "wordlist", "X", "ssh"]} |

### Browser automation tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "open X in browser" | playwright | `browser_navigate` {"url": "X"} |
| "screenshot X" | playwright | `browser_screenshot` {} |
| "click element on X" | playwright | `browser_click` {"selector": "X"} |
| "fill form on X" | playwright | `browser_fill` {"selector": "X", "value": "Y"} |

### Reasoning/planning tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "think through X step by step" | sequential-thinking | `sequentialthinking` {"thought": "X"} |
| "plan the attack on X" | sequential-thinking | `sequentialthinking` {"thought": "plan for X"} |

### Memory tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "remember X" | memory | `create_entities` {"entities": [{"name": "X", "entityType": "fact", "observations": ["X"]}]} |
| "what do you know about X" | memory | `search_nodes` {"query": "X"} |
| "recall X" | memory | `read_graph` {} |

### File tasks → USE MCP AUTOMATICALLY
| User says | MCP server | Tool to call |
|-----------|-----------|--------------|
| "read file X" | filesystem | `read_text_file` {"path": "X"} |
| "write file X" | filesystem | `write_file` {"path": "X", "content": "Y"} |
| "list directory X" | filesystem | `list_directory` {"path": "X"} |

## EXECUTION RULES

1. **MCP FIRST**: When a task matches the routing table, call the MCP tool immediately. Do NOT ask the user.
2. **NO MENTION NEEDED**: The user does not need to say "use MCP" or "via MCP". Just use it.
3. **FALLBACK**: If the MCP tool returns an error (tool not found, timeout), THEN use bash as fallback.
4. **COMBINE**: Chain multiple MCP tools for complex tasks. E.g., recon = subdomain_enum → httpx → nuclei.
5. **REPORT**: Tell the user which MCP tool was used: "Used ghost-network subdomain_enum → found 42 subdomains".

## WORKFLOW EXAMPLES

### Example 1: "recon example.com"
```
1. ghost-network subdomain_enum {"domain": "example.com"} → get subdomains
2. security-tools tool_httpx {"args": ["-l", "subs.txt", "-silent", "-status-code"]} → live hosts
3. ghost-network quick_port_scan {"host": "example.com"} → open ports
4. ghost-web analyze_headers {"url": "https://example.com"} → security headers
5. ghost-intel cve_search {"query": "example.com tech"} → known CVEs
6. Report all findings
```

### Example 2: "is example.com vulnerable to anything?"
```
1. ghost-web detect_tech {"url": "https://example.com"} → identify stack
2. ghost-intel cve_search {"query": "<detected tech>"} → known CVEs for stack
3. security-tools tool_nuclei {"args": ["-u", "https://example.com", "-severity", "critical,high"]} → scan
4. ghost-web waf_detect {"url": "https://example.com"} → WAF presence
5. Report vulnerabilities with CVE references
```

### Example 3: "check this hash: 5f4dcc3b5aa765d61d8327deb882cf99"
```
1. ghost-intel hash_identify {"hash_value": "5f4dcc3b5aa765d61d8327deb882cf99"} → MD5
2. security-tools tool_hashcat {"args": ["-m", "0", "hash.txt", "rockyou.txt"]} → crack
3. Report cracked password
```

## OUTPUT FORMAT
```
[MCP] <server>.<tool> → <result summary>
```

## IMPORTANT
- MCP tools are ALWAYS available. They are the primary execution method.
- Never say "I can't use MCP" — the tools are loaded and ready.
- If a tool name isn't in the table, check `tool_status` on security-tools to see all 81 available tools.