## ADDED Requirements

### Requirement: Limpieza de Modelos NER Inválidos en Carga de Configuración
Al cargar la configuración desde `settings.json`, el sistema DEBE eliminar de `ner_models` cualquier modelo que no esté instalado en el entorno de ejecución, garantizando que la lista activa solo contenga modelos usables.

#### Scenario: settings.json heredado con modelos desinstalados
- **WHEN** el usuario tiene un `settings.json` previo que lista `es_core_news_sm` y `xx_ent_wiki_sm`, pero el ejecutable solo trae `es_core_news_lg`
- **THEN** el sistema carga correctamente con `ner_models: ["es_core_news_lg"]` y los modelos inválidos son descartados con un log de advertencia, sin requerir intervención del usuario
