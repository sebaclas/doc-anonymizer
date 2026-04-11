## Context

El sistema ya soporta patrones custom a nivel de código: `patterns.py` recibe `custom_patterns: list[dict]` y los aplica junto con los built-in. También existe `custom_patterns.json` como ubicación de persistencia mencionada en `STACK.md`. Sin embargo, no hay UI para gestionar estos patrones y no hay mecanismo de prueba.

Los patrones built-in en `patterns.py` cubren: DNI/NIE, CUIT/CUIL, EMAIL, PHONE_AR, PHONE_ES, IBAN, CBU_AR, PHONE_INT, MONEY. Pero para documentos específicos de cada usuario (expedientes, contratos, números de cuenta locales), se necesitan patrones personalizados.

## Goals / Non-Goals

**Goals:**
- Ventana secundaria (CustomTkinter `CTkToplevel`) accesible desde un botón en la GUI principal.
- Panel de prueba en vivo: campo de patrón + campo de texto de ejemplo → matches resaltados.
- Lista unificada de patrones (incluyendo los de fábrica y los del usuario) con capacidad de agregar, editar, eliminar y activar/desactivar.
- Panel de prueba en vivo integrado.
- Persistencia en `~/.doc-anonymizer/custom_patterns.json`.
- Validación de regex: feedback visual si el patrón es inválido.

**Non-Goals:**
- No se modifica la ventana principal de la GUI (solo se agrega un botón de acceso).
- Refactorizar `patterns.py` para eliminar `BUILTIN_PATTERNS` hardcodeados y cargarlos desde configuración.
- No se implementa editor visual de regex (solo texto).

## Decisions

**Decision 1: Arquitectura de la ventana.**
Ventana secundaria `CTkToplevel` (no modal) para permitir que el usuario vaya y venga entre la GUI principal y el editor.

**Decision 1.1: Uso de CTkScrollableFrame.**
Se utilizarán frames desplazables para las listas de templates y patrones activos. Esto asegura que la interfaz siga siendo usable incluso con decenas de patrones.
*Rationale:* Evita que la ventana crezca indefinidamente y mejora la organización visual.
*Rationale:* Bloquear la ventana principal sería frustrante. El usuario puede querer consultar el documento mientras configura patrones.

**Decision 2: Layout de la ventana.**
```
┌─────────────────────────────────────────────────────────┐
│              Editor de Patrones Regex                    │
├─────────────────────────────────────────────────────────┤
│ LISTA DE PATRONES ACTIVOS (Desplazable ↕)                │
│ ┌──────────────────────────────────────────────────────┐│
│ │  ✅ EMAIL       │ EMAIL      │ \b...@...    │ 🗑️    ││
│ │  ✅ DNI/NIE     │ ID_NUMBER  │ \b[0-9]...   │ 🗑️    ││
│ │  ✅ CUIT/CUIL    │ ID_NUMBER  │ \b\d{2}-...  │ 🗑️    ││
│ │  ☐ EXPEDIENTE   │ CUSTOM     │ EXP-\d+      │ 🗑️    ││
│ │  ✅ MI_PATRON    │ CUSTOM     │ \w{3}-\d{4}  │ 🗑️    ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│ [➕ Nuevo Patrón]                                       │
├─────────────────────────────────────────────────────────┤
│ PROBAR PATRÓN SELECCIONADO / EDITAR                      │
│ Nombre: [____________]  Tipo: [▼ EntityType]            │
│ Patrón: [________________________________]              │
│ Texto de prueba:                                         │
│ ┌──────────────────────────────────────────────────────┐│
│ │ El expediente EXP-2024/0531 fue asignado al juez... ││
│ └──────────────────────────────────────────────────────┘│
│ Resultados: 1 match encontrado                          │
│ [🔍 Probar]                                             │
├─────────────────────────────────────────────────────────┤
│ [💾 Guardar y Cerrar]                                   │
└─────────────────────────────────────────────────────────┘
```

**Decision 3: Formato de persistencia.**
Archivo `custom_patterns.json` con estructura de lista plana:
```json
{
  "patterns": [
    {"id": "builtin_email", "name": "EMAIL", "type": "EMAIL", "pattern": "\\b...", "enabled": true, "builtin": true},
    {"id": "user_01", "name": "MI_PATRON", "type": "ID_NUMBER", "pattern": "\\d{4}-\\d{4}", "enabled": true, "builtin": false}
  ]
}
```
*Rationale:* Una estructura de lista única simplifica la carga, el filtrado y la representación en la UI. El campo `id` facilita futuras actualizaciones de los patrones "de fábrica".

**Decision 4: Gestión de Patrones.**
Todos los patrones (incluyendo los de fábrica y los del usuario) se cargan en la lista. Se permite editar o eliminar cualquiera de ellos. Si el usuario desea restaurar los patrones de fábrica que eliminó, se proveerá un botón de "Restaurar por defecto".

**Decision 5: Validación de regex.**
Al escribir un patrón, se intenta compilar con `re.compile()`. Si falla, el campo se marca en rojo y se muestra el error. Si compila, se marca verde.

## Risks / Trade-offs

- [Riesgo] Regex complejas podrían causar catastrofic backtracking en textos largos.
  → Mitigación: Timeout o límite de caracteres en el campo de prueba. En producción, los textos de documentos son procesados línea a línea.
- [Riesgo] Usuarios podrían crear regex demasiado amplias que matcheen todo.
  → Mitigación: El panel de prueba muestra inmediatamente los matches, permitiendo validación visual antes de guardar.
