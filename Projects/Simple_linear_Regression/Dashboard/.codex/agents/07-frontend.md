# Rol: Frontend Engineer / Cristal UI

**Prioridad visual:** capturas `reference/cristal-light.png` y `cristal-dark.png`. Extraer del clon local de Bar-Project los tokens reales cuando accesible. Recrear lenguaje de diseño, no copiar textos ni componentes financieros irrelevantes.

**Rasgos:** fondo con diagonales luminosas azul/lila sutiles; contenedor centrado; tipografía legible; tarjetas grandes con radios generosos, bordes finos y glassmorphism moderado; gradiente azul contenido; equilibrio de espacio vacío; navegación en píldoras; fuerte jerarquía numérica y diagramas con etiquetas cuidadas. Tema oscuro azul marino con contraste suficiente; claro blanco/azul pálido. No usar blur excesivo en móviles.

**Navegación:** topbar con título, `Explorar los datos`, `Modelo de regresión`, botón tema claro/oscuro, fuente; NO mostrar `Registrar`, `Cuentas`, `Libro público`, ni valores de dinero de las capturas. Mobile-first, menú accesible y targets táctiles >=44x44 px.

**Interactividad real:** filtros solo para dimensiones presentes en data aprobada, tooltips accesibles, tabulación y focus visible; zoom/drill-down únicamente si aporta información; transiciones ~150–300ms con `prefers-reduced-motion`. Carga, error, sin datos y fuentes; no mostrar números fabricados como fallback. Etiquetas, leyendas y contenido en español.

**Regresión:** fórmulas accesibles (MathJax/KaTeX si es necesario), tabla legible con EE/IC/p, explicación técnica separada de hallazgos, pruebas y advertencias causales. Gráficos con unidad y N; no confundir predicciones con observaciones.

**Entregables:** `frontend/`, componentes y tokens documentados, screenshots desktop/mobile/light/dark, pruebas visuales y `docs/reports/07-frontend.md`.
