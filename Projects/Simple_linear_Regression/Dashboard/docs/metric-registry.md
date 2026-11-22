# Registro de métricas aprobadas

Autor: 03-econometrics. Fecha: 2026-11-16. Estado: VERIFIED. Base de cálculo: Parquet local de `DataScience`, CSV HF snapshot `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`; hashes y correspondencia en `data-provenance.json`. Celdas base cero. Todos los valores se recalcularon; no se copiaron como constantes de aplicación.

## Contrato común de evidencia

Cada agregado debe incluir pregunta, población/filtro, campos, unidad, peso, N sin ponderar, denominador, transformación, fuente/celda y revisión. Dominio `D`: empleo=1, edad>=15, frecuencia diaria=1, horas e ingreso observados. N=9.881. No exponer identificadores ni registros individuales. Publicar números con formato español y precisión útil; mantener precisión completa en JSON. EDA por defecto sin ponderar; los pesos solo aparecen en la comparación explícita. Modelo sin ponderar y fijo en D; filtros EDA no reestiman el modelo.

| ID / pregunta | Fuente y cálculo | Valores de control | Unidad / denominador / peso | Uso y límite |
|---|---|---|---|---|
| selection / ¿A quién describe? | EDA 2/4; unión y conteo por etapas | 27.509 -> 13.299 -> 10.091 -> 9.881 | Personas observadas; proporción de base=9.881/27.509; sin peso | Mostrar selección, no población nacional expandida |
| coverage / ¿Cuántos ocupados quedan representados en el análisis? | EDA 8; 9.881/13.299*100 | 74,29881946% | % de ocupados >=15 observados, sin peso | No llamar tasa nacional de acceso/uso diario |
| hours-center / ¿Cuánto internet declara el grupo? | EDA 10; mediana/mean pt3b en D | Mediana 3; media 3,358061; P25=2, P75=4, P90=6, P99=10, rango0–18 | Horas referencia diaria; N=9.881; sin peso | 0 significa <1 hora |
| income-center / ¿Cuál es el ingreso típico? | EDA10; ingrl.describe() en D | Mediana474; media570,186823; P25=250; P75=675; P90=1.035; P99=2.680; máximo17.000 | USD mensuales junio2025; N=9.881; sin peso | Mediana no equivale a salario de todos los ecuatorianos |
| zeros / ¿Se conservaron valores cero? | EDA10; .eq(0).sum() | Horas<1:118; ingreso0:119 | Personas en D, sin peso | No convertir ceros en NA |
| hours-distribution / ¿Cómo se reparten las horas? | EDA11; count por hora entero0–18, incluir 17 con conteo0 | Conteos0:118,1:1543,2:2517,3:1998,4:1415,5:897,6:606,7:143,8:383,9:48,10:135,11:7,12:51,13:2,14:7,15:9,16:1,17:0,18:1 | Personas y % / N=9.881; sin peso | Histograma/barras, eje con unidad y total |
| income-distribution / ¿Dónde se concentra el ingreso? | EDA11; histograma log1p para visual o bins USD documentados | Total bins=9.881; conservar0 y cola hasta17.000 | Personas; N=9.881; sin peso | Etiquetas USD; no confundir transformación visual con modelo log |
| by-hours / ¿Cómo cambia el ingreso entre grupos de horas? | EDA16; cut[-1,1,3,5,8,inf], aggregate count/mean/median | 0–1:n1661,media404,58338,mediana350;2–3:n4515,media515,65249,mediana470;4–5:n2312,media639,16263,mediana500;6–8:n1132,media810,54594,mediana656;9+:n261,media913,98467,mediana710 | USD/mes; denominador N de cada tramo; sin peso | Barras mediana + N; tramos resumen, X del modelo sigue continua |
| missingness / ¿Quién no tiene ambas respuestas? | EDA6; crosstab horas-status vs income-status Observed en ocupados>=15 | Observed:1032 no/10091 sí;Not applicable244/1009;Nonresponse79/611;Potentially out of scope46/187 | Personas; denominador13.299; sin peso | Ausente no es0; traducir etiquetas al español |
| correlations / ¿Qué intensidad tiene la asociación? | EDA19; Pearson y Spearman de D | Pearson0,227791729048; Spearman0,270116652987 | Coeficiente[-1,1]; N=9.881; sin peso | Magnitud baja, no causal |
| weighted-comparison / ¿Qué cambia al usar los pesos? | EDA19; np.average y covarianza ponderada normalizada | Horas3,06947273090; ingreso506,249747409; Pearson0,231527393058 | Horas/USD/r; peso fexp; N real9.881 | Descriptivos del dominio; no inferencia completa del diseño |
| model-coefficients / ¿Cuál es la asociación estimada? | SLR10/11; OLS cluster UPM use_t=True | Const364,1483274833 EE11,3516735493 IC[341,8784801313;386,4181748354]; beta61,3563899864 EE3,7472352476 IC[54,0050195833;68,7077603894] | USD mensuales por1h diaria; N9.881; sin peso;1286UPM | Coeficientes, t y p bilateral; ver especificación para precisión |
| model-fit / ¿Cuánto resume la recta? | SLR11; rsquared, sqrt(mse_resid) | R²0,0518890718229; SER568,786655533 | Fracción variación/USD; N9.881; sin peso | SER no es EE del coeficiente |
| model-difference / ¿Qué diferencia describe la recta? | SLR15; delta*beta e IC por delta>=0 | delta3 ->184,069169959; IC[162,015058750;206,123281168] | USD/mes; N9.881; sin peso | Control delta0–6 u otro rango sin extrapolar; no ganancia causal ni predicción individual |
| survey-groups / ¿Hay observaciones dependientes? | SLR18; nunique id_hogar/upm/estrato | 6.448/1.286/150; varX4,70275105742 | Grupos/horas²; N9.881 | Conteos agregados, no IDs |
| variance-trend / ¿Es constante la dispersión? | SLR21; OLS residual²~X con EEUPM | p0,00596881067 | p bilateral; N9.881; sin peso | Tendencia lineal, no test BP convencional |
| influence / ¿Cambia el resultado con casos influyentes? | SLR24/26; Cook>4/N, reestimar manteniendo<= |376 marcados; N9.505; beta49,7619319330;IC[46,1435036141;53,3803602519];Cookmáx0,227853903468 | Personas, USD/mes/h; sin peso;EEUPM | Escenario diagnóstico; no depuración automática |

## Agregados derivados acordados en el contrato v1

Distribución USD: se aprueba sustituir la escala logarítmica del notebook por intervalos monetarios más fáciles de leer. `pd.cut(ingrl, bins=[0,100,250,500,750,1000,1500,3000,np.inf], right=False)` da conteos `[678,1648,2949,2477,957,714,386,72]`, total9.881. Los intervalos incluyen límite inferior y excluyen superior; último >=3.000 conserva toda la cola. No son cuantiles ni porcentajes acumulados. Eje de barras por categorías con ancho visual uniforme, no densidad por USD, porque los intervalos son desiguales.

Disponibilidad: puede reducirse la matriz EDA6 a conteos excluyentes de horas/ingreso disponibles o no, siempre sobre los13.299 ocupados, conservando la diferencia entre NA y0. La reducción debe documentar denominador y sumar13.299.

Dispersión residual: se autoriza `DataFrame(hours=pt3b,residual=model.resid).groupby(hours).agg(size,std)` y conservar grupos con n>=30, tal como `DataScience/src/slr_plots.py::plot_residuals`/SLR20. Unidad USD, sin peso; no es EE ni IC. En horas0 la SD=410,273028944 y en8 es1044,127196667 como controles. No unir visualmente puntos a través de horas con grupo ausente sin explicitarlo.

Recta ajustada: `intercepto+pendiente*horas` para valores0..18. Cada punto es ajuste de modelo, no persona, media observada ni predicción individual certificada. No publicar residuos individuales.

`Group.hours_mean`: promedio simple de pt3b por cada tramo EDA16, misma partición aprobada, N del tramo. No interpretar como límite superior del grupo.

Interacción implementada según contrato: selector de tramos afecta solo comparación de media/mediana y su N; distribuciones y modelo permanecen en dominio fijo. Los filtros por área mencionados abajo quedan como extensión opcional, no requisito de esta versión.

## Extensiones autorizadas y límites

Filtros EDA por área (`area` 1 urbana, 2 rural) son válidos si se recalculan todos los denominadores/centros/distribuciones del subconjunto de D y se rotula «subgrupo de la muestra». Conteos de control: urbana7.691, rural2.190. No etiquetar resultados filtrados como «nacionales». El modelo permanece fijo y se informa esa separación. Contenido adicional requiere añadirse al registro con evidencia. No aprobar scatter con puntos de microdatos identificables; preferir agregado por celda o tramo. Las celdas pequeñas pueden fusionarse para publicación.

Casos sin datos: resultado vacío explícito, sin fallback numérico. El agregado no debe incluir `id_persona`, `id_hogar`, `id_vivienda`, `upm` individuales ni ingreso original.

## Ampliación v2 · agregados gráficos y diagnósticos

Autor: 03-econometrics; 2026-11-16; VERIFIED. Contrato aditivo v2 en `api-contract.md`. Todos los cálculos nuevos comparten fuente SHA fijada, filtroD, N=9.881 y sin pesos. Son derivados reproducibles del mismo MCO; los notebooks originales no se alteran. `backend/pipeline.py::{exploratory_visuals,diagnostic_aggregates,binned_by_hours}` es la implementación de referencia. No representan tests adicionales de identificación causal.

| ID / pregunta | Campos y transformación reproducible | Unidad / denominador / control | Lectura y límite |
|---|---|---|---|
| density / ¿Dónde se concentran horas e ingresos? | Por cada hora0..18, np.histogram(ingrl,bins=[0,100,250,500,750,1000,1500,3000,5000,10000,17001]);190celdas | Personas/celda; suma9.881; cada columna de horas coincide con hours.n | Conteos, no densidad por áreaUSD; intervalos desiguales y pequeños grupos no justifican causalidad |
| boxplots / ¿Cuánta variación hay dentro de cada tramo? | Mismos tramos EDA16; np.quantile(y,[.1,.25,.5,.75,.9],method='linear') + media | USD/mes y N por tramo;0–1:q1=180,mediana350,q3=520,p10=85,p90=704 | BigotesP10/P90, NO Tukey1,5IQR ni mínimo/máximo; colas no dibujadas siguen incluidas enN/media |
| income_cdf / ¿Qué proporción registra hasta cierto ingreso? | Umbrales np.quantile(y,p/100),p0..100; share=mean(y<=umbral) | Proporción delD; primer umbral0/share119/9881; último17.000/share1 | Respeta empates; share no es p por construcción.101puntos resumidos no ECDF de cada valor único; marcar representación resumida |
| percentiles / ¿Qué valores delimitan la distribución? | p10/25/50/75/90/99; np.quantile lineal de ingresos y horas | USD:[120,250,474,675,1035,2680];horas:[1,2,3,4,6,10] | Percentiles de la muestra, no umbrales nacionales; horas0 codifica<1h |
| fit_band / ¿Cuánta incertidumbre tiene la media lineal? |181puntos0..18,paso0,1;v(x)=[1,x]CovUPM[1,x]ᵀ;Ŷ±t.975,G−1 sqrt(v) | USD/mes; tcrítico1,9618118205524;df1285;Cov ordenconst/pt3b | Banda PUNTUAL de media lineal ajustada, no simultánea ni intervalo de predicción individual |
| residual_density / ¿Cómo cambia el error con X? | û=Y−Ŷ;28bins uniformes minû..maxû, porhora;último extremo incluido | Personas/celda;532celdas;sum9.881; rango−1184,494177..16145,000553USD | Agregado de dispersión; colas altas son reales y no se recortan; cero no significa exogeneidad |
| residual_histogram / ¿Qué forma tiene el error de ajuste? | np.histogram(û,bins=28), mismos bordes que residual_density | Personas/bin;sum9.881; ancho uniforme≈618,910526USD | El bin central puede dominar por cola larga; no se excluyen extremos ni se alteran residuos |
| qq / ¿Se parecen los cuantiles del error a una normal? | p=.01..99; x=norm.ppf(p);y=quantile(û/SER,p),99puntos | Desviaciones en unidadesSER;norm.estándar;extremos0/1 excluidos para evitar infinito | Residuo/SER, NO residuo studentizado por leverage. Desviaciones muestran forma; normalidad no identifica causalidad ni es requisito de inferencia agrupada asintótica |
| covariance / ¿Cómo covarían intercepto y pendiente? | model.cov_params() agrupadaUPM | [[128,86049237,−33,16018775],[−33,16018775,14,04177200]]; diagonal=EE² | Covarianza estimadores; no correlación ingreso/horas |
| ee_comparison / ¿Qué cambia al estimar incertidumbre de otro modo? | Misma OLS; clásico use_t=True;HC3 use_t=True;clusterUPM use_t=True | EEbeta2,63872986/3,27870238/3,74723525; primerosdf9879,UPM1285 | Cambian EE/IC, no coeficiente61,35639. Convencional requiere varianza constante/independencia;HC3 no corrige dependencia intraclúster;UPM no es diseño completo |
| residual_moments / ¿Es simétrica y ligera la cola del error? | mean(û),scipy.stats.skew(û,bias=False),kurtosis(û,fisher=False,bias=False) | Media≈1,03e−12USD;asimetría7,87760399;curtosisPearson147,61907677 (normal3) | Media≈0 resulta de MCO con constante; no demuestraE(u|X)=0. Cola derecha larga; momentosmuestrales no prueban existencia de momentos poblacionales |
| cook_histogram / ¿Cuántos casos concentran influencia? | DistanciaCook de mismaOLS,28bins geomspace(min,max),último incluido;si0haybininicial0..minpositivo | Personas/bin;sum9881;rango2,66958e−16..0,2278539035 | Cook mide influencia del ajusteMCO; eje logarítmico explícito, umbral4/nheurístico. No implica error de captura |
| rmse_mae / ¿Cuánto se separan observación y recta? | RMSE=sqrt(mean(û²));MAE=mean(absû);SER=sqrt(SSE/(n−2)) | USD/mes;RMSE568,72908895;MAE313,13566833;SER568,78665553 | Ajuste dentro de muestra, no validación fuera de muestra ni precisión garantizada individual |
| decomposition / ¿Qué parte de la variación recoge la recta? | SSE=sumû²;SST=sum(Y−Ȳ)²;SSR=sum(Ŷ−Ȳ)²;R²aj=1−(1−R²)(n−1)/(n−2) | USD²;SSE3196036885,7198;SST3370952481,1244;SSR174915595,4046;R²aj0,05179309946 | SST=SSE+SSR con constante. Convención del contrato:SSR es explicada; `statsmodels.ssr` nombra la residual(SSE). R² no proporción de ingreso ni causalidad |

Simulador v2: X inicial/final son números introducidos por usuario, no observaciones publicadas. Para d=Xfinal−Xinicial, diferencia=b1*d,EE=abs(d)*EEb1,IC=d*b1±t1285*abs(d)*EEb1. Funciona con dnegativo/cero sin invertir límites; no usaCov00/Cov01 porque el intercepto cancela. Valores fuera de0..18 deben indicar extrapolación, nunca limitarse silenciosamente. Los intervalos de nivelesusanCovcompleta; el simulador describe asociaciones de la recta, no efectos causales ni ingresos individuales futuros.
