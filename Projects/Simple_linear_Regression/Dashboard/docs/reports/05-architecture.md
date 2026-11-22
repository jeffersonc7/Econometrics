# Arquitectura y contratos
Autor: orquestador. Fecha:2026-11-16. Estado:PASS.

Inventario respaldó React/TS/Vite y stack científico Python existente. Selección estática con pipeline offline reduce servicios y permite una única URL; backend stdlib opcional sirve API y build sin cálculo en cada request. Sin FastAPI porque no se necesita servicio de estimación ni nuevos filtros remotos. Diseño API/data v1 fijado antes de frontend, tipos en frontend/src/types.ts y validador público Python independiente en backend/contract.py. Documentos: architecture.md, api-contract.md, data-contract.md, decision-log.md y deployment.md.

Revisión conjunta: auditoría fuentes, econometría66comparaciones, frontend separado por propiedad de archivos y QA integrado del coordinador. No autenticación, escrituras HTTP, fuente cruda en bundle ni servicios externos en tiempo de lectura. Proveedor de hosting y coste no se presuponen; requieren decisión posterior a autorización de publicación.
