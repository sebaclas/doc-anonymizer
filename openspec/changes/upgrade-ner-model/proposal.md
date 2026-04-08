## Why

El modelo NER actual (`xx_ent_wiki_sm`) es un modelo multilingüe de tamaño small entrenado con datos de Wikipedia. Si bien es rápido y tiene cobertura multilingüe, genera una cantidad significativa de falsos positivos en documentos legales/contractuales en español, donde muchos términos capitalizados (como nombres de procedimientos, cláusulas, y conceptos legales) son incorrectamente clasificados como entidades.

Se necesita evaluar modelos NER más potentes para reducir falsos positivos, manteniendo la capacidad multilingüe y la viabilidad de ejecución offline en CPU.

## What Changes

- Evaluar y seleccionar un modelo NER con menos falsos positivos, priorizando capacidad multilingüe.
- Actualizar la lista `_MODEL_CANDIDATES` en `ner.py` con el nuevo modelo preferido.
- Expandir y refinar la lista `_STOPWORDS` con términos legales/contractuales más comunes.
- Agregar filtros de confianza (score threshold) si el modelo lo soporta.
- Permitir selección de modelo desde configuración (sin hardcodear un solo modelo).
- Documentar el benchmark de modelos evaluados.

## Capabilities

### New Capabilities

- `ner-model-config`: Capacidad de seleccionar el modelo NER desde configuración.
- `confidence-filtering`: Filtrado de entidades NER por score de confianza mínimo.

### Modified Capabilities

- `entity-detection`: El modelo por defecto cambia para reducir falsos positivos.
- `stopwords-filter`: Lista de stopwords expandida con vocabulario legal/contractual.

## Impact

- `anonymizer/detectors/ner.py`: Modelo por defecto, _STOPWORDS, threshold de confianza.
- `anonymizer/config.py`: Configuración de modelo NER.
- `requirements.txt`: Si se cambia de framework NER (poco probable dado que spaCy funciona bien).
- Tamaño del .exe: podría crecer si se usa modelo `_md` o `_lg` (~40MB-440MB).
- `STACK.md`: Actualizar con el modelo seleccionado.
