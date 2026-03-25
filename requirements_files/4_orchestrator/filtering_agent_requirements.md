# Filtering Agent — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/filtering_agent_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### FR-FILT-001: Deterministic Regex Pre-Filter (Fast-Fail Layer)
- **Description:** Before invoking any LLM, the agent SHALL pass all requirements through a Regex Pre-Filter that detects and flags the following patterns as noise:
  - **Stack Traces:** `java.lang.*`, `at line \d+`, `Exception`, Python tracebacks.
  - **System Logs:** Timestamp patterns (`yyyy-mm-dd`), bracketed severity markers (`[INFO]`, `[ERROR]`, `[DEBUG]`).
  - **Empty/Whitespace:** Rows with fewer than 5 alphanumeric characters.
  When a match is found: mark `is_noisy=True`, `confidence=1.0`, `method='Regex'`. The row is dropped without incurring any LLM cost.
- **SRS Trace:** §9.2, §11.2.1
- **Priority:** Must
- **Acceptance Criteria:** A row containing `java.lang.NullPointerException at UserAuth.java:45` is flagged as noise with confidence 1.0 without any LLM call.

### FR-FILT-002: Massive Row Isolation (Token Safety)
- **Description:** The agent SHALL calculate the approximate token count (`chars / 4`) for each `Raw Description`. If the token count exceeds `max_input_tokens × 0.5` (safety buffer), the row SHALL be immediately flagged as `is_noisy=True` with reasoning: *"Input exceeds analysis context; discarded as likely binary/log dump."*
- **SRS Trace:** §9.2
- **Priority:** Must
- **Acceptance Criteria:** A row with 60,000 characters (~15,000 tokens) is flagged as noise without LLM invocation.

### FR-FILT-003: LLM Batch Processing
- **Description:** Requirements that pass FR-FILT-001 and FR-FILT-002 SHALL be processed by the LLM in fixed batches of 10 rows. The input payload SHALL be a JSON array `[{"id": "REQ-1", "text": "..."}]` and the output SHALL be a JSON array `[{"id": "REQ-1", "is_noisy": bool, "confidence": float}]`. The agent SHALL validate `len(input_batch) == len(output_batch)` — mismatches trigger retry logic (NFR-FILT-002).
- **SRS Trace:** §9.2
- **Priority:** Must
- **Acceptance Criteria:** A set of 35 qualifying rows is processed in 4 batches (10+10+10+5); each output batch has the exact count matching its input.

### FR-FILT-004: Critical Reviewer Persona — Noise Classification
- **Description:** The LLM SHALL operate with a "Critical Reviewer" persona that aggressively classifies the following as `is_noisy=True`:
  - Code snippets or CSS styling norms.
  - Meeting administration (dates, times, attendees without technical context).
  - Personal signatures or email footers.
  - Vague statements without actionable scope.
  The persona SHALL prefer False Positives (flagging valid text as noise) over False Negatives (allowing noise into the pipeline).
- **SRS Trace:** §9.2, §11.2.1
- **Priority:** Must
- **Acceptance Criteria:** The text "Let's meet on Monday at 2pm to discuss progress" is flagged as noise; "The system shall authenticate users via OAuth2" is not.

### FR-FILT-005: Mixed Content Handling
- **Description:** If a text block contains mixed content (e.g., a valid requirement embedded within a traceback or log dump), the agent SHALL flag the entire block as **Noise** to prevent downstream contamination.
- **SRS Trace:** §11.2.1
- **Priority:** Must
- **Acceptance Criteria:** A row containing "The system must support 1000 concurrent users. Stack trace: java.lang.OutOfMemoryError..." is flagged as noise.

### FR-FILT-006: User Override Precedence
- **Description:** If the `user_override` column is `True` for any requirement (from a previous manual review session), the agent SHALL force `is_noisy=False` regardless of the LLM's classification decision. The `user_override` flag takes absolute precedence over the filtering logic.
- **SRS Trace:** §9.2, §8.3, §1.6
- **Priority:** Must
- **Acceptance Criteria:** A row with `user_override=True` and an LLM confidence of 0.99 for `is_noisy=True` is still preserved as `is_noisy=False`.

### FR-FILT-007: Structured Output Generation
- **Description:** For each processed requirement, the agent SHALL generate a deterministic JSON object: `{"is_noisy": boolean, "confidence_score": float (0.0–1.0), "primary_pattern_detected": string, "reasoning": string (1–2 sentence justification)}`.
- **SRS Trace:** §9.2
- **Priority:** Must
- **Acceptance Criteria:** Every processed requirement has a valid JSON output conforming to the defined schema; no null fields.

### FR-FILT-008: Filtered CSV Artifact Generation
- **Description:** The agent SHALL write the filtering results to `filtered_requirements/requirements_filtered_{timestamp}.csv`. The schema SHALL extend the original data with `is_noisy`, `confidence_score`, and `extraction_method` columns. The `reasoning` text from the LLM SHALL be discarded (not included in the CSV) to minimize file size.
- **SRS Trace:** §9.2
- **Priority:** Must
- **Acceptance Criteria:** The output CSV contains all original columns plus `is_noisy`, `confidence_score`, and `extraction_method`; no `reasoning` column exists.

### FR-FILT-009: Pipeline Routing Logic
- **Description:** After filtering:
  - If `is_noisy == True` AND `user_override == False`: the requirement is dropped (excluded from downstream processing).
  - If `is_noisy == False` OR `user_override == True`: the requirement is preserved and forwarded to ARLO and subsequent agents.
- **SRS Trace:** §9.2
- **Priority:** Must
- **Acceptance Criteria:** A filtered CSV with 100 rows, 20 flagged as noise (no overrides), results in 80 requirements passed to ARLO.

### FR-FILT-010: System Prompt Specification
- **Description:** The filtering agent's system prompt SHALL follow the standardized template (`ROLE → TASK → CONTEXT → CONSTRAINTS → OUTPUT`) and SHALL include:
  ```
  ROLE: Critical Technical Reviewer.
  TASK: Clean a dataset for an Automated Architect Agent. Discard any text that is NOT a functional or non-functional software requirement.
  CRITERIA (Mark is_noisy=true): Source code, Stack traces, JSON/XML dumps, Meeting logistics, UI/CSS styling instructions, Vague statements without actionable scope.
  INPUT FORMAT: JSON List of {"id": "...", "text": "..."}
  OUTPUT FORMAT: JSON List of {"id": "...", "is_noisy": boolean, "confidence": float}
  CONSTRAINT: Return EXACTLY one result object per input object.
  ```
- **SRS Trace:** §11.2.1, §11.1
- **Priority:** Must
- **Acceptance Criteria:** The prompt template matches the specified structure and produces correctly formatted JSON output.

---

## 2. Non-Functional Requirements (NFR)

### NFR-FILT-001: Aggressive Fail-Open Bias
- **Description:** The system SHALL accept the LLM's boolean `is_noisy` decision at any confidence level. Even at low confidence (e.g., 0.55), if `is_noisy=True`, the row is dropped. False Negatives (keeping noise) harm ARLO's ILP solver more than False Positives (dropping vague requirements). Users can restore dropped items via the Requirement Editing Page (Page 4).
- **SRS Trace:** §9.2
- **Metric:** Under test with a mixed dataset, the agent drops ≥ 95% of known noise items even at low LLM confidence.

### NFR-FILT-002: Robustness — Tiered Error Handling
- **Description:** Batch failures SHALL be handled with escalating retry logic:
  - **Level 1 (JSON Parse Error):** Retry batch with strict instruction "Output valid JSON only."
  - **Level 2 (Count Mismatch):** Retry batch with instruction "Ensure exactly {N} items in output."
  - **Level 3 (3x Consecutive Failures):** Fallback to Regex-Only Mode for that specific batch — mark all remaining items as `is_noisy=False` (safe pass-through) and flag for manual review.
- **SRS Trace:** §13.1
- **Metric:** Level 3 fallback activates only after 3 consecutive failures on the same batch.

### NFR-FILT-003: Throughput Performance
- **Description:** The filtering agent SHALL process at least 50 requirements per minute (excluding LLM network latency). Local processing (regex, data manipulation) SHALL complete within 5 seconds per batch.
- **SRS Trace:** §9.2
- **Metric:** Processing 100 requirements completes within 2 minutes under normal LLM response times.

### NFR-FILT-004: LLM API Timeout Fallback
- **Description:** If the LLM API times out (HTTP response > 30 seconds) or returns `ConnectionError`, the system SHALL retry with exponential backoff (3 attempts: 2s/4s/8s). On 3rd failure, the system SHALL fall back to deterministic regex-only classification (mark all remaining as `is_noisy=False`).
- **SRS Trace:** §13.1 (F-1)
- **Metric:** After 3 consecutive timeouts, the fallback activates within 14 seconds total (2+4+8).

---

## 3. Interface Requirements (IR)

### IR-FILT-001: Input Interface
- **Source:** Ingestion & Extraction Service output (`structured_requirements/requirements.json`)
- **Expected Format:** JSON array of requirement objects with `id`, `description`, `extraction_method`, `confidence_score`, and `user_override` fields.

### IR-FILT-002: Output Interface
- **Target:** `filtered_requirements/requirements_filtered_{timestamp}.csv`
- **Schema:** All original columns + `is_noisy` (boolean), `confidence_score` (float), `extraction_method` (string).
- **Consumers:** ARLO Module, Requirement Editing Page (Page 4).

### IR-FILT-003: LLM Service Interface
- **Protocol:** LangChain Chat Models (model-agnostic)
- **Supported Types:** Ollama, Deepseek, Google Gemini, Groq
- **Batch Size:** 10 rows per LLM request.

---

## 4. Disaster Recovery Requirements (DR)

### DR-FILT-001: LLM API Timeout (F-1)
- **Failure Mode:** HTTP response > 30s or `ConnectionError`.
- **Blast Radius:** Current batch stalls; upstream file is safe.
- **Recovery Action:** Retry with exponential backoff (3 attempts, 2s/4s/8s). On 3rd failure, fallback to deterministic regex-only classification (mark all as `is_noisy=False`).
- **User-Facing Message:** ⚠️ *"The filtering model is temporarily unreachable. Requirements have been passed through without AI filtering. Please manually review flagged items."*
- **SRS Trace:** §13.1 (F-1)

### DR-FILT-002: Coverage Metric Failure (F-2)
- **Failure Mode:** `(tokens_extracted / tokens_source) < 0.80`
- **Blast Radius:** Potentially significant requirements invisible to downstream agents.
- **Recovery Action:** Re-invoke Grammar-Based Decoder with `temperature += 0.2` and relaxed schema. If still < 80%, halt and escalate.
- **User-Facing Message:** ⚠️ *"Extraction coverage is {X}%. Some requirements may not have been captured. Would you like to try the Grammar-Based strategy?"*
- **SRS Trace:** §13.1 (F-2)

### DR-FILT-003: Semantic Drift (F-3)
- **Failure Mode:** Cosine similarity < 0.85 for > 15% of sampled rows.
- **Blast Radius:** Meaning distortion in extracted requirements.
- **Recovery Action:** Switch extraction strategy: Regex → Grammar-Based. Log drifted samples for user review.
- **User-Facing Message:** ⚠️ *"Semantic verification failed for {N} requirements. The extraction strategy has been upgraded. Please review highlighted items."*
- **SRS Trace:** §13.1 (F-3)

---

*End of Filtering Agent Requirements Document*
