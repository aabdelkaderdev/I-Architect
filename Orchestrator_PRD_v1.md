# Product Requirements Document
## Orchestrator — Phase 1
**Version:** 1.1  
**Status:** Draft  
**Scope:** High-level design. Covers the orchestrator's role as the coordination layer between ARLO, RAA, AGA, and RGA.

---

## 1. Overview

The Orchestrator is the pipeline coordination layer. It does not perform any analytical or generative work itself. Its sole responsibilities are checkpointing, input transformation, sequencing, and output routing between the pipeline's modules.

---

## 2. Pipeline Position

```
NL Requirements (JSON)
      ↓
   [ARLO]
      ↓
[Orchestrator] ── checkpoint ──→ ARLOOutput.pkl
      │
      ├── transforms ARLOOutput into RAAInput
      │      ├── strips redundant / irrelevant fields
      │      ├── enriches requirements with full text (from JSON)
      │      └── restructures concerns into lean format
      │
      ↓
    [RAA]
      │
      ├── C4 Descriptions (L1, L2, L3) ──→ [AGA]
      └── concerns + stats ───────────────→ [RGA]
```

---

## 3. Responsibilities

### 3.1 Checkpointing

After ARLO completes, the Orchestrator persists the raw `ARLOOutput` as a `.pkl` file before any further processing occurs. This checkpoint enables pipeline recovery without re-running ARLO, which is the most computationally expensive stage.

### 3.2 Input Transformation

The Orchestrator transforms ARLO's raw output into the `RAAInput` schema — a minimal, non-redundant structure containing only the fields the RAA requires. This transformation has three sub-steps:

#### 3.2.1 Requirement Text Enrichment

ARLO's output contains requirement IDs and quality metadata but not the full original requirement text. The Orchestrator loads the original requirements from a JSON file structured as a flat key–value mapping:

```json
{
    "R1": "The system shall allow officers to log incidents in real time.",
    "R2": "Response times must remain below 2 seconds under normal load.",
    ...
}
```

This JSON file is the same source document originally passed to ARLO. The Orchestrator uses it to hydrate requirement IDs with their full text in both `condition_groups` and `non_asr`.

**Enrichment targets:**

- `condition_groups[].requirements[]` — each requirement entry receives a `text` field looked up by its `id`.
- `non_asr` — transformed from a flat list of ID strings into a list of `{id, text}` dicts.

#### 3.2.2 Field Stripping

The following fields are stripped from `ARLOOutput` because they are redundant, irrelevant, or unused by the RAA:

| Stripped Field | Reason |
|---|---|
| `stats` | Pipeline diagnostics; not referenced by any RAA process |
| `asrs` | Exact duplicate of data already in `condition_groups[].requirements[]` |
| `condition_groups[].requirements[].condition_text` | Always identical to parent group's `nominal_condition` |
| `condition_groups[].requirements[].is_architecturally_significant` | Always `true` by construction — these are ASRs by definition |
| `condition_groups[].conditions` | Index array into the redundant `asrs`; never needed since requirements are inline |
| `concerns[].satisfiable_group` | Internal ARLO grouping state; the RAA works from the top-level `condition_groups` |
| `concerns[].decisions[].score` | Optimizer ranking score; the RAA takes decisions as given |
| `concerns[].decisions[].satisfied_qualities` | QA trade-off metadata not consumed by any RAA process |
| `concerns[].decisions[].unsatisfied_qualities` | QA trade-off metadata not consumed by any RAA process |
| `concerns[].decisions[].arch_pattern_name` | Always identical to `selected_pattern` (confirmed by ARLO optimizer code: `groups` parameter is never passed, so group label falls back to row name) |

#### 3.2.3 Structural Reshaping

The Orchestrator restructures the surviving fields into the `RAAInput` schema:

**`condition_groups`** — cleaned to contain only:
```python
[
    {
        "nominal_condition": str,
        "cluster": int,
        "requirements": [
            {
                "id": str,
                "text": str,                   # injected by enrichment
                "quality_attributes": list[str]
            }
        ]
    }
]
```

**`concerns`** — reshaped to contain only:
```python
[
    {
        "ccg_id": int,                        # matches cluster index in condition_groups
        "weights": dict[str, int],            # per-CCG QA weights
        "decisions": [
            {
                "selected_pattern": str        # winning architectural pattern
            }
        ]
    }
]
```

**`non_asr`** — transformed from `list[str]` to:
```python
[
    {
        "id": str,
        "text": str                            # injected by enrichment
    }
]
```

**`quality_weights`** — passed through unchanged:
```python
dict[str, int]
```

### 3.3 RAA Invocation

The Orchestrator passes the transformed `RAAInput` to the RAA as a single input. It does not manage the RAA's internal batch sequencing — that is the RAA's own responsibility. The Orchestrator simply invokes the RAA and waits for `RAAOutput`.

### 3.4 Output Routing

Once the RAA returns `RAAOutput`, the Orchestrator routes the outputs to downstream modules:

| Source | Output Field | Destination | Notes |
|---|---|---|---|
| `RAAOutput` | `l1_description`, `l2_descriptions`, `l3_descriptions` | AGA | C4 diagram descriptions for rendering |
| `RAAOutput` | `entity_registry` | AGA | Final registry state, used by AGA to resolve entity references during rendering |
| `RAAOutput` | `coverage_gaps`, `conflicts` | RGA | Quality diagnostics produced by the RAA (unresolved conflicts and uncovered requirements) |
| `ARLOOutput` (pre-transformation checkpoint) | `concerns`, `stats` | RGA | Passed through directly from the original ARLO output; the RAA does not produce these |

---

## 4. Complete RAAInput Schema

The following is the full schema that the Orchestrator produces and the RAA consumes:

```python
class RAAInput(TypedDict):
    condition_groups: list[ConditionGroup]
    concerns:         list[Concern]
    non_asr:          list[NonASR]
    quality_weights:  dict[str, int]
```

Where:

```python
class Requirement(TypedDict):
    id:                  str
    text:                str
    quality_attributes:  list[str]

class ConditionGroup(TypedDict):
    nominal_condition: str
    cluster:           int          # -1 = conditionless group
    requirements:      list[Requirement]

class Decision(TypedDict):
    selected_pattern: str

class Concern(TypedDict):
    ccg_id:    int               # matches cluster index in condition_groups
    weights:   dict[str, int]
    decisions: list[Decision]

class NonASR(TypedDict):
    id:   str
    text: str
```

---

## 5. What the Orchestrator Does Not Do

- It does not interpret, analyze, or modify the semantic content of `ARLOOutput` — transformation is purely structural.
- It does not manage the RAA's internal batch execution order.
- It does not make any decisions about C4 diagram structure or content.
- It does not interact with the Global Entity Registry, which is internal to the RAA.
