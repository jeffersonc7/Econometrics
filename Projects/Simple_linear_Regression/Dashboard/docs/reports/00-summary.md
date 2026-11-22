# Entrega local · Dashboard de econometría
Autor: orquestador. Fecha: 2026-11-16. Estado: implementado y validado localmente; sin publicación.

Se coordinó auditoría/custodia de datos, econometría, frontend/comunicación, lector/UX y QA/backend. Los especialistas revisaron el trabajo de los demás y se corrigieron hallazgos reales antes de la entrega. Instrucciones originales en `.codex/`; implementación y documentación bajo Dashboard. DataScience no fue modificado.

## Aplicación
React/TypeScript/Vite con estética Cristal a partir de las capturas, sin clon Bar Project accesible. Dos secciones: exploración cotidiana y regresión técnica. Claro/oscuro persistente, móvil primero, gráficas con tablas alternativas, comparación de tramos, escenario de diferencias de una a tres horas y fuentes trazables. Sin autenticación ni endpoints de escritura.

Pipeline Python reproduce notebooks con revisión HF fijada y hashes estrictos. Publica JSON de 8,8 KB; servidor stdlib opcional ofrece API/build en un origen. Hosting estático también soportado sin backend remoto. No microdatos en build, no HF por visita.

## Evidencia
Cuatro notebooks auditados y limpieza completa de 19 columnas replicada. Fuente HF `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`, Parquet idéntico al local. Selección: 27.509 → 13.299 → 10.091 → 9.881. Modelo real MCO sin ponderar con EE agrupados en 1.286 UPM y t. Pendiente 61,3563899864 USD/mes por hora; IC 95 % [54,0050; 68,7078]. Resultado asociativo, sin identificación causal. Revisión independiente: 66 comparaciones numéricas PASS.

Doce pruebas Python PASS, TypeScript/build PASS y catorce pruebas Chromium PASS (incluida accesibilidad Axe); detalles finales en 10-qa.md. Capturas en `docs/evidence`. Revisión de lector simulada en dos rondas, no investigación con participantes humanos.

## Uso
Desde la raíz del proyecto: `python3 Dashboard/backend/server.py` y abrir http://127.0.0.1:8000 (build ya generado). Para reconstruir, fuentes, dependencias y pruebas, ver `Dashboard/README.md`. El servidor no queda iniciado por la suite de pruebas; iniciar con el comando anterior.

## Límites y pendientes explícitos
No se hizo push, merge ni despliegue. Publicación requiere autorización. El ODS no incluye catálogo exhaustivo de códigos especiales; se reproduce la limpieza existente, con advertencia. No se simula inferencia de encuesta completa. Safari/Firefox, lector de pantalla real y evaluación con usuarios no ejecutados. La reconstrucción visual deriva de imágenes, no del código original de Bar Project.
