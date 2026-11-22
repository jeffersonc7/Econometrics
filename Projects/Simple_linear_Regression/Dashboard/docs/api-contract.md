# Contrato de agregados v1
Autor: orquestador / arquitectura. Fecha: 2026-11-16. Estado: aprobado para implementación; números sujetos a réplica de econometría.

Se elige React + TypeScript + Vite y pipeline Python (pandas, pyarrow, statsmodels). Sitio estático con datos agregados reproducibles; servidor Python opcional de solo lectura, sin dependencias web. No necesidad de un backend de cómputo durante requests. No microdatos en cliente. Única fuente pública `/data/dashboard.json`; API equivalente `GET /api/v1/dashboard`, salud `GET /health`. Backend y frontend pueden servirse en una sola URL. Sin CORS abierto, sin endpoints de escritura.

## Tipos (frontend debe definirlos literalmente)
```
Envelope = { data: DashboardData, meta: Meta }
Meta = {schema_version: '1.0', generated_at: string, source: string, revision: string, clean_sha256: string, raw_sha256: string, population: string, period: string, income_period: string, weight: string, n: number, source_url: string, license_status: string}
DashboardData = {selection: {label:string,n:number}[], overview: Overview, groups: Group[], hours: {hours:number,n:number}[], income: {label:string,lower:number,upper:number|null,n:number}[], availability: {label:string,n:number}[], model: Model}
Overview = {n:number, income_mean:number, income_median:number, hours_mean:number, hours_median:number, income_weighted_mean:number, hours_weighted_mean:number, pearson:number, spearman:number, weighted_pearson:number, zero_hours_n:number, zero_income_n:number, income_p99:number, income_max:number, hours_max:number}
Group = {key:string,label:string,n:number,income_mean:number,income_median:number,hours_mean:number}
Model = {n:number,clusters:number,households:number,strata:number,r_squared:number,ser:number,x_variance:number,coefficients:Coefficient[],heteroskedasticity_p:number,cook_flagged_n:number,sensitivity:{n:number,slope:number,ci_low:number,ci_high:number},residual_spread:{hours:number,n:number,std:number}[],fitted:{hours:number,income:number}[]}
Coefficient = {term:string,estimate:number,se:number,t:number,p:number,ci_low:number,ci_high:number}
```
`coefficients[0]` intercepto; `[1]` pt3b. Meta contiene referencias, fechas y cautelas. Toda cifra usa precisión completa; redondear solamente en UI. `groups` reproduce tramos EDA: 0–1, 2–3, 4–5, 6–8, 9 o más. `hours` cubre todos los enteros 0..18. `income` usa bins en USD [0,100,250,500,750,1000,1500,3000,infinito] con intervalos cerrados a izquierda. No controles que reestimen el modelo: muestra fija. El selector de tramos cambia solo la tarjeta comparativa (media/mediana), nunca resultados de regresión. Cero horas significa menos de una hora. La media ponderada es descriptiva, no diseño completo.

## Estados
Carga explícita, error de fetch con reintento, muestra vacía sin números de sustitución, validación de schema/n antes de render. Archivos corruptos -> error en español. Servidor no hace descargas por request; datos ausentes -> 503 JSON `{error:{code,message}}`; ruta inexistente 404. POST/PUT/PATCH/DELETE -> 405. Cache agregados `public,max-age=300`; metadatos incluyen revisión inmutable y hashes. No listados de directorios ni rutas de notebooks/microdatos.

# Revisión visual v2 · contrato aditivo aprobado (2026-11-16)
El usuario reemplaza el estilo anterior: sólo claro, marca Grupo 2, más espacio y tamaño de letra, EDA gráfico y texto mínimo, modelo técnico y vista Datos. Muestra y modelo permanecen idénticos. Se añaden agregados reales, nunca registros identificables. `schema_version` sigue1.0 por compatibilidad aditiva.

```
data.visuals = {
 density: {hours:number,lower:number,upper:number,n:number}[],
 boxplots: {key:string,label:string,n:number,q1:number,median:number,q3:number,p10:number,p90:number,mean:number}[],
 income_cdf: {income:number,share:number}[],
 percentiles: {p:number,income:number,hours:number}[]
}
data.model.diagnostics = {
 fit_band: {hours:number,income:number,ci_low:number,ci_high:number}[],
 residual_density: {hours:number,lower:number,upper:number,n:number}[],
 residual_histogram: {lower:number,upper:number,n:number}[],
 qq: {theoretical:number,empirical:number}[],
 covariance: number[][],
 t_critical:number, df_inference:number,
 ee_comparison: {method:string,se:number,ci_low:number,ci_high:number}[],
 residual_mean:number, residual_skew:number, residual_kurtosis:number,
 cook_histogram: {lower:number,upper:number,n:number}[],
 rmse:number,mae:number,adjusted_r_squared:number,
 sse:number,sst:number,ssr:number
}
```
`density` por cada hora entera y bins USD [0,100,250,500,750,1000,1500,3000,5000,10000,17001]; bins cerrados izquierda, incluye todos sin truncar. Residual_density porhora y 28bins uniformes min..max residuales (último extremo incluido); histogram28bins mismos límites. QQ son cuantiles de residuos estandarizados por SER frente a normal estándar, sólo diagnóstico visual (no prueba de exogeneidad ni necesidad de normalidad para inferencia agrupada). Banda puntual IC95 de media lineal usa cov clusterUPM y t(G−1). `ee_comparison` convencional,HC3,clusterUPM; no cambia coeficientes. `covariance` orden const,pt3b. `cook_histogram` bins log por rango observado, conservaN. `rmse=sqrt(mean(resid²))`,SER=sqrt(SSE/(n−2)),MAE=mean(abs(resid)). CDF empírica de ingresos en umbrales cuantiles0..100; percentiles p10,p25,p50,p75,p90,p99.

Simulador admite X inicial/final numérico y sliders0..18, paso0.1; permite número fuera de soporte si muestra aviso «Extrapolación» y no limita silenciosamente. Diferencia b1*(x1−x0) y EE abs(delta)*EEb1; IC ordenado correctamente incluso delta negativo. Diferencias de asociación, no efecto causal identificado. Y ajustado no es predicción individual. Todos los diagnósticos e interpretaciones técnicas extendidas pueden ir en paneles plegables para evitar párrafos largos.
