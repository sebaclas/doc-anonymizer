## Context

`ner.py` usa `xx_ent_wiki_sm` como modelo preferido, con fallback a `es_core_news_sm` y `en_core_web_sm`. El modelo multilingüe wiki detecta entidades PER, ORG, LOC/GPE pero con alta tasa de falsos positivos en texto legal español. La lista `_STOPWORDS` tiene ~60 palabras pero los documentos legales tienen vocabulario mucho más amplio de términos que se capitalizan sin ser entidades propias.

El principal problema no es que el modelo no detecte entidades (recall), sino que detecta demasiadas cosas que no son entidades reales (baja precisión). La solución debe balancear:
1. Reducir falsos positivos sin perder entidades reales.
2. Mantener capacidad multilingüe (docs en español, inglés, y mixtos).
3. Funcionar offline en CPU con tiempos aceptables.

## Goals / Non-Goals

**Goals:**
- Evaluar `es_core_news_md` y `es_core_news_lg` contra el modelo actual en documentos de prueba reales.
- Evaluar combinación de modelos: `xx_ent_wiki_sm` (multilingüe) + `es_core_news_md` (español) con intersección de resultados.
- Implementar threshold de confianza configurable para filtrar entidades con baja certeza.
- Expandir `_STOPWORDS` con al menos 50 términos legales/contractuales adicionales.
- Hacer el modelo seleccionable desde `~/.doc-anonymizer/config.json` o `custom_patterns.json`.

**Non-Goals:**
- No entrenar un modelo custom (requiere datos anotados).
- No integrar modelos que requieran GPU (transformer-based como Flair o spaCy trf).
- No cambiar el framework NER (se mantiene spaCy).
- No implementar OCR ni procesamiento de PDFs escaneados.

## Decisions

**Decision 1: Estrategia de evaluación.**
Crear un benchmark con 3-5 documentos legales reales. Medir:
- True Positives (entidades reales detectadas correctamente)
- False Positives (detecciones incorrectas)
- False Negatives (entidades reales no detectadas)
Para cada modelo candidato. El modelo ganador minimiza FP sin degradar TP significativamente.

**Decision 2: Estrategia combinada de modelos (explorar).**
Opción A: Un solo modelo mejorado (ej: `es_core_news_md`).
Opción B: Dos modelos en paralelo → solo las entidades detectadas por ambos se mantienen (intersección → alta precisión).
Opción C: Un modelo + threshold de confianza ajustable.
*Decisión final:* Se tomará después del benchmark. Preparar la arquitectura para soportar cualquier opción.

**Decision 3: Threshold de confianza.**
spaCy no expone directamente un "confidence score" para NER en modelos estadísticos (los `sm/md/lg` no tienen logits accesibles). Sin embargo, se puede usar la longitud del texto y la categoría como proxy:
- Entidades de 1-2 caracteres → descartar (ya implementado: mínimo 4 chars).
- Entidades tipo PERSON con una sola palabra → marcar como baja confianza.
- Entidades tipo ORG que son genéricas → filtrar con stopwords.

**Decision 4: Configurabilidad.**
Agregar a `config.py` una función que lea el modelo preferido. Default: mantener candidatos en orden de preferencia pero actualizar el orden según resultados del benchmark.

**Decision 5: Mantener multilingüe.**
No eliminar `xx_ent_wiki_sm` de los candidatos. Si se usa un modelo español como primario, mantener el multilingüe como segundo paso para textos en otros idiomas o documentos mixtos.

## Risks / Trade-offs

- [Riesgo] `es_core_news_lg` pesa ~440MB, lo que aumentaría significativamente el tamaño del .exe.
  → Mitigación: Si `es_core_news_md` (~40MB) ofrece resultados suficientes, preferirlo.
- [Riesgo] La estrategia de intersección de modelos duplica el tiempo de procesamiento.
  → Mitigación: Solo aplicar si el beneficio en precisión lo justifica. Medir tiempos en el benchmark.
- [Riesgo] Reducir falsos positivos agresivamente podría causar que se pierdan entidades reales (false negatives).
  → Mitigación: El usuario siempre puede agregar entidades manualmente o via la DB maestra. El objetivo es reducir ruido, no eliminar toda detección.
