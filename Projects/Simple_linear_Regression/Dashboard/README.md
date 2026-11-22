# Grupo 2 · Internet e ingreso laboral

Dashboard en español de ENEMDU TIC, julio de 2025. Autores: **Jefferson Cueva, Giorge Steven y Jenifer Fernandez**.

## Publicar sin instalar nada

El paquete compilado se entrega en `entrega/grupo-2-netlify.zip`. Arrastrarlo a [Netlify Drop](https://app.netlify.com/drop) genera una dirección de Netlify. Ver [instrucciones de publicación](entrega/COMO-PUBLICAR.md). El ZIP incluye JavaScript, estilos, fuentes matemáticas y agregados; no necesita backend ni credenciales. La versión v2 no se publica en el dominio anterior de ChatGPT.

## Qué incluye

- **Explorar:** concentración conjunta de horas e ingreso, distribuciones, cajas con percentiles, curva acumulada y selección de muestra. Color, animaciones y explicaciones breves.
- **Modelo:** fórmulas KaTeX, MCO y covarianza por UPM, tabla completa de inferencia, laboratorio con dos entradas numéricas y banda de media, residuos, Q–Q, dispersión, errores estándar e influencia.
- **Datos:** tablas agregadas con búsqueda, orden, paginación y descargas CSV/JSON.

Sólo modo claro, ancho amplio, texto legible y movimiento reducido cuando el sistema lo solicita. Fuente y metodología desplegables. Ningún escenario del simulador identifica por sí mismo un efecto causal.

## Desarrollo local

Requiere Node 22+ y Python 3.12+. Desde `Dashboard`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
.venv/bin/python backend/pipeline.py --download
cd frontend
npm ci
npm run build
cd ..
.venv/bin/python backend/server.py
```

Abrir http://127.0.0.1:8000. Para desarrollo de interfaz: `npm run dev` en frontend. El JSON real se incluye; no se descarga Hugging Face por visita. El servidor stdlib sólo expone build y agregados, nunca las fuentes individuales.

## Comprobar y empaquetar

Desde `Dashboard`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s backend/tests -v
cd frontend
npm run typecheck
npm run build
npx playwright install --with-deps chromium
npm run test:e2e
cd ..
python3 tools/package_netlify.py
```

Las pruebas Python requieren las fuentes fijadas bajo `data/source` (`pipeline.py --download` una vez). El navegador de pruebas puede configurarse con `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`; Playwright inicia/detiene un servidor loopback temporal. El empaquetado verifica fuente, recursos y ausencia de archivos ajenos al build.

## Procedencia

HF `Jefferson7c/Econometrics`, revisión `d8a5794b62c4e5ec1f7f11b41c28d4ac82d47698`, idéntica al Parquet local auditado. Muestra: **9.881 ocupados de 15 años o más, usuarios diarios con horas e ingreso disponibles**. Ingreso referido a junio de 2025; encuesta de julio. MCO sin ponderar con EE agrupados por 1.286 UPM y t de 1.285 grados de libertad; no reproduce el diseño completo de encuesta ni identifica causalidad.

[Contrato](docs/api-contract.md) · [Métricas y cálculos](docs/metric-registry.md) · [Revisión independiente v2](docs/reports/v2-review.md) · [Decisiones](docs/decision-log.md). Las instrucciones originales están en `.codex/`. `DataScience` se mantiene sólo lectura.
