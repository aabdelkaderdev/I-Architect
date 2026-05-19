# Authoritative Source Register

Per RAA_Plan.md Section 2A. This register is the authoritative index of sources that govern all prompt-driven RAA nodes. Every constraint in `c4_constraints.md`, `saam_constraints.md`, and `excerpts/*.txt` traces back to a row in this table.

## Source Table

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| C4 Model — Diagrams | https://c4model.com/diagrams | (set on retrieval) | Level definitions (Context, Container, Component), element types, relationship notation |
| C4 Model — Notation | https://c4model.com/diagrams/notation | (set on retrieval) | Labelling rules, technology annotation, description requirements, relationship syntax |
| SAAM — SEI Technical Report | https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf | (set on retrieval) | 5-step SAAM evaluation method: partition, map requirements, select quality attributes, define scenarios, evaluate |

## Retrieval Tag Mapping

Per RAA_Plan.md Section 21C. Nodes retrieve constraint excerpts by tag name. Each tag resolves to exactly one file under `raa/prompts/excerpts/`.

| Tag | File | Node Usage |
|-----|------|------------|
| `c4:levels` | `c4_levels.txt` | Entity extraction, Pattern selection, Final merge |
| `c4:notation` | `c4_notation.txt` | Entity extraction, Relationship extraction, Final merge |
| `c4:technology` | `c4_technology.txt` | Relationship extraction, Final merge |
| `saam:steps` | `saam_steps.txt` | Judge SAAM tradeoff scoring |
| `saam:scenarios` | `saam_scenarios.txt` | Judge SAAM tradeoff scoring |

## Retrieval Policy

Per RAA_Plan.md Section 2D:

1. **Full source documents are never copied into prompts.** Only paraphrased constraint excerpts (≤25 words each) are injected.
2. **Direction of authority:** Source Register → Prompt Resource Bundle (`raa/prompts/`) → skill prompts (at runtime).
3. **Each LLM node receives only the excerpts relevant to its function.** No node receives the full bundle.
4. **The Source Register is the single authority** for all C4 and SAAM content in the Prompt Resource Bundle. If a constraint in `c4_constraints.md` or `saam_constraints.md` cannot be traced to a source register entry, it must be added to this table or removed.
