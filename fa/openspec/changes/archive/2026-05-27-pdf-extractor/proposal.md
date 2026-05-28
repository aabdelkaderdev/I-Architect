# Proposal: PDF Extractor (Phase 4)

## What

Refactor `extract_from_pdf` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) from a minimal page-text-dump into the full extraction pipeline defined by Phase 4 of the Ingestion PRD: page-by-page traversal, frequency-based header/footer stripping, table-aware parsing with semantic header prepending, three-tier text block segmentation, and encoding cleanup.

Currently, `extract_from_pdf` opens the PDF, concatenates all page text, and splits on newlines — producing one block per non-empty line. It performs no header/footer removal, no table detection, and no structured segmentation. The resulting blocks are noisy and poorly bounded, which pushes all cleanup responsibility onto the normaliser.

## Why

- **PRD compliance**: Phase 4 specifies header/footer stripping, table extraction with semantic headers, and a three-tier segmentation strategy (numbered lists → paragraphs → sentences). The current implementation has none of these.
- **Better extraction quality**: Removing repetitive headers/footers before segmentation prevents them from becoming false-positive requirement candidates. Preserving table structure keeps columnar requirements intact instead of splitting them across rows.
- **Separation from normaliser**: The PRD explicitly separates extraction (Phase 4) from normalisation (Phase 6). The extractor outputs raw candidate blocks; the normaliser applies length filters, deduplication, and ID assignment. Keeping these separate makes each stage independently testable.
- **Configurable engine**: The `pdf_engine` and `header_footer_threshold` fields already exist on `IngestionConfig` (Phase 2) but are not fully exercised by the current extractor.

## Scope

- Rewrite `extract_from_pdf` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to implement the full Phase 4 pipeline.
- Add an `extracted_blocks` channel (`list[dict]`) to `IngestionState` in [schema.py](file:///e:/file1/fa/ingestion/schema.py) for the extractor → normaliser handoff. Each dict contains `text`, `source_page`, and `source_section`.
- Update `pdf_extractor_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to write `extracted_blocks` instead of calling `generate_ids_for_blocks` directly (normalisation is Phase 6's concern).
- Add unit tests covering header/footer stripping, table detection with semantic headers, and all three segmentation tiers.

## Out of scope

- Normaliser refactoring (Phase 6) — the normaliser will be updated separately to consume `extracted_blocks`.
- DOCX/TXT extractor refactoring (Phase 5) — those extractors keep their current implementation.
- OCR or scanned-image PDF support (explicitly out of scope per PRD).
- Content sniffing or magic-byte detection (the format router handles format validation).
