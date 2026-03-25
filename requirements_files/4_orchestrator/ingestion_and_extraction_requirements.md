# Ingestion & Extraction Layer — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/ingestion_and_extraction_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 File Parsing (Layer 1)

#### FR-ING-001: Multi-Format File Parsing
- **Description:** The system SHALL parse uploaded documents into an in-memory text stream or tabular DataFrame using the following format-specific libraries:
  | Extension | Library | Strategy |
  |:--|:--|:--|
  | `.pdf` | `PyMuPDF` (fitz) | Iterate pages → `page.get_text("text")`; discard images |
  | `.docx` | `python-docx` | Iterate `doc.paragraphs`; ignore image runs |
  | `.txt` | Native Python | Read as UTF-8 string |
  | `.xls`, `.xlsx` | `pandas` + `openpyxl` | Heuristic Restructuring (FR-ING-002) |
  | `.csv` | `pandas` | Schema Validation for CSV Bypass (FR-ING-003) |
- **SRS Trace:** §8
- **Priority:** Must
- **Acceptance Criteria:** Each supported file type is parsed into a raw text stream or DataFrame without errors; embedded images are discarded.

#### FR-ING-002: Excel Heuristic Restructuring
- **Description:** For `.xls`/`.xlsx` files, the system SHALL:
  1. Iterate through all active sheets.
  2. Scan the first 10 rows for header keywords: `['id', 'requirement id', 'req_id', 'description', 'summary', 'text']` (case-insensitive).
  3. If keywords found: set that row as header and drop preceding rows.
  4. If NO keywords found: assume Column A = ID, Column B = Description.
  5. Drop non-matching columns and concatenate all sheets into a single intermediate DataFrame.
- **SRS Trace:** §8
- **Priority:** Must
- **Acceptance Criteria:** An Excel file with metadata headers in rows 1–3 and data starting row 4 is correctly normalized with headers detected.

#### FR-ING-003: CSV Schema Bypass Rule
- **Description:** If a `.csv` file is uploaded and its columns match (case-insensitive) the target schema `{Requirement ID, Description}`, the system SHALL:
  1. Skip the extraction phase entirely (no LLM invocation).
  2. Preserve user-provided `Requirement ID` values (do NOT overwrite with `REQ-[HASH]`).
  3. Pass the cleaned DataFrame directly to the Filtering Agent (if enabled) or to `filtered_requirements/`.
  4. Display a subtle info banner: *"CSV format detected — extraction skipped. Proceeding directly to requirement editing."*
- **SRS Trace:** §8, §1.5
- **Priority:** Must
- **Acceptance Criteria:** A matching CSV bypasses extraction; user-provided IDs (e.g., `REQ-001`) are preserved in the output.

#### FR-ING-004: No OCR Policy
- **Description:** The system SHALL NOT perform OCR on any uploaded documents. Only extractable text content is processed; embedded images, charts, and scanned content are silently discarded.
- **SRS Trace:** §8
- **Priority:** Must
- **Acceptance Criteria:** A scanned PDF with only image-based text produces an empty or near-empty text stream without errors.

### 1.2 UID Generation & Traceability

#### FR-ING-005: Unique Identifier (UID) Generation
- **Description:** The system SHALL assign a unique identifier to every extracted requirement block using the format `REQ-[FILE_HASH_PREFIX]-[INCREMENTAL_ID]`, where `FILE_HASH_PREFIX` is the first 6 characters of the SHA-256 hash of the binary file content.
- **SRS Trace:** §8.3
- **Priority:** Must
- **Acceptance Criteria:** Two different uploads of the same file produce identical `FILE_HASH_PREFIX` values; different files produce different prefixes.

#### FR-ING-006: CSV Bypass ID Preservation
- **Description:** In CSV Bypass mode (FR-ING-003), user-provided Requirement IDs SHALL be preserved and SHALL NOT be overwritten by the auto-generated `REQ-[HASH]` format.
- **SRS Trace:** §8.3
- **Priority:** Must
- **Acceptance Criteria:** A CSV with `REQ-CUSTOM-001` retains that exact ID throughout the pipeline.

### 1.3 Extraction Strategies (Layer 2)

#### FR-ING-007: Line-by-Line Extraction (Strategy A — Deterministic)
- **Description:** For pre-formatted text, the system SHALL split text by newline `\n`, filter out empty lines and lines with fewer than 10 characters (noise), and assign incremental UIDs. No LLM cost is incurred.
- **SRS Trace:** §8.1
- **Priority:** Must
- **Acceptance Criteria:** A 50-line `.txt` file with 5 empty lines produces 45 requirement entries with sequential IDs.

#### FR-ING-008: Regex Extraction (Strategy B — Agent-Assisted)
- **Description:** For files with repetitive headers, the system SHALL:
  1. Send the first 1000 tokens of the document to an LLM with prompt: "Identify the repeating pattern and return a Python Regex."
  2. Execute the returned Regex over the entire document using `re.finditer`.
- **SRS Trace:** §8.1
- **Priority:** Must
- **Acceptance Criteria:** A document with `REQ-001: ...`, `REQ-002: ...` patterns produces a regex that matches all requirements.

#### FR-ING-009: Grammar-Based Decoding (Strategy C — Constrained)
- **Description:** For unstructured prose, the system SHALL use LangChain with `PydanticOutputParser` or integration with Outlines/Guidance to enforce a BNF grammar that constrains the LLM to output valid JSON or CSV-row format.
- **SRS Trace:** §8.1
- **Priority:** Must
- **Acceptance Criteria:** An unstructured meeting transcript produces structured JSON requirement objects without hallucinated content.

#### FR-ING-010: Token Budget Check Before LLM Invocation
- **Description:** Before invoking the LLM for Grammar-Based Decoding, the module SHALL calculate the token count of the prompt + injected state. If the count exceeds `max_input_tokens × 0.85`, the module SHALL switch to `map-reduce` processing (chunk → extract → merge).
- **SRS Trace:** §8.5
- **Priority:** Must
- **Acceptance Criteria:** A 50,000-token document automatically triggers chunked map-reduce processing without manual intervention.

#### FR-ING-011: Hybrid Extraction (Strategy D — Catch-All)
- **Description:** The Hybrid strategy SHALL execute the following workflow:
  1. **Pass 1 (Regex):** Execute rigid regex pattern matching.
  2. **Pass 2 (LLM):** Send chunks to LLM with prompt: "Extract requirements as JSON list."
  3. **Set Union & Deduplication:** Combine results from both passes, applying Fuzzy Deduplication (Levenshtein Distance > 95% similarity = duplicate, prefer LLM version).
- **SRS Trace:** §8.1
- **Priority:** Must
- **Acceptance Criteria:** A document processed by Hybrid produces a superset of results from Regex and LLM individually, with no semantic duplicates.

### 1.4 Disaster Detection & Quality Guardrails (Layer 3)

#### FR-ING-012: Coverage Metric Check
- **Description:** After extraction, the system SHALL calculate: `Coverage = Extracted Requirement Tokens / Total Document Tokens`. If coverage is below 80%, the system SHALL trigger Auto-Correction by switching to a more aggressive extraction strategy (e.g., Regex → Grammar-Based). CSV/Excel files SHALL skip this check (assumed 100% coverage).
- **SRS Trace:** §8.2
- **Priority:** Must
- **Acceptance Criteria:** An extraction yielding 65% coverage automatically upgrades the strategy and re-extracts.

#### FR-ING-013: Semantic Drift Verification
- **Description:** The system SHALL verify extraction fidelity by:
  1. Sampling 10% of extracted requirements (random sample).
  2. Generating vector embeddings for both the `Extracted Requirement` and its `Source Chunk` using `sentence-transformers/all-MiniLM-L6-v2` via the ChromaDB client.
  3. Calculating Cosine Similarity. If similarity < 0.85, flag as "Potential Hallucination."
- **SRS Trace:** §8.2
- **Priority:** Must
- **Acceptance Criteria:** An extracted requirement that significantly deviates from its source text is flagged; if >15% of samples fail, strategy escalation is triggered.

#### FR-ING-014: Auto-Correction Strategy Escalation
- **Description:** When Disaster Detection triggers (coverage < 80% or semantic drift > 15%), the system SHALL:
  1. Automatically switch extraction strategy (Regex → Grammar-Based).
  2. Re-extract on the same page without redirecting the user.
  3. Display a full-screen modal: *"Extraction coverage was {X}%. The strategy has been automatically upgraded to {new_strategy}. Re-extraction in progress."*
- **SRS Trace:** §8.2, §1.5
- **Priority:** Must
- **Acceptance Criteria:** A failed extraction triggers strategy escalation and displays the auto-correction modal without page navigation.

### 1.5 Output Schema

#### FR-ING-015: Intermediate Output Format
- **Description:** The extractor SHALL output a standardized JSON structure containing arrays of requirement objects, each with: `id`, `description`, `source_file`, `extraction_method`, and `confidence_score`.
- **SRS Trace:** §8.3
- **Priority:** Must
- **Acceptance Criteria:** The output JSON validates against a Pydantic schema with all required fields non-null.

#### FR-ING-016: Post-Filtering Output Schema
- **Description:** The final output (after Filtering Agent processing) SHALL follow the Refined Output Schema with columns: `Requirement ID`, `Raw Description`, `Extraction Method`, `is_noisy`, `confidence_score`, `user_override`, and `Source Context (Metadata)`.
- **SRS Trace:** §8.3
- **Priority:** Must
- **Acceptance Criteria:** The output CSV contains all 7 columns with valid values; `user_override` defaults to `FALSE`.

---

## 2. Non-Functional Requirements (NFR)

### NFR-ING-001: Memory Constraint for PDF Parsing
- **Description:** PDF parsing using PyMuPDF SHALL NOT exceed 4GB RAM usage for any single document, regardless of file size.
- **SRS Trace:** §8
- **Metric:** Peak memory usage during PDF parsing stays below 4GB for files up to 256MB.

### NFR-ING-002: Extraction Performance
- **Description:** Line-by-Line extraction SHALL complete within 2 seconds for files with up to 10,000 lines. LLM-based strategies are bounded by network latency.
- **SRS Trace:** §8
- **Metric:** Deterministic extraction of 10,000 lines completes in ≤ 2 seconds.

### NFR-ING-003: Idempotent UID Generation
- **Description:** The SHA-256-based UID generation SHALL be deterministic — the same file uploaded twice SHALL produce identical UIDs for all extracted requirements.
- **SRS Trace:** §8.3
- **Metric:** Two uploads of the same file produce an identical set of `REQ-[HASH]-[N]` identifiers.

---

## 3. Interface Requirements (IR)

### IR-ING-001: File Input Interface
- **Source:** Streamlit UI (Page 3 — File Upload Zone)
- **Target:** Ingestion Service (`orchestrator/services/ingestion_service.py`)
- **Protocol:** HTTP REST via Django API
- **Accepted Formats:** `.docx`, `.pdf`, `.xls`, `.xlsx`, `.csv`, `.txt`
- **Max File Size:** 256MB

### IR-ING-002: ChromaDB Interface (Semantic Drift Check)
- **Target:** ChromaDB Container (`http://i-architect-chromadb:8000`)
- **Operation:** `collection.query(query_texts=[...])` for embedding generation and cosine similarity computation.

### IR-ING-003: Output Interface
- **Target Directory:** `/{project_name}/structured_requirements/`
- **Output File:** `requirements.json` (intermediate) → `filtered_requirements/requirements_filtered_{timestamp}.csv` (post-filtering)

---

## 4. Disaster Recovery Requirements (DR)

### DR-ING-001: Extraction Coverage Failure (F-2)
- **Failure Mode:** Coverage Metric < 80%.
- **Recovery Action:** Re-invoke Grammar-Based Decoder with `temperature += 0.2` and relaxed Pydantic schema. If still < 80%, halt and escalate to user.
- **User-Facing Message:** ⚠️ *"Extraction coverage is {X}%. Some requirements may not have been captured. Would you like to try the Grammar-Based strategy?"*
- **SRS Trace:** §13.1 (F-2)

### DR-ING-002: Semantic Drift Failure (F-3)
- **Failure Mode:** Cosine similarity < 0.85 for > 15% of sampled rows.
- **Recovery Action:** Switch extraction strategy: Regex → Grammar-Based. Log drifted samples for user review.
- **User-Facing Message:** ⚠️ *"Semantic verification failed for {N} requirements. The extraction strategy has been upgraded. Please review highlighted items."*
- **SRS Trace:** §13.1 (F-3)

---

*End of Ingestion & Extraction Requirements Document*
