## Context

The `doc-anonymizer` currently operates exclusively through a PowerShell/CLI interface. While functional, it lacks the visual feedback and ease of use required for occasional users. This design outlines a modern web-based frontend that bridges the gap between the complex backend logic and a premium user experience.

## Goals / Non-Goals

**Goals:**
- Create a visually stunning (premium aesthetic) web interface for document anonymization.
- Support file selection (DOCX, PDF) with drag-and-drop.
- Implement automated output saving in the source file's directory.
- Build a "Database Explorer" to view the entity mapping history.

**Non-Goals:**
- Cloud-based processing (all data remains local).
- Complex user management or authentication (local-only tool).

## Decisions

- **Architecture**: **Local Web App (LWA)** model. A FastAPI backend will serve the React frontend and handle file system interactions.
- **Frontend Stack**: **Vite + React + Tailwind**. This combination ensures high performance and allows for the "wow" factor through custom animations and a curated color palette.
- **File Dialog Implementation**: Since standard browser `<input type="file">` does not expose the full path for security, the backend will expose a specialized endpoint that triggers a native OS file picker (via `tkinter.filedialog` or `pywin32`) to allow the system to know exactly where the file is and where to save outputs.
- **Database Link**: The "DB link" will be implemented as a separate route in the React app, fetching data from the `known_entities.json` through the FastAPI API.

## Risks / Trade-offs

- **[Risk] Browser Security**: Standard browsers prevent writing to local files outside downloads. → **[Mitigation]** The backend executes the file operations directly using the absolute path obtained via the native file dialog.
- **[Trade-off] Dependency Bloat**: Adding Vite/React adds a build step. → **[Mitigation]** We will provide a simple `npm run dev` or a pre-built static distribution.
