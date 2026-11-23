#!/usr/bin/env python3
"""Local Job Broker for Tailscale Funnel Reverse-Pull Worker.

Bound to 127.0.0.1:8765 using Python stdlib ThreadingHTTPServer.
All endpoints require X-Worker-Token header for authentication.

Phases:
- Phase 1: Remote worker POSTs hardware specs to /checkin
- Phase 2: Local CLI long-polls GET /next-job (up to 20s timeout)
- Phase 3: Remote worker POSTs results to /result
"""

import json
import os
import sys
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta

# Configuration
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 8765
TOKEN_TIMEOUT_MINUTES = 30
MAX_JOB_AGE_SECONDS = 300  # 5 minutes max age for jobs

# In-memory storage (will be persistent per session)
jobs = {}  # job_id -> {"cmd": ..., "files": ..., "timeout": ..., "created": ..., "token": ...}
results = {}  # job_id -> {"returncode", "stdout", "stderr", "received": ...}
tokens = {}  # token -> {"created": ..., "last_seen": ...}
token = None  # Current session token

# Lock for thread safety
jobs_lock = threading.Lock()
tokens_lock = threading.Lock()


def generate_token():
    """Generate a fresh 32-char random token."""
    global token
    import secrets
    token = secrets.token_hex(16)  # 32 hex chars = 16 bytes
    tokens[token] = {"created": datetime.utcnow(), "last_seen": datetime.utcnow()}
    return token


def validate_token(req_token):
    """Validate the X-Worker-Token header. Returns True if valid."""
    global token
    if req_token is None:
        return False
    if req_token != token:
        return False
    # Update last_seen
    if req_token in tokens:
        tokens[req_token]["last_seen"] = datetime.utcnow()
    return True


class WorkerBrokerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the worker broker."""

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Worker-Token, Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging to avoid filling RAM."""
        pass

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = self.path.rstrip("/")
        
        # Check authentication
        req_token = self.headers.get("X-Worker-Token")
        if not validate_token(req_token):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid or missing token"}).encode())
            return

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = self.path.rstrip("/")
        
        # Check authentication
        req_token = self.headers.get("X-Worker-Token")
        if not validate_token(req_token):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid or missing token"}).encode())
            return

        if parsed_path == "/next-job":
            self.handle_next_job()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())

    def handle_next_job(self):
        """Long-poll endpoint: return next queued job or idle/shutdown."""
        with jobs_lock:
            for job_id in list(jobs.keys()):
                job = jobs[job_id]
                # Check if job is too old
                age = (datetime.utcnow() - job["created"]).total_seconds()
                if age > MAX_JOB_AGE_SECONDS:
                    # Remove stale job
                    del jobs[job_id]
                    continue
                
                # Check if result already posted
                if job_id in results:
                    # Return the existing result
                    result = results[job_id]
                    del results[job_id]
                    del jobs[job_id]
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "job_id": job_id,
                        "cmd": job["cmd"],
                        "files": job.get("files", []),
                        "timeout": job.get("timeout", 60),
                        "returncode": result.get("returncode"),
                        "stdout": result.get("stdout", ""),
                        "stderr": result.get("stderr", ""),
                        "status": "completed"
                    }).encode())
                    return
                else:
                    # Return job waiting for result
                    # Actually, we should return the job spec and let the worker run it
                    # But per design: worker polls, gets job, runs it, then POSTs result
                    # So we return the job command for the worker to execute
                    job_data = jobs[job_id]
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "job_id": job_id,
                        "cmd": job_data["cmd"],
                        "files": job_data.get("files", []),
                        "timeout": job_data.get("timeout", 60),
                        "status": "pending",
                        "action": "run_job"
                    }).encode())
                    return
            
            # No jobs available - check if shutdown requested
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"action": "idle"}).encode())

    def do_PUT(self):
        """Handle PUT requests for job submission (alternative to POST)."""
        parsed_path = self.path.rstrip("/")
        
        req_token = self.headers.get("X-Worker-Token")
        if not validate_token(req_token):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid or missing token"}).encode())
            return

        if parsed_path == "/checkin":
            self.handle_checkin()
        elif parsed_path == "/result":
            self.handle_result()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())

    def handle_checkin(self):
        """Remote worker POSTs hardware specs here."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            spec = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid JSON"}).encode())
            return

        with tokens_lock:
            if token and token in tokens:
                tokens[token]["last_seen"] = datetime.utcnow()

        with jobs_lock:
            # Save specs to .worker_specs.json
            specs_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "..", "..", "..", ".worker_specs.json"
            )
            # Actually, use the config dir
            specs_path = os.path.join(
                os.path.expanduser("~"), ".config", "opencode", ".worker_specs.json"
            )
            
            # Merge with existing specs
            existing_specs = {}
            if os.path.exists(specs_path):
                try:
                    with open(specs_path, "r") as f:
                        existing_specs = json.load(f)
                except (json.JSONDecodeError, IOError):
                    existing_specs = {}
            
            # Add/update this session's specs
            existing_specs[token] = {
                "received": datetime.utcnow().isoformat(),
                "spec": spec,
                "broker_url": f"http://{BROKER_HOST}:{BROKER_PORT}",
                "funnel_url": None,  # Will be set by manager
            }
            
            os.makedirs(os.path.dirname(specs_path), exist_ok=True)
            with open(specs_path, "w") as f:
                json.dump(existing_specs, f, indent=2)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "specs_received"}).encode())

    def handle_result(self):
        """Remote worker POSTs results here."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            result_data = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid JSON"}).encode())
            return

        job_id = result_data.get("job_id")
        if not job_id:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "missing job_id"}).encode())
            return

        with jobs_lock:
            if job_id in jobs:
                jobs[job_id]["result_posted"] = True
        
        with results_lock:
            results[job_id] = {
                "returncode": result_data.get("returncode", -1),
                "stdout": result_data.get("stdout", ""),
                "stderr": result_data.get("stderr", ""),
                "received": datetime.utcnow().isoformat(),
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "result_received"}).encode())


def broker_main():
    """Main function to start the worker broker server."""
    global token
    
    # Generate session token
    token = generate_token()
    print(f"[BROKER] Session token: {token}")
    print(f"[BROKER] Broker URL: http://{BROKER_HOST}:{BROKER_PORT}")
    print(f"[BROKER] Share this token with remote workers.")
    
    # Ensure directories exist
    os.makedirs(os.path.join(os.path.expanduser("~"), ".config", "opencode"), exist_ok=True)
    
    server = HTTPServer((BROKER_HOST, BROKER_PORT), WorkerBrokerHandler)
    
    # Set socket timeout for graceful shutdown
    server.socket.settimeout(60)
    
    print(f"[BROKER] Server running on {BROKER_HOST}:{BROKER_PORT}")
    print("[BROKER] Press Ctrl+C to stop.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[BROKER] Shutting down broker...")
    finally:
        server.server_close()


if __name__ == "__main__":
    broker_main()