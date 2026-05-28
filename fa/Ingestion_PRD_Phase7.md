# Data Ingestion & Requirement Filtering — Phase 7: RFA Signal/Noise Taxonomy & Prompt Spec

## Summary

This phase defines what the Requirement Filtering Agent asks the LLM to do and what it expects in return. It covers the normative Signal and Noise classification criteria (grounded in IEEE 830), the specification for the `filter_classification.md` prompt template, and the structured output schema the LLM must conform to. It contains no batching logic, no threshold mechanics, and no report generation — those belong to Phase 8.

**Depends on:** Phase 1 (Foundation & Contracts) — for the standard requirement format and the intentional design decision that the RFA is the only LLM-based operation in the pipeline. Phase 2 (Configuration) — for `FilterConfig`, whose fields are referenced in the prompt but whose mechanics are defined in Phase 8.

**Required reading before:** Phase 8 (RFA: Batching, Threshold & Filtering Report).

---

## 1. Purpose

The Requirement Filtering Agent (RFA) is the gatekeeper between raw ingested text and ARLO. It evaluates each requirement and classifies it as Signal or Noise. This phase defines the classification criteria, the prompt template that conveys them to the LLM, and the structured output types that enforce a valid response. It answers the question "what is the LLM being asked to do?" — Phase 8 answers "how are the results used?"

---

## 2. Authoritative Source Register

The RFA's classification criteria are not ad-hoc. They are anchored to two sources:

| Source | What It Governs |
|--------|-----------------|
| **IEEE 830** — Recommended Practice for Software Requirements Specifications | Requirement characteristics: a well-formed requirement must be clear, complete, consistent, verifiable, and traceable |
| **Project Noise Taxonomy** (this document, §4) | Normative classification criteria for Signal vs Noise categories |

These sources are paraphrased into constraints in the prompt template — the raw document text is not embedded.

### IEEE 830 Constraints (Signal Characteristics)

The following constraints are embedded in the prompt to define what qualifies as a well-formed requirement:

- A well-formed requirement describes **what** the system must do, not **how** it is implemented.
- A well-formed requirement is unambiguous, complete, and verifiable.
- A well-formed requirement states a single behaviour or constraint — compound requirements indicate under-specification.

---

## 3. Signal Criteria

A requirement entry is classified as **SIGNAL** when the text describes one or more of the following:

| Category | Description |
|----------|-------------|
| Functional behaviour | System actions, responses, workflows — what the system must do |
| Integration points | System interfaces, APIs, data flows between systems |
| Security constraints | Authentication, encryption, access control requirements |
| Quality attributes | Performance targets, reliability guarantees, scalability limits, usability requirements |
| Business logic | Domain rules, workflow constraints, business invariants |
| Compliance & regulatory | Legal or regulatory requirements the system must satisfy |

A Signal requirement states architectural intent. It is a statement about the system that would influence design decisions.

---

## 4. Noise Criteria

A requirement entry is classified as **NOISE** when the text falls into one of the following categories:

| Noise Category | Description | Example |
|----------------|-------------|---------|
| Tracebacks & exceptions | Chains of execution errors, stack traces | `Traceback (most recent call last): File "app.py", line 42...` |
| Terminal & log output | Raw console artifacts, memory metrics, CLI logs, timestamps | `[INFO] 2024-01-15 Server started on port 8080. Memory: 2.4GB` |
| Implementation dependencies | Hyper-specific library version constraints | `Requires numpy>=1.24.0,<1.25.0 due to ABI incompatibility with scipy` |
| Isolated state reports | Highly specific runtime failure descriptions | `The Redis connection pool exhausts after 47 concurrent writes on node 3` |
| Code & configuration snippets | Inline code, property files, CLI flags | `server.port=8443` or `def handle_request(ctx):` |
| Change log entries | Version history, commit messages, patch notes | `v2.3.1: Fixed null pointer in auth module` |
| Test case descriptions | Unit/integration test specifications | `Test: verify that login fails after 3 attempts with wrong password` |

These categories are exhaustive for the purposes of this pipeline. Entries that do not clearly match any Noise category should be classified as Signal.

---

## 5. Prompt Template Specification

The RFA prompt is stored in `ingestion/prompts/filter_classification.md` and loaded at runtime. It follows the same convention as `arlo/prompts/`, `raa/prompts/`, `aga/prompts/`, and `sa/prompts/`.

### 5.1 Structure

The prompt template has two parts:

**System message (static):** Contains the full Signal and Noise classification criteria (§3 and §4), the IEEE 830 constraints (§2), and the structured output schema the model must conform to (§6). This message is the same for every batch — it does not change between calls.

**Human message (per-batch):** Contains the serialised batch of requirements as a JSON array of `{id, text}` objects. Example:

```json
[
  {"id": "REQ-1", "text": "The system shall refresh the display every 60 seconds."},
  {"id": "REQ-2", "text": "Traceback (most recent call last): File \"app.py\", line 42..."}
]
```

Each batch call receives a fresh human message with the requirements for that batch. The system message is reused across all batches within a pipeline run.

### 5.2 Loading Convention

The prompt file is read from disk at Node invocation time, not at graph compilation time. This allows prompt iteration without recompiling the graph. The file path is relative to the `ingestion/prompts/` directory.

### 5.3 LLM Invocation

The RFA invokes the LLM using LangChain's `with_structured_output` method, passing the `FilterBatch` schema (§6). This ensures the model's response is automatically validated against the schema and returned as a typed object. If the response fails schema validation, the call is retried up to 2 times (configurable).

LangChain supports multiple structured output methods (`json_schema`, `function_calling`, `json_mode`). The RFA uses the provider's default method unless overridden via pipeline configuration.

---

## 6. Structured Output Schema

The LLM must return its classification results in a specific structure. These types are defined as Pydantic models.

### 6.1 FilteredRequirement

Represents the classification result for a single requirement.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | The requirement ID, exactly as provided in the input batch |
| `classification` | `str` | One of `"SIGNAL"` or `"NOISE"` |
| `confidence` | `float` | The LLM's confidence in its classification, range `0.0`–`1.0` |
| `reason` | `str` | A one-sentence justification for the classification. For Noise, identifies which noise category the entry matches. For Signal, identifies which signal category applies. |

### 6.2 FilterBatch

Represents the classification result for an entire batch.

| Field | Type | Description |
|-------|------|-------------|
| `requirements` | `list[FilteredRequirement]` | All classified requirements in the batch. Must contain exactly one entry per input requirement — every input must be classified. |

### 6.3 Validation Guarantees

Because `with_structured_output` validates the response against these schemas:
- The `classification` field is guaranteed to be either `"SIGNAL"` or `"NOISE"` — never an arbitrary string.
- The `confidence` field is guaranteed to be a float.
- Every input requirement ID is guaranteed to appear in the output (the schema enforces completeness).
- Malformed responses trigger a retry, not a silent failure.

---

## 7. Skills vs Static Templates

Following the same principle used by RAA, AGA, and SA:

- **Skill (LLM):** The Signal/Noise classification itself requires interpretation of ambiguous requirement text. Distinguishing a borderline architectural requirement from a technical implementation detail is a semantic judgment call — the classification criteria provide constraints, but the model must exercise judgment in edge cases.

- **Static template (deterministic):** The prompt file is loaded from disk, formatted with batch data, and sent to the LLM. The prompt loading and formatting are deterministic operations.

The RFA prompt is the single skill in the ingestion pipeline. Everything else — extraction, normalisation, routing, threshold application, report generation — is deterministic.

---

## Phase Complete When...

- The IEEE 830 source register is specified with its paraphrased constraints.
- All Signal categories (6) are named and described.
- All Noise categories (7) are named, described, and given an example.
- The prompt template structure (system message + human message) is specified with the content each part contains.
- The prompt loading convention (disk read at invocation time) is documented.
- The `FilteredRequirement` and `FilterBatch` schemas are fully typed and described.
- The structured output retry behaviour is specified.
- No batching strategy, threshold mechanics, report generation, or state schema details appear in this file.
