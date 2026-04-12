## MODIFIED Requirements

### Requirement: Interfaz Gráfica (GUI) para usuarios finales
El sistema DEBE poseer una interfaz de escritorio standalone en `anonymizer/gui.py` usando `customtkinter` y un tema visual oscuro estandarizado.

#### Scenario: Interacción visual completa con sugerencias de pseudónimos
- **WHEN** un usuario no técnico abre la aplicación y corre el análisis NER/Regex
- **THEN** el Excel generado para auditar las detecciones SHALL incluir sugerencias automáticas de pseudónimos para todas las nuevas entidades encontradas.
- **AND THEN** puede generar el documento de salida en un solo click usando estas sugerencias o editándolas.

### Requirement: Generación de binarios multi-SO
El flujo DEBE mantener scripts (`build_exe.py` y `AnonymizerPro.spec`) para invocar a `pyinstaller` y generar un binario autocontenido para distribución off-grid.

#### Scenario: Building Standalone App
- **WHEN** el desarrollador quiere lanzar una versión portatil
- **THEN** utiliza la receta de `PyInstaller` que incluye de forma embebida `spaCy` y sus modelos para que corra el motor analítico sin dependencias en el sistema operativo cliente.
