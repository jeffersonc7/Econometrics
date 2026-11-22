# Aceptación local
Autor: orquestador / QA. Fecha: 2026-11-16.

- [x] Cuatro notebooks, scripts, entorno y datos auditados, sin editar DataScience.
- [x] HF público verificado, revisión inmutable, hashes y coincidencia local/remoto.
- [x] Limpieza de las 19 columnas reproducida; selección y resultados verificados.
- [x] Variables, población, periodo, filtros, pesos, unidades y procedencia documentados.
- [x] MCO real, EE por UPM, t, p, IC, SER, R², supuestos y sensibilidad reproducidos.
- [x] Descriptivos sin ponderar y medias ponderadas explícitas; limitaciones causales visibles.
- [x] Dos vistas en español, sin login ni escritura, con interacción real y estados de carga/error/vacío.
- [x] Capturas Cristal usadas; temas persistentes claro/oscuro y reduced-motion.
- [x] Navegación/overflow comprobados en Chromium a 360, 375, 390, 430, 768, 1024 y 1440 px.
- [x] Teclado, enlace de salto, tablas alternativas y comprobación Axe en ambas vistas/temas.
- [x] Contrato versionado y agregados sin microdatos en bundle; API sólo lectura.
- [x] Doce pruebas Python PASS; typecheck y build PASS; suite navegador documentada en 10-qa.md.
- [x] Guía local y opciones de publicación preparadas, sin publicación.

Limitaciones registradas: catálogo oficial incompleto para ciertos códigos especiales; MIT declarada en HF no se interpreta como permiso ilimitado sobre microdatos. No hubo entrevistas con usuarios, ensayo con lector de pantalla real ni validación en Safari/Firefox. Zoom se comprobó por viewport equivalente, no con el menú de zoom de un navegador de escritorio. La inferencia no reproduce el diseño complejo completo y no identifica efectos causales.

Las reglas originales de aceptación se conservan en `.codex/docs/definition-of-done.md`.
