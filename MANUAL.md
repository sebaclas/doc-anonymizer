# doc-anonymizer — Manual de uso

Herramienta para anonimizar documentos Word (.docx) y PDF mediante pseudonimización: reemplaza datos personales por nombres o valores ficticios elegidos por el usuario.

---

## Objetivo

Tomar un documento con datos reales (nombres de personas, empresas, direcciones, CUITs, teléfonos, etc.) y generar una versión anonimizada donde esos datos fueron reemplazados por pseudónimos consistentes, manteniendo la coherencia a lo largo de todo el documento.

---

## Instalación (solo la primera vez)

```bash
cd "ruta/a/doc-anonymizer"
pip install -e .
python -m spacy download xx_ent_wiki_sm
```

---

## Interfaz Gráfica (GUI) - Recomendado
Para usuarios que prefieran una experiencia visual, el programa incluye una aplicación de escritorio nativa:

```bash
python -m anonymizer.gui
```

### Funciones de la Interfaz:
1.  **Paso 1: Seleccionar Documento**: Elige archivos `.docx` o `.pdf`.
2.  **Paso 2: Detectar y Generar Excel**: Analiza el archivo y crea un Excel de revisión.
3.  **Paso 3: Revisión en Excel**: Marcá con `s` la columna **Accion** para las entidades que querés anonimizar. Las entidades ya conocidas en la BD vienen pre-marcadas.
4.  **Paso 4: Generar Documento**: Presiona el botón verde. Se generará el documento anonimizado junto con su archivo `.reversal.json` de reversión.
5.  **Revertir anonimización**: Botón para restaurar un documento previamente anonimizado a su versión original. Usa el sidecar `.reversal.json` generado automáticamente al anonimizar. Si ese archivo no está presente, la reversión no es posible.

---

## Flujo de trabajo (Core)

### Paso 1 — Extracción
El sistema lee el documento y extrae todo el texto preservando la estructura (párrafos, tablas, celdas).

### Paso 2 — Detección de entidades
Se detectan automáticamente dos tipos de entidades:

- **NER (inteligencia artificial)**: detecta nombres de personas, organizaciones y lugares usando el modelo de lenguaje spaCy. Útil para documentos generales. Puede generar falsos positivos en contratos legales (palabras capitalizadas que no son nombres propios).

- **Regex (patrones)**: detecta datos estructurados con reglas fijas. Muy preciso. Detecta: CUIT/CUIL, DNI/NIE, emails, teléfonos argentinos e internacionales, IBAN, CBU de 22 dígitos.

> Para documentos legales o contratos, se recomienda usar `--no-ner` para saltear el NER y trabajar solo con regex + base de datos.

### Paso 3 — Matching contra la base de datos
Antes de mostrar entidades al usuario, el sistema busca cada texto detectado en la base de datos de entidades conocidas:

- **Coincidencia exacta**: se aprueba automáticamente y se muestra en una tabla resumen sin necesidad de intervención.
- **Coincidencia aproximada** (fuzzy, por defecto >= 85% de similitud): se muestra al usuario para confirmar. Útil para variaciones de nombres ("Ordoñez" vs "Ordóñez", abreviaturas, etc.).
- **Sin coincidencia**: pasa a revisión manual.

### Paso 4 — Revisión interactiva
Para cada entidad no reconocida por la base de datos, el sistema pregunta qué hacer:

```
[3/12] PERSONA: "Empresa XYZ SA" (fuente: ner)
  Que hacer? Si / No / Editar [s/n/e] (n):
```

| Opción | Tecla | Qué hace |
|--------|-------|----------|
| **Si** | `s` | Acepta la entidad. Se incluirá en la anonimización. |
| **No** | `n` | Descarta la entidad. El texto NO se reemplaza en el documento. Usar para falsos positivos ("Las Partes", "El Contratante", nombres de países genéricos, etc.). |
| **Editar** | `e` | Corrige el texto detectado antes de aceptarlo. Usar cuando el NER capturó texto de más (ej: detectó `"Corrales Rosana Valeria-M.B.I. Saneamiento"` pero solo querés reemplazar `"Corrales Rosana Valeria"`). |

> **Nota sobre los defaults**: Todas las entidades **nuevas** (no encontradas en la base de datos) requieren aprobación explícita — tanto las detectadas por NER como por Regex. El sistema **no auto-aprueba** ninguna entidad nueva para evitar falsos positivos. Solo las entidades con coincidencia exacta en la base de datos se aprueban automáticamente.
>
> Las entidades duplicadas solo se preguntan **una vez** — la decisión se aplica a todas las ocurrencias en el documento.

### Paso 5 — Asignación de pseudónimos (Sugerencias Automáticas)
Para cada entidad aceptada que no tiene pseudónimo en la base de datos, el sistema **sugerirá un pseudónimo automático** basado en su tipo para ahorrar tiempo de escritura (ej: Persona1, Org1, Lugar1).

#### En el Flujo Interactivo (CLI):
El sistema propone la sugerencia como default. Podés presionar `Enter` para aceptarla o escribir un pseudónimo propio.

#### En el Excel (Detect / GUI):
Al generar el Excel de revisión, la columna **Pseudonimo** ya vendrá pre-llenada con estas sugerencias. **El usuario tiene el control final**: podés borrar el pseudónimo, cambiarlo por uno manual o cambiar la acción a `n` si decidís no anonimizar esa entidad.

Si aceptás una sugerencia y respondés `s` a guardar en base de datos, la entidad y su pseudónimo quedan guardados permanentemente para uso futuro.

### Paso 6 — Generación del documento
Se genera el documento anonimizado con todos los reemplazos aplicados:
- **DOCX**: preserva el formato original (fuentes, estilos, tablas, negritas).
- **PDF**: genera un nuevo PDF con texto plano (el layout del original no se preserva).

---

## Archivos generados

Cada vez que se ejecuta `anonymize run`, se crean tres archivos junto al documento original:

| Archivo | Descripción |
|---------|-------------|
| `documento_anonimizado.pdf` / `.docx` | El documento con los datos reemplazados. |
| `documento_anonimizado_mapeo.json` | El mapeo completo usado: `{"original": "pseudónimo"}`. Se puede reutilizar con `anonymize apply`. |
| `documento_anonimizado_mapeo.xlsx` | El mismo mapeo en formato Excel, editable. |
| `documento_anonimizado.docx.reversal.json` / `.pdf.reversal.json` | **Sidecar de reversión.** Contiene la lista ordenada de todas las sustituciones aplicadas. Necesario para ejecutar `anonymize deanonymize` y restaurar el documento original. Se genera automáticamente; no modificar manualmente. |

### Base de datos de entidades conocidas

Archivo Excel persistente que guarda todas las entidades y pseudónimos que el usuario fue confirmando. Es la **única fuente de verdad** del sistema — cualquier fila eliminada deja de ser reconocida:

```
C:\Users\<usuario>\.doc-anonymizer\known_entities.xlsx
```

---

## Referencia de comandos

### `anonymize run` — Flujo completo

```bash
anonymize run "ruta/documento.pdf"
anonymize run "ruta/documento.docx"
```

**Opciones:**

| Opción | Descripción |
|--------|-------------|
| `--output` / `-o` | Ruta del archivo de salida. Por defecto: mismo directorio con sufijo `_anonimizado`. |
| `--mapping` / `-m` | Cargar un mapeo JSON previo como punto de partida. |
| `--no-ner` | Saltear la detección NER. Recomendado para contratos y documentos legales donde el NER genera demasiado ruido. |
| `--threshold` / `-t` | Umbral de similitud para matching aproximado (0-100, default: 85). Bajar para ser más permisivo, subir para ser más estricto. |
| `--skip-review` | Saltear la revisión interactiva. Aprueba todo automáticamente usando la base de datos. |
| `--no-excel` | No generar el archivo `.xlsx` del mapeo. |

**Ejemplos:**

```bash
# Contrato legal (sin NER para evitar ruido)
anonymize run contrato.pdf --no-ner

# Con umbral de similitud más alto
anonymize run informe.docx --threshold 90

# Especificar dónde guardar el resultado
anonymize run documento.pdf --output "C:/Documentos/anonimizado.pdf"

# Reutilizar un mapeo anterior
anonymize run nuevo_contrato.pdf --mapping contrato_anonimizado_mapeo.json
```

---

### `anonymize detect` — Solo detectar
Detecta entidades sin generar ningún documento. Útil para explorar qué detectaría el sistema antes de anonimizar.

**Flujo interactivo vía Excel (NUEVO):**
Permite exportar una grilla de decisión para ser revisada asincrónicamente por el usuario u otros departamentos (e.g. Legales/Compliance).
```bash
anonymize detect documento.docx --output revision.xlsx
```
- **Formato del Excel:** Contiene 9 columnas en este orden: `Original`, `Contexto`, `Pseudonimo`, `Tipo`, `Accion`, `Guardar DB`, `Origen`, `Aliases`, `Modo`.
  - **`Contexto`**: hasta 5 palabras antes y después de la entidad detectada, para facilitar la evaluación de cada caso.
  - **`Pseudonimo`**: pre-llenado con sugerencias automáticas (ej: `Persona1`, `Org1`) para entidades nuevas. Modificable.
  - **`Accion` por defecto**: las entidades con coincidencia exacta en la BD vienen pre-marcadas con `s`. Las entidades nuevas (NER, Regex) vienen con la columna **vacía** y requieren aprobación explícita del usuario.
- **Codificación por colores:** Las filas en color verde son entidades ya conocidas en la Base de Datos.
- **Instrucciones incorporadas:** El archivo incluye una solapa de ayuda con una guía de uso rápida.

**Exportar a JSON:**
```bash
anonymize detect documento.pdf --output entidades.json
```

---

### `anonymize apply` — Aplicar mapeo existente
Aplica un mapeo JSON o la revisión realizada en Excel directamente al documento.

```bash
# Aplicar el Excel de revisión generado en el paso anterior (paso 3 del flujo interactivo)
anonymize apply documento.docx revision.xlsx

# Aplicar un mapeo simple JSON
anonymize apply documento.pdf mapeo.json
```

---

### `anonymize deanonymize` — Revertir un documento anonimizado
Restaura un documento previamente anonimizado a su versión original usando el sidecar `.reversal.json` que se genera automáticamente al anonimizar.

```bash
# Auto-detecta el sidecar (busca <input>.reversal.json en la misma carpeta)
anonymize deanonymize documento_anonimizado.docx documento_restaurado.docx

# Especificar el sidecar manualmente
anonymize deanonymize documento_anonimizado.pdf documento_restaurado.pdf --reversal mi_sidecar.reversal.json
```

**Opciones:**

| Opción | Descripción |
|--------|-------------|
| `--reversal` / `-r` | Ruta explícita al sidecar `.reversal.json`. Si se omite, se busca automáticamente como `<input>.reversal.json`. |

> **Requisito**: el archivo sidecar `.reversal.json` debe existir junto al documento anonimizado. Sin él, la reversión **no es posible**. El sidecar se crea automáticamente cada vez que se ejecuta `anonymize run`.
>
> Formatos soportados: `.docx` y `.pdf`.

---

### `anonymize db` — Base de datos de entidades conocidas

#### Listar todas las entidades guardadas
```bash
anonymize db list
```

#### Editar en Excel (recomendado)

La forma más cómoda de gestionar la base de datos es exportarla a Excel, editarla, y volver a importarla.

```bash
# 1. Exportar a Excel
anonymize db export
# Genera: C:\Users\<usuario>\.doc-anonymizer\known_entities.xlsx

# 2. Abrir en Excel, editar libremente:
#    - Modificar pseudónimos existentes
#    - Agregar filas nuevas
#    - Agregar aliases (columna D, separados por coma)
#    - Cambiar el tipo de una entidad

# 3. Reimportar
anonymize db import "C:\Users\<usuario>\.doc-anonymizer\known_entities.xlsx"
```

El Excel tiene cinco columnas:

| Columna | Descripción |
|---------|-------------|
| **Original** | El texto tal como aparece en los documentos. |
| **Pseudonimo** | El texto de reemplazo. |
| **Tipo** | `PERSONA`, `ORGANIZACION`, `LUGAR`, `EMAIL`, `TELEFONO`, `DNI/NIE`, `CUENTA BANCARIA`, `PERSONALIZADO` |
| **Aliases** | Variantes del nombre original, separadas por coma (ej: `A. García, García`). |
| **Modo** | `palabra` (default) o `substring`. Controla cómo se busca el texto en el documento. Ver sección siguiente. |

> Las filas con **Original** o **Pseudonimo** vacíos se ignoran al importar.

#### Modo de búsqueda (`Modo`)

Cada entidad en la base de datos tiene un modo de búsqueda que controla cómo se localiza en el documento:

| Modo | Descripción | Cuándo usarlo |
|------|-------------|---------------|
| `palabra` | Busca el texto con bordes de palabra (`\b`). Evita que "Ana" reemplace "Mariana". Funciona correctamente con paréntesis y puntuación. | **RECOMENDADO** para nombres de personas, empresas, lugares. Evita falsos positivos. |
| `substring` | Busca el texto en cualquier posición, incluso dentro de palabras más largas. | Para **siglas, códigos**, o cuando el nombre aparece pegado a otros caracteres o números. |

**Ejemplos:**
- `palabra`: Si el DB tiene "Ana López", no reemplaza "AnaLópez" ni el "Ana" dentro de "Banana". Sí reemplaza "(Ana López)" y "Ana López-Ramírez".
- `substring`: Reemplaza "ANA_LOPEZ", "XAnaLopezX", etc.

**Tip para nombres con guiones:** Si un nombre aparece como `Juan-García` pero en la DB está como `Juan García`, agregá un alias:
```bash
anonymize db alias "Juan García" "Juan-García"
```

#### Exportar a una ubicación específica
```bash
anonymize db export --output "C:/Documentos/mi_base.xlsx"
```

#### Agregar una entidad desde el CLI
```bash
anonymize db add "Nombre Real" "Nombre Falso"
anonymize db add "Empresa SA" "Empresa Ejemplo SA" --type ORGANIZACION

# Con modo de búsqueda explícito (default: palabra)
anonymize db add "ABC" "XYZ" --mode substring   # sigla que puede aparecer pegada a otro texto
anonymize db add "Juan García" "Pedro Lopez" --mode palabra  # nombre con bordes de palabra (default)
```

#### Agregar un alias (variante del mismo nombre)
Permite que distintas grafías de un mismo nombre se mapeen al mismo pseudónimo.

```bash
# "Ana Lopez" y "Ana López" -> mismo pseudónimo
anonymize db alias "Ana Lopez" "Ana López"

# Abreviatura
anonymize db alias "Ana García" "A. García"
```

#### Eliminar una entidad
```bash
anonymize db remove "Nombre Real"
```

#### Importar desde JSON
```bash
# Mapeo simple {"original": "pseudonimo"}
anonymize db import mapeo_anterior.json

# Con tipo por defecto
anonymize db import mapeo_anterior.json --type PERSONA
```

---

## Consejos de uso

**Para documentos recurrentes del mismo cliente o proyecto:**
Después de anonimizar el primero, importá el mapeo a la base de datos:
```bash
anonymize db import contrato_cliente_mapeo.json
```
Los próximos documentos del mismo cliente se anonimizarán casi automáticamente.

**Para contratos legales:**
Siempre usar `--no-ner`. El NER confunde términos legales capitalizados ("Las Partes", "El Contratante", "La Sociedad") con nombres propios.

**Para ajustar el matching aproximado:**
Si el sistema no reconoce variaciones de nombres que debería reconocer, bajar el threshold:
```bash
anonymize run documento.pdf --threshold 75
```
Si está reconociendo cosas que no debería, subirlo:
```bash
anonymize run documento.pdf --threshold 92
```

**Para reutilizar pseudónimos entre documentos:**
Usar `--mapping` para partir de un mapeo previo, combinado con la base de datos para máxima cobertura automática.

---

## Suite de Diagnóstico

Si encontrás una palabra o entidad que **debería ser detectada pero no lo es**, podés usar la suite de diagnóstico para entender por qué la herramienta la está ignorando.

### Cómo usarlo

1. **Agregar el caso problemático**: Abrí el archivo `tests/regression/cases.csv` y agregá una fila con el texto donde aparece la palabra y qué palabra esperás que sea detectada.
   ```csv
   id,text,expected,type
   mi_error_01,"El documento menciona a Juan Perez","Juan Perez",PERSONA
   ```

2. **Ejecutar el diagnóstico**:
   ```bash
   python scripts/run_diagnostics.py
   ```

### Posibles causas de falla reportadas:
- **FILTERED**: La palabra es demasiado corta (< 3 caracteres), está en la lista de `stopwords` (ej: "Empresa", "Servicio"), contiene saltos de línea, o solo contiene números/símbolos.
- **SHADOWED**: Otra entidad (más larga o de mayor prioridad) la está ocultando. Por ejemplo, si se detecta "Juan Perez", no se detectará "Juan" individualmente.
- **NER_REGEX_FAILURE**: Ni el modelo de IA (NER) ni las reglas de patrones (Regex) reconocieron la palabra.
- **NOT_IN_TEXT**: El texto esperado no coincide exactamente (case-insensitive) con lo que escribiste en `cases.csv`.

> **Tip**: Si compartís un error con el equipo de desarrollo, incluí la salida de este script para agilizar la solución.
