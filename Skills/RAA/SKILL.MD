---
name: raa-requirement-analysis
description: >
  Requirement Analysis Agent — middle pipeline stage between ARLO and AGA.
  Partitions requirements into condition-group-anchored batches, runs three
  parallel analysis subgraphs per batch, judges/merges results, and outputs
  a C4-compliant entity-relationship JSON model. No diagrams, no code.
---

# RAA — Requirement Analysis Agent

## Pipeline Position

```
ARLO → RAA (this) → AGA
```

ARLO feeds ASRs, condition groups, quality weights, and embeddings.
RAA outputs a C4-compliant JSON model. AGA generates diagrams and code.

---

## Execution Model

1. **Prepare** — normalize requirements; embed non-ASRs (same FastEmbed model as ARLO).
2. **Build batches** — each ARLO condition group anchors a batch (ASRs + top-k non-ASRs via ANN, threshold ≥ 0.65, max 10).
3. **Bridge** — 1–3 shared requirements between adjacent batches (hard cap: 3).
4. **Coherence gate** — score < 0.55 triggers split or `reduced_confidence` fallback.
5. **Execute** — per batch, 3 parallel subgraphs (RAA-A: SAAM-first, RAA-B: pattern-driven, RAA-C: entity-driven).
6. **Judge** — SAAM-weighted scoring → select best fragment → deterministic merge → update `running_arch_model`.
7. **Final merge** — combine all batch outputs into one C4 JSON.

Batches run sequentially; each batch inherits the accumulated model as hard constraints.

---

## Subgraph Strategies

| Subgraph | Strategy | Focus |
|----------|----------|-------|
| RAA-A | Conservative, SAAM-first | Quality attribute scenarios → entities |
| RAA-B | Pattern-driven | Architectural patterns → requirements |
| RAA-C | Entity/relationship-driven | Bottom-up C4 extraction |

---

## Output

C4-compliant JSON: systems, containers, components, people, external systems, directed relationships, patterns, confidence metadata. **No diagrams. No code.**

---

## References

| Reference | Content | When to Load |
|-----------|---------|-------------|
| [SAAM.md](references/SAAM.md) | Adapted SAAM scoring for judge node | Judge merge/scoring logic |
| [C4 Model](https://c4model.com/diagrams) | C4 level definitions, element types | Entity/relationship extraction |
| [SAAM — SEI](https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf) | Original 5-step SAAM method | SAAM constraint reference |
