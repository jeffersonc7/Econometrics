# Revisión como lector sin econometría

Autor: agente auditor adoptando rol09 · Fecha:2026-11-16.
Método: simulación crítica de rol. No se realizaron entrevistas ni pruebas con personas usuarias.

## Ronda1 — propuesta y contrato, antes de interfaz

Estado: PASS CON CONDICIONES. Dependencias: `api-contract.md`, `metric-registry.md`, `model-specification.md`; App todavía no existía al efectuar esta ronda.

Rubrica0–2 por columna: claridad(C), pregunta respondida(P), relevancia(R), evidencia(E), legibilidad móvil prevista(M), acción informativa útil(A). M=1 solo evalúa viabilidad del diseño propuesto; no acredita prueba en navegador. Umbral≤7/12 implica devolución.

| Elemento propuesto | C | P | R | E | M | A | Total | Qué aporta / condición |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Contexto y muestra |2|2|2|2|1|2|11| Explicar ocupado≥15, uso diario, ambas respuestas; julio encuesta/junio ingreso |
| Mediana de ingreso y horas |2|2|2|2|1|2|11| «La mitad tiene un ingreso de hasta USD474» y mediana3h; no promedio nacional |
| Distribución de horas |2|2|2|2|1|2|11| Responde cuánto se conectan;0 debe decir<1hora; conservar categorías sin casos |
| Barras de ingreso |1|2|2|2|1|2|10| Intervalos monetarios legibles; anchos uniformes son categorías, no densidad |
| Comparación por tramos |1|2|2|2|1|2|10| Selector media/mediana y grupo con N; indicar qué tarjeta cambia y cuáles no |
| Flujo de selección |1|2|2|2|1|2|10| No confundir4etapas anidadas con grupos excluyentes; mostrar por qué baja N |
| Tabla MCO avanzada |1|2|2|2|1|2|10| Definir EE/IC/p con lenguaje claro; tabla con scroll localizado o apilada |
| Diferencia ajustada |1|2|2|2|1|2|10| Texto «la recta describe», jamás promesa de ganar dinero por conectarse |
| Diagnósticos y límites |1|2|2|2|1|2|10| Explicar heterocedasticidad/influencia y distinguir EE de SER |

Condiciones transmitidas al orquestador: mantener población y ponderación visibles cerca de cifras; glosario simple de mediana; ingreso ausente no equivale a cero; selector de tramos no afecta modelo global; ejemplos de diferencias no son recomendaciones de horas óptimas; no destacar correlaciones redundantes sin explicación.

## Ronda2 — revisión de aplicación

Estado: REVISIÓN ESTÁTICA DE APP REAL; CSS y navegador pendientes. Se leyó App.tsx, tipos y artefacto real. La validación en navegador y capturas corresponde al orquestador; no se acredita como ejecutada a partir de lectura estática.

La aplicación responde al propósito general: habla de internet e ingreso, explica quiénes integran la muestra, señala junio/julio, define mediana y conserva ceros. El selector declara qué cambia y qué permanece fijo. La sección avanzada distingue asociación de ganancia causal, EE de SER y diferencias ajustadas de predicciones individuales.

| Elemento real | C | P | R | E | M* | A | Total | Revisión |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Principal ingreso/muestra |2|2|2|2|1|2|11| PASS contenido; móvil pendiente |
| Distribuciones |2|2|2|2|0|2|10| Contenido fiel; legibilidad de ejes exige navegador |
| Comparador de tramos |2|2|2|2|1|2|11| Alcance del control declarado; valores/N precisos |
| Selección de muestra |2|2|2|2|1|2|11| Distingue ausente de0; no generaliza |
| Metodología/pesos |1|2|2|2|1|2|10| Corregir etiqueta «sin ponderar...Pearson ponderado» |
| Resultados e incertidumbre |2|2|2|2|1|2|11| Tabla EE/IC/p y definición; definirUPM |
| Diagnósticos/causalidad |2|2|2|2|1|2|11| Crítica explícita y límites defendibles |

*M es puntuación provisional por lectura estática, no prueba móvil. Los componentes superan7/12 en contenido; el pase funcional está condicionado a corregir errores de carga/navegación registrados en08-ux y ejecutar navegador. Hallazgos enviados al agente frontend. No se encontraron cifras inventadas ni promesas causales en la aplicación revisada.

## Cierre de ronda2 tras correcciones

Estado: **PASS de contenido y revisión estática**. La claridad de metodología/pesos sube de 1 a 2 al etiquetar Spearman sin ponderar y Pearson con fexp explícitamente. Se define UPM y se añade la referencia de últimos 12 meses. La pregunta de horas ahora dice «este grupo», evitando sugerir que describe a toda la población.

La aplicación conserva una pregunta por gráfico, unidades y N, tablas alternativas y explicaciones del significado de los resultados. No se recomienda eliminar ninguna de las cuatro tarjetas EDA: distribución horaria, comparación de ingresos por horas, distribución monetaria y selección responden preguntas diferentes. El modelo técnico explica por qué una asociación estadísticamente significativa puede coexistir con baja capacidad descriptiva y ausencia de identificación causal.

El agente frontend corrigió los problemas funcionales y visuales indicados en la revisión; el código fue releído. La puntuación móvil continúa provisional hasta las comprobaciones del orquestador en navegador. No hubo usuarios reales ni entrevistas; ambas rondas son simulación crítica documentada.

## Evidencia visual de cierre
Orquestador inspeccionó capturas reales de Chromium (exploración escritorio claro y móvil claro/oscuro; modelo escritorio oscuro). Se conservan jerarquía, tramos, fuentes y avisos en móvil; no se detectó recorte global. La revisión sigue siendo simulación crítica de rol, no estudio con usuarios. Ver evidencia y suite en10-qa.md.
