# Technology Inference — Skill Reference

## 1. Purpose

Guidelines for inferring technology stack annotations from requirement text. Applied by all three RAA subgraphs when assigning `technology` fields on containers, components, external systems, and relationships.

## 2. Input

- **Normalized requirements**: the batch requirements with full text descriptions.
- **Proposed entities**: containers, components, external systems, and relationships extracted by the subgraph.
- **Running architecture model** (`running_arch_model`): technology annotations already committed from prior batches.

## 3. Normative rules

1. **Explicit signal detection:** Assign `technology` when the requirement text contains an explicit technology name (framework, database engine, message broker, API protocol, deployment target). Examples of strong signals: "Django", "PostgreSQL", "RabbitMQ", "Kubernetes", "REST API", "GraphQL".
2. **Null default:** Leave `technology` as `null` when no explicit technology signal exists in the requirement text. Never guess a technology.
3. **Signal keywords by category:**
   - **Databases:** PostgreSQL, MySQL, MongoDB, Redis, SQLite, Elasticsearch, Cassandra, DynamoDB.
   - **Message brokers:** RabbitMQ, Kafka, SQS, Redis Pub/Sub, NATS, Pulsar.
   - **API protocols:** REST, GraphQL, gRPC, SOAP, WebSocket, WebHook.
   - **Deployment targets:** Kubernetes, Docker, AWS Lambda, ECS, Cloud Run, Heroku.
   - **Web frameworks:** Django, Flask, FastAPI, Express, Spring Boot, Rails, Laravel.
4. **Confidence levels:** When technology is explicitly named, confidence is high. When inferred from context (e.g., "a relational database" without naming one), record the signal in `rationale.confidence_notes` and leave `technology` as `null` — do not guess the specific database.
5. **Conflicting signals:** When requirements mention conflicting technologies for the same entity, prefer the more specific signal. Record the conflict in `rationale.confidence_notes`.

## 4. Decision guidelines

- **Container technology:** Assign the primary runtime framework or environment.
- **Component technology:** Assign the implementation language or library when explicitly stated.
- **External system technology:** Assign the protocol or API type when the integration method is described.
- **Relationship technology:** Assign the communication protocol when stated.
- **Technology consistency:** If a technology annotation for the same entity already exists in `running_arch_model`, do not overwrite it unless the new annotation is more specific.
- **No-signal cases:** A requirement like "The system shall store data" provides no technology signal. Leave `technology` as `null` — this is a correct and expected outcome.

## 5. Output schema

Technology annotations are written to:
- `ArchContainer.technology: str | None`
- `ArchComponent.technology: str | None`
- `ArchExternalSystem.technology: str | None`
- `ArchRelationship.technology: str | None`

All four fields accept `null`. Never substitute a generic string like "unknown" or "TBD" for a null technology annotation.

## 6. Error cases

| Situation | Handling |
|-----------|----------|
| Requirement names a technology not in the recognized keyword list | Accept it as-is; the keyword list is a guide, not a closed registry |
| Two requirements name different technologies for the same entity | Record the more specific one; note the conflict in `rationale.confidence_notes` |
| Technology signal is too vague to be actionable (e.g., "a cloud service") | Leave technology as `null`; record the vague signal in `rationale.confidence_notes` |
| Technology annotation contradicts running_arch_model | Do not overwrite; record in `rationale.confidence_notes` |

## 7. Examples

**Worked example from requirements dataset:**

Requirement R30: "The web application shall use Django 4.2 with a PostgreSQL 15 database for persistent storage."

Extracted entities with technology:
- `ArchContainer(id='web_app', label='Web Application', technology='Django 4.2', parent_system_id='payment_gateway')`
- `ArchContainer(id='payment_db', label='Payment Database', technology='PostgreSQL 15', parent_system_id='payment_gateway')`

Both technologies are explicitly named in the requirement text — confidence is high. No guessing required.

---

Requirement R31: "The system needs a database."

This provides no specific technology signal. The entity receives `technology=None`.
