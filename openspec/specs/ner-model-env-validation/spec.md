## ADDED Requirements

### Requirement: Validación de Modelos NER al Cargar Configuración
Al cargar `settings.json`, el sistema DEBE validar que cada modelo listado en `ner_models` esté instalado en el entorno de ejecución actual. Los modelos no disponibles DEBEN ser eliminados de la lista activa con un log de advertencia. Si la validación falla por error interno (e.g., API de spaCy no disponible), el sistema DEBE omitir el filtrado y continuar con la lista original.

#### Scenario: Modelos inválidos en settings.json son filtrados
- **WHEN** el archivo `settings.json` contiene `ner_models: ["xx_ent_wiki_sm", "es_core_news_lg"]` y solo `es_core_news_lg` está instalado
- **THEN** el sistema carga la configuración con `ner_models: ["es_core_news_lg"]` y registra un WARNING indicando que `xx_ent_wiki_sm` no fue encontrado

#### Scenario: Lista queda vacía tras el filtrado
- **WHEN** todos los modelos en `ner_models` son inválidos
- **THEN** el sistema carga con lista vacía, registra un WARNING crítico, y al intentar usar NER se lanza un error descriptivo listando los modelos que se intentaron

#### Scenario: Error en la API de validación
- **WHEN** `spacy.util.get_installed_models()` lanza una excepción
- **THEN** el sistema omite el filtrado, conserva la lista original, y registra un WARNING indicando que la validación fue omitida
