# C4 Normative Prompt Constraints

Per RAA_Plan.md Section 2B. These are hard constraints injected into every LLM node that extracts entities, relationships, or patterns. Authority: C4 Model source register entries (Diagrams + Notation).

## C4 Levels

All entities must be assigned to exactly one of three C4 levels based on granularity:

- **Context:** The top-level system view. Includes software systems, persons (human actors), and external systems. Shows system-to-system and system-to-actor interactions.
- **Container:** The deployable-unit view within a single system. Includes web applications, databases, message brokers, and services. Shows container-to-container and container-to-actor interactions.
- **Component:** The internal building-block view within a single container. Includes modules, workers, controllers, and libraries. Shows component-to-component and component-to-container interactions.

## Element Rules

Every C4 element must carry:
- A **type label** identifying its element kind (system, container, component, person, external system).
- A **short description** explaining the element's purpose in the architecture.
- **Clearly labelled relationships** to other elements, each with direction and an interaction description.

## Technology Annotations

- Containers and components must specify their **technology stack** when determinable from requirements.
- Leave technology as `null` when the requirement text provides no technology signal — never guess.
- Valid examples: "Django 4.2", "PostgreSQL 15", "RabbitMQ", "React 18".

## Relationship Rules

- Every relationship must state a **direction** (source → target) and a **short interaction description** (verb phrase, e.g. "sends payment events to").
- Each relationship must carry an explicit `diagram_scope` value: `context`, `container`, or `component`, determined by the endpoint types (see §12 scoping rules).
- Relationships must trace to the requirement IDs that imply them.
