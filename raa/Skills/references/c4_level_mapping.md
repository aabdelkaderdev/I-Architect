---
name: c4_level_mapping
description: Use when deciding the C4 type (person, system, external_system, container, component) of a candidate entity. Covers classification rules, parent references, and verification.
metadata:
  target_node: raa_a
  version: "1.0"
---

# C4 Level Mapping

## Product Summary / Definition

Authoritative reference for mapping requirement concepts to C4 model levels: person, system, external_system, container, and component.

## When to Use

Use when an extraction node must decide the C4 type of a candidate entity. Apply rules before emitting any entity.

## Quick Reference / Rules <!-- tag: c4_level_mapping:rules -->

- Person entities represent human actors described in requirements.
- System entities represent software systems owned by the organization.
- External system entities represent third-party systems outside organizational control.
- Container entities represent deployable units within a system.
- Component entities represent logical modules inside a container.
- Default to system when entity scope is ambiguous.

## Decision Guidance

If a requirement mentions both a deployable unit and its internal structure, assign the outer entity as container and inner entities as components. If only a name is given without deployment context, classify as system. Person entities must have explicit user-role language in the requirement.

## Workflow

1. Scan requirement text for actor nouns and system nouns.
2. Classify each noun into one of the five C4 levels.
3. Assign parent references (system for containers, container for components).
4. Flag ambiguous classifications as open questions.

## Common Gotchas

- Do not classify a database as a system; it is a container.
- Do not create component entities without a parent container.
- External systems are not owned; do not assign internal containers to them.

## Verification Checklist <!-- tag: c4_level_mapping:checklist -->

- Every entity has exactly one c4_type.
- Container entities have a parent_system_id.
- Component entities have a parent_container_id.
- Person entities have no parent reference.
- External system entities have no parent reference.
