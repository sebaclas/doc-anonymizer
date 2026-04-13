---
description: Flujo de trabajo para guardar cambios en Git con gestión opcional de Versiones (SemVer) y Changelog.
---

Este flujo de trabajo se utiliza para guardar una nueva versión de tu código y, opcionalmente, gestionar el versionado semántico del proyecto.

// turbo-all
1. **Sincronización Inicial**: Ejecuta `git status`. Si no es un repositorio Git, inicialízalo (`git init`). Asegura que exista un `.gitignore` adecuado basado en la tecnología del proyecto (Node, Python, etc.).

2. **Preparación**: Ejecuta `git add .` para incluir todos los cambios actuales. Revisa que no se incluyan archivos sensibles o innecesarios.

3. **Decisión de Versión**: Pregunta al usuario: "¿Deseas realizar un Lanzamiento de Versión (Release) en este momento?"
   
   **Si la respuesta es SÍ:**
   a. **Lectura**: Localiza el archivo de configuración de versión (ej: `pyproject.toml`, `package.json`). Lee la versión actual (vX.Y.Z).
   b. **Selección**: Pregunta al usuario: "¿Qué tipo de incremento deseas aplicar?" (Opciones: Major, Minor, Patch).
   c. **Cálculo**:
      - `Patch`: Incrementa Z (ej: 0.1.0 -> 0.1.1). Para correcciones menores (bugfixes).
      - `Minor`: Incrementa Y y resetea Z (ej: 0.1.1 -> 0.2.0). Para nuevas funcionalidades compatibles.
      - `Major`: Incrementa X y resetea Y/Z (ej: 0.2.0 -> 1.0.0). Para cambios estructurales o incompatibles.
   d. **Actualización**: Modifica el archivo de configuración con la nueva versión calculada.
   e. **Changelog**: 
      - Busca o crea un archivo `CHANGELOG.md` en la raíz.
      - Añade una entrada al principio con la nueva versión, la fecha actual y un resumen de los cambios (basado en el historial de commits o los cambios realizados en esta sesión).
   f. **Marca interna**: Establece una marca para que el commit y el push incluyan la etiqueta (tag).

4. **Commit**: 
   - Si es un Release: Ejecuta `git commit -m "chore(release): vX.Y.Z"`.
   - Si NO es Release: Analiza los diffs de los cambios (puedes usar la skill `git-commit`) y ejecuta `git commit -m "<MENSAJE_DESCRIPTIVO>"`.

5. **Tagging (Solo en Release)**: Ejecuta `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.

6. **Publicación**:
   - Corrobora si hay repositorio remoto (`git remote -v`). 
   - Si existe: Pregunta si desea subir los cambios. En caso afirmativo, ejecuta `git push`. 
   - Si fue un Release, ejecuta también `git push --tags`.
   - Si no existe remoto, ofrece al usuario añadir uno.
