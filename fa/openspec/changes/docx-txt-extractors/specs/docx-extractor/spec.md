## ADDED Requirements

### Requirement: Extract paragraphs from DOCX
The DOCX extractor SHALL iterate every paragraph in the document via `python-docx`, skip paragraphs with fewer than 10 characters or only whitespace, and emit the rest as `extracted_blocks` dicts with `text`, `source_page` (always `None` for DOCX), and `source_section`.

#### Scenario: Normal paragraph extraction
- **WHEN** the document contains a standard paragraph over 10 characters
- **THEN** it is emitted as an extracted block dict with the paragraph text

#### Scenario: Empty or short paragraph filtering
- **WHEN** a paragraph contains only whitespace or fewer than 10 characters
- **THEN** it is ignored and not emitted

### Requirement: Flatten and extract lists from DOCX
The DOCX extractor SHALL detect list styles (`List Bullet`, `List Number`, `List Paragraph` and similar variants) via `paragraph.style.name` and emit each list item as a separate block, stripping the list marker. Nested lists SHALL be flattened — each item at any nesting level becomes its own block.

#### Scenario: Bullet list extraction
- **WHEN** a paragraph has a list-related style name
- **THEN** it is extracted as its own block without the bullet/number marker

### Requirement: Extract tables with headers from DOCX
The DOCX extractor SHALL iterate all tables. If the first row contains ≥ 2 cells matching header keywords (`ID`, `Requirement`, `Description`, `Shall`, `Must`, `Functional`, `Non-Functional`), it SHALL prefix subsequent row cells with the column header (e.g., `"ID: REQ-1 | Description: ..."`). If no header is detected, cells SHALL be concatenated with a separator. Empty tables (all cells whitespace) SHALL be skipped.

#### Scenario: Table with recognised headers
- **WHEN** a table has a first row with ≥ 2 matching header keywords
- **THEN** subsequent rows are extracted with cell contents prefixed by their column headers

#### Scenario: Table without recognised headers
- **WHEN** a table has no recognised header row
- **THEN** all cells are concatenated with a separator and extracted as blocks

#### Scenario: Empty table
- **WHEN** a table has all empty or whitespace-only cells
- **THEN** the table is skipped entirely

### Requirement: Track heading-based sections in DOCX
The DOCX extractor SHALL track heading paragraphs (`Heading 1`, `Heading 2`, `Heading 3`, etc.). If a heading contains keywords like `Requirements`, `Functional Requirements`, `Non-Functional Requirements`, `Business Requirements`, or `System Requirements`, subsequent paragraphs (until the next heading of equal or higher level) SHALL have their `source_section` field set to the heading text. Heading text itself SHALL NOT be emitted as a block.

#### Scenario: Section context propagation
- **WHEN** a paragraph follows a recognised heading
- **THEN** its extracted block includes the heading text in the `source_section` field

#### Scenario: Heading text not emitted
- **WHEN** a heading paragraph is encountered
- **THEN** it is NOT emitted as a requirement block

### Requirement: DOCX output format
The DOCX extractor SHALL return `list[dict]` where each dict has keys: `text` (str), `source_page` (None for DOCX), and `source_section` (str or None). This matches the `extracted_blocks` contract from Phase 4.

#### Scenario: Output structure
- **WHEN** blocks are extracted from a valid DOCX
- **THEN** each block is a dict with `text`, `source_page`, and `source_section` keys

### Requirement: DOCX error handling
The DOCX extractor SHALL raise `FormatMismatchError` (from `ingestion.exceptions`) if the file cannot be opened as DOCX, and `ExtractionError("No text content found")` if the document contains no extractable text.

#### Scenario: Corrupt or non-DOCX file
- **WHEN** the file cannot be parsed by `python-docx`
- **THEN** a `FormatMismatchError` is raised

#### Scenario: Empty DOCX document
- **WHEN** the DOCX file contains no text (only images, charts, or empty paragraphs)
- **THEN** an `ExtractionError("No text content found")` is raised
