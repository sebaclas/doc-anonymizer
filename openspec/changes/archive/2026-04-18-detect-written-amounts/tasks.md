## 1. Setup & Config

- [x] 1.1 Modificar las dependencias del proyecto (`pyproject.toml` o similar) agregando el paquete `text2num`.
- [x] 1.2 Evaluar y aplicar cambios en `anonymizer/models.py` si es estrictamente necesario añadir `AMOUNT` al Enum `EntityType`, o en su defecto validar el mapeo a `CUSTOM`.

## 2. Core Detection Module

- [x] 2.1 Crear un nuevo archivo `anonymizer/detectors/amounts.py`.
- [x] 2.2 Escribir la funcionalidad base invocando al parser tolerante de `text2num` (usando "es" por defecto) para escanear `doc.full_text`.
- [x] 2.3 Traducir las iteraciones o matches extraídos de `text2num` a instancias del dataclass `Entity` que devuelva un listado compatible con la arquitectura actual.

## 3. Pipeline Integration

- [x] 3.1 En `anonymizer/detectors/detector.py`, importar el módulo creado.
- [x] 3.2 Integrar la nueva llamada en `detect_all(doc, ...)` y fusionar las _entities_ resultantes en conjunto con `ner_entities` y `regex_entities` antes de enviarlos a `_deduplicate()`.

## 4. Quality & Build

- [x] 4.1 Crear un set de test rápido que compruebe la detección exitosa de montos como "Un mil doscientos pesos" u "ochenta días".
- [x] 4.2 Refrescar un build local de PyInstaller (usando el actual `AnonymizerPro.spec`) para garantizar que los artefactos `.pyd`/rutinas Rust subyacentes de la librería hayan sido descubiertos y empaquetados.
