# Stack tecnológico

## Lenguaje

| Componente | Versión |
|------------|---------|
| Python | >= 3.10 |

---

## Dependencias principales

### Interfaces de usuario
| Librería | Uso |
|----------|-----|
| **CustomTkinter** | Framework para la interfaz gráfica (GUI) de escritorio. Proporciona un diseño moderno y oscuro con soporte para escalado visual. |
| **Typer** | Framework para construir el CLI (interfaz de línea de comandos). |
| **Rich** | Formato visual en terminal: tablas, colores y progreso para la versión CLI. |

### Procesamiento de documentos
| Librería | Uso |
|----------|-----|
| **python-docx** | Lectura y escritura de Word (.docx). Soporta reemplazo profundo en párrafos, tablas, encabezados y pies de página. |
| **pdfplumber** | Extracción de texto de archivos PDF preservando la estructura básica. |
| **reportlab** | Generación de nuevos documentos PDF a partir del texto anonimizado. |
| **openpyxl** | Gestión de archivos Excel (.xlsx). Usado para el mapeo interactivo y la edición de la base de datos maestra. |

### Detección de entidades
| Librería | Uso |
|----------|-----|
| **spaCy** | Motor de NLP para NER (Named Entity Recognition). |
| **Modelos NER** | `xx_ent_wiki_sm` (Multilingüe/Wiki) y `es_core_news_sm` (Español). |
| **re** (stdlib) | Expresiones regulares para detectar CUIT/CUIL, DNI, emails e IBAN. |

### Inteligencia de negocio y Matching
| Librería | Uso |
|----------|-----|
| **rapidfuzz** | Algoritmos de similitud de strings para reconocer variaciones de nombres (acentos, abreviaturas) contra la base de datos. |

### Distribución y Empaquetado
| Librería | Uso |
|----------|-----|
| **PyInstaller** | Conversión del código Python en un ejecutable standalone (.exe) para Windows. |

---

## Persistencia

| Formato | Ubicación | Uso |
|---------|-----------|-----|
| **JSON** | `~/.doc-anonymizer/known_entities.json` | Base de datos maestra de entidades conocidas, pseudónimos fijos y modos de coincidencia. |
| **Excel (.xlsx)** | Directorio del documento | Tabla de mapeo temporal generada para que el usuario revise y edite antes de aplicar cambios. |

---

## Arquitectura del proyecto

```
doc-anonymizer/
├── anonymizer/
│   ├── gui.py              # Interfaz gráfica principal (CustomTkinter)
│   ├── cli.py              # Interfaz de línea de comandos (Typer)
│   ├── utils.py            # Orquestación y lógica común de procesos
│   ├── models.py           # Dataclasses (Entity, EntityType, Document)
│   ├── mapping.py          # Lógica de carga/guardado de Excel de mapeo
│   ├── known_entities.py   # Gestión de la base de datos maestra (JSON <-> Excel)
│   ├── matcher.py          # Motores de búsqueda exacta y fuzzy
│   ├── replacer.py         # Motores de reemplazo para DOCX y PDF
│   ├── extractors/         # Módulos de extracción de texto
│   └── detectors/         # Motores de detección (NER + Regex)
├── build_exe.py            # Script automatizado de compilación con PyInstaller
├── AnonymizerPro.spec      # Configuración de compilación para Windows
├── MANUAL.md               # Documentación completa del usuario
└── pyproject.toml          # Configuración del proyecto y dependencias
```

---

## Datos persistidos del usuario

| Archivo | Ubicación predeterminada |
|---------|-----------|
| **Base de Datos Maestra** | `C:\Users\<usuario>\.doc-anonymizer\known_entities.json` |
| **Patrones Custom** | `C:\Users\<usuario>\.doc-anonymizer\custom_patterns.json` |
