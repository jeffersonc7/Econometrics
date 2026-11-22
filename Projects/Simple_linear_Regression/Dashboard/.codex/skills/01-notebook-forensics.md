# Skill: Notebook Forensics

1. Listar notebooks, scripts y dependencias sin alterarlos.
2. Extraer título, objetivo, origen de datos, celdas de limpieza, filtros, variables/modelo y resultados.
3. Verificar si outputs guardados son coherentes con el código y el dataset. Nunca tratar outputs obsoletos como evidencia final.
4. Ejecutar solo copias o procesos seguros, documentar entorno y semilla.
5. Crear tabla ruta/celda -> cálculo -> resultado -> evidencia -> elemento UI en `docs/source-map.md`.
6. Si no se reproduce, etiquetar `NO VERIFICADO`, ocultar el indicador de producción y crear incidencia.
