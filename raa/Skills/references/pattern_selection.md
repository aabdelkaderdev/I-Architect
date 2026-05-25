---
name: pattern_selection
description: Use when classifying a requirement batch against known architectural patterns (e.g. layered, microservices). Covers pattern recognition signals, scoring, and C4 mapping.
metadata:
  target_node: raa_b
  version: "1.0"
---

# Pattern Selection

## Product Summary / Definition

Authoritative reference for matching requirement batches to known architectural patterns. Covers pattern recognition signals, confidence scoring, and pattern-to-C4 mapping.

## When to Use

Use when a pattern-driven extraction node must classify a requirement batch against a catalog of architectural patterns.

## Quick Reference / Rules <!-- tag: pattern_selection:rules -->

- Match requirements against known pattern signals before extracting entities.
- Prefer patterns with the highest signal count in the batch.
- A pattern match requires at least two confirming signals.
- Default to layered architecture when no pattern signals are detected.
- Record pattern confidence in fragment metadata.
- Map matched pattern to expected C4 entity types and relationships.

## Decision Guidance

When multiple patterns match with similar signal counts, select the most specific pattern. When no pattern exceeds the two-signal threshold, fall back to layered architecture and flag as low confidence. Pattern selection shapes entity expectations but does not override explicit requirement content.

## Workflow

1. Scan requirement batch for pattern signal keywords.
2. Score each known pattern by matching signal count.
3. Select the highest-scoring pattern above threshold.
4. Record pattern name and confidence in extraction metadata.
5. Use pattern expectations to guide entity and relationship extraction.

## Common Gotchas

- Do not force-fit requirements into a pattern when signals are weak.
- Do not ignore requirement content that contradicts the selected pattern.
- Pattern selection is guidance, not a constraint on entity extraction.

## Verification Checklist <!-- tag: pattern_selection:checklist -->

- Selected pattern has at least two confirming signals or is explicit fallback.
- Pattern name is recorded in fragment metadata.
- Confidence score is recorded with the pattern.
- Entity extraction is informed but not constrained by the pattern.
