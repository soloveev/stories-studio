#!/usr/bin/env python3
"""HTTP server with image proxy endpoint for CORS-free export via html2canvas
and a /save endpoint that writes the editor state back to the HTML file."""

import http.server
import os
import shutil
import tempfile
import urllib.request
import urllib.parse
import sys

MAX_SAVE_BYTES = 200 * 1024 * 1024  # data-URL картинки легко раздувают файл


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/proxy?url='):
            self.handle_proxy()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/save'):
            self.handle_save()
        else:
            self.send_error(404)

    def handle_save(self):
        query = urllib.parse.urlparse(self.path).query
        name = urllib.parse.parse_qs(query).get('name', [None])[0]
        # basename отсекает path traversal: сохраняем только в папку, откуда раздаём
        name = os.path.basename(name or '')
        if not name.endswith('.html'):
            self.send_error(400, 'Only .html files can be saved')
            return
        length = int(self.headers.get('Content-Length') or 0)
        if not 0 < length <= MAX_SAVE_BYTES:
            self.send_error(400, f'Bad Content-Length: {length}')
            return
        body = self.rfile.read(length)
        target = os.path.join(os.getcwd(), name)
        try:
            if os.path.exists(target):
                backup = name[:-len('.html')] + '.backup.html'
                shutil.copy2(target, os.path.join(os.getcwd(), backup))
            fd, tmp = tempfile.mkstemp(dir=os.getcwd(), suffix='.tmp')
            with os.fdopen(fd, 'wb') as f:
                f.write(body)
            os.replace(tmp, target)  # атомарная замена
        except Exception as e:
            self.send_error(500, f'Save failed: {e}')
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', '2')
        self.end_headers()
        self.wfile.write(b'ok')

    def handle_proxy(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        url = params.get('url', [None])[0]
        if not url:
            self.send_error(400, 'Missing url parameter')
            return
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                content_type = resp.headers.get('Content-Type', 'application/octet-stream')
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(502, f'Proxy error: {e}')

    def log_message(self, format, *args):
        print(f'[server] {args[0]}')


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    with http.server.HTTPServer(('', port), ProxyHandler) as httpd:
        print(f'Serving on http://localhost:{port}')
        httpd.serve_forever()
