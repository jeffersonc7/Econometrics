# Mapa de procedencia

Autor: agente auditor · Fecha:2026-11-16 · Estado: verificado.
Los índices de celda son base cero. Snapshot y hashes: `data-provenance.json`.

| Fuente/celda | Transformación / filtro | Resultado y vista autorizable | Limitación |
|---|---|---|---|
| 01.data_inspection, c3–7 | CSV HF personas y hogar, ODS | Identifica origen ENEMDU TIC julio2025 | Notebooks originalmente main no fijado |
| 01, c10–17 | Selecciona11 identificadores+3diseño+2variables | Interim27.509×16 | Exportación depende de celda16 sin ejecución persistida |
| 02.data_cleaning,c5–9 | String IDs, pesos coma→decimal | Sin duplicados/NA diseño, fexp>0 | No constituyen por sí solos inferencia de encuesta |
| 02,c13–22 | pt3b blanco/888→NA, estados por pt2a | 21.172horas registradas;6.337NA |0 significa<1hora;1.803vacíos sin interpretación uniforme |
| 02,c25–33 | Ingreso blanco/-1/999999→NA;conserva0 | 11.906ingresos,157ceros | Códigos especiales interpretados en notebook;ODS sin catálogo |
| 02,c35–36 | Exporta19columnas | Limpio533.387bytes, idénticoHF | Celda36 sin contador; reproducción en memoria confirmó equivalencia |
| 03.EDA,c2/4 | Merge CSV y filtros empleo/edad/completos/diario | Flujo27.509→13.299→10.091→9.881 | No representa automáticamente a todos los ocupados |
| 03,c6 | Cruce estados de horas/ingreso entre ocupados | Disponibilidad y selección | Ingreso ausente≠cero |
| 03,c7/8 | Condiciona pt3a1 | Unidad diaria;N9.881,74,3%ocupados | Horas últimos12meses, ingreso junio |
| 03,c10–12 | describe sin ponderar | Mediana3h,USD474;media3,358h/USD570,187 | No son medias nacionales;cola ingresos |
| 03,c11 | Histograma horario y log1p ingreso | Distribuciones con N y unidades | Transformación solo visual;conservar0 |
| 03,c14 | Dispersión/hexbin | Asociación visual | App debe usar agregación para no exponer filas |
| 03,c16 | pd.cut[-1,1,3,5,8,∞] y resúmenes | N por tramo1.661/4.515/2.312/1.132/261 | Grupos no controles causales |
| 03,c19 | fexp np.average y correlación ponderada | Medias ponderadas3,07h/USD506,25;Pearson0,232 | No varianza/IC de encuesta;selección por respuesta |
| 03,c22 | P99/ingreso positivo | Sensibilidad descriptivaN9.783/N9.762 | No modificar limpio |
| 04.SLR,c6–10 | Misma selección;OLS clusterUPM,use_t=True | b0=364,148;b1=61,356 | Sin ponderación/estratos;EE no diseño completo |
| 04,c11 | params/bse/conf_int/pvalues | Tabla coeficientes,EE,IC,t,p;R²0,0519;SER568,79 | Significancia≠causalidad/importancia |
| 04,c15 | 3×pendiente y límites | USD184,07;IC[162,02;206,12] | Diferencia ajustada, no ingreso individual esperado garantizado |
| 04,c18 | nunique y varianzaX |6.448hogares,1.286UPM,150estratos,varX4,703 | Dependencia interna y exogeneidad no comprobada |
| 04,c21 | OLS residuos² en X,clusterUPM | p0,006 tendencia de varianza | No prueba universal de heterocedasticidad |
| 04,c24/26 | Cook y reestimación sin Cook>4/N | Pendiente49,76,IC[46,14;53,38] | Diagnóstico;no borrado automático |

Fuentes originales: `DataScience/notebooks/` y `DataScience/src/`. Las cifras indicadas son resultados redondeados de outputs contrastados con selección/descriptivos; para coeficientes finales usar reproducción completa del pipeline y revisión econométrica.
