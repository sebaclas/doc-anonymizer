# Proposal: Detection of Monetary Amounts

## Intent
The user needs the system to automatically detect and flag monetary amounts in documents for anonymization review. 

## Motivation
Financial documents, contracts, and term sheets frequently contain sensitive financial figures (e.g., service fees, purchase prices, investment amounts). Currently, the system relies on generic NER which often misses specific currency formats like "$1.000", "50.000 Pesos", or "USD 500". Adding explicit regex patterns for these will ensure high recall for financial data.

## Goals
- Add a new `EntityType.MONEY` (label: "MONTO").
- Implement robust regex patterns to detect:
    - Currency symbols followed/preceded by numbers (e.g., "$ 100", "€50").
    - Currency codes (USD, EUR, ARS).
    - Spanish currency words ("Pesos", "Dólares").
- Ensure it works with different separators (dots/commas).

## Strategy
1. **Model Update**: Add `MONEY` to `anonymizer.models.EntityType`.
2. **Regex Implementation**: Add common money patterns to `anonymizer.detectors.patterns.BUILTIN_PATTERNS`.
3. **Validation**: Test with snippets from the provided `sample_docs` (e.g. term sheets).
