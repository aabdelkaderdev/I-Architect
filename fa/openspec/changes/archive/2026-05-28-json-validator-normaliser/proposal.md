## Why

Phase 6 implements the final piece of the ingestion extraction stage: the JSON validator and the normaliser. The JSON validator is needed to support the passthrough path for pre-structured compliant JSON requirements. The normaliser is needed to take raw extracted text blocks from non-JSON formats (PDF, DOCX, TXT) and systematically convert them into standardized requirement records by assigning IDs, normalising whitespace, enforcing length bounds, and removing duplicates.

## What Changes

- Add a JSON validator node that checks incoming JSON files against Phase 1 standard requirement rules.
- Route compliant JSON directly to output (passthrough), bypassing extraction and RFA.
- Raise `NonStandardJSONError` for non-compliant JSON files.
- Add a normaliser node that processes extracted blocks from PDF, DOCX, and TXT.
- Implement ID assignment in the normaliser, preserving inline IDs or auto-generating sequential IDs using `id_prefix`.
- Implement whitespace normalisation, minimum length (default 15), and maximum length (default 2000) filtering.
- Implement exact-match deduplication in the normaliser if enabled.

## Capabilities

### New Capabilities
- `json-validator`: Validation of JSON requirement files against structural rules with a passthrough flow and non-compliance error handling.
- `normaliser`: Normalisation of raw extracted text blocks into clean requirements, handling whitespace cleanup, length limits, deduplication, and ID assignment.

### Modified Capabilities
None

## Impact

- **Graph/Architecture:** Adds the `json_validator_node` and updates `normaliser_node` in `ingestion/graph.py` from their temporary mock implementations to final logic.
- **Exceptions:** Introduces/uses `NonStandardJSONError` and `EmptyRequirementsError`.
- **Flow:** The RFA node will now receive clean, structured `extracted_requirements` dicts from the normaliser.
