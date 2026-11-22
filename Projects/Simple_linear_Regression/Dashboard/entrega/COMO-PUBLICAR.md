# Publicar Grupo 2 en Netlify

1. Abre https://app.netlify.com/drop .
2. Arrastra `grupo-2-netlify.zip` a la zona de publicación.
3. Abre el enlace que te entrega Netlify (dominio `netlify.app`).

El ZIP ya contiene el sitio compilado. No requiere comandos, backend, token de Hugging Face ni variables de entorno. Si Netlify pide iniciar sesión o reclamar el sitio para conservarlo y administrarlo, hazlo con tu cuenta.

Para volver a generar el paquete tras cambios: ejecutar `npm run build` en `Dashboard/frontend` y después `python3 Dashboard/tools/package_netlify.py` desde la raíz del proyecto. El ZIP contiene sólo recursos públicos y agregados: no subas `DataScience`, `Dashboard/data/source` ni la carpeta completa del proyecto.

Guía oficial: https://docs.netlify.com/start/quickstarts/netlify-drop-quickstart/
