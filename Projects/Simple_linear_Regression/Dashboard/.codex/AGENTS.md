# REGLAS PARA LOS AGENTES — Dashboard

## Contexto
Trabajas dentro de `Simple_Linear_Regression/Dashboard`, proyecto hermano de `../Data-Science` (también puede llamarse `../Data Science`; detectar nombre real). `Data-Science` es fuente de verdad: notebooks, modelo, EDA, datos y explicaciones. Tu tarea es **construir** un dashboard web de solo lectura; estos archivos solo coordinan la construcción.

## Instrucción principal
LEE primero `START_HERE.md`, `agents/00-orchestrator.md`, `docs/definition-of-done.md`, las referencias visuales, y **audita** `../Data-Science` antes de escribir código de aplicación. No preguntes datos que puedas localizar en el repositorio. No finjas haber ejecutado código o consultado rutas inaccesibles.

## Límites innegociables
- **No editar** archivos fuente ni notebooks dentro de `../Data-Science` sin aprobación explícita. Leer, extraer, ejecutar de forma controlada y producir copias/artefactos derivados bajo `Dashboard`.
- Todo texto visible al usuario final **en español**, incluidos títulos, tooltips, leyendas, mensajes de error, fechas y unidades (los identificadores de código pueden seguir en inglés).
- Sin login, formulario de registro, perfiles, endpoints de escritura ni panel de administrador.
- Mantener trazabilidad de todo número mostrado: archivo/ruta, columna, filtro, denominador, peso, notebook/celda o cálculo reproducible, commit/revisión de dataset.
- Nunca escribir «efecto causal» como hecho demostrado solo por OLS; presentar resultado como asociación condicional si no hay identificación defendible. Discutir endogeneidad y supuestos.
- `fexp` es peso de expansión y `estrato`/`upm` son identificadores del diseño: validar si existen y determinar uso correcto, no inventar inferencia robusta al diseño si la implementación no la hace.
- Optimizar móvil primero, verificar 360–430 px, tablet y desktop; accesibilidad WCAG práctica y reduced-motion.
- Tema claro/oscuro y cambio manual persistente; por defecto preferencia del sistema.
- No datos simulados en producción, salvo modo demo claramente etiquetado que se mantenga fuera del despliegue final.
- No ejecutar comandos destructivos (`git reset --hard`, borrado de carpetas) sin autorización. No desplegar públicamente ni hacer push/merge sin autorización.

## Flujo
1. Agente de auditoría: inventario real, estructura, hallazgos, variables y fuentes.
2. Hugging Face + econometría: comprobar dataset, columnas, filtros, replicación y solidez.
3. Comunicador + lector no técnico: definir mensaje, métricas, exclusiones y explicaciones.
4. Arquitecto: elegir stack y contratos de frontend/backend.
5. Backend y frontend: implementar en paralelo **solo después** de acordar contrato.
6. UX + lector crítico + QA: iterar hasta pasar checklist y pruebas.

## Comunicaciones y entregables
- Toda decisión y bloqueo se anota en `docs/decision-log.md` (crear).
- Cada número usado se registra en `docs/metric-registry.md` (crear).
- Reportes individuales en `docs/reports/<rol>.md` con: hallazgos, evidencia, decisiones, archivos creados, pruebas y riesgos.
- Agentes deben compartir archivos/contratos, no asumir memoria común.
- Si los análisis en notebooks contradicen los datos, detener visualización de ese resultado y documentar discrepancia.
