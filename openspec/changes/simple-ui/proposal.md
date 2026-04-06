## Why

Currently, the doc-anonymizer only provides a CLI interface. Users need a simpler, more visual way to interact with the tool, especially for tasks like selecting files and managing the entity database. A "WOW" design UI will improve the UX for non-technical or mouse-oriented users.

## What Changes

- **Web Interface**: A modern, sleek web-based UI built with Vite/React.
- **File Selection**: Visual file picker that allows selecting `.docx` or `.pdf` files.
- **Local Saving**: Automatically save output files (`.xlsx` mapping and `.docx` anonymized) in the source file's directory.
- **Database Link**: A dedicated section to browse and possibly edit the known entities database.
- **FastAPI Backend**: A lightweight local backend to serve the API and interface with the core Python logic.

## Capabilities

### New Capabilities
- `web-ui`: Implementation of a responsive and aesthetically pleasing web dashboard for document anonymization.

### Modified Capabilities
- none

## Impact

- **New Backend**: A FastAPI server to bridge the GUI with the core logic.
- **New Frontend**: A Vite/React project for the user interface.
- **Core Integration**: Refactor or wrap existing `anonymizer` logic for API access.
