## Why

Muchos parámetros críticos del sistema (rutas de bases de datos, modelos de spaCy, umbrales de coincidencia difusa y listas de palabras prohibidas) están actualmente hardcodeados en el código fuente. Esto dificulta que el usuario final personalice la herramienta, limita la adaptabilidad a diferentes dominios lingüísticos y complica el mantenimiento y despliegue multiplataforma.

## What Changes

- **Centralización de Configuración**: Creación de un sistema de gestión de ajustes basado en un archivo externo (JSON o YAML).
- **Modelos NER Dinámicos**: Posibilidad de configurar la lista y orden de preferencia de los modelos de spaCy a cargar.
- **Filtrado Personalizable**: Extracción de las `STOPWORDS` de NER a la configuración para permitir ajustes según el dominio (legal, médico, contable).
- **Rutas Configurables**: Permitir la definición de rutas para la base de datos de entidades conocidas y el archivo de patrones personalizados.
- **Parámetros Algorítmicos**: Mover el umbral de `fuzzy_threshold` a la configuración global.
- **Persistencia**: Implementación de una jerarquía de carga: Valores por defecto -> Archivo de configuración del usuario -> Variables de entorno (opcional).

## Capabilities

### New Capabilities
- `configuration-management`: Capacidad de cargar, validar y persistir los ajustes de la aplicación desde un archivo externo, permitiendo cambios de comportamiento sin modificar el código.

### Modified Capabilities
- (Ninguna)

## Impact

- **Módulos Afectados**: `anonymizer/config.py`, `anonymizer/detectors/ner.py`, `anonymizer/detectors/patterns.py`, `anonymizer/known_entities.py`, `anonymizer/gui.py`, `anonymizer/cli.py`.
- **Dependencias**: Se evaluará la inclusión de `PyYAML` o `pydantic` para una gestión de configuración más robusta.
- **Compatibilidad**: Se deben mantener los defaults actuales para asegurar que la aplicación siga funcionando "out of the box" si no existe el archivo de configuración.
