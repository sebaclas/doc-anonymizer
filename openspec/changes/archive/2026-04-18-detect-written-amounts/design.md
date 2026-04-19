## Context

AnonymizerPro utilizes spaCy for Named Entity Recognition (NER), but testing has shown that it frequently misses written amounts in natural language, such as "ciento veinticinco" or "seis millones". Estas omisiones resultan en fugas de montos visibles. Para evitar la carga de entrenar modelos NLP costosos, la librería `text2num` (con núcleo en Rust) resulta ideal porque maneja Español/Inglés de forma determinista y ultrarrápida.

## Goals / Non-Goals

**Goals:**
- Detectar frases numéricas escritas (palabras) en Español e Inglés nativamente.
- Devolver esas extracciones como objetos `Entity` estándar para que entren a la etapa manual de revisión/Excel.
- Operar 100% offline.
- Aceptar una tasa razonable de falsos positivos en pos de redundancia estricta.

**Non-Goals:**
- No se reemplazarán montos automáticamente sin pasar por la validación manual / planilla.
- No reemplaza la detección actual por expresiones regulares de símbolos matemáticos o divisas (`$5.00`), sino que la complementa atrapando la versión verbal.

## Decisions

- **Implementar `text2num` package**: Se integrará la función de tokenización / parseo de `text2num`.
  - *Rationale*: Identifica de manera determinista casos de borde y maneja ordinales y cardinales nativamente. 
  - *Alternative considered*: Usar regex pesado. Descartado por ser intratable a nivel de mantenimiento en múltiples idiomas.

- **Priorización en Pipeline de Detección**: Se correrá `text2num` como un recolector adicional dentro de `detector.detect_all`.
  - *Rationale*: Nos permite usar el mismo mecanismo de deduplicación que usa spaCy y los regex. Si el regex de DNI detecta un número, y `text2num` detecta una parte, `_deduplicate` se encargará de resolver colisiones usando el span más largo o prioritario.

- **Mapeo de Entidad**: Se inyectará a las entidades detectadas con el type `EntityType.CUSTOM` o se ampliará el Enum.
  - *Rationale*: Transparente para la UI, entrará en la columna de Entidad del Excel bajo la categorización correspondiente.

## Risks / Trade-offs

- [Risk] **PyInstaller falla en incrustar DLLs de libreria Rust** → *Mitigation*: Verificar explícitamente el empaquetado y, si falta, agregar dependencias ocultas (`hiddenimports`) en el archivo `AnonymizerPro.spec`.
- [Risk] **Ruido por palabras comunes ("un", "una")** → *Mitigation*: Avisar al usuario que estos falsos positivos son intencionales o, en el peor caso, añadir una lista de `stop_words` locales si el ruido vuelve la herramienta inoperable.
