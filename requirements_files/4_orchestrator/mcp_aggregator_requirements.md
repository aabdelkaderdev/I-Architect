# MCP Aggregator — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/mcp_aggregator_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Barrier Synchronization

#### FR-MCP-001: Parallel Branch Barrier
- **Description:** The MCP Aggregator SHALL wait for all active parallel branches (Alpha, Beta, Gamma) to complete before aggregation begins. The waiting mechanism SHALL use LangGraph's `Send` API barrier with a global async timeout.
- **SRS Trace:** §9.1
- **Priority:** Must
- **Acceptance Criteria:** Aggregation does not start until all 3 parallel branches have either completed or timed out.

#### FR-MCP-002: Barrier Timeout (5 Minutes)
- **Description:** The barrier SHALL enforce a 5-minute maximum wait time. If an instance has not completed within 5 minutes while others have finished:
  1. Log a warning: *"[LLM_name] instance timed out."*
  2. Proceed with partial aggregation using the available outputs (minimum 2 required).
  3. If fewer than 2 outputs are available, fail the workflow with a retry suggestion.
- **SRS Trace:** §9.1, §13.3
- **Priority:** Must
- **Acceptance Criteria:** If Gamma hangs beyond 5 minutes, aggregation proceeds with Alpha + Beta; the result is annotated as "Partial Consensus."

### 1.2 Input Resolution

#### FR-MCP-003: User Override Input Selection
- **Description:** Before aggregation, the node SHALL check the Django API at `GET /api/projects/{id}/active_versions/{agent_name}` for user-selected version overrides (from the History Drawer). If specific overrides exist, those exact file paths are loaded.
- **SRS Trace:** §1.1, §5
- **Priority:** Must
- **Acceptance Criteria:** If the user selected "Version 2" for RAA Alpha via the History Drawer, the aggregator uses that specific file, not the latest.

#### FR-MCP-004: Automatic Latest Fallback
- **Description:** If no user override exists, the aggregator SHALL scan `/{project_name}/{agent}_output/llm_{instance}/`, sort files by timestamp descending, and select the newest file (`[0]`).
- **SRS Trace:** §5
- **Priority:** Must
- **Acceptance Criteria:** In the absence of user overrides, the most recently generated file is used for each instance.

### 1.3 Aggregation Strategies (By Agent)

#### FR-MCP-005: RAA Aggregation — LLM-Based Semantic Synthesis
- **Description:** The aggregator SHALL merge 3 distinct TOON files (`alpha.toon`, `beta.toon`, `gamma.toon`) using `llm_alpha` with the prompt: *"Act as a Lead Architect. Review these 3 proposed architectural models (Alpha, Beta, Gamma). Synthesize a single, unified TOON model that incorporates the strongest structural elements of all three. Ensure no duplicate Entities exist. Resolve logical conflicts."*
- **Output:** `raa_output/mcp_aggregator/raa_aggregated.toon`
- **SRS Trace:** §9.1
- **Priority:** Must
- **Acceptance Criteria:** The aggregated TOON contains no duplicate entity IDs and represents a coherent merge of all three inputs.

#### FR-MCP-006: AGA Aggregation — LLM-Based Code Merge
- **Description:** The aggregator SHALL merge 3 distinct PlantUML files (`alpha.puml`, `beta.puml`, `gamma.puml`) using `llm_alpha` with the prompt: *"Analyze these three PlantUML architectural variants. Synthesize a single, unified PlantUML file that incorporates the strongest structural elements of all three. Ensure syntax validity (no duplicate IDs, closed brackets)."*
- **Output:** `aga_output/mcp_aggregator/aga_aggregated.puml`
- **SRS Trace:** §9.1
- **Priority:** Must
- **Acceptance Criteria:** The aggregated `.puml` compiles without syntax errors when sent to the PlantUML server.

#### FR-MCP-007: SA Aggregation — Elective Selection (Median Voting)
- **Description:** The aggregator SHALL combine 3 SA evaluation JSONs using a deterministic Python function (no LLM required):
  1. Extract `total_percent_correct` from Alpha (S_α), Beta (S_β), Gamma (S_γ).
  2. Calculate Mathematical Median M.
  3. Identify the Median Instance: the instance whose score is closest to M.
  4. Adopt the *entire JSON payload* of the Median Instance as `sa_aggregated.json`.
  5. **Divergence Check:** If `(Max(S) - Min(S)) > 30%`, append a `divergence_warning` object.
- **Output:** `sa_output/mcp_aggregator/sa_aggregated.json`
- **SRS Trace:** §9.1, §9.6
- **Priority:** Must
- **Acceptance Criteria:** Scores [72, 85, 90] produce median 85; Beta's full JSON is adopted; no divergence warning (range = 18).

### 1.4 Context Compression

#### FR-MCP-008: History Management via Memory Summarization
- **Description:** After aggregation, the node SHALL run `ConversationSummaryBufferMemory` on the `messages` list of Alpha, Beta, and Gamma to generate 3 short summaries (~200 tokens each). The raw message history SHALL be cleared from the LangGraph state to prevent token bloat.
- **SRS Trace:** §9.1
- **Priority:** Must
- **Acceptance Criteria:** After aggregation, the LangGraph state's `messages` list is empty; `previous_step_summary` contains a concise string.

#### FR-MCP-009: State Return Payload
- **Description:** The aggregator SHALL return a state update containing:
  ```python
  {
      "aggregated_output_path": "/path/to/aggregated/file",
      "previous_step_summary": "Alpha focused on microservices. Beta suggested modular monolith...",
      "messages": []  # Clear raw history
  }
  ```
- **SRS Trace:** §9.1
- **Priority:** Must
- **Acceptance Criteria:** Downstream nodes receive the `aggregated_output_path` and summary without access to the raw message history.

---

## 2. Non-Functional Requirements (NFR)

### NFR-MCP-001: Deterministic SA Aggregation
- **Description:** SA aggregation (median voting) SHALL produce identical results given identical inputs — no randomness or LLM involvement.
- **SRS Trace:** §9.1
- **Metric:** Same 3 SA inputs always produce the same aggregated output.

### NFR-MCP-002: LLM Synthesis Quality
- **Description:** The LLM-based RAA/AGA aggregation SHALL preserve all unique entities/relationships from the 3 inputs and introduce no hallucinated entities not present in any input.
- **SRS Trace:** §9.1
- **Metric:** Post-aggregation audit shows zero hallucinated entities and ≥ 90% entity coverage from all 3 inputs.

### NFR-MCP-003: Memory Efficiency
- **Description:** Context compression SHALL reduce the LangGraph state size by ≥ 80% after aggregation to prevent downstream token budget violations.
- **SRS Trace:** §9.1
- **Metric:** State size (in tokens) decreases by ≥ 80% after the aggregator node executes.

---

## 3. Interface Requirements (IR)

### IR-MCP-001: Input Interfaces
| Input | Source | Format |
|:--|:--|:--|
| RAA Alpha/Beta/Gamma TOON | `raa_output/llm_alpha/*.toon`, etc. | TOON (JSON) |
| AGA Alpha/Beta/Gamma .puml | `aga_output/llm_alpha/*.puml`, etc. | PlantUML text |
| SA Alpha/Beta/Gamma JSON | `sa_output/llm_alpha/*.json`, etc. | Evaluation JSON |
| User Version Overrides | `GET /api/projects/{id}/active_versions/{agent}` | JSON response |

### IR-MCP-002: Output Interfaces
| Output | Target | Format |
|:--|:--|:--|
| Aggregated RAA TOON | `raa_output/mcp_aggregator/raa_aggregated.toon` | TOON (JSON) |
| Aggregated AGA PUML | `aga_output/mcp_aggregator/aga_aggregated.puml` | PlantUML text |
| Aggregated SA JSON | `sa_output/mcp_aggregator/sa_aggregated.json` | Evaluation JSON |

### IR-MCP-003: File System Structure
```
/{project_name}/
├── raa_output/
│   ├── llm_alpha/     ← Read (Input)
│   ├── llm_beta/      ← Read (Input)
│   ├── llm_gamma/     ← Read (Input)
│   └── mcp_aggregator/
│       └── raa_aggregated.toon  ← Write (Output)
├── aga_output/
│   ├── llm_alpha/
│   ...
│   └── mcp_aggregator/
│       └── aga_aggregated.puml  ← Write (Output)
└── sa_output/
    ...
    └── mcp_aggregator/
        └── sa_aggregated.json   ← Write (Output)
```

---

## 4. Disaster Recovery Requirements (DR)

### DR-MCP-001: Partial Consensus (Timeout)
- **Failure Mode:** One of three parallel instances times out after 5 minutes.
- **Recovery Action:** Proceed with 2-instance aggregation. For LLM merges (RAA/AGA), reduce prompt to reference 2 variants. For SA, calculate median of 2 scores (use average). Annotate result as "Partial Consensus."
- **User-Facing Message:** ⚠️ *"The '{LLM_name}' instance timed out. Results are based on partial (2/3) consensus."*
- **SRS Trace:** §13.3

### DR-MCP-002: OOM / Sequential Fallback
- **Failure Mode:** A parallel node experiences an OOM (Exit Code 137).
- **Recovery Action:** Per SRS §13.3, the Orchestrator restarts that specific node in sequential mode. The Aggregator's 5-minute timeout clock pauses/resets if a "Recovery Restart" signal is detected.
- **User-Facing Message:** ⚠️ *"Instance '{LLM_name}' ran out of memory and has been restarted in sequential mode."*
- **SRS Trace:** §13.3 (R-3)

### DR-MCP-003: Insufficient Outputs
- **Failure Mode:** Fewer than 2 outputs are available after timeout expiry.
- **Recovery Action:** Fail the workflow entirely. Suggest user retry with Workflow 1 (single LLM) or reduced model complexity.
- **User-Facing Message:** 🛑 *"Pipeline failed: Only {N}/3 analysis instances completed. Please try Workflow 1 (Single LLM) or reduce input complexity."*
- **SRS Trace:** §13.3

---

*End of MCP Aggregator Requirements Document*
