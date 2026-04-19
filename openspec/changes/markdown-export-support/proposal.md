## Why

Some applications and users require a safer, simplified version of documents that strips away the complexity of DOCX (metadata, macros, hidden XML) while preserving the hierarchy of headings. Transitioning to Markdown provides a clean, portable, and secure format for anonymized content.

## What Changes

- **New Output Format**: Support for generating `.md` (Markdown) files from `.docx` source.
- **Hierarchy Preservation**: Detection of Word heading styles (Heading 1-6) and conversion to Markdown headers (`#` to `######`).
- **Table Simplification**: Conversion of Word tables into simple GFM-style Markdown tables.
- **Image Removal**: Intentional removal of images in the Markdown version for maximum simplicity and security.
- **Dual Export Support**: GUI update to allow users to select both DOCX and MD outputs simultaneously or individually.

## Capabilities

### New Capabilities
- `markdown-export`: Logic for mapping DOCX structured elements to Markdown syntax and managing the export lifecycle.

### Modified Capabilities
- `document-processing`: Update requirements to include capturing hierarchical structure (styles) during extraction.
- `gui-workflow`: New requirements for the export selection interface (checkboxes for Word/MD).

## Impact

- `anonymizer.extractors.docx_extractor`: Needs to capture style names for paragraphs.
- `anonymizer.replacer`: Needs a new function/module for Markdown generation.
- `anonymizer.gui`: UI update with two checkboxes; `anonymize_file` logic update to handle multiple output formats.
- `anonymizer.cli`: Potentially add a flag `--format md` or similar.
