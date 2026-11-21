"""Servidor local/portable de lectura: API de agregados y build estático. Sin microdatos."""
from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit

from contract import validate_public_artifact

ROOT = Path(__file__).resolve().parents[1]


def create_handler(public_dir: Path, artifact: Path):
    public_dir = public_dir.resolve()
    artifact = artifact.resolve()

    class Handler(BaseHTTPRequestHandler):
        def send_body(self, status, body: bytes, content_type='application/json; charset=utf-8', cache=False):
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'none'")
            self.send_header('Cache-Control', 'public, max-age=300' if cache else 'no-store')
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)

        def error(self, status: int, code: str, message: str):
            self.send_body(status, json.dumps({'error': {'code': code, 'message': message}}, ensure_ascii=False).encode())

        def do_GET(self):
            path = unquote(urlsplit(self.path).path)
            if '\x00' in path:
                self.error(404, 'NOT_FOUND', 'Recurso no encontrado.')
                return
            if path == '/health':
                try:
                    validate_public_artifact(json.loads(artifact.read_bytes()))
                    ready = True
                except (OSError, ValueError):
                    ready = False
                self.send_body(200 if ready else 503, json.dumps({'status': 'disponible' if ready else 'sin datos válidos'}).encode())
                return
            if path in ['/api/v1/dashboard', '/data/dashboard.json']:
                if not artifact.is_file():
                    self.error(503, 'DATA_UNAVAILABLE', 'Los datos no están disponibles. Genere los agregados antes de iniciar.')
                    return
                try:
                    body = artifact.read_bytes()
                    content = json.loads(body)
                    validate_public_artifact(content)
                except (OSError, ValueError, KeyError, TypeError):
                    self.error(503, 'INVALID_DATA', 'Los datos no se pudieron validar.')
                    return
                self.send_body(200, body, cache=True)
                return
            # Whitelist de build: nunca servir fuentes, docs, carpetas ocultas ni listados.
            segments = Path(path).parts
            if '..' in segments or any(s.startswith('.') for s in segments if s != '/'):
                self.error(404, 'NOT_FOUND', 'Recurso no encontrado.')
                return
            relative = 'index.html' if path == '/' else path.lstrip('/')
            allowed = relative == 'index.html' or relative == 'favicon.svg' or relative.startswith('assets/')
            target = (public_dir / relative).resolve()
            if not allowed or not target.is_relative_to(public_dir) or not target.is_file():
                self.error(404, 'NOT_FOUND', 'Recurso no encontrado.')
                return
            content_type = mimetypes.guess_type(target.name)[0] or 'application/octet-stream'
            self.send_body(200, target.read_bytes(), content_type, cache=relative.startswith('assets/'))

        def do_HEAD(self):
            self.do_GET()

        def reject_write(self):
            self.error(HTTPStatus.METHOD_NOT_ALLOWED, 'READ_ONLY', 'Este sitio es de sólo lectura.')

        do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = do_TRACE = do_CONNECT = reject_write

    return Handler


def main():
    parser = argparse.ArgumentParser(description='Servir dashboard público de sólo lectura')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--public-dir', type=Path, default=ROOT / 'frontend/dist')
    parser.add_argument('--artifact', type=Path, default=ROOT / 'frontend/public/data/dashboard.json')
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), create_handler(args.public_dir, args.artifact))
    print(f'Dashboard local: http://{args.host}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
