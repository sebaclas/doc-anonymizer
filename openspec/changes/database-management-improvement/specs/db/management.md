# Specs: Database Management

## Scenarios

### 1. New User Initialization
- **GIVEN** the folder `~/.doc-anonymizer` does not exist
- **WHEN** the application starts
- **THEN** it creates the folder and an empty `known_entities.json` file automatically.

### 2. Controlled Feed from Excel
- **GIVEN** a detection Excel file
- **WHEN** the user sets `x` for "Anonymize" AND `s` for "Guardar en DB"
- **THEN** after `apply`, the entity is saved in the persistent database.
- **BUT WHEN** the user sets `x` for "Anonymize" AND leaves "Guardar en DB" empty
- **THEN** the entity is anonymized in this document but NOT saved to the database.

### 3. Open DB for manual edit
- **GIVEN** entities exist in the DB
- **WHEN** the user clicks "Editar DB Maestra (Excel)"
- **THEN** an Excel file opens with all known entities and their pseudonyms.
