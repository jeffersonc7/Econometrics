# Preparación de publicación (sin ejecutar)
Autor: arquitectura/QA. Fecha: 2026-11-16. Estado: local; publicación requiere autorización del usuario.

## Opción estática recomendada
Ejecutar `npm ci && npm run build` dentro de frontend. Publicar exclusivamente `frontend/dist/` en un hosting estático con HTTPS y MIME correctos. El build incluye `/data/dashboard.json`, no necesita API, secretos, tokens, CORS ni microdatos. Navegación por hash funciona sin reglas SPA. Directorio raíz público jamás debe ser Dashboard ni data/source.

No se ha seleccionado proveedor, registrado proyecto ni comprobado tarifas actuales: no se promete un plan gratuito. Esa selección y autorización se realizan al decidir publicar.

## Opción servidor único
Tras build, `python3 backend/server.py --host 0.0.0.0 --port 8000`. El servidor sirve build y API agregada en el mismo origen. Para operación pública usar proceso supervisado y terminación HTTPS; no exponer un dev server Vite. Healthcheck `/health`; fuentes ausentes en hosting son válidas si JSON ya existe. Rutas POST/PUT/PATCH/DELETE están bloqueadas. Regenerar JSON y reconstruir frontend juntos para mantener versión coherente. La ejecución CLI falla si hashes o resultados difieren de la revisión auditada.

## Antes de publicar
Obtener autorización expresa; repetir build y pruebas si cambian fuentes/código; inspeccionar carpeta dist para confirmar sólo assets/HTML/agregado; conservar atribución INEC y metadatos HF. Mantener artefacto previo para reversión. No incluir data/source, entornos, node_modules, notebooks, referencias de trabajo ni documentos internos en el directorio público.

## Publicación autorizada y completada
2026-11-16: el usuario solicitó expresamente una web accesible por enlace. Sitio público publicado con Sites: https://cristal-econometria-ecuador.palebrownie3.chatgpt.site . El registro exacto de versión, commit y despliegue está en published-site.json. Las secciones anteriores describen el estado previo a esta autorización.
