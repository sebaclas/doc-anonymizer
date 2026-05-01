## Context

El proyecto usa spaCy para detección de entidades nombradas (NER). Los modelos se listan en `config.py → DEFAULT_NER_MODELS` y se persisten en `settings.json` del usuario en `%APPDATA%\doc-anonymizer\`. Al compilar con PyInstaller, solo el modelo explícitamente incluido en el `.spec` queda embebido. Si el `settings.json` heredado del usuario lista modelos que no están en el ejecutable, `ner.py` lanza un `RuntimeError` con un mensaje de error que sugiere instalar modelos que ya no son los relevantes.

Estado actual:
- `ner.py` itera `current_settings.ner_models` y hace `spacy.load()` por cada uno; si ninguno carga, lanza excepción con mensaje hardcoded que menciona `xx_ent_wiki_sm` y `es_core_news_sm`.
- `config.py` no valida si los modelos de la lista están realmente instalados antes de guardarlos/usarlos.
- El `.spec` ya fue corregido para incluir `es_core_news_lg`.

## Goals / Non-Goals

**Goals:**
- Filtrar en `Settings.load()` cualquier modelo de `ner_models` que no esté disponible en el entorno de ejecución actual, loggueando una advertencia por cada uno omitido.
- Actualizar el mensaje de error en `ner.py` para ser dinámico (lista los modelos que intentó) en lugar de sugerir nombres hardcoded.
- Mantener retrocompatibilidad total con `settings.json` existentes.

**Non-Goals:**
- Descargar o instalar modelos automáticamente.
- Cambiar la lógica de carga lazy del modelo en `ner.py`.
- Modificar la estructura de `settings.json` o agregar nuevas claves.

## Decisions

### D1: Filtrar modelos en `Settings.load()`, no en `ner.py`

**Decisión**: La validación ocurre al cargar la configuración, no al intentar usar el modelo.

**Alternativa considerada**: Detectar en `ner.py._load_model()` qué modelos están disponibles antes de iterar.

**Rationale**: Centralizar la validación en la capa de configuración respeta la separación de responsabilidades. `ner.py` ya tiene su lógica correcta (iterar y fallar gracefully); agregarle responsabilidad de inspección del entorno lo acopla con spaCy de formas no deseadas. Además, filtrar en `load()` significa que `current_settings.ner_models` siempre refleja solo modelos usables, lo cual beneficia también a la UI (si en el futuro muestra qué modelos están activos).

### D2: Usar `spacy.util.get_installed_models()` para la validación

**Decisión**: Llamar a `spacy.util.get_installed_models()` en `Settings.load()` para obtener la lista de modelos disponibles y hacer intersección.

**Alternativa considerada**: Intentar `spacy.load(model)` por cada modelo y capturar `OSError`.

**Rationale**: `get_installed_models()` es O(1) (lectura de paquetes instalados) vs. cargar cada modelo en memoria al arranque, que sería muy costoso. No queremos cargar el modelo en el momento de leer la configuración.

**Riesgo aceptado**: Si spaCy cambia la API de `get_installed_models()` en versiones futuras, la validación silenciaría modelos válidos. Mitigación: wrappear en try/except — si falla la API, omitir el filtro y dejar que `ner.py` maneje el error como antes.

### D3: Mensaje de error dinámico en `ner.py`

**Decisión**: El `RuntimeError` en `_load_model()` lista los modelos que intentó en lugar de sugerir nombres hardcoded.

**Rationale**: El mensaje hardcoded `xx_ent_wiki_sm` era correcto cuando se escribió pero se desactualizó. Un mensaje dinámico nunca puede quedar stale.

## Risks / Trade-offs

- **[Riesgo] Filtrado vacía toda la lista**: Si ningún modelo instalado coincide con `ner_models`, la lista queda vacía y `ner.py` fallará igual. → Mitigación: loggear un `WARNING` crítico al detectar lista vacía post-filtrado, y el mensaje de error final en `ner.py` sigue siendo claro.
- **[Trade-off] Importar spaCy en `config.py`**: El módulo de configuración adquiere una dependencia implícita en spaCy. → Aceptable porque el proyecto ya depende de spaCy centralmente; si spaCy no está disponible el app no funciona de ningún modo.
- **[Riesgo] Overhead de import en startup**: `spacy.util` se importa al cargar `config.py`. → Negligible; `spacy.util` es liviano y no carga modelos.
