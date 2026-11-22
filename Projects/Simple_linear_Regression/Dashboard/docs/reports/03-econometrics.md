# Revisión econométrica

Autor: 03-econometrics. Fecha: 2026-11-16. Estado: VERIFIED reproducción; WARN alcance inferencial. Documentos: `model-specification.md`, `metric-registry.md`. No se modificó ni ejecutó notebook original; cálculos en proceso Python de solo lectura con `PYTHONDONTWRITEBYTECODE=1`.

## Evidencia y resultados

Se inspeccionaron código, markdown y salidas de los cuatro notebooks. La fuente de diseño es `03. EDA.ipynb` y `04. SLR.ipynb`; inspección/limpieza documentan los especiales y faltantes. Se replicó unión uno a uno del Parquet local con CSV en caché HF del snapshot `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`. Mismos N, descriptivos, coeficientes, EE, IC, p, R², SER, regresión de varianza y sensibilidad Cook que las salidas guardadas. Ninguna discrepancia numérica material.

Entorno observado: Python3.12, pandas3.1.1, numpy2.5.5, statsmodels0.15.0. La fórmula exacta está en `model-specification.md`. No se supuso HC ni errores convencionales: se respetó `cov_type='cluster'`, UPM y `use_t=True` con df inferencial1285.

## Matriz crítica

No se encontró un enunciado externo del profesor; se evalúan los requisitos académicos listados por el paquete de agentes, sin inventar una rúbrica original.

| Punto | Estado | Evidencia / decisión |
|---|---|---|
| Pregunta y población | PASS/WARN | Asociación internet-ingreso; restringir al dominio observado, no todos los ocupados |
| Unidad y tiempo | PASS | Persona; encuesta julio2025, ingreso junio; horas según frecuencia en últimos12meses |
| Y/X y ecuaciones | PASS | SLR2/3/10; pt3b diaria e ingrl niveles; constante |
| Selección y missingness | PASS/WARN | EDA4, limpieza21/31; ceros conservados; pérdida por empleo no remunerado/norespuesta/códigos debe explicitarse |
| Linealidad en parámetros | PASS | Constante y una X; no implica forma funcional correcta |
| Variación y colinealidad | PASS | VarX4,702751>0 y rango diseño2 |
| Media condicional cero | WARN | No identificada; edad/educación/ocupación/habilidades omitidas, simultaneidad y causalidad inversa posibles |
| Muestreo e i.i.d. | WARN | Diseño de conglomerados;1286UPM/150estratos/6448hogares; independencia entreUPM es supuesto |
| EE y significancia | PASS/WARN | CRV1 UPM; t1285; no incorpora estratificación ni ponderación; p no prueba causalidad |
| Homocedasticidad | WARN | Auxiliar residual²~X, p0,00596881; presentar prueba como tendencia lineal |
| Influencia | WARN |376 Cook>4/N; pendiente cambia61,36->49,76; no borrar automáticamente |
| Normalidad y momentos | WARN | Cola de ingreso; normalidad residual no requerida para identificación; momentos finitos no verificables |
| Relevancia sustantiva | PASS | Coeficiente USD61,36/mes/h, SER568,79, R²5,19%; no prometer rendimiento de conectividad |
| Inferencia causal | BLOCKED para afirmación causal | No hay instrumento, experimento, panel ni identificación defendida; producción solo «asociación» |
| Diseño completo encuesta | BLOCKED para inferencia de diseño | No hay estimador que use simultáneamente fexp/estrato/upm; no etiquetarlo así |
| Códigos especiales | WARN | ODS cache confirma nombres; formulario confirma0horas<1 y temporalidad. -1/999999 heredados de limpieza, sin tabla oficial de codificación localizada |

## Decisiones para la interfaz

- Modelo fijo verificado; filtros exploratorios no cambian coeficientes.
- Diferencia por3h y su IC deben llamarse asociación de la recta; nunca recomendación de «horas óptimas».
- Intercepto para X0 está en dominio pero representa código<1h, no «sin acceso».
- EDA sin ponderar por defecto. Si se muestra comparación con fexp, rotular pesos descriptivos y evitar IC de encuesta inventados.
- No mostrar registros individuales de casos extremos; Cook y dispersión se publican como agregados.
- No afirmar efectos «ceteris paribus controlando otros factores»: modelo no contiene controles.

## Validación ejecutada

Lectura Parquet/CSV, merge validate one_to_one, secuencia de selección (27509/13299/10091/9881), estimación statsmodels, IC/p, conteo grupos, pesos positivos (rango8,81518–13782,83101;0faltantes), unicidad UPM->estrato, correlaciones, mediana/media/cuantiles, tramos y sensibilidad. Resultado: todos coinciden con el redondeo fuente. Se verificaron formulario INEC y documentación primaria de statsmodels; enlaces en especificación.

## Pendientes de revisión final

Revisar en UI: unidades/temporalidad visibles, denominadores de filtros, tabla técnica completa, etiqueta EEUPM y diseño incompleto, p bilateral/IC95, accesibilidad de tabla, cautela causal y ausencia de microdatos. Este informe no sustituye esa revisión posterior.

## Revisión cruzada de backend (segunda ronda)

Se inspeccionó `backend/pipeline.py` y el JSON generado por otro agente/orquestador. PASS: filtros exactos, unión verificable, hashes/versionado fijos, MCO sin pesos/EEUPM, correspondencia del CSV, preservación de ceros/cola, totales, tramos y sensibilidad. Se ejecutó además una réplica independiente contra el Parquet original de DataScience: 66 comprobaciones de valores/series (coeficientes, EE, t, p, IC, selección, centros, conteos de horas/ingreso, tramos, R² y SER), tolerancia relativa1e-12: PASS.

Decisiones agregadas al registro: barras de ingreso con intervalos desiguales se interpretan como categorías de personas, no densidades; disponibilidad reducida conserva13.299 como denominador; residual_spread conserva n>=30 y unidadUSD; fitted es la recta de modelo, no observaciones. No se requirieron cambios numéricos al backend. Revisión UI aún pendiente.

## Revisión cruzada de frontend (contenido del código)

Se leyó `frontend/src/App.tsx` completo tras implementación del agente frontend. PASS: títulos/alcance del dominio, temporalidad junio/julio, mediana/promedio, horas0<1, bins USD sin densidad engañosa, N por tramo, selector limitado a tarjeta, disponibilidad entre ocupados, MCO fijo sin ponderar, tabla completa de coeficientes/EE/IC/t/p, df1285, SER distinto deEE, Cook diagnóstico sin eliminar de principal, varianza auxiliar correctamente nombrada y límites causales explícitos. La interpretación no finge controles ausentes ni inferencia de encuesta completa. Se usa recta agregada y no microdatos.

Incidencia menor enviada al frontend: pie genérico «sin ponderar» junto a «Pearson ponderado» en tarjeta metodológica puede confundirse; especificar etiquetas de peso distintas en ese pie. Recomendación editorial opcional: explicitar fórmula del residuo junto a ecuaciones. Esta revisión es del código y contenido, no sustituye comprobación visual/navegador de QA/UX.
