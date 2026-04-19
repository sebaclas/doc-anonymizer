# amount-detection Specification

## Purpose
TBD - created by archiving change detect-written-amounts. Update Purpose after archive.
## Requirements
### Requirement: Detección de montos verbales
El sistema DEBE (SHALL) escanear el documento para buscar valores numéricos y ordinales expresados enteramente en palabras naturales (Español o Inglés) valiédose de un parser de lenguaje natural.

#### Scenario: Frase de número compuesto
- **WHEN** el texto del documento contiene "trescientos cuarenta y dos"
- **THEN** el sistema extrae todo el bloque de texto continuo como una única entidad.

#### Scenario: Transparencia hacia el proceso de revisión
- **WHEN** un número en palabras es detectado
- **THEN** la entidad es registrada junto al contexto original (5 palabras previas y posteriores) y mostrada al usuario en la planilla de mapeo, con source marcado como `text2num`.

### Requirement: Tolerancia estricta a falsos negativos (Greedy detection)
El sistema DEBE (MUST) fallar en favor de crear ruido sobre la planilla del usuario antes que omitir un número. Se asumirá que palabras ambivalentes (ej: "un", "una") serán evaluadas manualmente por el operador.

#### Scenario: Palabra de doble uso
- **WHEN** el documento dice "Aprobado por un periodo de tiempo"
- **THEN** la palabra "un" es detectada como prospecto de entidad y delegada a la grilla de revisión.

