## ADDED Requirements

### Requirement: TXT encoding detection
The TXT extractor SHALL read the raw bytes and pass them through `chardet` to detect the file encoding. If `chardet` reports confidence below 0.7, the extractor SHALL fall back to the `encoding_fallback` parameter (sourced from `IngestionConfig.encoding_fallback`, default `"utf-8"`). Decoding failures with the detected encoding SHALL trigger a retry with the fallback encoding.

#### Scenario: High confidence encoding
- **WHEN** `chardet` returns a confidence ≥ 0.7
- **THEN** the file is decoded using the detected encoding

#### Scenario: Low confidence encoding
- **WHEN** `chardet` returns a confidence < 0.7
- **THEN** the file is decoded using the fallback encoding and the uncertain detection is logged

#### Scenario: Decode error with detected encoding
- **WHEN** decoding with the detected encoding raises an exception
- **THEN** decoding is retried with the fallback encoding

### Requirement: TXT structured format detection
The TXT extractor SHALL check if > 50% of non-empty lines match the pattern `^([A-Za-z]+-?\d+)\s*[:\.]\s*(.+)$`. If so, matched lines SHALL be extracted as blocks containing both the inline ID and description text. Unmatched lines SHALL be skipped.

#### Scenario: Structured file matched
- **WHEN** more than 50% of non-empty lines match the ID-description regex
- **THEN** matched lines are emitted as blocks with the parsed inline ID preserved

#### Scenario: Structured file not matched
- **WHEN** fewer than 50% of non-empty lines match the regex
- **THEN** the extractor falls back to unstructured segmentation

### Requirement: TXT unstructured fallback
If the file is not structured, the extractor SHALL compute the average non-empty line length. If < 200 characters, it SHALL use **line mode** (each non-empty line is one block). If ≥ 200, it SHALL use **paragraph mode** (split by `\n\n`, internal newlines collapsed to spaces).

#### Scenario: Short-line unstructured file
- **WHEN** unstructured and average line length is < 200 chars
- **THEN** each non-empty line is extracted as a separate block

#### Scenario: Long-line unstructured file
- **WHEN** unstructured and average line length is ≥ 200 chars
- **THEN** text is split by `\n\n` into paragraph blocks with internal newlines collapsed

### Requirement: TXT bullet and number stripping
The TXT extractor SHALL strip leading bullets, dashes, and numbering artifacts from description text using the regex `^\s*(\d+[\.\\)]\s+|[a-zA-Z][\.\\)]\s+|•\s+|[-–]\s+)`. This applies in both structured and unstructured paths.

#### Scenario: Line starting with bullet or number marker
- **WHEN** an extracted block text starts with a bullet or numbering marker
- **THEN** the marker is stripped from the extracted text

### Requirement: TXT output format
The TXT extractor SHALL return `list[dict]` where each dict has keys: `text` (str), `source_page` (None for TXT), and `source_section` (None for TXT). For structured TXT, the inline ID SHALL be carried in the block dict in a field recognised by the normaliser (Phase 6).

#### Scenario: Output structure
- **WHEN** blocks are extracted from a valid TXT file
- **THEN** each block is a dict with `text`, `source_page`, and `source_section` keys

### Requirement: TXT error handling
The TXT extractor SHALL raise `ExtractionError("No text content found")` (from `ingestion.exceptions`) if the file contains no non-whitespace characters. It SHALL raise `ExtractionError` with encoding details if the file cannot be decoded with either the detected or fallback encoding.

#### Scenario: Empty TXT file
- **WHEN** the TXT file contains no non-whitespace text
- **THEN** an `ExtractionError("No text content found")` is raised

#### Scenario: Undecodable file
- **WHEN** decoding fails with both detected and fallback encoding
- **THEN** an `ExtractionError` with encoding details is raised
