---
name: saam
description: Use when performing SAAM-first architectural scenario evaluation. Covers scenario definition, quality mapping, and satisfaction analysis.
metadata:
  target_node: raa_a
  version: "1.0"
---

# SAAM (Software Architecture Analysis Method)

## Product Summary / Definition

Authoritative reference for SAAM-based scenario evaluation. Covers scenario definition, stakeholder prioritization, quality attribute mapping, and interaction analysis.

## When to Use

Use when RAA-A performs SAAM-first architectural extraction. Apply when evaluating how well a candidate architecture satisfies quality scenarios.

## Quick Reference / Rules <!-- tag: saam:rules -->

- Define scenarios from requirement text before evaluating architecture.
- Each scenario must describe a stimulus, context, and expected response.
- Map scenarios to quality attributes from the quality_attributes reference.
- Evaluate candidate architecture against each scenario independently.
- Record scenario satisfaction as satisfied, partially satisfied, or unsatisfied.
- Flag unsatisfied scenarios as open questions with suggested resolutions.

## Decision Guidance

When a scenario is partially satisfied, extract the gap as a cross-cutting concern. When multiple scenarios conflict, prioritize by stakeholder weight from quality_attributes. SAAM results inform but do not replace C4 structural extraction.

## Workflow

1. Extract candidate scenarios from requirement batch.
2. Map each scenario to relevant quality attributes.
3. Evaluate the candidate fragment against each scenario.
4. Score satisfaction per scenario.
5. Emit cross-cutting concerns for partial or failed scenarios.

## Common Gotchas

- Do not evaluate scenarios against entities that have not been extracted yet.
- Do not treat SAAM results as entity extraction; SAAM evaluates, C4 extracts.
- Avoid scenario explosion; one scenario per distinct quality concern.

## Verification Checklist <!-- tag: saam:checklist -->

- Every scenario has stimulus, context, and response defined.
- Each scenario maps to at least one quality attribute.
- Satisfaction is recorded for each scenario.
- Unsatisfied scenarios generate cross-cutting concerns.
