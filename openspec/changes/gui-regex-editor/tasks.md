## 1. Definir templates predefinidos

- [ ] 1.1 En `anonymizer/detectors/patterns.py`, crear lista `PREDEFINED_TEMPLATES` con patrones comunes: Nro. Expediente, Nro. Contrato, Nro. Cuenta Bancaria, CUIL extendido, Patente vehicular, Nro. Legajo.
- [ ] 1.2 Cada template tiene: `id`, `name`, `type` (EntityType), `pattern`, `description`.

## 2. Implementar persistencia de patrones custom

- [ ] 2.1 En `anonymizer/config.py`, crear funciones `load_custom_patterns()` y `save_custom_patterns()` para leer/escribir `~/.doc-anonymizer/custom_patterns.json`.
- [ ] 2.2 Estructura: `{"custom": [...], "templates_enabled": [...]}`.
- [ ] 2.3 Manejo de archivo inexistente (defaults vacíos).

## 3. Crear ventana de editor de regex

- [ ] 3.1 Crear `anonymizer/regex_editor.py` con clase `RegexEditorWindow(CTkToplevel)`.
- [ ] 3.2 Sección superior: Lista de templates predefinidos con checkboxes de activación.
- [ ] 3.3 Sección media: Lista de patrones custom con botones de edición y eliminación.
- [ ] 3.4 Panel de entrada: campos Nombre, Tipo (dropdown EntityType), Patrón. Botón "Agregar".
- [ ] 3.5 Validación en vivo del patrón: compilar con `re.compile()`, feedback visual (verde=válido, rojo=error).

## 4. Implementar panel de prueba

- [ ] 4.1 Sección inferior: campo de patrón de prueba + textarea de texto de ejemplo.
- [ ] 4.2 Botón "Probar" que ejecuta `re.finditer()` y muestra matches con posiciones.
- [ ] 4.3 Indicar número de matches encontrados y destacar cada uno.

## 5. Integrar con GUI principal

- [ ] 5.1 Agregar botón "🔧 Editor de Regex" en la GUI principal (zona de configuración, cerca del botón de DB Maestra).
- [ ] 5.2 Al hacer click, abrir `RegexEditorWindow` como ventana no-modal.
- [ ] 5.3 Al cerrar el editor, recargar patrones para la siguiente detección.

## 6. Integrar con flujo de detección

- [ ] 6.1 En `anonymizer/detectors/detector.py`, cargar patrones custom + templates activos al inicio de `detect_all()`.
- [ ] 6.2 Pasar la lista combinada a `patterns.detect(text, custom_patterns)`.

## 7. Validación

- [ ] 7.1 Verificar que un patrón regex custom detecta correctamente en un documento de prueba.
- [ ] 7.2 Verificar que activar/desactivar un template predefinido funciona correctamente.
- [ ] 7.3 Verificar que el panel de prueba muestra matches en tiempo real.
- [ ] 7.4 Verificar que un regex inválido muestra feedback visual y no se puede guardar.
- [ ] 7.5 Verificar persistencia: cerrar y reabrir la app, los patrones custom y templates activos se mantienen.
