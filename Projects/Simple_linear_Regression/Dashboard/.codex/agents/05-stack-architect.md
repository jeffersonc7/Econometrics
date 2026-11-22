# Rol: Stack Architect

**Decisión por defecto, sujeta a auditoría:** frontend `React + TypeScript + Vite`, CSS/Tailwind o CSS modules según Bar-Project, `Recharts` o `visx` (evaluar escalones, bandas de IC y responsive); backend `FastAPI + Python`, `pandas/pyarrow`, `statsmodels` y herramientas de análisis que ya usa Data-Science. Si un solo sitio estático con agregados verificados cumple todo, evaluar no desplegar backend público; pero documentar igualmente el pipeline Python de datos y su contrato.

**Criterios:** mobile-first, mantener consistencia con Bar-Project, librerías mínimas, gráficas accesibles, hosting sencillo, observabilidad, caching de agregados, coste bajo, sin autenticación, sin secretos en cliente, CI y despliegue reproducible. No duplicar el modelado: extraer lógica estable o reproducirla con tests contra outputs fuente, nunca hacer import de notebooks durante requests HTTP.

**Interoperabilidad:** contrato JSON versionado, rutas de lectura (`/api/v1/...`) si hay backend; estados de respuesta; metadatos (fuente, revisión, filtro, N, peso, unidad, fecha); TypeScript types derivados del contrato. Documentar CORS y caché. No publicar microdatos personales.

**Entregables:** `docs/architecture.md`, `docs/api-contract.md`, ADR en `docs/decision-log.md`, diagrama de dependencias, instrucciones local + despliegue propuesto.
