# Revisión crítica v2 · UX, lector y QA científico

Autor: agente auditor, independiente de frontend y econometría. Fecha: 2026-11-16. Estado inicial: revisión del contrato; implementación v2 en curso.

La revisión parte de las fuentes y del modelo ya auditados. No repite descargas ni modifica DataScience. Alcance recibido del orquestador: EDA muy visual y con texto mínimo; sección técnica ampliada; inputs X inicial/final; sólo tema claro; marca Grupo 2 y autores; vista Datos con CSV de agregados; preparación local para Netlify, sin nueva publicación en ChatGPT.

## Criterios concretos de aceptación

| Área | Criterio verificable | Evidencia exigida |
|---|---|---|
| Identidad | Grupo 2 y autores solicitados; interfaz en español, sólo claro | Revisión de código y captura; ausencia de control de tema oscuro |
| EDA | Gráficos contestan preguntas distintas con unidades, N y color informativo; explicación extensa plegable | Rúbrica de lector y capturas móvil/escritorio |
| Densidad | Cada celda cuenta registros reales; suma N=9.881; bins USD desiguales se identifican como categorías | Réplica independiente numpy y notas/ejes |
| Cajas | Q1/mediana/Q3 y bigotes P10/P90 fieles al grupo; no presentar bigotes como rango total ni Tukey | Réplica por tramos y leyenda |
| Distribución acumulada | Umbrales ordenados, share = proporción observada Y≤umbral, incluido tratamiento de empates | Réplica empírica; no asignar automáticamente p a cada cuantil |
| Percentiles | P10/P25/P50/P75/P90/P99 de ingreso y horas reproducibles | np.quantile sobre dominio D |
| Banda de ajuste | IC puntual de media lineal usando matriz cluster UPM y t(G−1); no intervalo individual | Réplica xCovx y etiquetas |
| Residuos | Histograma y densidad conservan N; mismo conjunto de 28 bins; último extremo incluido | Conteos numpy contra residuos originales |
| QQ | Cuantiles finitos de residuos/SER frente normal; no afirmar prueba de exogeneidad ni normalidad necesaria | Revisión de fórmula y cálculo independiente |
| Inferencia | Covarianza 2×2 en orden const/pt3b, EE convencional/HC3/UPM correctos | Statsmodels independiente |
| Métricas | RMSE≠SER correctamente; SSE+SSR=SST; R²/MAE reproducidos | Identidades numéricas y réplica |
| Fórmulas | KaTeX legible y accesible; ecuación poblacional/muestral, MCO, varianza, IC, contrastes y residuos coherentes | Fuente y navegador; sin copiar notación errónea |
| Simulador | X0/X1 numéricos amplios, sliders 0–18 paso 0,1; no límites ocultos | Navegador y lectura del cálculo |
| Diferencia negativa | Δ=(X1−X0), ajuste β1Δ; EE=abs(Δ)EEβ; IC siempre ordenado, Δ=0 → [0,0] | Casos X0=8/X1=2, X0=X1 y positivos |
| Extrapolación | X positivo mayor de 18 muestra aviso inequívoco y conserva valor introducido. X negativo es físicamente inválido y se puede rechazar sin cálculo, según aclaración del orquestador | X0=25/X1=30; X0=−1 debe mostrar validación y ocultar resultado; sin clamp silencioso |
| Interpretación | Asociación, no causalidad identificada; predicción media distinta de individual | Lectura crítica de títulos, tooltips y notas |
| Datos | CSV sólo agregado, sin ID ni filas/residuos individuales; coherente con visuales | Inspección de exportación y sumas |
| Móvil y acceso | Sin overflow de página; tablas con scroll local; controles ≥44 px; teclado/foco y alternativas de gráficas | Orquestador: navegador 360–1440 px, Axe y zoom |
| Entrega | ZIP estático reproducible, sólo dist, sin fuentes ni entornos; no nuevo despliegue en ChatGPT | Inspección de paquete por orquestador |

## Observaciones tempranas comunicadas a otros agentes

Se pidió a econometría calcular la CDF por conteos reales ante empates, evitar cuantiles normales infinitos y explicitar grados de libertad de cada comparación de EE. Se pidió a frontend ordenar IC para diferencias negativas, respetar soporte y definir bigotes P10/P90. Estos puntos son condiciones de aceptación; no son fallos confirmados de un código que aún no se había escrito.

## Resultados de implementación

Pendiente de los archivos v2 y su artefacto. Las pruebas de esta revisión se documentarán aquí con comandos y resultados reales. La validación visual en navegador corresponde al orquestador y no se dará por ejecutada por leer código.

## Réplica independiente del artefacto v2

**PASS: 11 pruebas**, ejecutadas mediante:

```bash
PYTHONDONTWRITEBYTECODE=1 DataScience/.venv/bin/python -m unittest discover -s Dashboard/backend/tests -p test_v2_review.py -v
```

Se añadieron en `backend/tests/test_v2_review.py`. Leen el Parquet original de `DataScience` y el CSV auxiliar fijado, reconstruyen la muestra y estiman statsmodels por separado. No importan `pipeline.py` ni comparten funciones productoras. Se verificó cada celda de densidad (19×10), cada celda residual (19×28), cuantiles por tramo, CDF con empates, percentiles, covarianza y 181 puntos de banda, 99 cuantiles QQ, tres esquemas de EE, identidades de sumas de cuadrados, medidas de error, momentos y los 28 bins de Cook. Las sumas conservan N=9.881. No se encontraron discrepancias ni identificadores individuales en el JSON.

Controles reproducidos:

- EE de pendiente: convencional 2,6387298598; HC3 3,2787023766; UPM 3,7472352476.
- RMSE 568,7290889463; SER 568,786655533; MAE 313,1356683272. Sus definiciones son diferentes.
- R² ajustado 0,05179309946; asimetría residual 7,8776039904; curtosis de Pearson residual 147,6190767720 (normal=3, no exceso de curtosis).
- SSE 3.196.036.885,719764; SST 3.370.952.481,12438; SSR 174.915.595,404616.
- CDF usa proporción observada ≤ umbral, incluido el salto de ingresos cero; no presupone que cada cuantil tenga exactamente la participación nominal cuando existen empates.
- QQ usa probabilidades 0,01…0,99 y residuos/SER; evita los cuantiles normales infinitos de 0 y 1.

Casos de control entregados al orquestador para verificar el simulador real:

| X inicial | X final | Diferencia ajustada USD | IC 95 % USD | Extrapolación |
|---:|---:|---:|---|---|
| 2 | 8 | 368,138339918 | [324,030117500; 412,246562337] | No |
| 8 | 2 | −368,138339918 | [−412,246562337; −324,030117500] | No |
| 3 | 3 | 0 | [0; 0] | No |
| 25 | 30 | 306,781949932 | [270,025097916; 343,538801947] | Sí |
| −1 | 2 | Entrada físicamente inválida: no presentar cálculo como escenario válido | Mensaje de validación; sin resultado | No aplica |

Estas cifras son referencias de prueba calculadas de coeficientes y covarianza verificados. El pase científico del JSON no acredita aún que el frontend las represente correctamente ni que las fórmulas KaTeX sean legibles.


## Primera revisión de gráficas v2 y coordinación

Se detectó que FitChart inicialmente tenía dominio X mínimo 0 y recortaba valores Y negativos a 0 en su transformación. Se notificó al frontend. El orquestador aclaró que horas negativas son físicamente inválidas: la corrección aceptable es validarlas y ocultar cálculo/escenarios, manteniendo válido un Δ negativo cuando X final es menor que X inicial y ambos son no negativos. Los valores positivos >18 deben conservarse con aviso de extrapolación.

Se detectó también que SpreadChart unía puntos de horas 10 y 12 pese a ausencia del grupo de 11 horas bajo el umbral n≥30. Se solicitó interrumpir la línea en huecos o utilizar puntos sin interpolación. Estado: pendiente de relectura del código corregido.

Se detectó un tercer punto concreto en la validación del cliente v2: `rows([])` aceptaba arrays vacíos de CDF, cajas, QQ, banda y comparación de EE. CDF accedía al último elemento sin comprobar existencia, lo que podía causar una excepción tras pasar `isEnvelope`. Se solicitó exigir longitudes y restricciones del contrato antes de renderizar; es relevante para entrega estática sin backend. Estado: reportado al frontend y al orquestador, pendiente de relectura.

## Revisión estática inicial de App v2

App v2 ya contiene tres vistas, identidad Grupo 2, autores en el pie, sólo modo claro y exportaciones de tablas agregadas. La sección exploratoria usa métricas de contexto, mapa de concentración, barras horarias/monetarias, cajas, acumulada y selección, con textos principales breves. Las explicaciones de método extensas se pliegan. La sección técnica incorpora KaTeX, fórmula CRV1 con corrección G/(G−1)·(n−1)/(n−k), tabla bilateral, laboratorio de escenarios, residuos, QQ, dispersión, comparación de EE, influencia y supuestos.

Por lectura, el laboratorio calcula correctamente Δ = X final − X inicial; diferencia β̂1·Δ; EE = abs(Δ)·EEβ; margen t·EE; intervalo centrado en la diferencia. Rechaza campos vacíos y horas negativas, y avisa para valores mayores de 18. La validación permite mantener un Δ negativo válido sin invertir límites. La prueba en navegador corresponde al orquestador.

Las descargas CSV usan exclusivamente tablas agregadas: horas, intervalos monetarios, tramos/cuantiles, celdas de concentración, coeficientes, percentiles, selección e histograma residual. El JSON adicional contiene el mismo sobre agregado, sin IDs ni residuos individuales. CSV conserva precisión, comillas escapadas y BOM UTF-8. Se encontró un detalle menor: la búsqueda usaba «Abierto» para límites superiores nulos mientras la tabla mostraba «Sin límite superior»; se pidió coherencia.

Se pidió también validar finitud de resultados derivados ante una entrada extrema como 1e308: aunque el número introducido es finito, multiplicarlo por la pendiente puede desbordar. El comportamiento correcto es un error de validación, sin ∞ ni coordenadas NaN; no un máximo silencioso.

La estructura técnica no hace afirmaciones causales. Diferencia ajustada, banda de media e intervalos individuales están distinguidos. Los EE convencionales y HC3 usan t(n−2), los UPM t(G−1), y la UI advierte que no incorporan el diseño completo. Los residuos de media casi cero se presentan como resultado de MCO, no evidencia de exogeneidad. SSE/SSR/SST están definidos con la convención del contrato.
