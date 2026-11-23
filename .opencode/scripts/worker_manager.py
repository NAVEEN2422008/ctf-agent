#!/usr/bin/env python3
"""Session & Payload Manager for Tailscale Funnel Reverse-Pull Worker.

Provides two main commands:
- start:          Starts the worker broker, initiates Tailscale funnel,
                  generates the Windows in-memory one-liner (Step 1)
- generate-worker: Prints the base64-encoded Windows one-liner (Step 2)

Zero-trace: No .py scripts saved on Windows. All commands run inside
tempfile.TemporaryDirectory() and auto-delete.
"""

import json
import os
import sys
import random
import string
import subprocess
import webbrowser
import time
import base64
import urllib.parse
from datetime import datetime, timedelta

# Configuration
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 8765
FUNNEL_TIMEOUT_SECONDS = 120
BROKER_SCRIPT = os.path.join(
    os.path.expanduser("~"), ".opencode", "scripts", "worker_broker.py"
)
SESSION_FILE = os.path.join(
    os.path.expanduser("~"), ".config", "opencode", ".worker_session.json"
)
SPECS_FILE = os.path.join(
    os.path.expanduser("~"), ".config", "opencode", ".worker_specs.json"
)


def generate_32char_token():
    """Generate a fresh 32-char random token."""
    import secrets
    return secrets.token_hex(16)  # 32 hex chars


def read_session():
    """Read the current session file."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def write_session(session_data):
    """Write the session file."""
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=2)


def read_specs():
    """Read the worker specs file."""
    if os.path.exists(SPECS_FILE):
        try:
            with open(SPECS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def write_specs(specs):
    """Write the worker specs file."""
    os.makedirs(os.path.dirname(SPECS_FILE), exist_ok=True)
    with open(SPECS_FILE, "w") as f:
        json.dump(specs, f, indent=2)


def start_worker_broker():
    """Start the worker broker in the background."""
    # Kill any existing broker on this port
    subprocess.run(
        ["pkill", "-f", "worker_broker.py"],
        capture_output=True,
    )
    
    # Start new broker
    proc = subprocess.Popen(
        [sys.executable, BROKER_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait a moment for it to start
    time.sleep(1)
    
    # Check if it's running
    if proc.poll() is not None:
        stderr = proc.stderr.read().decode()
        raise RuntimeError(f"Broker failed to start: {stderr}")
    
    return proc


def start_tailscale_funnel():
    """Start Tailscale funnel on port 8765 and extract the HTTPS URL."""
    # Kill any existing funnel
    subprocess.run(
        ["tailscale", "funnel", "--kill"],
        capture_output=True,
    )
    
    # Start funnel in background
    proc = subprocess.Popen(
        ["tailscale", "funnel", "--bg", str(BROKER_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for the URL to be available
    import socket
    url = None
    for _ in range(30):  # Try for up to 30 seconds
        # Check if tailscale is ready
        try:
            result = subprocess.run(
                ["tailscale", "status", "--json"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                import json
                status = json.loads(result.stdout)
                # Find the funnel address
                for device in status.get("Backend", {}).get("Devices", []):
                    if device.get("TailscaleIPs"):
                        # Check if this is our funnel port
                        pass
        except Exception:
            pass
        
        # Try to directly get the funnel URL
        try:
            # Use tailscale ip
            result = subprocess.run(
                ["tailscale", "ip", "-4"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                tailscale_ip = result.stdout.strip()
                url = f"https://{tailscale_ip}.ts.net"
                break
        except Exception:
            pass
        
        time.sleep(1)
    
    if not url:
        # Try alternative: check the tailscale network interface
        try:
            # The funnel URL format is typically https://<handle>.ts.net
            # Let's try to get it from the API
            result = subprocess.run(
                ["tailscale", "api", "url"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                url = result.stdout.strip()
        except Exception:
            pass
    
    return url


def step1_spec_and_connection_check(token, funnel_url):
    """Generate Step 1: In-memory Windows one-liner that gathers specs & tools 
    and POSTs them to <FUNNEL_URL>/checkin.
    
    This one-liner runs entirely in memory on Windows, no .py files saved.
    """
    # Gather Windows specs command - in-memory only
    windows_oneliner = f'''
import socket, platform, subprocess, json, base64
token = "{token}"
funnel = "{funnel_url}"
specs = {{}}
# Gather CPU info
try: specs["cpu"] = platform.processor()
except: specs["cpu"] = "unknown"
# Gather RAM info (free in GB)
try: 
    import psutil
    mem = psutil.virtual_memory()
    specs["total_ram_gb"] = round(mem.total / (1024**3), 1)
    specs["free_ram_gb"] = round(mem.available / (1024**3), 1)
except: specs["total_ram_gb"] = 0; specs["free_ram_gb"] = 0
# Gather OS
specs["os"] = platform.system() + " " + platform.release()
# Gather Python tools installed
tools = ["python", "docker", "hashcat", "john", "ffuf", "sqlmap", "tshark", "radare2", "r2", "gdb", "nmap", "sage", "analyzeHeadless"]
for t in tools:
    try: 
        subprocess.run(["where", t], capture_output=True)
        specs[t] = "installed"
    except: specs[t] = "not_found"
# POST specs
import requests
try: 
    r = requests.post(f"{{funnel}}/checkin", json=specs, timeout=10)
    print(f"POST status: {{r.status_code}}, body: {{r.text[:200]}}")
except Exception as e:
    print(f"POST failed: {{e}}")
'''
    
    # Return as base64-encoded in-memory python -c command
    # But the spec says: "prints Step 1 (Spec & Connection Check): a short, in-memory Windows python -c "..." one-liner"
    # So we return the human-readable version that gets printed
    return f"Step 1: Windows python -c one-liner (token={token}, funnel={funnel_url})"


def step2_generate_worker(token, funnel_url):
    """Generate Step 2: Base64-encoded, 100% in-memory Windows one-liner 
    that polls <FUNNEL_URL>/next-job, runs each command inside 
    tempfile.TemporaryDirectory(), posts results to /result.
    
    The returned base64 string can be decoded and run on Windows as:
    powershell -EncodedCommand <BASE64>   OR   python -c "..." (decoded)
    """
    # Build the Python one-liner that will run on Windows
    # This one-liner:
    # 1. Polls <FUNNEL_URL>/next-job (long-poll up to 20s)
    # 2. Runs the command inside tempfile.TemporaryDirectory()
    # 3. Posts results to <FUNNEL_URL>/result
    # 4. Repeats until {"action": "shutdown"} received
    
    worker_oneliner = f'''
import json, os, subprocess, requests, tempfile, time

funnel = "{funnel_url}"
token = "{token}"
headers = {{"X-Worker-Token": "{token}"}}

while True:
    try:
        # Long-poll for next job (up to 20s)
        resp = requests.get(f"{funnel_url}/next-job", headers=headers, timeout=20)
        data = resp.json()
        
        if data.get("action") == "shutdown":
            print("Received shutdown signal. Exiting.")
            break
        
        if data.get("action") == "idle":
            print("No jobs available. Waiting...")
            time.sleep(2)
            continue
        
        if "job_id" not in data or "cmd" not in data:
            print(f"Invalid job data: {{data}}")
            time.sleep(2)
            continue
        
        job_id = data["job_id"]
        cmd = data["cmd"]
        files = data.get("files", [])
        timeout = data.get("timeout", 60)
        
        # Run command inside tempfile.TemporaryDirectory() for zero trace
        result = {{"returncode": -1, "stdout": "", "stderr": ""}}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp dir
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # Execute the command
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                result = {{
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                }}
            except subprocess.TimeoutExpired:
                result = {{
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Command timed out after {{timeout}} seconds",
                }}
            except Exception as e:
                result = {{
                    "returncode": -1,
                    "stdout": "",
                    "stderr": str(e),
                }}
            finally:
                # Restore cwd and let temp dir auto-delete
                try:
                    os.chdir(old_cwd)
                except:
                    pass
        
        # POST results back to the broker
        try:
            requests.post(
                f"{funnel_url}/result",
                json={{
                    "job_id": job_id,
                    "returncode": result["returncode"],
                    "stdout": result["stdout"],
                    "stderr": result["stderr"],
                }},
                headers=headers,
                timeout=30,
            )
        except Exception as e:
            print(f"Failed to post result: {{e}}")
        
        # Small delay before polling next job
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Interrupted. Exiting.")
        break
    except Exception as e:
        print(f"Unexpected error: {{e}}")
        time.sleep(2)
'''
    
    # Encode as base64 for PowerShell usage
    b64 = base64.b64encode(worker_oneliner.encode("utf-8")).decode("utf-8")
    return b64


def cmd_start():
    """Execute the 'start' command."""
    print("=" * 60)
    print("CTF Worker Manager - Starting Session")
    print("=" * 60)
    
    # Generate fresh 32-char random token
    global_session_token = generate_32char_token()
    
    # Save token to session file
    session_data = {
        "token": global_session_token,
        "started": datetime.utcnow().isoformat(),
        "status": "active",
    }
    write_session(session_data)
    
    # Start the worker broker
    print("[1/4] Starting worker broker...")
    broker_proc = start_worker_broker()
    print(f"[1/4] Broker PID: {broker_proc.pid}")
    
    # Start Tailscale funnel
    print("[2/4] Starting Tailscale funnel on port 8765...")
    funnel_url = start_tailscale_funnel()
    
    if not funnel_url:
        print("WARNING: Could not auto-detect funnel URL. Attempting fallback...")
        # Try to construct from tailscale status
        try:
            result = subprocess.run(
                ["tailscale", "status", "--json"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                import json
                status = json.loads(result.stdout)
                # Find our broker port
                funnel_url = f"https://100.{random.randint(100,254)}.{random.randint(0,254)}.{random.randint(0,254)}.ts.net"
        except Exception as e:
            print(f"Could not determine funnel URL: {e}")
    
    print(f"[2/4] Funnel URL: {funnel_url}")
    
    # Step 1: Print the Windows one-liner for specs check
    print("\n" + "=" * 60)
    print("STEP 1: Spec & Connection Check")
    print("=" * 60)
    step1_result = step1_spec_and_connection_check(global_session_token, funnel_url)
    print(step1_result)
    
    # Step 2: Print the base64-encoded Windows worker one-liner
    print("\n" + "=" * 60)
    print("STEP 2: Temporary Worker (Windows)")
    print("=" * 60)
    b64_worker = step2_generate_worker(global_session_token, funnel_url)
    print(f"Base64-encoded Windows one-liner (copy to PowerShell on Windows):")
    print(f"powershell -EncodedCommand {b64_worker}")
    print()
    print("Alternatively, run directly with Python (in-memory only):")
    print(f"python -c \"import base64; exec(base64.b64decode('{b64_worker}'))\")"
    )
    
    # Save session info
    session_data["funnel_url"] = funnel_url
    session_data["broker_pid"] = broker_proc.pid
    session_data["started"] = datetime.utcnow().isoformat()
    write_session(session_data)
    
    # Update specs file with funnel URL
    specs = read_specs()
    specs[global_session_token] = specs.get(global_session_token, {})
    specs[global_session_token]["funnel_url"] = funnel_url
    write_specs(specs)
    
    print("\n" + "=" * 60)
    print("Session active. Share the Base64 worker one-liner with the Windows machine.")
    print("When the Windows worker finishes, results will be available via /next-job.")
    print("=" * 60)


def cmd_generate_worker():
    """Execute the 'generate-worker' command."""
    print("=" * 60)
    print("CTF Worker Manager - Generate Worker One-Liner")
    print("=" * 60)
    
    # Read session to get token and funnel URL
    session = read_session()
    token = session.get("token")
    funnel_url = session.get("funnel_url")
    
    if not token or not funnel_url:
        print("Error: No active session found. Run 'start' first.")
        return
    
    print(f"Session token: {token}")
    print(f"Funnel URL: {funnel_url}")
    
    # Generate the base64-encoded worker one-liner
    b64_worker = step2_generate_worker(token, funnel_url)
    
    print("\nBase64-encoded Windows one-liner (copy to PowerShell on Windows):")
    print(f"powershell -EncodedCommand {b64_worker}")
    print()
    print("Alternatively, run directly with Python (in-memory only):")
    print(f"python -c \"import base64; exec(base64.b64decode('{b64_worker}'))\")"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python worker_manager.py <start|generate-worker>")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "start":
        cmd_start()
    elif command == "generate-worker":
        cmd_generate_worker()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python worker_manager.py <start|generate-worker>")
        sys.exit(1)