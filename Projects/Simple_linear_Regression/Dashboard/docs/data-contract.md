# Contrato de datos v1

Autor: agente custodio de datos · Fecha: 2026-11-16 · Estado: verificado.
Dependencias: auditoría y snapshot HF d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698; ver `data-provenance.json`.

## Entrada

`DataScience/data/processed/data_clean.parquet` (solo lectura), equivalente al `Dashboard/data/source/data_clean.parquet` fijado. 27.509 filas, 19 columnas. CSV auxiliar `Dashboard/data/source/enemdu_persona_tics_2025_07.csv`,27.509 filas×171 columnas.

| Columna | Tipo limpio / auxiliar | Definición y uso |
|---|---|---|
| id_persona, id_hogar, id_vivienda | string | Identificadores; nunca cliente/público |
| ciudad, area, conglomerado, panelm, vivienda, hogar, p01 | string | Metadatos; área1 urbana/2 rural en contexto ENEMDU; no publicar niveles identificables |
| periodo | string | Único202507; clave unión |
| fexp | Float64 no NA | Factor expansión finito>0. Solo descriptivos ponderados explícitos; no OLS ponderado |
| estrato | string no NA | Estrato de diseño; modelo original no incorpora estratificación |
| upm | string no NA | Agrupación para covarianza cluster; no exponer identificadores |
| pt3b | Int64 nullable | Horas según frecuencia;0=menos de una hora;888 y blanco convertidos en NA |
| ingrl | Float64 nullable | Ingreso laboral mensual USD; blanco,-1,999999→NA; ceros conservados |
| internet_hours_status | str | Observed / Not applicable / Potentially out of scope / Nonresponse; traducciones visibles en español |
| labor_income_status | str | Observed y siete motivos no observados; ver informe02 |
| ingrl_original | str | Respuesta original conservada para auditoría; nunca pública |
| p03 (CSV) | int64 | Edad años; elegibilidad≥15 |
| empleo (CSV) | string normalizado | Código1=ocupado según notebook/diccionario |
| pt3a (CSV) | string normalizado | Frecuencia;1 diaria,2 semanal,3 mensual,4 anual; filtro1 |

## Limpieza y selección exactas

No volver a limpiar ceros. Normalizar auxiliares id_persona/periodo/empleo/pt3a a string y `.str.strip()`; unir por id_persona+periodo `validate='one_to_one'`; afirmar correspondencia de todas las filas. Se exige periodo202507.

1. Base limpia N27.509.
2. `empleo == '1' & p03 >= 15`: N13.299.
3. `dropna(subset=['pt3b','ingrl'])`: N10.091.
4. `pt3a == '1'`: N9.881.

Muestra final: 118 códigos horarios0;119 ingresos0;1.286UPM,150estratos,6.448hogares. No mezclar frecuencias para llamar al eje «horas diarias». Descriptivos/OLS sin ponderar por defecto. Si se muestra media ponderada, usar np.average con fexp y etiquetar que solo describe dominio con respuesta; no intervalos de encuesta.

Filtros admitidos: toda muestra/área urbana/área rural, siempre mantienen elegibilidad y N visibles. Cualquier filtro exploratorio debe indicar que no reestima automáticamente el modelo global. Tramos de horas del EDA: (-1,1],(1,3],(3,5],(5,8],(8,∞), etiquetas0–1,2–3,4–5,6–8,9o más. No inferir causalidad.

## Salida pública

Solo JSON de agregados y resultados; sin IDs, registros, respuestas originales ni enlaces de descarga de microdatos. Cada bloque incluye fuente, revisión, filtro, unidad, N y ponderación. El pipeline debe fallar ante hash/esquema/modelo discrepante. El cliente nunca descarga desde HF durante navegación.
