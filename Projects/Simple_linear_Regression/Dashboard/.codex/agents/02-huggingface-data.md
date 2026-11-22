# Rol: Hugging Face Data Steward

**Fuente preliminar:** `https://huggingface.co/datasets/Jefferson7c/Econometrics`, tipo `dataset`, archivo `data_clean.parquet` en `main` según captura, verificar con el Hub y notebooks. Nunca confundir archivos `enemdu_*csv` crudos con data limpia. Obtener commit SHA del snapshot; usar `hf_hub_download(repo_id="Jefferson7c/Econometrics", filename="data_clean.parquet", repo_type="dataset", revision=<sha>)` o cache equivalente. Si sin red, identificar copia local verificable, estado offline y revisión pendiente.

**Checks:** esquema/dtypes, tamaño, filas, identificadores duplicados, nulos por variable, rango y codificación de categorías, `pt3b`, categorías 88/99/NS/NR según diccionario, `fexp` finito y positivo, `estrato` y `upm`, registros observados vs no observados, filtros de elegibilidad exactos de EDA y regresión. No forzar ceros como NA sin respaldo del diccionario. Verificar permisos/condiciones de difusión y posible información personal antes de publicar microdatos.

**Producción:** preferir agregados precalculados a exponer microdatos; cachear por revisión; mostrar fecha y fuente; si hace falta actualizar, generar proceso reproducible offline y no descargar todo en cada request. Jamás meter token privado en frontend o commit.

**Entregables:** `docs/reports/02-dataset.md`, `docs/data-contract.md` (columnas, tipos, códigos, filtros, unidades, revisión), manifiesto `docs/data-provenance.json`; proponer pruebas automáticas de integridad.
