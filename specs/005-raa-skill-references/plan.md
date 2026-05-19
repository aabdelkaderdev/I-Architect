# Implementation Plan: RAA Skill Resource Bundle References

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/005-raa-skill-references/spec.md`

**Input**: Feature specification from `specs/005-raa-skill-references/spec.md`

## Summary

This plan directs the authoring of the RAA Skill Resource Bundle reference files under `Skills/RAA/references/`. It involves creating `C4.md` and `Quality_Attributes.md` (authoritative references), as well as `Entity_Extraction.md`, `Relationship_Extraction.md`, `Pattern_Selection.md`, `Technology_Inference.md`, and `C4_Level_Mapping.md` (skill references). Skill references will strictly follow the seven-section template, incorporating hard constraints such as orphan prevention and explicit diagram scoping. The existing `SAAM.md` will be protected from alteration.

## Technical Context

**Language/Version**: Markdown

**Primary Dependencies**: None

**Storage**: Local filesystem

**Testing**: Validation script to verify all 7 files exist under `Skills/RAA/references/`, and that the five skill files contain all seven-section headers in the correct order.

**Target Platform**: Linux filesystem

**Project Type**: Agent Skill References

**Performance Goals**: N/A

**Constraints**: Skill reference files must exactly follow the template sections. Authoritative files omit Input/Output sections. No changes to the existing `SAAM.md`.

**Scale/Scope**: 7 markdown reference files under `Skills/RAA/references/`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. Reference documents explicitly define the C4 levels and notation, along with guidelines for RAA subgraphs.
- **Principle II: Deterministic Data Pipeline**: Passed.
- **Principle III: LLM Isolation & Context Injection**: Passed. These design-time guidelines define the rules that the runtime nodes and prompts implement.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/005-raa-skill-references/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
Skills/RAA/references/
├── SAAM.md                    # Protected (existing)
├── C4.md                      # Authoritative Reference
├── Quality_Attributes.md      # Authoritative Reference
├── Entity_Extraction.md       # Skill Reference
├── Relationship_Extraction.md # Skill Reference
├── Pattern_Selection.md       # Skill Reference
├── Technology_Inference.md    # Skill Reference
└── C4_Level_Mapping.md        # Skill Reference
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
