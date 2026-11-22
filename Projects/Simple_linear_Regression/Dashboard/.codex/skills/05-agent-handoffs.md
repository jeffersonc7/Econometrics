# Skill: Agent Handoffs

Cada handoff debe tener documento concreto:
- Auditor -> Data/Model: `docs/source-map.md` + inventario.
- Data -> Econometrics/Backend: `docs/data-contract.md`, `docs/data-provenance.json`.
- Econometrics -> Storytelling/API: `docs/model-specification.md`, `docs/metric-registry.md`.
- Storytelling -> Frontend/UX: `docs/content-map.md`.
- Architect -> Backend/Frontend: `docs/api-contract.md`, `docs/architecture.md`.
- Frontend+Backend -> UX/Reader/QA: app local, comandos, pruebas y screenshots.

Cada archivo identifica autor, fecha, estado (draft/verified/blocked), dependencias y decisión. Al fallar un contrato, no parchear UI para ocultarlo: resolver desde el productor y repetir pruebas.
