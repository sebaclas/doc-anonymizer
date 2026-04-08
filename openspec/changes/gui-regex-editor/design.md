## Context

El sistema ya soporta patrones custom a nivel de código: `patterns.py` recibe `custom_patterns: list[dict]` y los aplica junto con los built-in. También existe `custom_patterns.json` como ubicación de persistencia mencionada en `STACK.md`. Sin embargo, no hay UI para gestionar estos patrones y no hay mecanismo de prueba.

Los patrones built-in en `patterns.py` cubren: DNI/NIE, CUIT/CUIL, EMAIL, PHONE_AR, PHONE_ES, IBAN, CBU_AR, PHONE_INT, MONEY. Pero para documentos específicos de cada usuario (expedientes, contratos, números de cuenta locales), se necesitan patrones personalizados.

## Goals / Non-Goals

**Goals:**
- Ventana secundaria (CustomTkinter `CTkToplevel`) accesible desde un botón en la GUI principal.
- Panel de prueba en vivo: campo de patrón + campo de texto de ejemplo → matches resaltados.
- Lista de patrones custom activos con capacidad de agregar, editar, eliminar.
- Catálogo de templates predefinidos con checkbox de activación.
- Persistencia en `~/.doc-anonymizer/custom_patterns.json`.
- Validación de regex: feedback visual si el patrón es inválido.

**Non-Goals:**
- No se modifica la ventana principal de la GUI (solo se agrega un botón de acceso).
- No se cambia la lógica core de `patterns.py` (ya soporta custom_patterns).
- No se implementa editor visual de regex (solo texto).

## Decisions

**Decision 1: Arquitectura de la ventana.**
Ventana secundaria `CTkToplevel` (no modal) para permitir que el usuario vaya y venga entre la GUI principal y el editor.
*Rationale:* Bloquear la ventana principal sería frustrante. El usuario puede querer consultar el documento mientras configura patrones.

**Decision 2: Layout de la ventana.**
```
┌─────────────────────────────────────────────────────────┐
│              Editor de Patrones Regex                    │
├─────────────────────────────────────────────────────────┤
│ TEMPLATES PREDEFINIDOS                                   │
│ ☐ Nro. Expediente (EXP-\d{4}/\d{4})                    │
│ ☐ Nro. Contrato (CONT-\d+)                             │
│ ☐ Nro. Cuenta Bancaria (\d{3}-\d{6}-\d{2})             │
│ ☐ CUIL extendido (\d{2}-\d{8,11}-\d{1,2})              │
│ ☐ Patente vehicular ([A-Z]{2}\d{3}[A-Z]{2}|...)        │
├─────────────────────────────────────────────────────────┤
│ PATRONES PERSONALIZADOS                                  │
│ ┌──────────────────────────────────────────────────────┐│
│ │  ✅ MI_PATRON  │ ID_NUMBER  │ \d{4}-\d{4}  │ ❌ Del ││
│ │  ✅ OTRO       │ CUSTOM     │ REF-\w+      │ ❌ Del ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│ Nombre: [____________]  Tipo: [▼ EntityType]            │
│ Patrón: [________________________________]              │
│ [➕ Agregar Patrón]                                     │
├─────────────────────────────────────────────────────────┤
│ PROBAR PATRÓN                                            │
│ Patrón: [________________________________]              │
│ Texto de prueba:                                         │
│ ┌──────────────────────────────────────────────────────┐│
│ │ El expediente EXP-2024/0531 fue asignado al juez... ││
│ └──────────────────────────────────────────────────────┘│
│ Resultados: 1 match encontrado                          │
│   → "EXP-2024/0531" (posición 15-29)                   │
│ [🔍 Probar]                                             │
├─────────────────────────────────────────────────────────┤
│ [💾 Guardar y Cerrar]                                   │
└─────────────────────────────────────────────────────────┘
```

**Decision 3: Formato de persistencia.**
Archivo `custom_patterns.json` con estructura:
```json
{
  "custom": [
    {"name": "MI_PATRON", "type": "ID_NUMBER", "pattern": "\\d{4}-\\d{4}", "enabled": true}
  ],
  "templates_enabled": ["expediente", "contrato"]
}
```
*Rationale:* Separar custom de templates activados permite actualizar el catálogo de templates sin afectar los patrones del usuario.

**Decision 4: Templates predefinidos.**
Se mantienen como constante en código (`PREDEFINED_TEMPLATES` en `patterns.py`). El usuario solo puede activar/desactivar, no editar. Los templates activos se guardan por nombre en `custom_patterns.json`.

**Decision 5: Validación de regex.**
Al escribir un patrón, se intenta compilar con `re.compile()`. Si falla, el campo se marca en rojo y se muestra el error. Si compila, se marca verde.

## Risks / Trade-offs

- [Riesgo] Regex complejas podrían causar catastrofic backtracking en textos largos.
  → Mitigación: Timeout o límite de caracteres en el campo de prueba. En producción, los textos de documentos son procesados línea a línea.
- [Riesgo] Usuarios podrían crear regex demasiado amplias que matcheen todo.
  → Mitigación: El panel de prueba muestra inmediatamente los matches, permitiendo validación visual antes de guardar.
