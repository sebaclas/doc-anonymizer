## 1. Preparar benchmark de evaluación

- [ ] 1.1 Seleccionar 3-5 documentos legales/contractuales representativos como corpus de prueba.
- [ ] 1.2 Crear anotaciones gold-standard: listar manualmente las entidades reales en cada documento.
- [ ] 1.3 Crear script `tests/benchmark_ner.py` que ejecute la detección con un modelo dado y reporte TP, FP, FN.

## 2. Evaluar modelos candidatos

- [ ] 2.1 Instalar `es_core_news_md` y `es_core_news_lg` (`python -m spacy download ...`).
- [ ] 2.2 Ejecutar benchmark con `xx_ent_wiki_sm` (baseline actual).
- [ ] 2.3 Ejecutar benchmark con `es_core_news_md`.
- [ ] 2.4 Ejecutar benchmark con `es_core_news_lg`.
- [ ] 2.5 Ejecutar benchmark con combinación `xx_ent_wiki_sm` ∩ `es_core_news_md` (intersección).
- [ ] 2.6 Documentar resultados comparativos en tabla: modelo → TP, FP, FN, F1, tiempo.

## 3. Expandir filtros de stopwords

- [ ] 3.1 Analizar los falsos positivos del benchmark para identificar patrones comunes.
- [ ] 3.2 Expandir `_STOPWORDS` con términos legales/contractuales frecuentes.
- [ ] 3.3 Re-ejecutar benchmark post-expansión para medir mejora.

## 4. Implementar mejoras seleccionadas

- [ ] 4.1 Actualizar `_MODEL_CANDIDATES` con el orden óptimo según benchmark.
- [ ] 4.2 Implementar filtros adicionales basados en hallazgos del benchmark (ej: entidades de una sola palabra tipo PERSON con baja relevancia contextual).
- [ ] 4.3 Agregar configurabilidad de modelo en `config.py` → `~/.doc-anonymizer/config.json`.

## 5. Actualizar documentación y build

- [ ] 5.1 Actualizar `STACK.md` con el modelo seleccionado y rationale.
- [ ] 5.2 Actualizar `build_exe.py` / `.spec` si se cambia el modelo incluido.
- [ ] 5.3 Actualizar `requirements.txt` si hay cambios de dependencias.

## 6. Validación final

- [ ] 6.1 Re-ejecutar benchmark completo con la configuración final y verificar mejora en precisión.
- [ ] 6.2 Verificar que la capacidad multilingüe se mantiene (probar con un doc en inglés o mixto).
- [ ] 6.3 Verificar tiempos de procesamiento aceptables en CPU (< 30 seg para doc de 20 páginas).
