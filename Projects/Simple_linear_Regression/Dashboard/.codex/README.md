# Dashboard Econometrics — paquete de agentes

**Qué es:** instrucciones para orquestar agentes en VS Code/Codex/Claude Code; **no es el dashboard terminado**. Los archivos Markdown son reutilizables entre herramientas. No dependen de que una plataforma admita subagentes automáticos: si no los admite, el coordinador ejecuta cada rol secuencialmente.

## Instalación

1. Copia **el contenido** de esta carpeta en `Simple_Linear_Regression/Dashboard/` (adapta solo si tu nombre real es diferente). No lo copies encima de `Data-Science`.
2. Abre `Simple_Linear_Regression` en VS Code para que el agente tenga permiso de lectura sobre **ambas carpetas**.
3. Inicia tu agente en VS Code con el prompt de `START_HERE.md`. Para Codex, `Dashboard/AGENTS.md` proporciona las reglas locales; si abres la raíz, usa además el prompt de inicio o copia esas reglas en la configuración del agente.
4. Si existe un clon **local** del proyecto Bar-Project, proporciona su ruta al agente. Si no, las imágenes `reference/cristal-*.png` son el respaldo visual. El paquete no ha inspeccionado ese clon local.
5. Revisa los informes de auditoría antes de aceptar la implementación. Los agentes no deben alterar los notebooks originales.

## Organización esperada (flexible)

```text
Simple_Linear_Regression/
├── Data-Science/             # FUENTE: datos tratados, notebooks, análisis, modelo
└── Dashboard/
    ├── AGENTS.md             # reglas de trabajo para todos los agentes
    ├── START_HERE.md         # prompt maestro
    ├── agents/               # roles y contratos entre agentes
    ├── skills/               # procedimientos compartidos
    ├── docs/                 # contratos y checklist
    ├── reference/            # capturas de estilo
    ├── frontend/             # A CREAR POR LOS AGENTES
    └── backend/              # A CREAR POR LOS AGENTES
```

## Roles

1. `00-orchestrator.md`: orquestación y dependencias.
2. `01-repository-auditor.md`: auditoría del proyecto Data Science y Bar-Project.
3. `02-huggingface-data.md`: fuente, licencia, versionado y validación de datos.
4. `03-econometrics.md`: rigor estadístico, ponderaciones, inferencia y causalidad.
5. `04-research-storytelling.md`: hallazgos, comunicación y contenido en español.
6. `05-stack-architect.md`: arquitectura, dependencias y despliegue.
7. `06-backend.md`: API, cálculo reproducible y pruebas.
8. `07-frontend.md`: diseño Cristal, interfaz, gráficas y accesibilidad.
9. `08-ux.md`: experiencia móvil, estados y usabilidad.
10. `09-naive-reader.md`: lector sin econometría, crítico de valor informativo.
11. `10-quality-deploy.md`: QA integrado, seguridad, rendimiento y publicación.

**Importante:** todos son archivos de instrucciones, no servicios que se ejecutan solos. El agente coordinador debe invocarlos mediante los mecanismos disponibles o adoptar sus roles de forma secuencial. No publicar ni fusionar a main sin que el usuario lo autorice expresamente.

## Fuente de datos prevista

Repositorio: `https://huggingface.co/datasets/Jefferson7c/Econometrics`.
Archivo indicado: `data_clean.parquet` de la rama `main` (comprobar presencia, esquema y revisión exacta antes de usar). No confundir con CSV crudos ni con diccionarios ODS. Reutilizar resultados de `Data-Science` cuando sean trazables. La disponibilidad pública no implica por sí sola permiso ilimitado de redistribución de microdatos: revisar condiciones, confidencialidad y contenido.

## Decisiones preestablecidas

- Dashboard **sin inicio de sesión**, solo lectura, en español, responsive/mobile-first, con tema claro/oscuro y preferencia del sistema.
- Dos áreas: **Explorar los datos** para cualquier persona y **Modelo de regresión** para audiencia técnica.
- No inventar variable dependiente, regresores, muestra, coeficientes, significancias ni causalidad: inferirlos únicamente de notebooks/scripts/resultados reproducibles.
- No copiar funcionalidades de la aplicación financiera de referencia (caja, banco, registrar); copiar solo lenguaje visual, jerarquía, composición y tema.
- Preferir una solución frontend React/TypeScript + Vite y backend Python/FastAPI si el inventario la respalda. No imponerla antes del diagnóstico. Opcionalmente desplegar frontend en Vercel/Netlify y API en Render/Fly.io o un único servicio si reduce complejidad. Verificar condiciones actuales y plan gratuito antes de adoptar.
