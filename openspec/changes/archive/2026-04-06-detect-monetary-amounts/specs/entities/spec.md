## Requirement: Monetary amount detection
The system MUST detect monetary values using predefined regular expressions to ensure consistent identification across documents.

### Scenario: Common currency symbols
- **GIVEN** a document containing "$1.000", "€ 50,22", or "£10"
- **WHEN** `detect` is executed
- **THEN** it identifies "MONTO" as the entity type for these strings.

### Scenario: Currency words and codes
- **GIVEN** a document containing "50.000 Pesos", "USD 500", or "cien mil Dólares"
- **WHEN** `detect` is executed
- **THEN** it identifies "MONTO" as the entity type for these strings.

### Scenario: Separator handling
- **GIVEN** different locales using dots or commas for thousands/decimals
- **WHEN** `detect` is executed
- **THEN** it correctly captures the full numeric amount plus currency marker.
