---
name: entity_extraction
description: Use when analyzing a requirement batch to extract C4 entities with appropriate names, types, and traceability. Covers identification rules, naming standards, and deduplication.
metadata:
  target_node: raa_c
  version: "1.0"
---

# Entity Extraction

## Product Summary / Definition

Authoritative reference for extracting C4 entities from natural-language requirements. Covers entity naming, deduplication, and traceability to source requirements.

## When to Use

Use when an extraction node processes a batch of requirements and must produce a flat list of C4 entities with requirement traceability.

## Quick Reference / Rules <!-- tag: entity_extraction:rules -->

- Extract one entity per distinct architectural concept in the requirements.
- Prefer existing running-model entities when requirement intent matches.
- Name entities with domain terminology from the requirement text.
- Each entity must reference at least one requirement_id.
- Do not create duplicate entities for the same concept within one batch.
- Flag near-duplicate entities as open questions for later deduplication.

## Decision Guidance

When a requirement describes a concept already present in the running model, reuse the existing entity id and name. When a requirement describes a modification to an existing entity, extract the updated form and reference the same id.

## Workflow

1. Read each requirement in the batch.
2. Identify noun phrases that represent architectural elements.
3. Map each noun phrase to a C4 type using c4_level_mapping rules.
4. Check the running model for existing matching entities.
5. Create new entities only for genuinely new concepts.
6. Attach requirement_ids to every entity.

## Common Gotchas

- Do not extract entities for purely functional requirements with no architectural footprint.
- Do not conflate deployment concepts with logical architecture concepts.
- Avoid entity name collisions with the running model unless they represent the same concept.

## Verification Checklist <!-- tag: entity_extraction:checklist -->

- Every entity has requirement traceability.
- No duplicate entity names exist within the fragment.
- Entity names use domain terminology from source requirements.
- Running-model entities are reused when intent matches.
- Each entity has a valid c4_type.
