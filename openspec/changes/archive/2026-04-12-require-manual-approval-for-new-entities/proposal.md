## Why

Currently, the system suggests "s" (apply) as the default action for all detections, including NER, Regex, and Database matches. This can lead to unintended anonymizations if the user isn't careful. Restricting auto-approval to only those entities already present in the Known Entities Database ensures a higher level of precision and forces a deliberate review of all new entities.

## What Changes

- **Restricted Auto-Approval**: The `Accion` column in the generated Excel mapping file will only pre-fill with "s" if the entity has an exact match in the Master Database.
- **Manual Action for New Detections**: NER and Regex detections will have an empty "Accion" value (or a neutral default), requiring the user to explicitly approve them by typing "s" or a custom pseudonym.
- **CLI Default Alignment**: The interactive CLI review will also be updated to default to non-approval (requiring input) for entities not found in the database.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `excel-workflow`: Update requirement regarding pre-filling the `Accion` column to exclude new detections.
- `cli-workflow`: Update requirement for interactive review defaults to prioritize manual validation of new entities.

## Impact

- `anonymizer/gui.py`: Update `_detection_thread` to only set `accion="s"` for DB hits.
- `anonymizer/cli.py`: Update interactive review logic to set appropriate defaults based on entity source.
- `anonymizer/mapping.py`: Ensure generated data rows reflect the new conditional default logic.
