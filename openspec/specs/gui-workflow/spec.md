# gui-workflow Specification

## Purpose
Añadido durante la auditoría de limpieza. Documenta y oficializa el uso de la app de escritorio desarrollada con CustomTkinter para la interacción con usuarios finales sin conocimientos de consola.

## Requirements
### Requirement: Interfaz Gráfica (GUI) para usuarios finales
El sistema DEBE poseer una interfaz de escritorio standalone en `anonymizer/gui.py` usando `customtkinter` y un tema visual oscuro estandarizado.

#### Scenario: Interacción visual completa
- **WHEN** un usuario no técnico abre la aplicación
- **THEN** puede elegir un archivo .pdf o .docx, correr el análisis NER/Regex, cargar un Excel visual para auditar las detecciones, y generar el documento de salida en un solo click.
- **AND THEN** el Excel generado por la detección DEBE contener sugerencias automáticas de pseudónimos (ej: Persona1) para todas las entidades nuevas no encontradas en la BD.

### Requirement: Generación de binarios multi-SO
El flujo DEBE mantener scripts (`build_exe.py` y `AnonymizerPro.spec`) para invocar a `pyinstaller` y generar un binario autocontenido para distribución off-grid (ej. sin entorno Python local).

#### Scenario: Building Standalone App
- **WHEN** el desarrollador quiere lanzar una versión portatil
- **THEN** utiliza la receta de `PyInstaller` que incluye de forma embebida `spaCy` y sus modelos para que corra el motor analítico sin dependencias en el sistema operativo cliente.
