# SAAM Normative Prompt Constraints

Per RAA_Plan.md Section 2B. These are hard constraints injected into the judge node and any node performing SAAM tradeoff analysis. Authority: SAAM — SEI Technical Report source register entry.

## The 5-Step SAAM Process

Apply these steps in strict order:

1. **Canonical Partitioning:** Divide the architecture into its constituent systems, containers, and components. Each partition must be coherent and traceable to requirements.
2. **Map Requirements to Structures:** Assign every requirement in the current batch to the architectural structures it affects. Record requirement-to-structure traces.
3. **Choose Quality Attributes:** Select quality attributes informed by ARLO quality weights. Prioritize attributes with the highest aggregate frequency counts across satisfiable groups.
4. **Define Evaluation Scenarios:** For each selected quality attribute, define one or more concrete evaluation scenarios. A scenario describes a specific usage context that exercises the quality attribute.
5. **Evaluate Structures Against Scenarios:** Score each architectural structure (system, container, component, relationship) against every scenario. Use weighted scoring: structures that satisfy more high-weight scenarios receive higher SAAM scores.

## Quality-Attribute Scenario Guidance

- Use ARLO `quality_weights` (frequency counts) to prioritize which quality attributes drive scenario definition.
- Scenarios must be concrete and testable — not abstract quality descriptions.
- A single quality attribute may require multiple scenarios to cover its distinct dimensions (e.g., Security → authentication, authorization, data encryption).
- When ARLO quality weights are unavailable, default to equal weighting across all quality attributes present in the requirement set.

## Scoring Rules

- Fragment-level SAAM score is the weighted sum of scenario coverage, divided by total scenarios.
- Higher-weighted quality attributes contribute proportionally more to the aggregate score.
- Fragments from incoherent batches (reduced_confidence = true) receive a 0.5× SAAM weight multiplier.
