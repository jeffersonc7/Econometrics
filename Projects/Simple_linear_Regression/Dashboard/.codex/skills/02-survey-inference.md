# Skill: Survey Design & Causal Claims

- Verificar diccionario de variables (incluidos códigos especiales), elegibilidad, observados/no observados, unidad de análisis, representatividad y periodo.
- Si se usan `fexp`, `estrato`, `upm`, comprobar valores, grupos, dominio de estimación y compatibilidad del software de inferencia.
- Documentar si las medias/tablas son ponderadas; informar denominador y N muestral; no tratar el factor de expansión como frecuencia de observaciones idénticas.
- Separar OLS/WLS/estimación de encuesta y errores estándar convencionales/HC/clúster/diseño.
- Especificar supuestos MCO: linealidad, variación en X, ausencia de colinealidad perfecta, exogeneidad condicional, distribución muestral e inferencia pertinente. Tests de residuos no prueban exogeneidad.
- Etiquetas honestas: `asociación condicional` por defecto; `efecto causal` solo con argumento de identificación explícito, suficientemente defendible y documentado.
