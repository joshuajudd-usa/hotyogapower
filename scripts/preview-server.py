#!/usr/bin/env python3
"""
Local preview server for hotyogapower.com.

Mimics the netlify.toml clean-URL rewrites (/app -> app.html, /web -> web.html)
so the front-door links are clickable locally, exactly as they'll behave once
deployed. Dev convenience only — Netlify serves the real thing in production.

Run:  python3 scripts/preview-server.py [port]   (default 8765)
Open: http://localhost:8765/
"""
import sys, os
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

CLEAN = {
    "/": "/index.html",
    "/app": "/app.html", "/app/": "/app.html",
    "/web": "/web.html", "/web/": "/web.html",
}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        p = path.split("?", 1)[0].split("#", 1)[0]
        if p in CLEAN:
            p = CLEAN[p]
        elif not os.path.splitext(p)[1] and os.path.exists(os.path.join(ROOT, p.lstrip("/") + ".html")):
            p = p + ".html"
        return super().translate_path(p)

if __name__ == "__main__":
    print("hotyogapower preview -> http://localhost:%d/  (root=%s)" % (PORT, ROOT))
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
