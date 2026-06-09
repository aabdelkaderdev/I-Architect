## 1. JSON Validator implementation

- [x] 1.1 Implement `extract_from_json` in `ingestion/extractors.py`
- [x] 1.2 Add logic to parse JSON and perform the four schema compliance checks
- [x] 1.3 Raise `NonStandardJSONError` if compliance checks fail
- [x] 1.4 Return the parsed dict if compliant

## 2. Normaliser implementation

- [x] 2.1 Implement `normalise_blocks` in `ingestion/normaliser.py`
- [x] 2.2 Add whitespace collapsing and stripping for each block
- [x] 2.3 Implement length filtering (drop if < min_block_length, truncate if > max_block_length)
- [x] 2.4 Implement deduplication (if enabled in config)
- [x] 2.5 Implement ID assignment (preserve inline or generate sequential)

## 3. Graph Node Updates

- [x] 3.1 Update `json_validator_node` in `ingestion/graph.py` to use `extract_from_json`
- [x] 3.2 Update `normaliser_node` in `ingestion/graph.py` to use `normalise_blocks`
- [x] 3.3 Ensure `normaliser_node` raises `EmptyRequirementsError` if the output dict is empty

## 4. Testing

- [x] 4.1 Write unit tests for `extract_from_json` (compliant and non-compliant cases)
- [x] 4.2 Write unit tests for `normalise_blocks` (whitespace, length limits, dedup, IDs)
- [x] 4.3 Verify graph flow handles both JSON passthrough and non-JSON extraction + normalisation
