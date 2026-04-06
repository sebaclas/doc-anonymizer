---
description: Revisar/auditar estructura del proyecto, especificaciones, dependencias. Correr el flujo antes de lanzar nueva versión
---

### Ejecutar esto en el contexto de openspec, comando /opsx-explore

## Fase A: Auditoría de Estructura
Revisá si la jerarquía de carpetas respeta el estándar de Anti-Gravity (api/internal/pkg). Reportá archivos que estén en la raíz o en carpetas no estandarizadas según el framework.

## Fase B: Análisis de Especificación vs. Código
Leé el archivo OpenSpec principal. Listá todas las funciones del código que no tienen una entrada en la especificación (posible código muerto) y todas las definiciones en OpenSpec que no tienen código asociado (funcionalidad faltante).

## Fase C: Limpieza de Dependencias de Terceros
Revisá el archivo de gestión de dependencias. Identificá librerías que se importan pero no se usan en ninguna implementación de los servicios de Anti-Gravity.

## Matriz de Decisión para Limpieza
#Construir la siguiente matriz de decición. No ejecutar ningún cambio.

| Tipo de Problema | Ubicación | Impacto en OpenSpec | Acción Propuesta |
| :--- | :--- | :--- | :--- |
| **Archivo Huérfano** | `/src/services/old_auth.py` | Ninguno (Sin uso en la especificación) | `rm` |
| **Dependencia Rota** | `/src/models/user.py` | Inconsistencia de Tipos (Breaking Change) | `Refactor / Update Schema` |
| **Archivo Innecesario** | `/tmp_backup/` | Riesgo de confusión en el despliegue | `rm -rf` |
| **Endpoint Fantasma** | `/src/api/v1/debug.py` | Ruta activa no documentada en OpenSpec | `Eliminar o Documentar` |
| **Spec Mismatch** | `/src/api/handlers/` | Contrato OpenSpec desactualizado | `Sincronizar con Spec` |