# Guía Rápida — Anonimizador Pro 🚀

¡Hola! Esta es la guía rápida para que domines el programa sin complicaciones. El secreto está en los archivos **Excel**.

### 1. Seleccioná tu archivo (Word o PDF) 📄
Elegí el documento que querés anonimizar. El programa lo va a leer entero (incluyendo cuadros de texto, pies de página y tablas).

### 2. Detectar y Generar Excel 🧠
Al darle a este botón, el programa "busca" nombres, empresas y montos. Te genera un archivo Excel en la misma carpeta que el original. 
**Abrilo y trabajá sobre él:**

- **Columna "Pseudónimo"**: El programa ya te sugiere un pseudónimo automático (ej: `Persona1`, `Org1`). Podés aceptarlo (dejarlo tal cual), cambiarlo por uno propio, o borrarlo si no querés reemplazar esa entidad.
- **Columna "Acción"**: Las entidades que el programa **ya conoce de antes** vienen pre-marcadas con `s`. Para las entidades **nuevas** (detectadas por IA o por patrones), esta columna viene **vacía**: tenés que poner `s` para que se reemplace, o dejarla vacía para ignorarla.
- **Columna "Contexto"**: Muestra el fragmento del texto donde apareció la entidad (5 palabras antes y después). Muy útil para decidir si una detección es válida o un falso positivo.
- **Columna "Guardar DB"**: ¡Esto es muy útil! Si ponés una **'s'** acá, el programa se "acuerda" de este nombre para siempre. La próxima vez que proceses un archivo similar, ya sabrá cómo anonimizarlo y te aparecerá ya marcado en el Excel particular.

### 3. Generar Documento 🔄
Una vez que guardaste y cerraste el Excel, volvé al programa y dale al botón verde. ¡Listo! Se creará una copia anonimizada de tu documento, junto con un archivo `.reversal.json` que permite deshacer la anonimización más adelante.

### 4. Revertir Anonimización ↩️
Si necesitás restaurar el documento original, usá el botón **"Revertir anonimización"**. El programa buscará automáticamente el archivo `.reversal.json` que se generó junto al documento. Si ese archivo no está, la reversión no es posible.

### 5. Base de Datos Maestra (Tu "Memoria") ⚙️
En la parte inferior tenés el botón para abrir la base de datos completa. 
- Usala para limpiar nombres viejos o agregar nombres a mano.
- Usá la columna **"Aliases"** si una persona se escribe de varias formas (ej: "Juan Pérez, J. Pérez").
- También podés agregar varias líneas con el mismo pseudónimo.
- Poné el modo en **"substring"** para siglas que aparezcan pegadas a números o guiones.

---
**Tip Pro:** Si ya tenés el Excel corregido de antes, no hace falta que vuelvas a detectar. Podés usar el botón **"Cargar Excel Existente"** y generar el documento de una.
