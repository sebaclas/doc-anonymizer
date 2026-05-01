## 1. Validación de modelos en config.py

- [x] 1.1 Agregar función `_filter_installed_ner_models(models: list[str]) -> list[str]` en `config.py` que use `spacy.util.get_installed_models()` para filtrar modelos no disponibles, con manejo de excepción si la API falla
- [x] 1.2 Llamar a `_filter_installed_ner_models()` dentro de `Settings.load()` después de construir la instancia y antes de retornarla, loggueando WARNING por cada modelo omitido
- [x] 1.3 Verificar que si la lista queda vacía se registre un WARNING adicional de nivel crítico

## 2. Mensaje de error dinámico en ner.py

- [x] 2.1 Modificar el `RuntimeError` en `_load_model()` para que el mensaje liste los modelos intentados dinámicamente en lugar del texto hardcoded con `xx_ent_wiki_sm` y `es_core_news_sm`

## 3. Tests

- [x] 3.1 Agregar test en `tests/` que verifique que `Settings.load()` filtra correctamente un modelo inválido de `ner_models` (mock de `spacy.util.get_installed_models`)
- [x] 3.2 Agregar test que verifique el comportamiento cuando `get_installed_models()` lanza excepción (la lista original se conserva)
- [x] 3.3 Agregar test que verifique que el `RuntimeError` en `ner._load_model()` contiene los nombres de los modelos intentados

## 4. Verificación

- [x] 4.1 Correr `pytest tests/` y confirmar que todos los tests pasan
- [x] 4.2 Verificar manualmente que con `.venv` activo, `python -m anonymizer.gui` arranca sin error de spaCy

