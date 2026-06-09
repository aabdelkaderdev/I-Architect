# Product Requirements Document
## Requirements Analysis Agent (RAA) — Phase 1
**Version:** 1.0  
**Status:** Draft  
**Scope:** High-level design. A mid-level PRD will follow in a subsequent session to elaborate implementation details.

---

## 1. Overview

The Requirements Analysis Agent (RAA) receives `RAAInput` from the Orchestrator — a lean, non-redundant transformation of ARLO's output enriched with full requirement text — and produces accurate, traceable natural language descriptions of a software system's C4 architecture diagrams across three levels. These descriptions serve as the primary input to the Architecture Generation Agent (AGA), which renders the actual diagrams.

The RAA bridges the gap between ARLO's architectural decisions — grounded in quality attributes and optimization — and the concrete, human-readable C4 model that communicates those decisions to stakeholders.

---

## 2. Inputs

The RAA receives `RAAInput` from the Orchestrator — a minimal, non-redundant transformation of ARLO's raw output. The Orchestrator strips all fields that the RAA does not consume and enriches requirement entries with their full text from the original requirements JSON file. The complete `RAAInput` schema and its rationale are defined in the Orchestrator PRD (§4).

`RAAInput` contains exactly four fields:

### 2.1 `condition_groups`

The primary working structure. Contains all ASRs organized by semantically equivalent
conditions. Each requirement carries only the fields the RAA needs: its ID, full text, and
quality attributes. The `cluster: -1` group is the conditionless group — requirements that
hold under any circumstances.

Each condition group maps to exactly one batch. The batch input schemas are defined in
Phase 2 §7.2: `ConcernBatchInput` for groups with `cluster != -1`, `FoundationBatchInput`
for the conditionless group (`cluster == -1`).

### 2.2 `concerns`

The optimizer output from ARLO, stripped to essentials. One concern per co-satisfiable
condition group (CCG). Each concern carries the winning architectural pattern per decision.
This is the RAA's primary source for *what* architectural decisions have been made.

The `decisions` field maps to `ConcernBatchInput.decisions` (Phase 2 §7.2). QA weights
are global, not per-concern — see `_CommonBatchInputFields.quality_weights` (Phase 2 §7.2).

### 2.3 `non_asr`

Requirements dismissed by ARLO as non-architecturally significant. Enriched by the Orchestrator from bare IDs to `{id, text}` dicts. These are functionally relevant and must contribute to C4 descriptions — they imply external systems, user types, and functional services that ASRs alone would not surface.

```python
[
    {
        "id": "REQ-002",
        "text": "The system should support OAuth2 and biometric login."
    },
    {
        "id": "REQ-005",
        "text": "Users should be able to export their data as CSV."
    }
]
```

### 2.4 `quality_weights`

Global normalized QA priorities derived from ASR frequency across the entire system. Used by the ASR Subgraph to assess the relative importance of each quality attribute when proposing entities.

```python
{
    "Performance Efficiency": 40,
    "Security": 20,
    "Reliability": 13,
    "Maintainability": 10,
    "Cost Efficiency": 8,
    "Interaction Capability": 5,
    "Compatibility": 4
}
```

---

## 3. Outputs

The RAA produces structured natural language descriptions consumed by AGA to render C4 diagrams.
The full `RAAOutput` schema is defined in Phase 2 §9. It includes L1, L2, and L3 descriptions,
the final entity registry, coverage gaps, and unresolved conflicts.

---

## 4. C4 Diagram Scope

The RAA targets the first three levels of the C4 model only.

**Level 1 — System Context (1 diagram)**
Represents the system as a whole: its users, external systems, and boundaries. Stable across all operational modes. Produced by the Foundation Batch after all concern batches have completed, so it reflects the full picture of the system.

**Level 2 — Container Diagrams (N diagrams, one per concern)**
Each concern (CCG) produces one L2 diagram reflecting the architectural decisions resolved by that concern's optimizer output. Containers from the Foundation Batch appear in every L2 diagram as the stable backbone; concern-specific containers are attached as variants.

**Level 3 — Component Diagrams (M diagrams per L2 container)**
Each container from an L2 diagram may have one or more L3 component diagrams describing its internal composition and relationships. The number of L3 diagrams is not predetermined — it is determined by the richness of requirements referencing that container.

---

## 5. Core Design Principles

These principles govern all design decisions in the RAA and must not be violated in implementation.

1. **Simplicity over engineering** — every design choice favors the simplest solution that correctly solves the problem. Complexity is added only when the simpler alternative is demonstrably insufficient.

2. **Requirements coverage** — both ASR and non-ASR requirements must contribute to C4 descriptions. Non-ASRs populate user types, external systems, and functional services that ASRs alone would miss.

3. **No entity duplication** — the same real-world entity must never appear more than once across diagram descriptions. Concern-specific variations are expressed as variants on a single canonical entity, not as separate entities.

4. **Traceability** — every proposed entity must be traceable to at least one source requirement ID.

5. **ASR primacy** — when ASR-derived and non-ASR-derived proposals conflict for the same entity, the ASR-derived definition takes authority. ASRs encode architectural intent; non-ASRs encode functional intent.

6. **Strict naming** — entity names follow a deterministic naming convention enforced through LLM prompts and output parsing, eliminating the need for fuzzy identity matching.

---

## 6. Batch Construction

### 6.1 Rationale

Batches are the unit of processing in the RAA. Each batch is self-contained — it carries all ASRs, non-ASRs, and a frozen registry snapshot needed to produce its portion of the C4 descriptions without referencing other in-progress batches.

### 6.2 Batch Types

One concern maps to exactly one CCG, one condition group, and one batch (1:1:1:1). The
Foundation Batch is the sole exception — it maps to the conditionless group (`cluster == -1`).

**Concern Batches (one per non-foundation condition group)**
Each concern batch corresponds to a condition group with `cluster != -1`. It contains:
- The ASRs belonging to that condition group.
- The non-ASRs assigned to that condition group (see Section 6.4).
- The `decisions` from the concern whose CCG includes this condition group.
- A read-only snapshot of the Global Entity Registry at the time of processing.

**Foundation Batch (one, processed last)**
Corresponds to the condition group with `cluster == -1`. It contains:
- All ASRs from the conditionless group.
- All non-ASRs not assigned to any concern batch (orphans).
- A read-only snapshot of the Global Entity Registry after all concern batches have completed.

### 6.3 Batch Processing Order

```
Concern Batch 1 → Concern Batch 2 → ... → Concern Batch N → Foundation Batch
```

Concern batches are processed sequentially. Each batch reads the registry as it stands after the previous batch's judge has written to it. The Foundation Batch runs last, benefiting from all prior registry entries — appropriate since its L1 output must represent the entire system.

Rationale for sequential over parallel: entities proposed by an earlier concern batch should not be re-proposed by a later one. Sequential processing ensures each judge can consult a progressively richer registry, minimizing redundant proposals and conflicts.

### 6.4 Non-ASR Assignment to Batches

Non-ASRs are assigned to batches using embedding similarity against condition group vectors.

**Step 1 — Compute group vectors once before batch construction begins:**
```
For each condition_group where cluster != -1:
    vectors = [embed(req.text) for req in condition_group.requirements]
    group_vector = mean(vectors)
```
Requirement text is embedded rather than `nominal_condition` because requirement text carries richer semantic signal.

**Step 2 — Assign each non-ASR exclusively:**
```
For each non_asr:
    non_asr_vector = embed(non_asr.text)
    scores = {cg: cosine_similarity(non_asr_vector, cg.group_vector)
              for cg in condition_groups where cluster != -1}

    best_group = argmax(scores)
    if scores[best_group] > SIMILARITY_THRESHOLD:
        assign non_asr exclusively to best_group's batch
    else:
        assign to Foundation Batch as orphan
```

Assignment is exclusive — each non-ASR belongs to exactly one batch. This prevents redundant processing and the entity duplication that multi-batch membership would cause. The Global Entity Registry handles cross-concern visibility for any entities derived from these requirements.

Orphaned non-ASRs are contextually neutral — semantically indifferent to any specific operational mode — which is exactly the profile of the conditionless group. The Foundation Batch is their correct home.

`SIMILARITY_THRESHOLD` is a configuration parameter determined during implementation experimentation.

---

## 7. Global Entity Registry

### 7.1 Purpose

A shared, append-enrichable data structure that persists across all batch executions. It is the single source of truth for what entities have been defined, preventing duplication across batches and concerns.

### 7.2 Access Rules

- **Subgraphs**: read-only. They propose entities but never write to the registry.
- **Judge**: the sole writer. After resolving a batch it attempts to register each surviving entity.
- **Cross-batch reads**: each batch receives a frozen snapshot of the registry as it existed before that batch began.

### 7.3 Registry Entry Schema

Defined in full in Phase 2 §3.3 as `RegistryEntry`. Key fields: `canonical_id` (format `ENT-NNN`),
`canonical_name` (PascalCase + type suffix), `c4_level`, `c4_type`, `source_requirements`
(cumulative list), `authority` (`"asr"` or `"non_asr"`), `variants` (dict keyed by `batch_id`),
and `description`.

### 7.4 Registration Rules

1. **Name match found** → enrich the existing entry. Append new source requirement IDs and add concern-specific information to `variants`. Never overwrite the canonical name or authority.
2. **No name match** → register as a new entry. Authority is set to `asr` if proposed by the ASR Subgraph, `non_asr` if proposed by the Non-ASR Subgraph.
3. **Authority conflict** (same entity proposed by both subgraphs in the same batch) → the Judge resolves via SAAM Step 5 before registration. ASR-sourced definition wins authority; non-ASR details are merged into `source_requirements` and `variants` only.

### 7.5 Naming Conventions

Strict naming is enforced through LLM prompt design and output parsing, making the identity function a plain string equality check with no fuzzy matching required.

- Entity names are **PascalCase** with no spaces, hyphens, or underscores.
- Each C4 type carries a **mandatory canonical suffix**:

| C4 Type  | Required Suffix | Example                  |
|----------|-----------------|--------------------------|
| Service  | `Service`       | `AuthenticationService`  |
| Database | `Database`      | `UserDatabase`           |
| Gateway  | `Gateway`       | `ApiGateway`             |
| Queue    | `Queue`         | `NotificationQueue`      |
| Store    | `Store`         | `SessionStore`           |
| External | `System`        | `PaymentGatewaySystem`   |
| Actor    | (none)          | `EndUser`, `SystemAdmin` |

Actors carry no suffix — the name stands alone. The actor type was added in Phase 2; all
other types follow the mandatory suffix rule.

LLM prompts include explicit instructions: use the most generic canonical term, do not use synonyms, apply the mandatory suffix for the entity's C4 type. Output parsing validates naming compliance before any entity is passed to the Judge.

---

## 8. Processing Architecture Per Batch

### 8.1 Overview

Each batch is processed by two parallel subgraphs followed by a Judge subgraph.

```
Batch Input
    ├── [ASR Subgraph]      → ASR-derived entity proposals
    └── [Non-ASR Subgraph]  → Non-ASR-derived entity proposals
                    ↓
                 [Judge]
    (SAAM validation + deduplication + relationship derivation + registry write)
                    ↓
      Partial C4 Descriptions + Registry Updates
```

### 8.2 ASR Subgraph

**Input:** ASRs in the batch, the concern's `decisions`, the condition group's per-group `weights`, registry snapshot.

**Responsibility:** Propose entities directly implied by quality attributes and concern-level architectural decisions. These proposals are high-confidence and architecturally load-bearing — they define the structural core of the C4 diagrams.

**Output:** A list of entity proposals with source requirement traceability.

### 8.3 Non-ASR Subgraph

**Input:** Non-ASRs assigned to the batch, registry snapshot.

**Responsibility:** Propose entities implied by functional requirements — user types, external systems, feature-bearing services — absent from the ASR-driven proposals. These proposals fill coverage gaps; for example, a non-ASR stating "the system should support OAuth2 login" produces an `IdentityProviderSystem` external entity.

**Output:** A list of entity proposals with source requirement traceability.

### 8.4 Judge Subgraph

The Judge is the sole decision-maker and sole writer to the Global Entity Registry. It receives proposals from both subgraphs and the current registry snapshot, then executes five steps based on the Software Architecture Analysis Method (SAAM):

**Step 1 — Scenario Development**
Each requirement (ASR and non-ASR) in the batch is treated as a scenario: a testable statement of what the system must do or be under a given condition.

**Step 2 — Architecture Description**
The union of proposals from both subgraphs forms the candidate architecture for evaluation.

**Step 3 — Scenario Classification**
Each proposed entity is classified as:
- **Direct**: explicitly required by a requirement in this batch.
- **Indirect**: implied by a quality attribute or architectural pattern but not explicitly stated in any requirement.

**Step 4 — Individual Scenario Evaluation**
For each requirement in the batch, verify that at least one proposed entity satisfies it. Requirements with no satisfying entity are flagged as coverage gaps and recorded in the batch output.

**Step 5 — Scenario Interaction**
Identify requirements that affect the same entity. These interactions surface:
- **Genuine conflicts**: two requirements demand mutually exclusive behaviors from the same entity. Flagged for human review.
- **Load-bearing entities**: entities referenced by many requirements. These receive richer descriptions in the C4 output.
- **Authority conflicts**: the same entity proposed by both subgraphs. Resolved in favor of the ASR Subgraph.

After SAAM execution, the Judge:
1. Deduplicates entities using canonical name equality.
2. Derives relationships between surviving deduplicated entities.
3. Writes surviving entities to the Global Entity Registry per the rules in Section 7.4.
4. Produces the partial C4 descriptions for this batch's scope.

---

## 9. Relationship Between Batches and C4 Levels

| Batch | Primary C4 Output | Registry Role |
|---|---|---|
| Concern Batch 1..N | L2 + L3 descriptions for that concern's operational mode | Writes concern-specific containers and components |
| Foundation Batch | L1 system context + stable L2 backbone shared across all concerns | Reads fully populated registry; writes top-level boundary entities |

L1 is assembled last because it must represent the system's full external interface — users, external systems, and boundaries — which only becomes fully visible once all concern batches and the foundation have been processed.

---

## 10. What This PRD Defers

The following are out of scope for this PRD and will be addressed in the mid-level PRD:

- Exact sub-schemas for `SystemContextDescription`, `ContainerDescription`, and `ComponentDescription`.
- LLM prompt templates for the ASR Subgraph, Non-ASR Subgraph, and Judge.
- Output parsing and naming convention validation logic.
- The exact value of `SIMILARITY_THRESHOLD` for non-ASR batch assignment.
- Internal state management within each subgraph.
- Error handling and fallback behavior for coverage gaps and genuine conflicts.
- The interface contract between RAA output and AGA input.
- Technology choices for the embedding model and vector similarity computation.

---

## 11. Design Constraints Summary

| Constraint | Rule |
|---|---|
| Entity identity | Canonical name string equality only — no fuzzy matching |
| Entity naming | PascalCase + mandatory type suffix, enforced by prompt and parser |
| Registry writes | Judge only — subgraphs are read-only consumers |
| Non-ASR assignment | Exclusive — one batch per non-ASR, highest similarity wins |
| Batch order | Concern batches sequentially first, Foundation batch last |
| Conflict resolution | SAAM Step 5 for interactions; ASR authority wins name conflicts |
| Duplication | Forbidden across all diagram levels and all concerns |
| Traceability | Every entity must reference at least one source requirement ID |
