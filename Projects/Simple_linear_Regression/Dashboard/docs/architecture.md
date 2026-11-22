# Arquitectura
Autor: orquestador. Fecha: 2026-11-16. Estado: verificado por inventario.

React/TypeScript + Vite para interfaz; CSS con tokens derivados visualmente de las capturas Cristal (no tokens del Bar Project). SVG/HTML accesible para gráficas simples, sin librería gráfica adicional. Pipeline Python pandas/pyarrow/statsmodels reproduce notebooks y publica solo agregados JSON. Un servidor Python de biblioteca estándar permite API de lectura y servir el build; el mismo build funciona en hosting estático sin API. Se evita descargar o estimar en cada petición.

Flujo: parquet limpio local + CSV auxiliar fijado -> validaciones + selección fiel al EDA -> MCO agrupado UPM -> JSON público -> React. La revisión y ambos SHA256 viajan con el artefacto. Fuente inmutable recuperable de Hugging Face, sin credenciales privadas. No microdatos, autenticación ni escrituras HTTP.

Ver api-contract.md para tipos. Pipeline y servidor en backend, app en frontend. Pruebas Python de integridad/contrato/rutas, TypeScript/build y navegador para integración y accesibilidad. No se registra ni publica un Site en esta fase: trabajo local por instrucción expresa del usuario.
