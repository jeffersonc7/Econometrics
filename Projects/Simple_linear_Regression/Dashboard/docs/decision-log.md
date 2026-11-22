# Registro de decisiones
Autor: orquestador. Fecha: 2026-11-16.

- D01: instrucciones originales residen en `.codex/`; se conservan intactas y se usan desde esa ruta. Fuente real `../DataScience`, solo lectura.
- D02: no clon Bar Project accesible bajo `/home/zaz/Econometrics`. Capturas obligatorias como referencia; colores y tipografía serán estimaciones visuales, no extracción de código original.
- D03: reproducir modelo real MCO sin ponderación con errores cluster UPM y t, no reemplazar con WLS/HC. Dominio usuarios diarios ocupados >=15 y ambas respuestas observadas.
- D04: frontend React/TypeScript/Vite y backend Python de agregación offline + servidor opcional stdlib. Artefacto estático evita servicio de cómputo innecesario, microdatos y dependencia de HF durante carga.
- D05: gráficos no ponderados por defecto, iguales al EDA; ponderación descriptiva separada y etiquetada. Sin estimar submodelos por filtros. Tramos permiten consultar media/mediana y tamaños; modelo siempre muestra fija.
- D06: uso de skill Sites limitado al flujo local, como permite su apartado Local-only. Sin registro, sincronización, push ni despliegue. Se usan además las cinco skills del paquete del proyecto.
- D07: fuente HF confirmada pública con MIT declarada y revisión `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`; Parquet local y remoto idénticos. Limpieza completa19columnas replicada. El ODS no contiene catálogo exhaustivo de códigos; clasificación `Potentially out of scope` no equivale siempre a menor de5años.
- D08: revisión cruzada detectó JSON incompleto aceptado, health sólo comprobaba existencia y ruta NUL no manejada. Se agregó validador contrato sin dependencias científicas, health valida contenido y NUL devuelve404; regresiones probadas.
- D09: frontend corrigió abortos StrictMode, timeout, foco/scroll, pesos ambiguos, definiciónUPM, ceros gráficos y ejes móviles. ResizeObserver permite fuente de11px sin reducción de viewBox fijo; intervalos USD de ancho desigual se presentan como categorías de conteos.
- D10: navegador preinstalado sin bibliotecas nspr/nss/alsa. Se descargaron paquetes Ubuntu con permiso y extrajeron en `/tmp/cristal-browser-libs`, sin instalar en sistema. Pruebas Chromium usan LD_LIBRARY_PATH temporal. No afecta código de producción.
- D11: Axe detectó semántica dl y etiquetas accesibles incoherentes con texto visible. Corregido con estructura válida y nombres naturales; validación final14e2ePASS (36s), incluyendo Axe en ambas vistas/temas. Build/typecheckPASS y12PythonPASS. Capturas archivadas y DataScience sin cambios según15hashes.

- D12: El usuario autorizó explícitamente subir el dashboard y entregar sólo un enlace. Publicación mediante Sites, acceso público sin login. Copia aislada en published-site contiene únicamente frontend y agregados; no se subieron DataScience ni microdatos. Estado succeeded; URL y trazabilidad en published-site.json. No se modificó ni fusionó el repositorio original.

## Revisión v2 solicitada por el usuario
- Sólo modo claro, marca Grupo 2 y autores Jefferson Cueva, Giorge Steven, Jenifer Fernandez. Revoca los requisitos previos de tema dual y marca Cristal.
- EDA prioriza gráficos/color, tipografía mayor y pantalla amplia; interpretaciones de una línea. El detalle metodológico pasa a paneles plegables.
- Modelo conserva especificación auditada y añade diagnósticos agregados reproducibles, fórmulas KaTeX locales y escenario X inicial/final con controles numéricos. Fuera de0–18horas se avisa extrapolación; no se interpreta causalidad identificada.
- Se añade vista Datos de agregados descargables, sin registros identificables.
- El usuario rechaza dominio de ChatGPT y acepta subir la web por sí mismo. Descubrimiento de integraciones no mostró Netlify conectado; se preparará ZIP estático validado para Netlify Drop. No se actualizará el alojamiento anterior sin necesidad.
