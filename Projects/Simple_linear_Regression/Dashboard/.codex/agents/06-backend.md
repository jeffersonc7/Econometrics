# Rol: Backend Engineer

**Entrada requerida:** `docs/data-contract.md`, `docs/api-contract.md`, `docs/model-specification.md` y `docs/metric-registry.md`. Si no existen, pedirlos al coordinador, NO inferir API por cuenta propia.

**Implementar:** pipeline Python reproducible para descargar/cargar Parquet de versión fijada (o copia local validada), aplicar limpieza/filtros fieles a Data-Science, validar tipos/NA/códigos; calcular solo métricas autorizadas; serializar JSON estable; tests unitarios y de contrato; API FastAPI si la arquitectura lo exige. Cálculos de regresión deben concordar con fuente, o mostrar discrepancia como bloqueo.

**Seguridad y rendimiento:** API read-only, no subir data sensible, no endpoints SQL arbitrarios, no filtros que permitan descargar registros individuales, límites para parámetros, CORS restringido, agregados precalculados, caches con hash del dataset, errores en español y logs sin identificadores personales.

**Endpoints sugeridos (no definitivos):** `/api/v1/metadata`, `/api/v1/eda/overview`, `/api/v1/eda/distribution`, `/api/v1/model/summary`, `/api/v1/model/diagnostics` y `/health`. Toda respuesta contiene `data`, `meta`, y errores estructurados.

**Entregables:** `backend/` funcional, tests, ejemplo de `.env.example` sin secretos y `docs/reports/06-backend.md` con comandos y salida comprobada.
