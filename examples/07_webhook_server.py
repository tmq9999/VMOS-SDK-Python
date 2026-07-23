"""Minimal webhook receiver for VMOS callbacks (stdlib only).

Configure the callback URL in the VMOS web console, then run:
    python3 examples/07_webhook_server.py
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from vmos.callbacks import parse_callback


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        event = parse_callback(json.loads(body or b"{}"))
        print(f"[{event.kind}] pad={event.pad_code} task={event.task_id} ok={event.succeeded}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
