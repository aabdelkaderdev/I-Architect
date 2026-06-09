# RAA PRD — Phase 4: Prompt Templates & LLM Skills

**Version:** 1.0
**Status:** Draft
**Depends on:** RAA PRD Phase 1 (design), Phase 2 (schemas), Phase 3 (tech stack)

---

## 1. Overview

This PRD defines every LLM prompt template the RAA uses. Templates are stored as
Markdown files with Mustache `{{variable}}` syntax and rendered at runtime via
`langchain_core.utils.mustache`. Mustache is chosen over f-string because the prompts
iterate over requirement lists, conditionally render concern-specific fields, and
access nested registry data — all requiring sections, inverted sections, and dot
notation that f-string syntax cannot express.

Each section below states WHAT the template must convey and WHY it is structured that
way. The verbatim Mustache blocks are the authoritative template content.

---

## 2. ASR Subgraph Prompts

### 2.1 Rationale

The ASR Subgraph proposes entities directly implied by quality attributes and
architectural decisions. Its prompt must prioritise QA-weighted reasoning: a
Performance Efficiency weight of 40 means performance-driven entities (caches, load
balancers) carry more justification weight than security-driven ones at weight 12.
The prompt must also ground proposals in the concern's winning architectural patterns
— a `"Microservices"` decision implies service-per-domain entities, while
`"Distributed Cache (Redis)"` implies a specific technology variant.

Existing registry entries are presented to prevent re-proposing entities already
registered. The prompt instructs the LLM to propose only entities not found in the
snapshot.

### 2.2 System Prompt — `asr_subgraph_system.md`

```
{{! ASR Subgraph — System Prompt }}
You are an architectural analyst specialising in quality-attribute-driven design.
Your task is to propose software entities implied by architecturally significant
requirements (ASRs) and architectural decisions.

{{! Naming Convention Enforcement }}
{{> naming_convention}}

{{! Output Format }}
You must produce a JSON array of entity proposals. Each proposal must conform to
the following structure and rules:

- proposed_name: PascalCase with mandatory type suffix (see naming rules above).
- c4_level: one of "system", "container", "component".
- c4_type: one of "service", "database", "gateway", "queue", "store", "external",
  "actor".
- description: one to two sentences describing the entity's role.
- responsibilities: ordered list of what this entity does.
- source_requirements: non-empty list of requirement IDs this entity addresses.
- proposing_subgraph: must be "asr".
- concern_technology: technology stack if implied by a decision; omit otherwise.
- justification: reasoning for why this entity is necessary.

{{#examples}}
Example input and expected output are provided below for reference.
{{/examples}}
```

### 2.3 User Prompt — `asr_subgraph_user.md`

```
{{! ASR Subgraph — User Prompt }}
Analyse the following inputs and propose architecturally significant entities.

{{! Quality Weights — ordered by priority }}
The system's quality attribute priorities are:
{{#quality_weights}}
- {{@key}}: {{.}}
{{/quality_weights}}

{{#condition}}
Operational condition: {{condition}}
{{/condition}}

{{! Architectural Decisions }}
{{#decisions}}
- Selected pattern: {{selected_pattern}}
{{/decisions}}

{{! ASR Requirements }}
Architecturally significant requirements for this batch:
{{#asrs}}
- [{{id}}] {{text}} (Quality attributes: {{#quality_attributes}}{{.}}{{^-last}}, {{/-last}}{{/quality_attributes}})
{{/asrs}}

{{! Registry Snapshot — entities already registered }}
{{#registry_snapshot.entries}}
Entities already defined in the system:
{{#.}}
- {{canonical_name}} ({{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}

{{^registry_snapshot.entries}}
No entities have been registered yet.
{{/registry_snapshot.entries}}

Propose entities implied by the ASRs and decisions above. For each entity, explain
your justification. Do NOT propose entities already present in the registry snapshot.
```

---

## 3. Non-ASR Subgraph Prompts

### 3.1 Rationale

The Non-ASR Subgraph fills coverage gaps that ASRs miss: user types, external
integrations, feature-bearing services. Its prompt must not reference quality
attributes or architectural decisions — those are the ASR Subgraph's domain. Instead,
it focuses on functional implications: an OAuth2 requirement implies an
`IdentityProviderSystem`; a CSV export requirement implies a `ReportingService`.

### 3.2 System Prompt — `non_asr_subgraph_system.md`

```
{{! Non-ASR Subgraph — System Prompt }}
You are a functional analyst. Your task is to propose software entities implied by
functional requirements that describe WHAT the system must do, not how well.

{{> naming_convention}}

You must produce a JSON array of entity proposals with the same structure as
described in the ASR Subgraph system prompt, except:
- proposing_subgraph: must be "non_asr".
- concern_technology: omit this field.
- justification: focus on functional need, not quality attributes.
```

### 3.3 User Prompt — `non_asr_subgraph_user.md`

```
{{! Non-ASR Subgraph — User Prompt }}
Analyse the following functional requirements and propose entities they imply.

{{! Non-ASR Requirements }}
Functional requirements for this batch:
{{#non_asrs}}
- [{{id}}] {{text}}
{{/non_asrs}}

{{#registry_snapshot.entries}}
Entities already defined in the system:
{{#.}}
- {{canonical_name}} ({{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}

{{^registry_snapshot.entries}}
No entities have been registered yet.
{{/registry_snapshot.entries}}

Propose entities implied by the functional requirements above. Focus on user types,
external systems, and feature-bearing services that the requirements suggest but
do not explicitly name. Do NOT propose entities already present in the registry.
```

---

## 4. Judge Prompts

### 4.1 Rationale

The Judge executes five SAAM steps (Phase 1 §8.4). Two prompt strategy options exist:
one unified prompt covering all five steps, or five separate prompts. The unified
approach is chosen because SAAM steps are sequential and share intermediate state —
a single LLM call with structured output for each step avoids serialisation overhead
and keeps the evaluation context intact across steps.

### 4.2 System Prompt — `judge_system.md`

```
{{! Judge — System Prompt }}
You are an architecture evaluator using the Software Architecture Analysis Method
(SAAM). Your role is to evaluate entity proposals against requirements, resolve
conflicts, and produce the final entity set for a batch.

{{> naming_convention}}

You will be asked to perform five sequential evaluation steps. For each step, you
must produce structured output conforming to the format described in that step.
```

### 4.3 User Prompt — `judge_user.md`

```
{{! Judge — User Prompt }}
Evaluate the following candidate architecture against the batch's requirements.

{{! Batch Requirements — all ASRs and non-ASRs }}
Requirements in this batch:
{{#requirements}}
- [{{id}}] {{text}}
{{/requirements}}

{{! ASR Proposals }}
Proposals from the ASR Subgraph:
{{#asr_proposals}}
- proposed_name: {{proposed_name}}
  c4_level: {{c4_level}}, c4_type: {{c4_type}}
  description: {{description}}
  responsibilities: {{#responsibilities}}- {{.}}{{/responsibilities}}
  source_requirements: {{#source_requirements}}{{.}}{{^-last}}, {{/-last}}{{/source_requirements}}
  justification: {{justification}}
{{/asr_proposals}}

{{! Non-ASR Proposals }}
Proposals from the Non-ASR Subgraph:
{{#non_asr_proposals}}
- proposed_name: {{proposed_name}}
  c4_level: {{c4_level}}, c4_type: {{c4_type}}
  description: {{description}}
  responsibilities: {{#responsibilities}}- {{.}}{{/responsibilities}}
  source_requirements: {{#source_requirements}}{{.}}{{^-last}}, {{/-last}}{{/source_requirements}}
  justification: {{justification}}
{{/non_asr_proposals}}

{{#registry_snapshot.entries}}
Existing registry entries:
{{#.}}
- {{canonical_name}} ({{canonical_id}}, {{c4_type}}): {{description}}
{{/.}}
{{/registry_snapshot.entries}}
{{/registry_snapshot.entries}}

---

Execute the following five SAAM steps:

**Step 1 — Scenario Development.**
Treat each requirement above as a scenario. Confirm that all requirements are
represented as evaluation scenarios.

**Step 2 — Architecture Description.**
The candidate architecture is the union of ASR and Non-ASR proposals listed above.
Confirm the full set of proposals.

**Step 3 — Scenario Classification.**
For each proposal, classify it as:
- direct: explicitly named or described in a source requirement's text.
- indirect: implied by a quality attribute or pattern, not stated explicitly.
For each classification, provide a one-sentence justification.

**Step 4 — Individual Scenario Evaluation.**
For each requirement, identify which proposal(s) satisfy it. A proposal satisfies a
requirement if its responsibilities and description address the concern in the
requirement text — this is a semantic match, not a keyword match. Requirements with
no satisfying proposal must be reported as coverage gaps with a specific reason why
no proposal addresses them.

**Step 5 — Scenario Interaction.**
Group proposals by proposed_name. For each group with multiple referencing
requirements:
- If requirements are compatible: mark the entity as load-bearing if referenced by
  3+ requirements.
- If proposals share a name but come from different subgraphs (authority conflict):
  retain the ASR proposal, merge non-ASR source_requirements and concern_technology
  into it. Record resolution as "asr_wins" or "merged".
- If requirements demand mutually exclusive behaviours from the same entity:
  record as a genuine conflict with resolution "unresolved".

After SAAM, perform post-evaluation:
1. Deduplicate proposals by canonical name string equality.
2. For each surviving entity, determine if it is new or enriches an existing
   registry entry. Produce a RegistryDelta.
3. Produce partial C4 descriptions for this batch's scope.
```

---

## 5. Naming Convention Enforcement

### 5.1 Rationale

Naming compliance must be identical across all three LLM roles. A single shared
Mustache partial (`naming_convention.md`) is included via `{{> naming_convention}}`
in every system prompt. This guarantees consistency and makes the naming rules
auditable in one place.

### 5.2 Partial — `naming_convention.md`

```
{{! Naming Convention — included in all system prompts }}
Entity naming rules (MUST be followed exactly):

1. Names are PascalCase: no spaces, hyphens, or underscores. Start each word with
   a capital letter.
2. Every entity name MUST end with a type suffix matching its c4_type:

   | c4_type   | Required suffix | Example                  |
   |-----------|-----------------|--------------------------|
   | service   | Service         | AuthenticationService    |
   | database  | Database        | UserDatabase             |
   | gateway   | Gateway         | ApiGateway               |
   | queue     | Queue           | NotificationQueue        |
   | store     | Store           | SessionStore             |
   | external  | System          | PaymentGatewaySystem     |
   | actor     | (no suffix)     | EndUser, SystemAdmin     |

3. Actors carry no suffix — the name stands alone.
4. Use the most generic canonical term. Do not use synonyms.
   Good: AuthenticationService. Bad: AuthService, LoginService.
```

---

## 6. Output Format Specification

### 6.1 Rationale

Each LLM's output is bound to a Pydantic model via `with_structured_output` (Phase 3
§2.3). The model enforces schema conformance automatically. The prompt's role is to
ensure the LLM understands what each field means — not to describe JSON syntax. Every
system prompt defines field semantics; the Pydantic model defines field types.

### 6.2 Schema Bindings

| Role | Pydantic Output Model | Wraps |
|------|----------------------|-------|
| ASR Subgraph | `list[EntityProposal]` (Phase 2 §4.1) | Proposals from ASR reasoning |
| Non-ASR Subgraph | `list[EntityProposal]` (Phase 2 §4.1) | Proposals from functional reasoning |
| Judge Step 3 | list of `JudgedProposal` (Phase 2 §4.2) with `scenario_classification` populated | Classified proposals |
| Judge Step 4 | list of `CoverageGap` (Phase 2 §8) | Requirements with no satisfying entity |
| Judge Step 5 | list of `ConflictRecord` (Phase 2 §8) | Detected conflicts |
| Judge Post-SAAM | `RegistryDelta` (Phase 2 §7.1) + partial C4 descriptions | Registry mutations + L2/L3/L1 output |

Each Pydantic model carries `@field_validator` and `@model_validator` methods
enforcing the rules in Phase 3 §6.3. The LLM does not need to reproduce validation
logic — it only needs to understand field semantics.

---

## 7. Few-Shot Example Strategy

### 7.1 Rationale

Few-shot examples reduce output variance in early batches when the registry is empty
and the LLM has no prior proposals to learn from. They are included inline in the
user prompt templates so the LLM sees the pattern immediately before producing its
own output.

### 7.2 Strategy

- **ASR Subgraph:** 2 examples — one showing a direct entity (requirement names a
  cache → CacheService), one showing an indirect entity (performance requirement
  implies LoadBalancerService).
- **Non-ASR Subgraph:** 2 examples — an external system (OAuth2 → IdentityProviderSystem)
  and a user type (export data → DataAnalyst actor).
- **Judge:** 1 example per SAAM step, using the same scenario to show the full
  evaluation chain.

Examples are stored in `prompts/examples/` and included via Mustache partial:
`{{> examples/asr_direct}}`. This keeps example data separate from prompt structure.

---

## 8. Prompt Versioning & Storage

### 8.1 File Layout

```
prompts/
  asr_subgraph_system.md
  asr_subgraph_user.md
  non_asr_subgraph_system.md
  non_asr_subgraph_user.md
  judge_system.md
  judge_user.md
  naming_convention.md          (shared partial)
  examples/
    asr_direct.md
    asr_indirect.md
    non_asr_external.md
    non_asr_user_type.md
    judge_chain.md
```

### 8.2 Versioning

Templates are versioned alongside code in the same repository. Changes to a prompt
template follow the same review process as code changes. The `Deferred Items` section
in future phases may specify a prompt registry or LangSmith Prompt Hub integration;
for Phase 4, file-based versioning with git is sufficient.

---

## 9. Deferred Items

1. **Prompt Hub integration** — whether to pull templates from LangSmith Prompt Hub
   at runtime instead of local files.
2. **A/B testing infrastructure** — running multiple prompt variants against the same
   batch and comparing output quality.
3. **Dynamic few-shot selection** — selecting examples based on requirement similarity
   rather than static inclusion.
4. **Token budgeting per prompt** — hard limits on input token counts and truncation
   strategy for large batches.
5. **Prompt-specific retry configuration** — per-role retry counts and backoff
   (deferred to Phase 6 error handling).
