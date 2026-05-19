# Research: RAA Synthesis and Audit

**Feature**: 021-raa-synthesis-audit
**Goal**: Identify exactly what needs to be audited from RAA_Plan.md Sections 17 and 20.

## Section 20 Deliverables to Audit
1. State schema (§4)
2. Batch construction node (§8)
3. Overlap bridging logic (§9)
4. Coherence gate (§10)
5. Parallel RAA orchestration (§12)
6. Judge node - scoring, merge, residual scan (§13)
7. Final JSON builder - deterministic merge, reconciliation, C4 validation (§16)
8. Prompt Resource Bundle (§2)
9. Skill Resource Bundle (§14)

## Section 17 Performance Profile to Audit
- Non-ASR embedding: O(n) complexity.
- ANN similarity search: O(k × m) complexity.
- RAA LLM calls: 3 per batch (reduced to 1 for incoherent batches).
- Judge LLM calls: 1 per batch.

## Findings
- **Decision**: The audit will be driven by a structured checklist mapping directly to the deliverable numbers from Section 20.
- **Rationale**: A simple checklist allows for straightforward verification without needing to invent a new reporting format.
- **Alternatives considered**: Automated AST parsing for complexity. Rejected in favor of manual code review and tracing during the audit implementation task, as it is simpler and more reliable.
