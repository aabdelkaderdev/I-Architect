# Data Model: RAA Skill Reference Template

This document defines the schema and templates enforced on the skill references.

## 1. Skill Reference Seven-Section Template

All files under `Skills/RAA/references/` (except authoritative references) must conform to this exact markdown layout:

```markdown
# [Skill Reference Name]

## 1. Purpose
[Description of the skill role and triggers]

## 2. Input
[Schema of input state channels]

## 3. Normative rules
[List of testable hard constraints]

## 4. Decision guidelines
[Heuristics and default rules]

## 5. Output schema
[Details of output dataclass and fields]

## 6. Error cases
[Known failure modes and error actions]

## 7. Examples
[Concrete worked example]
```

---

## 2. Authoritative References Structure

Authoritative files (`C4.md`, `Quality_Attributes.md`) define domains and do not contain dynamic input/output steps. They contain general structured sections detailing:
- Adaptations for the RAA pipeline.
- Taxonomy categories and examples.
