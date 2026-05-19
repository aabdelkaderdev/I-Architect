# C4 Level Mapping — Skill Reference

## 1. Purpose

Guidelines for assigning entities to C4 levels (Context, Container, Component) and resolving parent associations. Used by all three RAA subgraphs for entity output validation. References C4.md for level definitions and Relationship_Extraction.md for scope assignment.

## 2. Input

- **Proposed entities**: systems, containers, components, persons, external systems extracted by the subgraph.
- **Running architecture model** (`running_arch_model`): existing entities from prior batches.
- **Normalized requirements**: the batch requirements that the entities trace to.

## 3. Normative rules

1. **Parent system assignment (`parent_system_id`):** Every container must carry a `parent_system_id` that resolves to a system in the same fragment or in `running_arch_model`. When the owning system is implicit in requirements, the subgraph must propose a system or reference an existing one.
2. **Parent container assignment (`parent_container_id`):** Every component must carry a `parent_container_id` that resolves to a container in the same fragment or in `running_arch_model`.
3. **Implicit container handling:** When a requirement implies a component without any container context, the subgraph must propose a conservative container to host it, naming the container based on the component's domain. The component must not be submitted without a resolvable parent.
4. **Level promotion/demotion:** If a proposed entity is at the wrong level for its described scope, adjust it. A component-level entity described at system-level scope should be promoted to system (with an assumed container hosting it). A system-level entity described at container scope should be demoted to container (with an assumed parent system).
5. **Level-mixing prohibition:** Do not place a component at the context level. Do not place a container at the component level. Each entity must be assigned to exactly one C4 level.

## 4. Decision guidelines

- **Promotion vs. demotion:** When the correct level is ambiguous, default to the coarser level (promote rather than demote) to minimize fragmentation.
- **Implicit parent selection:** When proposing a container to host an otherwise-orphaned component, name it conservatively (e.g., `<component-domain>_service`). Do not invent elaborate architectures.
- **Cross-level relationships:** Relationships between entities at different levels use the scope of the lower-level entity. A container-to-system relationship uses `container` scope.
- **Boundary assignment:** Entities discovered in the same requirement batch that share a domain concept should be grouped under the same parent.

## 5. Output schema

After level mapping, the subgraph outputs an `ArchFragment` where:
- Each `ArchSystem` carries its `containers` list and `context_relationships`.
- Each `ArchContainer` carries `parent_system_id`, its `components` list, and `container_relationships`.
- Each `ArchComponent` carries `parent_container_id` and `component_relationships`.
- Relationships are scoped according to this table:

| Endpoint types | `diagram_scope` |
|---|---|
| system ↔ system, system ↔ person, system ↔ external_system | `context` |
| container ↔ container, container ↔ person, container ↔ external_system | `container` |
| component ↔ component, component ↔ container, component ↔ external_system | `component` |

## 6. Error cases

| Situation | Handling |
|-----------|----------|
| Container proposed with unresolvable `parent_system_id` | If no system can be identified, propose one in the same fragment; record ambiguity in `rationale.confidence_notes` |
| Component proposed without any container context | Propose a conservative container; name it after the component's domain; do not submit an orphan |
| Entity proposed at wrong level and cannot be corrected | Default to the coarser level; record in `rationale.confidence_notes` |
| Two entities at different levels proposed with the same canonical ID | Rename the lower-level entity with a suffix (e.g., `_worker`); record the collision in `rationale.confidence_notes` |
| Entity's level contradicts running_arch_model | Respect the running model's level assignment; log a gap if the requirement cannot be satisfied at that level |

## 7. Examples

**Worked example from requirements dataset:**

Requirement R20: "The system shall include a payment processing module that handles transaction reconciliation."

This requirement implies a component (`payment processing module`) but provides no container context. The subgraph must:
1. Check `running_arch_model` for a suitable existing container (e.g., a `web_app`).
2. If no container exists, propose one (e.g., `ArchContainer(id='payment_service', label='Payment Service', parent_system_id='payment_gateway', technology='Django')`).
3. Propose the component as `ArchComponent(id='payment_processor', label='Payment Processor', parent_container_id='payment_service')`.

The relationship between the component and its workload carries `diagram_scope='component'` because both endpoints are components or a component and an external system.
