---
name: technology_inference
description: Use when annotating C4 entities with technology stack choices based on requirement keywords. Covers keyword mapping, default stacks, and confidence levels.
metadata:
  target_node: raa_c
  version: "1.0"
---

# Technology Inference

## Product Summary / Definition

Authoritative reference for inferring technology stack annotations from natural-language requirements. Covers technology keyword detection, default assignments, and confidence levels.

## When to Use

Use when an extraction node must annotate entities with likely technology choices based on requirement language.

## Quick Reference / Rules <!-- tag: technology_inference:rules -->

- Infer technology only when requirement text contains explicit technology keywords.
- Do not invent technology choices for generic requirement descriptions.
- Record technology annotations in entity metadata with a confidence level.
- Default to the organization standard stack when requirements imply but do not name a technology.
- Flag technology inferences as assumptions in fragment metadata.

## Decision Guidance

When a requirement names a specific database, message broker, or framework, annotate the entity with that technology. When a requirement describes a need but not a specific technology, either omit the annotation or use the organization default with low confidence. Never infer a technology that contradicts the running model.

## Workflow

1. Scan requirement text for technology keywords.
2. Match keywords to known technology categories.
3. Assign technology annotations to relevant entities.
4. Record confidence level for each annotation.
5. Flag low-confidence inferences as assumptions.

## Common Gotchas

- Do not infer cloud provider specifics unless explicitly mentioned.
- Do not override running-model technology choices without explicit requirement evidence.
- Avoid inferring version numbers unless stated in requirements.

## Verification Checklist <!-- tag: technology_inference:checklist -->

- Each technology annotation has a confidence level.
- No technology contradicts the running model.
- Inferred technologies are recorded as assumptions when low confidence.
- Generic requirements do not receive invented technology choices.
