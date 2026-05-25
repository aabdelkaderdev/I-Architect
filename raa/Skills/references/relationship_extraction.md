---
name: relationship_extraction
description: Use when connecting C4 entities in a requirement batch with valid, directed relationships. Covers interaction identification, direction mapping, and diagram scoping.
metadata:
  target_node: raa_c
  version: "1.0"
---

# Relationship Extraction

## Product Summary / Definition

Authoritative reference for deriving directed relationships between C4 entities from requirement text. Covers relationship naming, direction, scope assignment, and cardinality.

## When to Use

Use when an extraction node has produced a candidate entity list and must connect them with valid C4 relationships.

## Quick Reference / Rules <!-- tag: relationship_extraction:rules -->

- Extract a relationship for every explicit interaction verb in the requirements.
- Source is the acting entity, target is the receiving entity.
- Relationship description must quote or paraphrase the requirement text.
- Use container scope for container-to-container relationships.
- Use component scope for component-to-component relationships.
- Use context scope for system-level or cross-system relationships.
- Each relationship must reference at least one requirement_id.
- Infer bidirectional relationships only when requirement text explicitly describes two-way interaction.

## Decision Guidance

When a requirement describes data flow, make the data producer the source and consumer the target. When a requirement describes a control action, make the controller the source and controlled entity the target. Skip relationships between entities that are merely co-located in text without an interaction verb.

## Workflow

1. Review each pair of extracted entities against requirement text.
2. Identify interaction verbs connecting entity pairs.
3. Determine direction from actor to target.
4. Assign diagram scope based on endpoint C4 types.
5. Generate relationship id from source and target ids.

## Common Gotchas

- Do not create relationships for entities that co-occur in text but do not interact.
- Do not assume bidirectional unless text explicitly describes both directions.
- Ensure both endpoints exist in the entity list before emitting the relationship.

## Verification Checklist <!-- tag: relationship_extraction:checklist -->

- Every relationship connects two valid entity ids.
- Relationship direction matches requirement intent.
- Diagram scope is assigned for every relationship.
- Each relationship references at least one requirement_id.
- No orphan relationships reference missing entities.
