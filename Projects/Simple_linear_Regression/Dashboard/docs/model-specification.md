# Especificación econométrica verificada

Autor: agente 03-econometrics. Fecha: 2026-11-16. Estado: VERIFIED para reproducción; WARN para inferencia poblacional/causal. Dependencias: `DataScience/notebooks/03. EDA.ipynb`, `04. SLR.ipynb`, Parquet local y CSV del snapshot HF `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`. Índices de celda base cero.

## Pregunta y dominio

¿Existe asociación entre las horas de internet y el ingreso laboral mensual? Unidad: persona. Encuesta ENEMDU TIC, Ecuador, levantamiento julio de 2025. Las preguntas de ingreso remiten a junio de 2025; las de uso de internet a los últimos doce meses y su frecuencia declarada. No es una serie temporal.

Dominio analítico: personas ocupadas (`empleo == '1'`), edad >=15 (`p03`), usuarios diarios (`pt3a == '1'`) con `pt3b` e `ingrl` no nulos. No representa automáticamente a todos los ocupados ni a toda la población nacional. La selección por respuesta y el uso diario pueden depender del ingreso y de características omitidas.

## Fuente y selección reproducible

1. Leer `DataScience/data/processed/data_clean.parquet` (27.509 filas, 19 columnas).
2. Leer `enemdu_persona_tics_2025_07.csv` del mismo snapshot HF, separado por `;`.
3. Seleccionar auxiliar `id_persona`, `periodo`, `p03`, `empleo`, `pt3a`; convertir a string y `strip` las cuatro columnas distintas de `p03`.
4. Unir uno a uno por `id_persona`, `periodo`, exigir correspondencia completa y periodo `202507`.
5. Aplicar filtros anteriores: 13.299 ocupados >=15; 10.091 con ambas respuestas; 9.881 además con uso diario.

Fuente exacta: EDA celdas 2/4 y SLR 6/7/8. El Parquet NO contiene edad, empleo ni frecuencia; no se puede reemplazar el cruce por una simple eliminación de nulos.

La limpieza original convierte `pt3b` vacío/888 a NA; `ingrl` vacío/-1/999999 a NA. Conserva cero. En horas, cero significa menos de una hora, no ausencia de internet. En ingreso se retienen 119 ceros en la muestra. Las etiquetas de -1/999999 se heredan de la limpieza; el diccionario ODS solo da nombres/descripciones y no verifica esos códigos. Las pérdidas económicas excluidas por la fuente deben explicitarse como limitación de selección, sin reinterpretarlas como cero.

## Variables y ecuaciones

| Papel | Campo | Operacionalización |
|---|---|---|
| X | `pt3b` | Horas con referencia diaria, solo `pt3a=1`. Valores observados 0–18; 0 codifica <1 hora. |
| Y | `ingrl` | Ingreso laboral mensual en USD; observado 0–17.000. |
| Peso descriptivo | `fexp` | Factor de expansión finito y positivo. No se usa para ajustar el MCO. |
| Conglomerado | `upm` | Agrupación de EE; 1.286 UPM en muestra. |
| Estrato | `estrato` | 150 estratos observados; no entra en la varianza del modelo. |

Modelo poblacional propuesto: `Yᵢ = β₀ + β₁ Xᵢ + uᵢ`. Recta muestral: `Ŷᵢ = β̂₀ + β̂₁ Xᵢ`; residuo `ûᵢ = Yᵢ − Ŷᵢ`.

La proyección lineal muestral describe la asociación. Interpretar β₁ como un cambio causal exige identificación/exogeneidad adicional; no está establecida.

```python
X = sm.add_constant(muestra['pt3b'].astype(float))
y = muestra['ingrl'].astype(float)
modelo = sm.OLS(y, X).fit(
    cov_type='cluster', cov_kwds={'groups': muestra['upm']}, use_t=True
)
```

MCO sin ponderar, covarianza agrupada por UPM CRV1 con correcciones por defecto de statsmodels, t de Student con 1.285 grados de libertad para inferencia. No es WLS ni estimación completa de encuesta. Requiere independencia entre UPM y condiciones asintóticas; no resuelve sesgo por omisión, selección o medición. El agrupamiento por UPM permite dependencia dentro de UPM, incluidos hogares anidados, sin usar explícitamente estratos/pesos.

## Resultados replicados

| Parámetro | Coeficiente | EE UPM | t | p bilateral | IC 95% |
|---|---:|---:|---:|---:|---|
| Intercepto | 364,1483274833 | 11,3516735493 | 32,078823083 | 2,4189076761e-166 | [341,8784801313; 386,4181748354] |
| Horas | 61,3563899864 | 3,7472352476 | 16,373775846 | 7,1086723940e-55 | [54,0050195833; 68,7077603894] |

N=9.881; R²=0,0518890718229; SER=USD 568,786655533; hogares=6.448; UPM=1.286; estratos=150. Varianza muestral de X=4,70275105742.

Interpretación: una hora diaria declarada adicional se asocia con USD 61,36 más de ingreso mensual en la recta del grupo observado. No expresa la ganancia esperada por pasar una hora extra conectado. Como el modelo solo tiene X, no mantiene constantes edad, educación, ocupación o experiencia: evitar decir «controlando por otros factores».

Prueba bilateral `H₀: β₁=0` frente a `H₁: β₁≠0`. El p-valor es muy pequeño bajo el procedimiento descrito; se rechaza al nivel ilustrativo 5%. No es probabilidad de que H₀ sea verdadera ni medida de relevancia económica. R² indica que la recta explica 5,19% de la variación muestral del ingreso, no «5,19% del ingreso».

Para una diferencia de tres horas: USD 184,069169959, IC95% [162,015058750; 206,123281168]. Es una diferencia ajustada de la recta, no un intervalo de predicción individual. No extrapolar fuera de 0–18.

## Diagnósticos autorizados

- Heterocedasticidad: regresión auxiliar de `û²` en constante/X, EE UPM, p bilateral de X=0,00596881067. Detecta tendencia lineal de la varianza; NO es Breusch–Pagan convencional ni prueba exhaustiva.
- Influencia: Cook máximo=0,227853903468; 376 observaciones con Cook>4/9881. Es un umbral diagnóstico, no una regla para borrar errores.
- Sensibilidad: manteniendo Cook<=4/N, N=9.505, pendiente=49,7619319330, IC95% [46,1435036141; 53,3803602519]. Se presenta como escenario secundario, sin reemplazar la estimación principal.
- Dependencia: 6.448 hogares y 1.286 UPM entre 9.881 personas; i.i.d. individual es inadecuado.
- Variación de X y rango completo: verificadas; con una sola X y constante no hay colinealidad perfecta.
- Linealidad en parámetros satisfecha por especificación; linealidad de media condicional no demostrada. No inventar un test RESET ni normalidad como requisito causal.
- Momentos cuartos finitos y exogeneidad no se prueban con datos finitos ni tests de residuos. Cola larga del ingreso, medición de horas y pocos casos en los extremos requieren cautela.

## Fuentes externas consultadas

[Formulario INEC julio 2025](https://www.ecuadorencifras.gob.ec/documentos/web-inec/Estadisticas_Sociales/TIC/2025/202507_Formulario_ENEMDU_Julio_2025.pdf), páginas PDF 18–19 (ingresos junio), 23 (3A/3B y 00 <1h); consulta 2026-11-16. [Documentación OLS.fit](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.fit.html) y [covarianza robusta](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.get_robustcov_results.html), verificadas con statsmodels local 0.15.0. La documentación consultada confirma el uso de t y grados por conglomerados, no avala exogeneidad ni representatividad.
