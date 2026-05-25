---
name: quality_attributes
description: Use when mapping non-functional requirements or analyzing quality attributes (e.g. performance, security). Covers quality dimensions, classification, and context weighting.
metadata:
  target_node: raa_a
  version: "1.0"
---

# Quality Attributes

## Product Summary / Definition

Authoritative reference for mapping non-functional requirements to quality attribute scenarios. Covers performance, scalability, security, availability, maintainability, and interoperability quality dimensions.

## When to Use

Use when RAA-A evaluates SAAM scenarios or when any extraction node must weigh quality attribute signals in requirement text.

## Quick Reference / Rules <!-- tag: quality_attributes:rules -->

- Map each non-functional requirement to exactly one primary quality attribute.
- Performance: response time, throughput, resource utilization.
- Scalability: horizontal scaling, vertical scaling, elasticity.
- Security: authentication, authorization, data protection, audit.
- Availability: uptime, fault tolerance, disaster recovery.
- Maintainability: modularity, testability, deployability.
- Record quality attribute weights in extraction context.

## Decision Guidance

When a requirement spans multiple quality attributes, select the primary attribute from the dominant concern. Record secondary attributes in entity metadata. Quality weights from the batch context influence scenario prioritization.

## Workflow

1. Identify non-functional language in each requirement.
2. Classify into one of the six quality dimensions.
3. Assign weight based on requirement priority.
4. Pass quality weights into extraction context.
5. Use weights to prioritize scenario evaluation.

## Common Gotchas

- Do not treat all non-functional requirements as performance.
- Do not ignore quality attributes when they are implicit in requirement language.
- Avoid double-weighting by mapping one requirement to multiple primary attributes.

## Verification Checklist <!-- tag: quality_attributes:checklist -->

- Each non-functional requirement maps to one primary quality attribute.
- Quality weights are recorded in extraction context.
- No requirement maps to more than one primary attribute.
- Implicit quality attributes are captured when detectable.
