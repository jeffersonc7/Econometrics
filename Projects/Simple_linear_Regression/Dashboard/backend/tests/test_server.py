import importlib.util
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import threading
import unittest
import urllib.error
import urllib.request

SPEC = importlib.util.spec_from_file_location('server', Path(__file__).resolve().parents[1] / 'server.py')
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        (cls.root / 'index.html').write_text('<html lang="es">Prueba</html>')
        (cls.root / 'assets').mkdir()
        (cls.root / 'assets/app.js').write_text('console.log("prueba")')
        (cls.root / 'secret.csv').write_text('no publicar')
        cls.artifact = cls.root / 'dashboard.json'
        cls.artifact.write_bytes((server.ROOT / 'frontend/public/data/dashboard.json').read_bytes())
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.create_handler(cls.root, cls.artifact))
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.httpd.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def request(self, path, method='GET'):
        try:
            response = urllib.request.urlopen(urllib.request.Request(self.base + path, method=method))
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, response.headers, response.read()

    def test_api_and_static_same_data_and_security_headers(self):
        status, headers, body = self.request('/api/v1/dashboard')
        self.assertEqual(status, 200)
        self.assertEqual(body, self.request('/data/dashboard.json')[2])
        self.assertIn('max-age=300', headers['Cache-Control'])
        self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertEqual(self.request('/')[0], 200)
        self.assertEqual(self.request('/assets/app.js')[0], 200)
        self.assertEqual(self.request('/health')[0], 200)
        self.assertEqual(self.request('/', 'HEAD')[2], b'')

    def test_sources_traversal_unknown_routes_blocked(self):
        for path in ['/data/source/data_clean.parquet', '/secret.csv', '/assets/', '/../secret.csv',
                     '/%2e%2e/secret.csv', '/.env', '/docs/', '/api/v1/unknown', '/assets/%00']:
            with self.subTest(path=path):
                status, _, body = self.request(path)
                self.assertEqual(status, 404)
                self.assertEqual(json.loads(body)['error']['message'], 'Recurso no encontrado.')

    def test_writes_rejected(self):
        for method in ['POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE', 'CONNECT']:
            with self.subTest(method=method):
                status, _, body = self.request('/api/v1/dashboard', method)
                self.assertEqual(status, 405)
                self.assertIn('sólo lectura', json.loads(body)['error']['message'])

    def test_absent_and_corrupt_data_have_spanish_errors(self):
        original = self.artifact.read_bytes()
        try:
            self.artifact.rename(self.root / 'saved.json')
            self.assertEqual(self.request('/api/v1/dashboard')[0], 503)
            self.assertEqual(self.request('/health')[0], 503)
            self.artifact.write_text('datos corruptos')
            status, _, body = self.request('/data/dashboard.json')
            self.assertEqual(status, 503)
            self.assertEqual(json.loads(body)['error']['code'], 'INVALID_DATA')
            self.assertEqual(self.request('/health')[0], 503)
            self.artifact.write_text(json.dumps({'data': {}, 'meta': {'schema_version': '1.0', 'n': 9881}}))
            self.assertEqual(self.request('/api/v1/dashboard')[0], 503)
            self.assertEqual(self.request('/health')[0], 503)
        finally:
            self.artifact.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
