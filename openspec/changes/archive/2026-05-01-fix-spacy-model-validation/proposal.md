## Why

Al compilar el ejecutable distributable con PyInstaller, los modelos de spaCy embebidos dependen de qué modelos están instalados en el `.venv` al momento del build. Cuando el entorno cambia (se desinstala/reemplaza un modelo), el `settings.json` del usuario puede quedar con referencias a modelos inexistentes, y el mensaje de error que guía al usuario queda desactualizado. Esto produce la apariencia de un bug crítico ("el modelo no existe") que antes funcionaba correctamente.

## What Changes

- **`anonymizer/detectors/ner.py`**: Actualizar el mensaje de error en `_load_model()` para reflejar el modelo actualmente instalado (`es_core_news_lg`) y guiar correctamente al usuario.
- **`anonymizer/config.py`**: Agregar lógica de validación en `Settings.load()` que descarte de `ner_models` cualquier modelo que no esté instalado en el entorno en ejecución, con log de advertencia por cada modelo omitido.

## Capabilities

### New Capabilities

- `ner-model-env-validation`: Al cargar la configuración, el sistema valida que cada modelo en `ner_models` esté disponible en el entorno y elimina silenciosamente (con log) los que no existen, garantizando que el ejecutable compilado no falle por modelos fantasma en el `settings.json` del usuario.

### Modified Capabilities

- `entity-detection`: El requisito "AI NER Detection" hace referencia a `xx_ent_wiki_sm` como modelo hardcoded. Debe actualizarse para reflejar que el modelo activo se determina en runtime por el primero disponible en la lista de configuración.
- `configuration-management`: El requisito de "Carga de Ajustes" debe extenderse con un escenario de limpieza de modelos inválidos.

## Impact

- `anonymizer/detectors/ner.py`: Modificación menor (texto del mensaje de error).
- `anonymizer/config.py`: Modificación en `Settings.load()` para filtrar modelos no instalados.
- `openspec/specs/entity-detection/spec.md`: Actualización del requisito NER.
- `openspec/specs/configuration-management/spec.md`: Nuevo escenario de validación.
- Sin cambios de API ni breaking changes. Retrocompatible con `settings.json` existentes.
