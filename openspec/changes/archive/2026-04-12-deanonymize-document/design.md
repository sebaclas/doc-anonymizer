## Context

The anonymizer applies a `{original → pseudonym}` mapping to DOCX and PDF documents. Pseudonyms are **not unique** in the master database — multiple different original entities can be assigned the same pseudonym token. This makes it impossible to reconstruct the original from the DB alone: a token like `[PERSONA_1]` in an anonymized file could correspond to any of several original names.

The current codebase has no reversal path at all. To add one correctly, the source of truth must be the **exact substitutions applied to each specific document**, not the global entity database.

## Goals / Non-Goals

**Goals:**
- Write a **sidecar reversal file** (`<output_path>.reversal.json`) every time a document is anonymized, capturing the ordered list of `{original, pseudonym, match_mode}` pairs that were actually substituted.
- Provide `deanonymize_docx` / `deanonymize_pdf` functions that read the sidecar and apply the inverse substitutions, restoring the original document without any DB access.
- Expose the operation via CLI (`deanonymize` subcommand) and GUI ("Revertir anonimización" button).

**Non-Goals:**
- Partial de-anonymization (selecting which entities to revert) — full reversal only.
- Preserving original PDF layout pixel-perfectly (same limitation as anonymization).
- Retroactive reversal of documents anonymized before this change shipped (no sidecar exists for those).
- Storing a history / audit log of de-anonymization events.

## Decisions

### D1: Sidecar file as the single source of truth for reversal

**Why not the DB:** Pseudonyms are not unique keys — the same `[PERSONA_1]` may appear in the DB mapped to multiple originals. Reversing from the DB would require picking one arbitrarily and would likely corrupt documents.

**Why not an inverted in-memory dict:** Even within a single document, the same pseudonym could in principle have replaced different originals (e.g., two entities aliased to the same token). The sidecar is an ordered list, not a dict, preserving that context.

**Format:**
```json
{
  "schema_version": 1,
  "source_document": "original_filename.docx",
  "replacements": [
    {"original": "Juan Pérez",  "pseudonym": "[PERSONA_1]", "match_mode": "palabra"},
    {"original": "Perez",       "pseudonym": "[PERSONA_1]", "match_mode": "substring"}
  ]
}
```

The sidecar lives beside the anonymized output: `output.docx` → `output.docx.reversal.json`.

### D2: De-anonymization builds a reverse dict from the sidecar at call-time

The sidecar list is unique by `(original, pseudonym)` pair. For reversal we invert to `{pseudonym: original}`. If two rows share the same pseudonym (which is allowed), the **last writer wins** by list order — this is a documented limitation. In practice, the list is built from the actual replacements made, so order is deterministic and the risk is low.

**Why not re-use `_apply_mapping_to_text` with a reversed dict:** We still do reuse it — `deanonymize_*` passes `{pseudonym: original}` with `"substring"` mode for all entries. Pseudonym tokens like `[PERSONA_1]` are unique-looking strings unlikely to appear as substrings of other text, so substring mode is safe and avoids word-boundary issues with bracket characters.

### D3: Sidecar writing is opt-out, not opt-in

`anonymize_docx` / `anonymize_pdf` write the sidecar **by default** (no breaking API change; callers can pass `write_reversal=False` to suppress). The CLI always writes it; the GUI always writes it.

### D4: CLI subcommand `deanonymize`

```
anonymizer deanonymize <input> <output> [--reversal <path>]
```

If `--reversal` is omitted, the CLI looks for `<input>.reversal.json` automatically.

### D5: GUI auto-detects sidecar

The "Revertir anonimización" button opens a file picker for the anonymized document. If `<selected_file>.reversal.json` exists, it is used automatically. If not, an error dialog is shown asking the user to provide the sidecar manually.

## Risks / Trade-offs

- **Documents anonymized before this change** have no sidecar → reversal is impossible for them. Mitigation: document clearly; show a clear error in GUI/CLI if sidecar is missing.
- **Pseudonym collision within the sidecar** (same pseudonym, different originals) → last-writer-wins. Mitigation: log a warning at de-anonymization time; a future task could enforce unique pseudonym assignment per document.
- **PDF reversal quality** → same limitation as anonymization: layout reconstructed from plain text. Mitigation: documented.
- **Sidecar file management** → users might accidentally delete the sidecar. Mitigation: document that sidecar must be kept alongside the anonymized document.

## Migration Plan

No DB schema changes. No migration needed for existing data.

Deployment steps:
1. Add sidecar-writing logic to `anonymize_docx` / `anonymize_pdf` in `replacer.py`.
2. Add `deanonymize_docx` / `deanonymize_pdf` to `replacer.py`.
3. Add `deanonymize` subcommand to `cli.py`.
4. Add GUI action to `gui.py`.
5. Run full test suite — all existing anonymization tests must remain green.

Rollback: revert the three changed files. Sidecars written before rollback are inert (`.json` files, ignored by old code).

## Open Questions

- Should the GUI offer a manual file picker for the sidecar (for cases where it was moved/renamed)? (v1: show error and guide user to use `--reversal` flag via CLI.)
- Should the sidecar be embedded inside the DOCX (as a custom XML part) to avoid separation? (Deferred — adds complexity; plain `.json` sidecar is simpler for v1.)
