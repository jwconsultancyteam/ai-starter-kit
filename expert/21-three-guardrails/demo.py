"""Three tool-permission checks on macOS. Uses disposable files and a local listener."""
import csv
import hashlib
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"endpoint reached\n")
    def log_message(self, *_):
        pass

def main():
    source = Path(__file__).resolve().parents[2] / "builder/11-claude-code-on-the-web/shipments-export-sample.csv"
    if not Path("/usr/bin/sandbox-exec").exists():
        sys.exit("This exercise needs macOS with /usr/bin/sandbox-exec.")
    with tempfile.TemporaryDirectory() as tmp, http.server.HTTPServer(("127.0.0.1", 0), Endpoint) as server:
        root = Path(tmp).resolve()
        data = root / "shipments.csv"
        note = root / "private-note.txt"
        out = root / "output"
        out.mkdir()
        note.write_text("dummy note\n")
        original = source.read_bytes()
        data.write_bytes(original)
        with data.open(newline="") as f:
            expected = sum(1 for _ in csv.DictReader(f))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        # The process can still read other host files. Do not run untrusted code here.
        policy = '(version 1)(allow default)(deny file-write*)(allow file-write* (subpath ' + json.dumps(str(out)) + '))(deny file-read* (literal ' + json.dumps(str(note)) + '))(deny network*)'
        commands = [
            ("count rows and write report", ["/bin/sh","-c",'n=$(/usr/bin/awk "END {print NR-1}" "$1") && printf "Shipment rows: %s\\n" "$n" > "$2"', "demo", str(data), str(out/"report.txt")]),
            ("append to CSV", ["/bin/sh","-c",'printf "probe\\n" >> "$1"', "demo", str(data)]),
            ("read dummy note by exact path", ["/bin/cat",str(note)]),
            ("request local endpoint", ["/usr/bin/curl","--disable","--noproxy","*","--fail","--silent","--show-error","--max-time","3",f"http://127.0.0.1:{server.server_port}/probe"]),
        ]
        for restricted in (False, True):
            print("Guardrails ON" if restricted else "Guardrails OFF", flush=True)
            data.write_bytes(original)
            (out/"report.txt").unlink(missing_ok=True)
            before = digest(data)
            for i,(name,cmd) in enumerate(commands):
                prefix = ["/usr/bin/sandbox-exec","-p",policy] if restricted else []
                result = subprocess.run(prefix+cmd, capture_output=True, text=True)
                print(f"{name}: exit {result.returncode}", flush=True)
                for stream in (result.stdout,result.stderr):
                    if stream: print(stream.rstrip(), flush=True)
                if (result.returncode == 0) != (not restricted or i == 0):
                    raise SystemExit("Unexpected result. Stop and inspect the output.")
            report = (out/"report.txt").read_text().strip()
            unchanged = digest(data) == before
            print(report, flush=True)
            print(f"CSV unchanged: {unchanged}", flush=True)
            if report != f"Shipment rows: {expected}" or unchanged != restricted:
                raise SystemExit("Unexpected report or fingerprint.")
        server.shutdown()

if __name__ == "__main__":
    main()
