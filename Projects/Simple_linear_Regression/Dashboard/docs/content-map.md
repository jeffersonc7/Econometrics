# Mapa editorial y visual
Autor: frontend / storytelling con revisión cruzada de auditoría y econometría. Fecha: 2026-11-16. Estado: implementado; revisión de navegador a cargo de QA.

## Mensaje y dominio
El sitio estudia asociación entre uso diario de internet e ingreso laboral mensual. Dominio fijo: ocupados de 15 años o más, uso diario, horas e ingreso observados. Levantamiento julio de 2025, ingreso junio de 2025; frecuencia de internet declarada para los últimos 12 meses. No estimación de todo Ecuador ni causalidad.

## Explorar los datos
| Elemento | Pregunta | Evidencia / unidad / denominador | Qué aporta y límite |
|---|---|---|---|
| Hero mediana | ¿Qué ingreso divide al grupo en mitades? | overview.income_median; USD mensuales; n9881 sin ponderar | Contexto intuitivo; explica las dos mitades y compara media. Dominio visible. |
| Horas diarias | ¿Cuántas horas declara este grupo? | hours; personas por hora, base9881; sin ponderar; pt3b diaria | Distribución sin mezclar frecuencias. 0 significa menos de una hora. Tooltip de foco/puntero y tabla. |
| Tramos e ingreso | ¿Difieren ingresos según tramo de horas? | groups, ingrl, media/mediana por tramo y n de cada grupo, sin ponderar | Comparación descriptiva; selección cambia solo esta tarjeta. No diferencia para una misma persona. |
| Ingreso | ¿Por qué media y mediana difieren? | income bins, conteos de personas; base9881; USD; sin ponderar | Cola derecha con ceros y extremos conservados. Bins desiguales son categorías/conteos, no densidad. |
| Selección | ¿Quiénes quedan fuera? | selection, etapas27509/13299/10091/9881 y availability denominador13299 | Delimita selección; falta de respuesta no es cero. No representa todos los ocupados. |
| Interpretación | ¿Qué aprendimos? | Pearson sin ponderar de EDA, con nota de dispersión | Relación positiva débil y cautela causal. Enlace al modelo. |
| Metodología | ¿Cómo leer mediana, pesos y período? | medias con fexp y correlaciones etiquetadas; periodo fuente | Distingue pesos descriptivos de diseño completo. Glosario contextual en lenguaje cotidiano. |

## Modelo de regresión
| Elemento | Pregunta | Evidencia | Límite |
|---|---|---|---|
| Hero beta | ¿Con qué diferencia se asocia una hora diaria? | model.coefficients[1], IC95%, N, R², UPM | Asociación entre personas, no intervención ni ingreso garantizado. |
| Ecuaciones y tabla | ¿Qué modelo se estima y con qué precisión? | MCO sin ponderar, EEclusterUPM/use_t, IC/t/p, SER | Variable X única; sin controles omitidos. Test bilateral no prueba causalidad. |
| Recta y delta | ¿Cómo interpretar ΔX? | fitted y delta1–3 por beta/IC, rango0..18 | Diferencia ajustada e ICmedio, no predicción individual. No reestima ni extrapola. |
| Sensibilidad | ¿Cuánto pesan extremos? | Cook>4/n376; muestra9505 y pendiente/IC réplica | Diagnóstico secundario, no elimina registros ni implica errores. |
| Supuestos | ¿Qué sabemos y qué no? | p tendencia residuos², nUPM/hogar/estrato, varX, R² | Distingue exogeneidad no comprobable, dependencia entre grupos y diseño incompleto. |
| Causalidad | ¿Puede hablarse de efecto? | Especificación observacional sin identificación | Respuesta explícita negativa; omitidas, selección y causalidad inversa. |

## Interacciones y fuentes
Navegación por hash con historial, foco al contenido y vuelta al inicio; tema manual persistente o preferencia del sistema; controles accesibles con foco visible. Gráficos SVG con títulos/descripción y tabla equivalente; readout responde a foco/puntero. Agregados generan textos, sin estadísticas de reemplazo. Loading/error/reintento/empty sin cifras inventadas. Cada visual lleva fuente, n, unidad y etiqueta de ponderación; pie común expone revisión, hashes, generación, fuentes INEC y reproducción.

## Diseño
Tokens son estimación visual de capturas Cristal claras/oscuras, no código BarProject: fondos azul pálido/azul marino, haces diagonales, glass moderado, bordes luminosos, gradientes de barras, tipografía de sistema, radios26–32px, navegación en píldoras. No activos financieros. SVG ajusta viewBox al ancho de tarjeta mediante ResizeObserver, con tipografía11px real tanto móvil como tablet. Ejes de ingreso usan límites inferiores abreviados (k=mil), intervalos completos en readout/tabla.
