---
name: raa
description: Requirements Analysis Agent references for C4 extraction, relationship mapping, pattern selection, technology inference, and SAAM-informed reconciliation.
metadata:
  version: "1.0"
  target: raa
---

# RAA Skill

## Overview

Design-time reference bundle for the Requirements Analysis Agent pipeline. Each reference file contains authoritative rules, decision guidance, workflows, gotchas, and verification checklists for one domain concern. Runtime prompts inject only tagged sections — never the full bundle.

## References

- `references/c4_level_mapping.md` — C4 level assignment rules and checklist. Use when categorizing entities by C4 type.
- `references/entity_extraction.md` — Entity extraction rules and checklist. Use when identifying C4 entities from requirements.
- `references/relationship_extraction.md` — Relationship derivation rules and checklist. Use when connecting entities.
- `references/pattern_selection.md` — Architectural pattern decision guidance. Use when matching requirements to known patterns.
- `references/technology_inference.md` — Technology annotation inference rules. Use when guessing tech stack from requirements.
- `references/saam.md` — SAAM scenario evaluation reference. Use for scenario-based architecture analysis.
- `references/c4.md` — General C4 model reference. Use for shared C4 metamodel rules.
- `references/quality_attributes.md` — Quality attribute reference. Use when evaluating non-functional requirements.
