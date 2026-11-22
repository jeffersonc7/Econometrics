# Backend
Autor: orquestador adoptando rol 06. Fecha: 2026-11-16. Estado: PASS local.

Implementados `backend/pipeline.py` (fuentes fijadas, hashes obligatorios, réplica selección y MCO, agregados validados, escritura atómica) y `backend/server.py` (stdlib, sólo lectura, API y build estático, mensajes españoles y headers). No dependencia de red durante reproducción con fuentes disponibles ni durante requests. CLI `--download` descarga únicamente dos fuentes de commit fijo y verifica SHA256. Fuentes y entornos ignorados por Git.

`PYTHONDONTWRITEBYTECODE=1 python3 backend/pipeline.py`: PASS, N9881 y pendiente coincide con notebook. Salida `frontend/public/data/dashboard.json`, menos de24KB. No registros individuales ni identificadores personales.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s backend/tests -v`:12 pruebas PASS (2026-11-16). Primer intento sandbox:8 pruebas de pipeline PASS y socket denegado al iniciar servidor; repetición con permiso de red local PASS12. Tests cubren réplica, bins/ceros, sensibilidad, denominadores, fuentes corruptas/ausentes, reproducibilidad sin timestamp, contenido público, API/static, headers,404, bloqueo escrituras, HEAD y503.

Revisión independiente econometría:66 comparaciones a tolerancia1e-12 PASS contra fuente original (ver03). Riesgos: no inferencia de diseño completo, códigos especiales heredados sin catálogo exhaustivo; el servidor es portable/local y TLS debe terminarlo el hosting futuro. No despliegue realizado.

Revisión posterior: se añadió `backend/contract.py` para validar estructura y conservación antes de servir datos o health. JSON incompleto/corrupto devuelve503; ruta NUL devuelve404. Los12tests pasaron de nuevo con estas regresiones incorporadas; auditor revalidó cuatro casos independientemente.
