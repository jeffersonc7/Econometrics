# V2 · ampliación estadística y revisión técnica

Autor: 03-econometrics. Fecha: 2026-11-16. Estado: VERIFIED cálculo/contrato; revisión visual final coordinada por UX/QA. Cambios limitados a pipeline/contrato/tests/agregados/documentación autorizados; DataScience solo lectura. Fuentes inmutables y N=9.881 se mantienen. Contrato aditivo en `api-contract.md`, trazabilidad completa en `metric-registry.md`.

## Implementación y resultados

Se añadieron funciones separadas de agregación exploratoria y diagnóstico, preservando cada clave/valor científico v1. No se descargaron paquetes, no se reestimó otro modelo como principal y no se publican observaciones/residuos individuales. JSON≈174KB con formato (≈97KB compacto).

- Concentración ingreso/horas:190celdas,19horas×10intervalosUSD fijados. Suma9.881, incluso cola17.000 y cero. Colores deben decir personas/celda, no densidad por unidad de área.
- Cajas:cuartiles y bigotesP10/P90 por mismos5tramosEDA, conN/media. No son bigotesTukey. Se retienen todos los ingresos al calcularlos.
- CDF:101umbrales a percentiles0..100 y fracción empírica<=umbral, incluidos empates. En0USDshare119/9881; en17.000share1. La curva es un resumen de ECDF, no cada salto original.
- Banda puntual de media:181puntos0..18paso0,1;covarianzaCRV1 UPM,df1285,tcrítico1,9618118205524. Se usa varianza de[1,x], sin añadirSER². No es banda simultánea ni predicción individual.
- Residuos:28intervalos uniformes de−1184,494177USD a16145,000553USD, histogramayrejilla19×28. Ambos conservanN y extremos, aunque la cola comprime visualmente el centro.
- QQ:99cuantiles deû/SER enp1..99%, comparados con normalestándar. Se excluyenprobabilidades0/1 y no se transmite cada residuo ordenado. No se studentiza por leverage.
- EEcomparados:mismo coeficiente61,35638999;convencionalEE2,63872986,HC3EE3,27870238,UPMEE3,74723525. Los dosprimeros usan t9879;UPMt1285. El principal conservaUPM. HC3 resiste heterocedasticidad, no correlación internaUPM.
- Cook:28bins logarítmicos,min2,66958e−16,max0,2278539035,sum9881. No se borran casos ni se cambia regla diagnóstica4/n.
- CovarianzaUPM const/horas:[[128,86049237,−33,16018775],[−33,16018775,14,04177200]]. Diagonal coincide conEE² y se usa para cualquier intervalo de nivel.
- RMSE568,72908895USD;MAE313,13566833USD;R²aj0,05179309946. SSE3196036885,7198;SST3370952481,1244;SSRexplicada174915595,4046. SER568,78665553 usa n−2,RMSEusan. Son errores dentro de muestra.
- Mediaresiduo≈0 porconstante;asimetría7,87760399 ycurtosisPearson147,61907677(normal3) evidencian cola derecha larga. Son momentos muestrales corregidos, no prueba de momentos poblacionales.

## Interpretaciones técnicas cortas para UI

| Diagnóstico | Texto sugerido |
|---|---|
| Recta y banda | La franja mide incertidumbre puntual de la media lineal, con EE agrupados por UPM. No contiene el ingreso de una persona. |
| Dispersión residual | Las diferencias observación−recta cambian entre horas y muestran cola positiva larga. El agrupamiento corrige parte de la incertidumbre, no el sesgo. |
| Histograma residual | La mayoría de errores está cerca del centro, pero unos pocos positivos son grandes. No se recortó la cola. |
| QQ | Los cuantiles se apartan de la normal, especialmente en la cola alta. Esto no demuestra ni refuta exogeneidad. |
| Media residual | Que los residuos promedien cero es una identidad del MCO con constante; no valida E(u\|X)=0. |
| Curtosis/asimetría | La cola derecha domina los momentos muestrales. La curtosis se informa en escala Pearson: normal=3. |
| ComparaciónEE | La pendiente es la misma; cambia la incertidumbre al permitir heterocedasticidad y dependencia por UPM. Ningún método incorpora todo el diseño. |
| Cook | Algunas observaciones tienen mayor influencia en la recta. El umbral4/n es diagnóstico y no identifica errores automáticamente. |
| RMSE/MAE | Resumen del error de ajuste dentro de muestra; la cola influye más en RMSE. No es rendimiento predictivo validado. |
| Descomposición | La recta explica5,19% de la variación muestral. La variación restante no se atribuye causalmente a una causa específica. |
| Simulador | Calcula diferencias de la recta para dos valores elegidos. El intercepto cancela; el IC admite diferencias negativas y marca extrapolación fuera del soporte. |

## Pruebas ejecutadas

`PYTHONDONTWRITEBYTECODE=1 DataScience/.venv/bin/python Dashboard/backend/pipeline.py`: PASS, hashes/selección/estimación/contrato estricto. `python -m unittest discover -s Dashboard/backend/tests -p test_pipeline.py -v`:8/8PASS. `... -p test_v2_diagnostics.py -v`:7/7PASS. Validan conservación por hora/colas, correspondenciahistograma-rejilla, banda usandoCov y noSER,descomposiciónSS,RMSE/SER,QQfinito,CDFempates,escenariosdnegativo/cero/positivo y rechazo artefactos numéricamente incoherentes. Se corrigió una constante de referencia del test tcrítico de aproximación1,6e−8; ningún resultado de producción cambió.

Revisión cruzada completada: el auditor añadió11pruebas en `test_v2_review.py`, sin importar pipeline y usandoParquet/CSV originales; todasPASS (celdas densidad/residuos,cuantiles/CDF,cov/banda,EE,Cook,errores). Suite completa ejecutada con `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s Dashboard/backend/tests -v`:30/30PASS,incluyendo4pruebasHTTP. El sandbox inicial impedía crear socketslocales; el mismo comando se reejecutó con permiso de ejecución ampliado ya autorizado y pasó. No hubo fallaHTTP de aplicación. El orquestador coordina e2e/visual/accesibilidad. Los bloques causales y limitaciones de muestra/diseño siguen vigentes.

## Revisión cruzada final del contenido frontend v2

Se inspeccionaron `Charts.tsx`, `App.tsx` y `Math.tsx` tras reescritura v2. PASS científico: concentración como conteos, cajas con P10/P90 y P25/P75 explícitos, CDF<=umbral con empates y escala declarada, QQ P1–P99 de residuos/SER, diagnóstico de varianza correctamente nombrado, errores convencional/HC3 t(n−2) y UPM t(G−1), banda puntual de media y escenarios separados de observaciones. Tabla completa y límites causales/diseño están presentes; texto extendido en paneles plegables, sin exigir más párrafos en vista inicial.

Se verificaron algebraicamente fórmulas visibles de MCO, pendiente/intercepto, covarianzaCRV1, corrección c=G/(G−1)*(n−1)/(n−k),EE,t,IC,SER,residuos,R²/RMSE y diferencias de escenarios. Se ejecutó renderlocalKaTeX con throwOnError=true sobre las14expresiones fuente (sustituyendo solo valores dinámicos por números de ejemplo):14/14sintaxisválida y MathMLpresente. El componente real usahtmlAndMathml,trust=false.

Simulador inspeccionado: horas negativas/vacías/no finitas y operaciones no representables invalidan. Diferencias negativas sí se permiten: A8→B2 da−368,138339918USD,IC[−412,246562337;−324,030117500] ordenado. A3→B3 da0,IC[0;0]. A18→B24 da368,138339918,IC[324,030117500;412,246562337] y muestraExtrapolación; no se limita el input numérico a18. Los deslizadores siguen0..18 y la recta extrapolada se dibuja discontinua, sin extender la banda observada. Los niveles A/B son ajustes, no predicciones individuales.

Incidencias enviadas a frontend/auditor y cerradas por frontend: (1)desviaciónresidual unía10hcon12h pese a11omitida;ahora segmenta al faltar una hora; (2)títuloCDFdecía«por debajo» mientras define<=;ahora «hasta cada ingreso»; (3)se simplificó advertenciaQQ para separar normalidad, inferencia asintótica y exogeneidad. Sin cambios de aplicación por este agente. EstadofinalPASScontenido; navegador/responsive/accesibilidad a cargo deQA/orquestador. No se repitieron pruebasbackend en esta fase.
