# Auditoría del repositorio

Autor: agente auditor · Fecha: 2026-11-16 · Estado: verificado con advertencias.
Dependencias: instrucciones de `Dashboard/.codex`, archivos leídos sin modificar.

La carpeta real se llama `DataScience`. El paquete de coordinación está en `Dashboard/.codex/` (no directamente en `Dashboard/`). No había implementación de aplicación al comenzar.

## Inventario

| Archivo | Contenido / ejecución persistida | Uso |
|---|---|---|
| `DataScience/notebooks/01. data_inspection.ipynb` | 18 celdas; 13 de código; celda 16 sin ejecución, 17 sí ejecutada | CSV original de personas (27.509 × 171), vivienda/hogar (8.607 × 69), diccionarios ODS; selecciona 16 columnas |
| `DataScience/notebooks/02. data_cleaning.ipynb` | 37 celdas; 25 de código; exportación celda 36 sin ejecución | Importa `data_inspection.parquet` desde rama HF `data-inspection`; limpia códigos, conserva estados y respuestas originales |
| `DataScience/notebooks/03. EDA.ipynb` | 24 celdas; 10 de código, todas ejecutadas | Selección de muestra, distribuciones, relación por tramos, pesos/correlaciones y sensibilidad |
| `DataScience/notebooks/04. SLR.ipynb` | 29 celdas; 13 de código, todas ejecutadas | Regresión simple en niveles; errores estándar agrupados por UPM, influencia y sensibilidad |
| `DataScience/src/data_loader.py` | `load_data` admite CSV, Parquet y ODS; descarga HF con revisión `main` por defecto | Fuente remota no fijada en los notebooks |
| `DataScience/src/slr_plots.py` | `plot_fit`, `plot_residuals`, `plot_influence` | Gráficos del modelo; no ejecutados durante peticiones HTTP |
| `DataScience/data/interim/data_inspection.parquet` | 27.509 × 16, 497.789 bytes | Copia local de etapa de inspección |
| `DataScience/data/processed/data_clean.parquet` | 27.509 × 19, 533.387 bytes | Fuente limpia local, idéntica al snapshot HF verificado |
| `DataScience/pyproject.toml` | pandas, huggingface_hub, pyarrow, odfpy, numpy, matplotlib, seaborn, scipy, statsmodels | Entorno Python existente `.venv`, leído para verificaciones |
| `DataScience/scripts/` | Vacía en la inspección | Sin pipeline adicional |
| `DataScience/econometrics_analysis.egg-info/`, `src/__pycache__/` | Metadatos de instalación y cachés existentes | No fuente analítica; sin modificaciones |

## Pregunta y muestra reales

Horas de uso de internet e ingreso laboral de ocupados de 15 años o más, Ecuador, ENEMDU TIC julio de 2025. Los ingresos corresponden a junio de 2025. `pt3b` debe condicionarse a frecuencia `pt3a=1` para obtener referencia diaria; cero significa menos de una hora, no ausencia de uso.

Merge uno a uno por `id_persona` y `periodo` entre limpio y CSV original; se recuperan `p03`, `empleo`, `pt3a`. Etapas reproducidas: 27.509 base → 13.299 ocupados ≥15 → 10.091 con horas/ingreso → 9.881 con uso diario. Se conservan 119 ingresos cero y 118 códigos de horas cero. Números de celdas en este informe y source-map usan índice base cero.

## Evidencia verificada

- Parquet local y HF tienen el mismo SHA256 y `DataFrame.equals=True`.
- Se ejecutaron en memoria todas las celdas de código de limpieza excepto exportación; se sustituyó únicamente el cargador por archivos locales verificados y se silenció `display`. Las 19 columnas resultantes son iguales al Parquet local, incluidos dtypes y estados. No se ejecutaron escrituras del notebook.
- Se reprodujeron selección y descriptivos con el CSV remoto fijado: coinciden con salidas guardadas del EDA.
- Modelo persistido: intercepto 364,148; pendiente 61,356; EE UPM pendiente 3,747; IC95% [54,005;68,708]; N=9.881; R²=0,0519. Su reproducción/validación inferencial corresponde al agente econometría.
- La exportación de limpieza sin contador de ejecución es una limitación de procedencia del notebook, resuelta para la app mediante coincidencia material y reproducción, no asumiendo una ejecución guardada inexistente.

## Riesgos / decisiones

No mostrar `Potentially out of scope` como exclusivamente menores de cinco: de 1.803 filas hay 1.436 menores de cinco y 367 de cinco o más (máximo 91). Mantener «Vacío por investigar». No convertir ingresos faltantes a cero. No inferir causalidad ni representatividad de toda la población a partir de esta selección.

Archivos de handoff: `../source-map.md`, `../data-contract.md`, `../data-provenance.json`, `02-dataset.md`. No se modificó ningún archivo de `DataScience`.
