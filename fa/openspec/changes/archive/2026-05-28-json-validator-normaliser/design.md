## Context

The Data Ingestion pipeline uses LangGraph to route and process files. Currently, the `json_validator_node` and `normaliser_node` use temporary/mock implementations. Phase 6 requires replacing these with full logic: JSON must be validated against the standard requirement schema (acting as a passthrough), and raw blocks from PDF/DOCX/TXT extractors must be fully normalised (whitespace cleanup, ID generation, deduplication, length filtering) into a final `dict[str, str]`.

## Goals / Non-Goals

**Goals:**
- Implement `extract_from_json` in `ingestion/extractors.py` to parse JSON and perform the four schema compliance checks.
- Implement `normalise_blocks` in `ingestion/normaliser.py` to handle inline IDs vs sequential IDs, deduplication, length filtering, and whitespace collapsing.
- Integrate these fully into `graph.py`'s `json_validator_node` and `normaliser_node`.

**Non-Goals:**
- No LLM calls (RFA handles that).
- No file format routing (handled in Phase 3).
- No new extractor logic for PDF/DOCX/TXT (handled in Phases 4 & 5).

## Decisions

1. **JSON Validator Logic Location:** 
   - *Decision:* Keep `extract_from_json` in `ingestion/extractors.py` and raise `NonStandardJSONError`. The graph node `json_validator_node` will call it.
   - *Rationale:* Keeps all file parsing in one module. 

2. **Normaliser State Handling:**
   - *Decision:* The `normaliser_node` will read `state["extracted_blocks"]` (which contains `list[dict]`) and return `{"extracted_requirements": requirements_dict}`.
   - *Rationale:* Matches the data contract where extractors produce blocks and the normaliser produces the final `dict[str, str]` for the RFA.

3. **Deduplication Strategy:**
   - *Decision:* Standard exact-match string deduplication using a `set` to track seen normalized descriptions. 
   - *Rationale:* Simple and deterministic. Whitespace is collapsed first, avoiding trivial duplicates.

## Risks / Trade-offs

- **Risk:** Auto-generated IDs (`REQ-1`, `REQ-2`) might change on subsequent uploads if a requirement is inserted in the middle of a document.
  - *Mitigation:* This is expected for document ingestion. Users who need stable IDs should use inline IDs in TXT or compliant JSON.
- **Risk:** High memory usage for huge JSON files.
  - *Mitigation:* The system limits file sizes upstream, and `json.load()` is sufficient for typical requirements files (which rarely exceed a few MB).
