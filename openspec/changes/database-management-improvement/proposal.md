# Proposal: Database Management Improvement

## Goal
Improve how the "Known Entities" database is fed and managed within the GUI.

## Problems to Solve
1. **Uncontrolled DB Growth**: Automatically adding every `S` (anonymize) from Excel to the DB causes clutter.
2. **First Use Experience**: The system must handle starting with a fresh, empty database without friction.
3. **Internal Accessibility**: The user should be able to view/edit the entire database from the GUI.

## Proposed Solution
- **New Excel Column**: Add a `Guardar DB` column to the detection Excel. Only rows marked with `s` (or `S`) in this column will be added to the persistent database.
- **Master DB Management**: Add a button to the GUI's sidebar/header to "Import/Export/Manage Database" via Excel.
- **Robust Auto-Init**: Ensure `known_entities.json` is created automatically in the home folder if it doesn't exist.
