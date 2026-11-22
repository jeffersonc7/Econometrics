"""Empaquetar únicamente el build público para Netlify Drop, nunca microdatos."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'.html', '.js', '.css', '.json', '.woff', '.woff2', '.ttf', '.otf', '.eot', '.svg', '.png', '.jpg', '.webp', '.ico'}


def package(source: Path, output: Path):
    source = source.resolve()
    if not (source / 'index.html').is_file():
        raise ValueError('Falta el build. Ejecute npm run build dentro de frontend.')
    files = sorted(p for p in source.rglob('*') if p.is_file())
    for file in files:
        rel = file.relative_to(source)
        if file.is_symlink() or any(part.startswith('.') for part in rel.parts):
            raise ValueError(f'Archivo oculto o enlace no permitido: {rel}')
        if file.suffix not in ALLOWED and file.name != '_headers':
            raise ValueError(f'No es un recurso público autorizado: {rel}')
    payload = json.loads((source / 'data/dashboard.json').read_text())
    if payload['meta']['n'] != 9881 or payload['meta']['revision'] != 'd8a5794b62c4e5ec1f7f11b41c28d4ac82d47698':
        raise ValueError('El artefacto no corresponde a la muestra auditada')
    for url in re.findall(r'(?:src|href)=["\']([^"\']+)', (source / 'index.html').read_text()):
        if not url.startswith(('data:', 'http:', 'https:', '#')) and not (source / url.lstrip('/')).is_file():
            raise ValueError(f'El HTML refiere a un recurso ausente: {url}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in files:
            entry = zipfile.ZipInfo(file.relative_to(source).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, file.read_bytes())
    manifest = dict(archive=str(output.relative_to(ROOT)), sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                    bytes=output.stat().st_size, files=len(files), source_revision=payload['meta']['revision'],
                    n=payload['meta']['n'], contents=[p.relative_to(source).as_posix() for p in files])
    (output.parent / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: manifest[k] for k in ['archive', 'files', 'bytes', 'sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preparar ZIP para Netlify Drop')
    parser.add_argument('--source', type=Path, default=ROOT / 'frontend/dist')
    parser.add_argument('--output', type=Path, default=ROOT / 'entrega/grupo-2-netlify.zip')
    args = parser.parse_args()
    package(args.source, args.output)
