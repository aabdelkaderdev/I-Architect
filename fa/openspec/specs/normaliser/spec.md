## ADDED Requirements

### Requirement: Whitespace normalisation
The system SHALL collapse multiple spaces/newlines to a single space and strip leading/trailing whitespace for every extracted text block.

#### Scenario: Block with irregular spacing
- **WHEN** a block contains "The   system  \n  shall"
- **THEN** it is normalised to "The system shall"

### Requirement: Block length filtering
The system SHALL drop blocks shorter than `min_block_length` and truncate blocks longer than `max_block_length`.

#### Scenario: Fragmented block
- **WHEN** a block has 5 characters (below min limit 15)
- **THEN** it is silently dropped

#### Scenario: Oversized block
- **WHEN** a block exceeds 2000 characters
- **THEN** it is truncated to exactly 2000 characters

### Requirement: Exact-match deduplication
If enabled, the system SHALL drop exactly duplicate blocks (post whitespace normalisation).

#### Scenario: Duplicate requirements detected
- **WHEN** two identical blocks appear after normalisation
- **THEN** the second block is dropped and only one instance is kept

### Requirement: ID assignment
The system SHALL preserve unique inline IDs if present, otherwise auto-generate sequential IDs using `id_prefix`.

#### Scenario: No inline IDs present
- **WHEN** extracting from a standard PDF
- **THEN** sequential IDs like `REQ-1`, `REQ-2` are generated and assigned to each valid block
