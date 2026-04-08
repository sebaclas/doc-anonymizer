## Context

Actualmente, la configuración está dispersa en constantes globales dentro de múltiples archivos (`ner.py`, `patterns.py`, `known_entities.py`, etc.). Esto impide ajustes rápidos y personalizados sin intervención en el código base.

## Goals / Non-Goals

**Goals:**
- Centralizar todos los parámetros en un único archivo `settings.json`.
- Permitir la modificación de modelos NER, stopwords y umbrales sin tocar el código.
- Mantener la compatibilidad con las instalaciones existentes usando valores por defecto robustos.

**Non-Goals:**
- Implementar una interfaz gráfica completa para editar todos los ajustes (solo se expondrá el archivo para edición manual o vía CLI).
- Cambiar el motor de NER (se sigue usando spaCy por ahora).

## Decisions

### 1. Formato de Archivo: JSON
- **Razón**: El proyecto ya utiliza JSON para patrones y entidades conocidas. Usar JSON evita añadir una dependencia pesada como `PyYAML`.
- **Alternativa**: YAML (descartado por ahora para mantener el core ligero).

### 2. Ubicación: Directorio de Usuario
- **Razón**: Almacenar en `~/.doc-anonymizer/settings.json` asegura que los ajustes persistan entre actualizaciones de la aplicación.

### 3. Modelo de Datos: Singleton de Configuración
- Se creará una clase `Settings` en `anonymizer/config.py` que cargue y valide los datos.
- Se usará un enfoque de "merge": los valores del archivo sobrescriben a los defaults hardcodeados.

### 4. Refactorización de Detectores
- `ner.py`: Utilizará el objeto `Settings` para obtener `model_candidates` y `stopwords`.
- `matcher.py`: Utilizará el objeto `Settings` para el `fuzzy_threshold`.

## Risks / Trade-offs

- **[Riesgo] Corrupción de JSON** → **[Mitigación]** Si el archivo JSON no es válido, la aplicación cargará los valores por defecto y mostrará un warning.
- **[Riesgo] Modelos NER no instalados** → **[Mitigación]** El sistema de carga de modelos ya maneja excepciones; se mantendrá esta lógica de fallback.
