## 1. Backend Infrastructure (FastAPI Integration)

- [ ] 1.1 Create `anonymizer/api.py` to host the FastAPI server
- [ ] 1.2 Implement `/api/select-file` endpoint that triggers a native Windows file selection dialog
- [ ] 1.3 Implement `/api/process` endpoint to run the anonymization logic using the provided path
- [ ] 1.4 Develop `/api/database` endpoint to expose metadata from `known_entities.json`
- [ ] 1.5 Add a health check and core logic wrappers in `anonymizer/api.py`

## 2. Frontend Development (Vite + React)

- [ ] 2.1 Scaffold the `webapp/` directory using Vite (React + TypeScript)
- [ ] 2.2 Configure a premium TailwindCSS theme: custom palette, Inter typography, and dark mode by default
- [ ] 2.3 Implement the **Dashboard Component**: central hub for document processing with "WOW" factor animations (Framer Motion)
- [ ] 2.4 Build the **Database Explorer**: a sleek, filterable table for viewing persistent entity mappings
- [ ] 2.5 Create a **Process Tracker**: visual progress indicators for detection and replacement steps

## 3. Integration & Local UX

- [ ] 3.1 Connect the "Select File" button to the backend's native dialog bridge
- [ ] 3.2 Ensure the backend correctly identifies and uses the absolute file directory for output saving
- [ ] 3.3 Add "Open in Explorer" functionality after successful processing for instant access to results
- [ ] 3.4 Implement a "DB Link" accessible from any page to jump to the database view

## 4. Polish & Final Delivery

- [ ] 4.1 Apply glassmorphism effects and final micro-animations for interactions
- [ ] 4.2 Optimize API response times and add robust error boundaries for when files are locked/inaccessible
- [ ] 4.3 Verify the "Super Sencilla" requirement by streamlining the flow to 2-3 clicks max
