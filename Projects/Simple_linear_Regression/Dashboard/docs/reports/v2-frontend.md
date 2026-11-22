# Frontend v2 · Grupo 2
Autor: agente frontend. Fecha: 2026-11-16. Estado: implementación completa y build verificado; QA navegador a cargo del orquestador.

## Rediseño autorizado
Se reemplazó totalmente el frontend previo: modo exclusivamente claro, marca GRUPO 2, ancho92vw hasta1800px, navegación Explorar/Modelo/Datos, jerarquía académica y footer Jefferson Cueva · Giorge Steven · Jenifer Fernandez. Fondos blancos, bordes suaves y cinco acentos funcionales azul/cian/violeta/coral/teal. Base16px, contenido principal15–16px y ejes12px ajustados al ancho real del contenedor. Sin textos de marca Cristal ni autenticación.

## Implementación
- `src/App.tsx`: tres vistas, métricas compactas, fuentes/metodología plegables, estados de carga/error/reintento/empty, navegación hash con foco e historial, validación del artefacto antes de render.
- `src/Charts.tsx`: concentración2D por conteos, barras de horas e ingreso, boxplotsP10/P25/P50/P75/P90 con mediana/media, CDF, ajuste con banda puntual95%, escenariosA/B, concentración residual, histogramas residuos/Cook, QQ, dispersiónresidual y forestdeEE/sensibilidad. SVG responsivo con ResizeObserver, tablas accesibles, títulos/descripciones, readoutdefoco/flechas donde corresponde.
- `src/Math.tsx`: KaTeXlocal con salidaHTML+MathML/trustfalse. Dosfórmulas principales visibles, detalleOLS/CRV1/correcciónfinita/t/IC/residuos/SER/covarianza enpanelesplegables.
- `src/types.ts`: contrato aditivo exacto, chequeosdefinitud, estructura, ICordenados,CDF[0,1],arraysnovacíos ysumasdeconteos.
- `src/styles.css`: diseño nuevo claro y mobilefirst, desktop/tablet/móvil, tipografíasManrope+DM Sansvariables empaquetadas localmente, targets≥44px,reducedmotion, animaciónreveal/trazosytransicioneshover.
- `src/format.ts`: formatos españoles; notación científica sólo para magnitudesabsurdamentegrandes(>=1e12), sin alterar valores descargables.

## Simulador
EntradasXinicial/Xfinal con números y sliders0–18paso0,1, inicial3→6. Número>18permitido conavisoExtrapolación yextensióndiscontinua; horasnegativas/vacías/aritméticano representable producenvalidaciónsinNaN. Delta negativo yceroválidos. Diferencia=beta×delta, EE=abs(delta)×EEbeta, IC=estimación±t×EE conlímitesordenados. Ŷsonmediasajustadas, noindividuosniefectocausal. Bandapuntualusa matrizcovarianzaUPMy t(G−1), dentro soporte0..18. Eje ingreso alternaUSDlineal/log1p(USD/100), todosdatosconservados.

## Datos
Tablas sóloagregadas:horas,ingresos,tramos/percentiles,concentración,coeficientes,percentiles,selección,residuos. Tabsbuscadorordenporcolumna,paginación15filas,CSVdelresultadobuscado/ordenado conBOMcomillasyprecisiónoriginal,JSONcompletodelartefacto. Ningúnidentificadorpersonal. Diccionario/trazabilidadplegados, fuentescomunesplegadas.

## Revisión cruzada
- Econometría validó fórmulasMCO/CRV1, t/IC,SER,simuladordelta±/0,QQresiduos/SER,nocausalidad ybandamedia.
- Auditoría corrigió guardasarraysvacíos, etiquetasnulasbuscador, magnitudesnuméricas, segmentaciónSpreadcuando falta11h ytargetsselect44px.
- Coordinador corrigiócopyacademic/plain,denominadorSpread(sumagruposmostrados),pruebatendenciadevarianzaconmuestracompleta,leyendacalibradaalmismocolormapqueheatmap.

## Verificación ejecutada
`npm install katex`, `npm install -D @types/katex`, `npm install @fontsource-variable/manrope @fontsource-variable/dm-sans`:correctos, sinvulnerabilidadesreportadas.
`npm run build`:PASS TypeScript+Vite,35módulos. JS549,7kB(gzip168,4),CSS71,7kB(gzip17,3), fuentesKaTeX/Manrope/DMSanslocalesenassets. AdvertenciaViteporchunk>500kB, nobloqueante. Se ejecutóbuildnuevotrascorrecciones; informeQA centralconservanavegación,Axe,screenshotsytestsE2E.

No se modificóDataScience,backend,tests,configQA,nipublic/data. No push,merge,registroSite,despliegue niURLpública creados. La distribuciónNetlifysólosepreparapororquestador.
