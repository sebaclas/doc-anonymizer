## 1. Implementación del Core de Configuración

- [ ] 1.1 Crear la clase `Settings` en `anonymizer/config.py` que soporte carga de JSON y valores por defecto.
- [ ] 1.2 Implementar lógica de "merge" para asegurar que los campos faltantes en el JSON usen los defaults.
- [ ] 1.3 Asegurar la creación del directorio `~/.doc-anonymizer` y un `settings.json` base si no existen.

## 2. Refactorización de Detectores y Rutas

- [ ] 2.1 Actualizar `anonymizer/detectors/ner.py`: reemplazar constantes por lecturas de `settings`.
- [ ] 2.2 Actualizar `anonymizer/known_entities.py`: dinamizar la ruta `DB_PATH`.
- [ ] 2.3 Actualizar `anonymizer/matcher.py`: utilizar el `fuzzy_threshold` global de configuración.

## 3. Integración en CLI y GUI

- [ ] 3.1 Modificar `anonymizer/cli.py` para inicializar el singleton de configuración.
- [ ] 3.2 Modificar `anonymizer/gui.py` para inyectar los ajustes en el flujo de detección.
- [ ] 3.3 Agregar comando en CLI (o mensaje en GUI) que indique la ubicación del archivo de configuración.

## 4. Pruebas y Validación

- [ ] 4.1 Probar el cambio de un modelo de spaCy vía `settings.json` y verificar su carga.
- [ ] 4.2 Validar que la aplicación inicie correctamente sin un archivo de configuración preexistente.
- [ ] 4.3 Verificar que el filtrado de entidades respete la nueva lista de `stopwords` externa.
