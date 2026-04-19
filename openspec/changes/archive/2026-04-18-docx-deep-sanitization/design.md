## Context
Actualmente, el sistema de reemplazo de `docx` se basa en `python-docx` y opera manipulando los nodos `<w:p>` y esporádicamente `<w:t>`. Sin embargo, los documentos de Word almacenan frecuentemente información confidencial en artefactos ocultos, como metadatos (core properties), relaciones de hipervínculos (`word/_rels/document.xml.rels`), comentarios (`word/comments.xml`), historial de cambios y notas (footnotes/endnotes) que el procesador estándar pasa por alto o donde la fragmentación del texto evita el reemplazo por Regex.

## Goals / Non-Goals

**Goals:**
- Desmantelar rutas de escape de información confidencial en DOCX.
- Convertir hipervínculos a texto plano forzosamente y borrar sus URIs en el nivel `.rels`.
- Borrar de forma irreversible datos de autoría, historial de control de cambios y proteger comentarios/notas secundarias.
- Extender la abstracción de `python-docx` manipulando el DOM (`_element.xpath`) para componentes faltantes.

**Non-Goals:**
- Soporte para preservar o restaurar hipervínculos tras el *de-anonymize*. Pasan a texto plano para siempre.
- Selección individual de partes a limpiar en la interfaz (es una purga transversal y obligatoria).
- Recuperar control de cambios.
## Decisions

1. **Destrucción de Hipervínculos (`w:hyperlink`)**: El DOM interceptará todos los tags de hipervínculo en el cuerpo. El texto interno (`w:t`) visible se promoverá como un sub-nodo texto plano ("run" puro) y el contenedor de enlace se destruirá. *Rationale*: Manejar y mapear `.rels` con iteraciones variables para correos electrónicos pseudonimizados es complejo e inseguro.
2. **Purgado de Propiedades**: Se forzará el vaciado (`=""` o `"Anónimo"`) de los atributos `author`, `last_modified_by`, y `comments` de `doc.core_properties`. *Rationale*: La API de `python-docx` lo resuelve nativamente sin lxml.
3. **Limpieza de XMLs Auxiliares (Notas/Comentarios)**: Aprovechando la recursividad, iteraremos `doc.part.related_parts` buscando parts de tipo XML (footnotes, endnotes, comments) y les aplicaremos `_deep_replace_xml`. *Rationale*: Usa el pipeline existente, mitigando el riesgo inherente de procesar XMLs desconocidos.
4. **Remoción de Revisiones en Track-Changes**: Implementaremos la lógica análoga a "Aceptar todos los cambios" nativa de Word. Usaremos `lxml` xpath (`.//w:del` o `.//w:delText`) para destruirlos del árbol de manera definitiva. Los nodos insertados (`w:ins`) simplemente se mantendrán y se les purgará su envoltura de marca de revisión, dejando el texto final intacto. *Rationale*: Aceptar los cambios elimina definitivamente el bloque viejo y consolida el nuevo, evadiendo filtraciones de datos ocultos en el historial.

## Risks / Trade-offs

- [Riesgo de corrupción Estructural DOCX] → Mitigación: Iterar, desenvolver y eliminar nodos mediante herramientas cuidadosas de lxml, validando que el documento abra correctamente tras las sustituciones.
- [Pérdida Funcional de Enlaces Legítimos] → Mitigación: Notificado en el "Non-Goals". Siendo una herramienta primariamente de privacidad, la hermeticidad asume mayor prioridad que el linkeo.
