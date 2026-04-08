## ADDED Requirements

### Requirement: Carga de Ajustes desde JSON
La aplicación DEBE cargar sus parámetros operativos (modelos NER, stopwords, umbrales y rutas) desde el archivo de configuración `settings.json` ubicado en el directorio de usuario.

#### Scenario: Carga exitosa de modelos NER
- **WHEN** el archivo `settings.json` define una lista personalizada de modelos en la sección `ner.models`
- **THEN** la aplicación intenta cargar únicamente esos modelos en el orden especificado

#### Scenario: Gestión de archivo inexistente
- **WHEN** la aplicación se inicia y no encuentra el archivo `settings.json`
- **THEN** el sistema carga sus valores por defecto internos y genera automáticamente un archivo `settings.json` base en el directorio del usuario

### Requirement: Mezcla de Ajustes (Deep Merge)
El sistema DEBE realizar una mezcla de los ajustes cargados con los valores por defecto, de modo que si falta una clave en el archivo, se utilice el valor predeterminado.

#### Scenario: Configuración parcial de umbrales
- **WHEN** el archivo de configuración especifica un `fuzzy_threshold` de `90.0` pero no define la lista de `stopwords`
- **THEN** la aplicación utiliza el nuevo umbral de `90.0` y la lista de `stopwords` interna por defecto

### Requirement: Ruta de Base de Datos Dinámica
El sistema DEBE utilizar la ruta de la base de datos de entidades especificada en la configuración.

#### Scenario: Cambio de ubicación de DB
- **WHEN** se modifica la ruta `paths.database` en la configuración
- **THEN** la aplicación guarda y consulta las entidades conocidas en la nueva ubicación especificada
