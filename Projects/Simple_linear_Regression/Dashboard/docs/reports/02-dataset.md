# Verificación de Hugging Face

Autor: agente auditor / custodio de datos · Fecha: 2026-11-16 · Estado: verificado con limitaciones de metadatos.

## Acceso y versión

API consultada: https://huggingface.co/api/datasets/Jefferson7c/Econometrics
Repositorio público, sin acceso restringido. Revisión fijada: `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`; última modificación reportada: `2026-11-16T15:06:47.000Z`.

El acceso web al Hub falló; `curl` inicialmente no resolvía DNS en sandbox. Tras escalación aprobada se consultó la API y se descargó la revisión exacta bajo `Dashboard/data/source/`. No se usaron credenciales.

| Archivo | Bytes | SHA256 |
|---|---:|---|
| data_clean.parquet | 533.387 | `8c59cf438743d06e2e1da2f00ae83575a159a353eb33e829259992115fa3e1a7` |
| enemdu_persona_tics_2025_07.csv | 12.789.333 | `a7071161a63c18cdbb4b6c48e06103c357baf06b961df47259c1d9959dc689ff` |
| persona_dictionary.ods (nombre local) | 8.157 | `f921b47ed02dd8467a7ef169df59580d2735ff8d443c29a488282948e3570e7a` |
| HF_README.md (nombre local) | 21 | `3e0e15fa0c5cc81675bd69af8eb469d128a725c1a7bfc71f03b7877b7b650567` |

El Parquet es idéntico byte a byte al local de DataScience y `DataFrame.equals=True`. El CSV aporta columnas de elegibilidad ausentes del Parquet; unión uno a uno completa de 27.509 personas/periodo.

## Integridad

27.509 filas, 19 columnas, periodo único 202507. Sin IDs persona-periodo duplicados. Identificadores y diseño sin NA. `fexp` finito y positivo: mínimo 8,8151826012, máximo 13.782,831008735. UPM de muestra final=1.286; estratos=150; hogares=6.448. Cada UPM final pertenece a un solo estrato.

`pt3b`: 6.337 NA y 21.172 valores numéricos entre 0 y 18. Estados: observado21.172, no aplicable3.279, vacío por investigar1.803, sin respuesta1.255.

`ingrl`: 15.603 NA, 11.906 observados entre 0 y17.000. Estados no observados: inactivo8.016; menor15=5.607; trabajo principal sin remuneración1.233; desempleo abierto517; oculto62; gastos mayores a ingresos129; no respuesta39. Los157 ceros del limpio se conservan (119 en muestra final).

Se reprodujo en memoria el notebook de limpieza con el interim local y CSV fijado: coincide exactamente con las19 columnas del limpio. La selección diaria reproduce N9.881, media ingreso570,186823196, mediana474, horas medias3,358060925 y mediana3. Frecuencias entre completos: diaria9.881, semanal194, mensual14, anual2. Filtro área de muestra diaria: código1=7.691, código2=2.190.

## Diccionario, formulario y límites

ODS verificado: INEC_PDA_2025, documento INEC_DIES_ENEMDU_2025_JUL, descripciones de variables. No incluye tabla detallada de todos los códigos especiales. Transformaciones `pt3b`888→NA e `ingrl`-1/999999→NA se reproducen de limpieza; su interpretación específica queda documentada como procedente de los notebooks, no como certificada por el ODS.

[Formulario oficial INEC](https://www.ecuadorencifras.gob.ec/documentos/web-inec/Estadisticas_Sociales/TIC/2025/202507_Formulario_ENEMDU_Julio_2025.pdf) consultado en web: página PDF23, preguntas3A/3B, confirma que las horas dependen de frecuencia y00 significa menos de una hora; páginas18/19, preguntas de ingresos, hacen referencia a junio. Esto respalda las unidades y el desfase temporal.

La etiqueta `Potentially out of scope` no confirma que todos sean menores de cinco: 367 de1.803 tienen≥5; conservar nombre «Vacío por investigar».

## Licencia y publicación

La tarjeta HF declara MIT y su README solo contiene `license: mit`. Esto acredita la declaración del repositorio, no un análisis independiente de todos los derechos del INEC ni permisos ilimitados de redistribución de identificadores. El formulario INEC declara confidencialidad y uso estadístico. Decisión concreta: la aplicación sirve únicamente agregados y resultados; jamás incluye IDs, filas de microdatos, CSV, ODS ni Parquet en la carpeta pública. Snapshot privado de trabajo bajo `data/source/`, excluido de Git y build.

## Pruebas recomendadas

Verificar hashes fijados, esquema/revisión, unicidad y cobertura del merge, periodo, pesos, códigos especiales ausentes en columnas numéricas, suma de histogramas=N, tamaños de filtros y réplica de coeficientes/EE/IC. Ante discrepancia, fallar pipeline en vez de mostrar outputs guardados como actuales.
