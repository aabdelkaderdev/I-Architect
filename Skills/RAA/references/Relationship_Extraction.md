# Relationship Extraction — Skill Reference

## 1. Purpose

Guidelines for deriving directed C4 relationships from requirement text. Applied by all three RAA subgraphs during batch entity analysis. References C4.md for relationship syntax and C4_Level_Mapping.md for diagram scope assignment.

## 2. Input

- **Current batch requirements** (normalized): `list[dict]` with keys `id`, `text`, `is_asr`, `quality_attributes`, `condition_text`.
- **Fragment entities**: the systems, containers, components, persons, and external systems proposed by the same subgraph in the current batch.
- **Running architecture model** (`running_arch_model`): entities from prior batches available as relationship endpoints.
- **ARLO quality weights**: used to prioritize relationship extraction for high-weight requirements.

## 3. Normative rules

1. **Explicit diagram_scope (hard rule):** Every proposed relationship must carry an explicit `diagram_scope` value. The scope is determined by the types of the source and target endpoints:
   - system ↔ system, system ↔ person, system ↔ external_system → `context`
   - container ↔ container, container ↔ person, container ↔ external_system → `container`
   - component ↔ component, component ↔ container, component ↔ external_system → `component`
2. **Direction:** Every relationship must state direction (source to target). Source is the initiating element; target is the receiving or serving element.
3. **Interaction descriptions:** Use a short verb phrase for `interaction_type` (e.g., "sends payment events to", "queries data from", "authenticates via").
4. **Technology inference:** Assign `technology` when the requirement text mentions a protocol, API type, or communication mechanism. Leave as `null` when no signal exists.
5. **Cardinality awareness:** When requirements indicate "multiple," "all," or "every" in the interaction context, note it in the interaction description but do not create duplicate relationships.
6. **Implicit relationships:** Do not invent relationships not implied by requirements. If requirement R1 says "the system sends orders to the warehouse," extract exactly one relationship; do not infer a bidirectional return path unless explicitly stated.
7. **Contradictory relationships:** If requirements imply contradictory directions for the same endpoint pair, extract the relationship from the requirement with the higher ARLO quality weight. Record the conflict in `rationale.confidence_notes`.

## 4. Decision guidelines

- **Single vs. multiple relationships:** If a requirement describes N distinct interactions, extract N relationships, not one composite.
- **Transitive relationships:** Preserve transitivity from the requirement text. If "A calls B" and "B calls C," extract both relationships; do not infer "A calls C" unless stated.
- **Technology default:** When a requirement mentions a technology in connection with an interaction, apply it to the relationship's `technology` field. When multiple technologies are mentioned for the same interaction, prefer the most specific one.
- **Endpoint resolution:** The target endpoint must resolve to an entity in the same fragment or in `running_arch_model`. If it does not resolve, record as a gap in `rationale.gaps`.

## 5. Output schema

Each relationship is an `ArchRelationship` with these fields:
- `source_id: str` — canonical ID of the source element.
- `target_id: str` — canonical ID of the target element.
- `interaction_type: str` — short verb phrase.
- `technology: str | None` — protocol, API type, or `null`.
- `requirement_ids: list[int]` — requirement IDs implying this relationship.
- `source_fragment: str | None` — which subgraph produced it.
- `diagram_scope: str` — one of `context`, `container`, `component`.

Relationships are written to `ArchFragment.relationships` (semi-flat) and to the relevant entity's relationship list (`context_relationships`, `container_relationships`, or `component_relationships`) during tree assembly.

## 6. Error cases

| Situation | Handling |
|-----------|----------|
| Target endpoint does not resolve to any known entity | Record in `rationale.gaps`; do not create a dangling relationship |
| Source and target are the same entity | Skip; self-referential relationships are not valid in C4 |
| Requirement implies a relationship that contradicts an existing running_arch_model relationship | Record in `rationale.confidence_notes`; do not overwrite |
| diagram_scope cannot be determined from endpoint types | Default to the broader scope and record ambiguity in `rationale.confidence_notes` |
| Interaction description is empty or placeholder | Use the requirement text as a fallback; record in `rationale.confidence_notes` |

## 7. Examples

**Worked example from requirements dataset:**

Requirement R15: "The web application sends payment requests to the Stripe gateway via HTTPS."

Extracted relationship:
- `ArchRelationship(source_id='web_app', target_id='stripe_gateway', interaction_type='sends payment requests to', technology='HTTPS', requirement_ids=[15], source_fragment='raa_a', diagram_scope='container')`

Scope is `container` because the source `web_app` is a container and the target `stripe_gateway` is an external system. The container ↔ external_system combination maps to `container` scope.
