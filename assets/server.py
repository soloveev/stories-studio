#!/usr/bin/env python3
"""HTTP server with image proxy endpoint for CORS-free export via html2canvas."""

import http.server
import urllib.request
import urllib.parse
import sys


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/proxy?url='):
            self.handle_proxy()
        else:
            super().do_GET()

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
