---
description: Analyze a prompt, select the best agent, rewrite it for that agent's context, and delegate via task tool
---

# /prompt — Smart Prompt Router & Delegator

Take any user prompt, analyze it, select the optimal specialist agent, rewrite the prompt
to match that agent's capabilities and constraints, then delegate via the `task` tool.

## Usage

```
/prompt <your raw prompt here>
```

Examples:
- `/prompt scan 10.0.0.5 for open ports and services`
- `/prompt there's a login form at http://target/login, try SQLi`
- `/prompt crack this RSA ciphertext: 0x1a2b3c... with e=3`
- `/prompt extract hidden data from this PNG: /path/to/image.png`
- `/prompt reverse engineer this binary: /path/to/challenge`
- `/prompt offload hashcat -m 1000 hash.txt rockyou.txt to worker`

## Step 1 — Analyze the Prompt

Parse the user's raw prompt and extract:
- **Intent**: What is the user trying to accomplish?
- **Target**: IP, URL, file path, ciphertext, binary, etc.
- **Keywords**: scan, web, SQLi, XSS, pwn, ROP, crypto, RSA, stego, carve, memory, pcap, worker, dispatch, etc.
- **Constraints**: speed, depth, specific tools mentioned

## Step 2 — Select the Best Agent

Use this decision matrix (first match wins):

| Keywords / Intent | Agent | Rationale |
|---|---|---|
| scan, recon, ports, services, subdomain, DNS, live host, nmap, naabu, httpx | `ctf-triage` | Fast recon specialist |
| web, URL, HTTP, SQLi, XSS, fuzz, auth bypass, IDOR, SSRF, login, form, API, OWASP | `ctf-web` | Web app specialist |
| binary, pwn, ROP, buffer overflow, shellcode, reverse engineer, gdb, objdump, ELF, PE | `ctf-pwn-rev` | Binary exploitation specialist |
| crypto, RSA, AES, cipher, decrypt, encrypt, hash, base64, encoding, classical, modern | `ctf-crypto` | Cryptanalysis specialist |
| forensics, stego, carve, memory, pcap, disk, image, binwalk, exiftool, LSB, hidden | `ctf-forensics` | Forensics specialist |
| worker, dispatch, offload, tailscale, funnel, hashcat, large wordlist, remote | `ctf-worker-dispatch` | Remote task offloading specialist |
| (none match / ambiguous) | `ctf-triage` | Default to recon first |

If the prompt contains MULTIPLE intents (e.g., "scan then exploit"), select the FIRST phase agent and note the follow-up in NEXT STEP.

## Step 3 — Rewrite the Prompt for the Selected Agent

Transform the raw user prompt into an agent-optimized prompt that includes:

1. **Task ID**: Generate a unique ID: `<agent-prefix>-<3-digit-number>` (e.g., `triage-001`, `web-042`, `pwn-013`)
2. **Objective**: One clear sentence stating what to accomplish
3. **Target**: Exact target (IP, URL, file path, ciphertext)
4. **Context**: Any relevant info from parent memory (tech stack, prior findings, constraints)
5. **Scope**: What to do and what NOT to do (agent boundaries)
6. **Artifact path**: `./artifacts/<task_id>/` for all raw output
7. **Return contract reminder**: "Return ONLY the compact report per Mandatory Return Contract. NEVER dump raw output."

### Rewrite Template

```
TASK ID: <task_id>
OBJECTIVE: <one sentence>
TARGET: <exact target>
CONTEXT: <relevant prior findings or constraints, or "none">
SCOPE: <what to do> | DO NOT: <what to avoid (other agent's domain)>
ARTIFACTS: ./artifacts/<task_id>/
RETURN: Compact report only (STATUS/RESULT/ROOT CAUSE/ARTIFACTS/NEXT STEP). No raw output.
```

### Agent-Specific Prompt Enhancements

**For ctf-triage:**
- Add: "Speed priority: top-1000 ports first, expand only if needed"
- Add: "Save naabu/httpx/nmap output to artifacts/"
- Add: "Identify service + version, delegate deep enum to specialist"

**For ctf-web:**
- Add: "Run nuclei + nikto first, then targeted ffuf"
- Add: "Save all raw output to artifacts/"
- Add: "Manual verification required before reporting vuln"

**For ctf-pwn-rev:**
- Add: "Start with file/checksec/strings/readelf, then gdb"
- Add: "Save exploit.py to artifacts/"
- Add: "Test locally before remote adaptation"

**For ctf-crypto:**
- Add: "Identify algorithm first (classical/modern/encoding)"
- Add: "Write solve.py, save to artifacts/"
- Add: "Report only the flag/plaintext, not the full derivation"

**For ctf-forensics:**
- Add: "Start with file/exiftool/strings/binwalk"
- Add: "Save extracted files to artifacts/"
- Add: "If payload needs crypto, note in NEXT STEP"

**For ctf-worker-dispatch:**
- Add: "Ensure broker running before submitting job"
- Add: "Save broker logs and results to artifacts/"
- Add: "Report job ID and completion time"

## Step 4 — Delegate via Task Tool

Spawn the selected agent with the rewritten prompt:

```json
{
  "description": "<3-5 words: what the subagent must do>",
  "prompt": "<rewritten prompt from Step 3>",
  "subagent_type": "<selected agent>"
}
```

## Step 5 — Return Result to User

Pass through the subagent's compact report verbatim. Do NOT add raw output or commentary.

If the subagent returns BLOCKED, suggest the next agent to try based on the blocker.

## Anti-Patterns

- ❌ Sending the raw user prompt without rewriting → ✅ Always rewrite with task ID, scope, artifact path
- ❌ Selecting the wrong agent → ✅ Use the decision matrix, first match wins
- ❌ Adding raw output to the report → ✅ Pass through compact report only
- ❌ Forgetting the artifact path → ✅ Always include `./artifacts/<task_id>/`
- ❌ Not generating a task ID → ✅ Every delegation gets a unique ID

## Example Flow

**User input:** `/prompt scan 192.168.1.0/24 for live hosts and open ports`

**Analysis:**
- Intent: network reconnaissance
- Target: 192.168.1.0/24
- Keywords: scan, live hosts, open ports
- Agent: ctf-triage

**Rewritten prompt:**
```
TASK ID: triage-001
OBJECTIVE: Discover live hosts and open ports in 192.168.1.0/24
TARGET: 192.168.1.0/24
CONTEXT: none
SCOPE: Fast recon (naabu top-1000 + httpx) | DO NOT: deep service enum, web testing, exploitation
ARTIFACTS: ./artifacts/triage-001/
RETURN: Compact report only (STATUS/RESULT/ROOT CAUSE/ARTIFACTS/NEXT STEP). No raw output.
Speed priority: top-1000 ports first, expand only if needed.
Save naabu/httpx/nmap output to artifacts/.
Identify service + version, delegate deep enum to specialist.
```

**Delegation:**
```json
{
  "description": "Scan 192.168.1.0/24 live hosts",
  "prompt": "<rewritten prompt above>",
  "subagent_type": "ctf-triage"
}
```

**User sees:** The compact report from ctf-triage, nothing else.
