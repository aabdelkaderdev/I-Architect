# Sprint Change Proposal: Skill Resource Bundle and Tag-Based Prompt Injection
**Date:** 2026-05-23  
**Project:** raa  
**Author:** Winston (Solution Architect) & Delatom  
**Classification:** Minor (Direct implementation by Developer agent)

---

## Section 1: Issue Summary
During the preparation for executing the strategy-parallel subgraphs under Epic 2, a planning gap was identified:
- **The Issue:** While basic mustache prompt templates were created in Story 2.2, they currently lack the authoritative design-time guidelines (C4 Level Mapping, Entity Extraction, Relationship Extraction, Pattern Selection, and Technology Inference) described in Section 7 of the RAA Module Specification.
- **The Risk:** Without these guidelines, the LLM nodes performing parallel subgraph analysis (RAA-A, RAA-B, RAA-C) and final judge reconciliation will operate without specific instructions, leading to inconsistent outputs.
- **The Gap:** The `epics.md` backlog has no stories to create the `./Skills/` resource bundle or implement the tag-based runtime prompt injection utility.

---

## Section 2: Impact Analysis
- **Epic Impact:** Adds a new user story (**Story 2.6**) to **Epic 2: Strategy-Parallel Subgraph Execution and Judge Reconciliation (Phase 6)**.
- **Story Sequencing Impact:** Story 2.6 is prioritized to execute immediately following Story 2.2 (currently in review) and preceding Story 2.3, ensuring the prompt loading and injection foundations are verified before building downstream scoring/deduplication logic.
- **Code & Repository Impact:**
  1. Creation of `./Skills/` directory.
  2. Creation of 5 new skill files matching the markdown + YAML frontmatter format (structured like developer reference guides).
  3. Refactoring of `raa/utils/prompt_loader.py` to add markdown parsing, YAML parsing, and tag-lookup capabilities.
  4. Integration of excerpt extraction (enforcing $\le 25$ words per rule/excerpt) into prompt template rendering.
  5. Addition of a dedicated unit test suite: `tests/raa/unit/test_prompt_loader.py`.

---

## Section 3: Recommended Approach
We recommend **Option 1: Direct Adjustment**.
- **Rationale:** This approach addresses the gap directly by scheduling a focused story (Story 2.6) without disrupting completed work or reducing MVP scope.
- **Effort Estimate:** Low-to-Medium (1 developer day).
- **Risk Assessment:** Low risk. The prompt loader utility remains backward-compatible for templates that do not require skill injection.

---

## Section 4: Detailed Change Proposals

### 4.1 Update to `_bmad-output/planning-artifacts/epics.md`
Append the following story description under **Epic 2** (after Story 2.5):

```markdown
### Story 2.6: Skill Resource Bundle and Tag-Based Prompt Injection

As a Pipeline Engineer,
I want to define design-time reference guidelines under a Skills resource bundle matching the structure of developer reference skills,
So that strategy-parallel subgraphs and final reconciliation nodes execute with structured, concise, and context-targeted instructions.

**Acceptance Criteria:**

**Given** a Skills directory (`./Skills/`) containing reference markdown files for C4 Level Mapping, Entity Extraction, Relationship Extraction, Pattern Selection, and Technology Inference
**When** a Skill reference file is authored, it must follow the standard skill template:
  - **YAML Frontmatter:** Containing `name`, `description`, and `metadata` (e.g., `target_node`, `version`)
  - **Product Summary / Definition:** Explaining the architectural concept
  - **When to Use:** Bulleted list of when the guidelines apply
  - **Quick Reference / Rules:** Structured tables or lists mapping requirements to extraction rules
  - **Decision Guidance:** Comparative logic or matrices (e.g., SQL vs NoSQL, Monolith vs Microservices)
  - **Workflow:** Step-by-step extraction steps for the LLM node
  - **Common Gotchas:** Mistakes or edge cases to avoid (e.g., circular dependencies, orphaned components)
  - **Verification Checklist:** Self-validation checkboxes for the LLM node's output
**When** the prompt loader renders a prompt template containing skill placeholders
**Then** it must retrieve the specific Skill file by name (e.g., `Skills/Entity_Extraction.md`) and extract target sections or items by header tag (e.g., `entity_extraction:rules` from "Quick Reference", or `entity_extraction:checklist` from "Verification Checklist")
**And** it must validate and enforce that any injected instruction excerpt or individual rule statement is highly concise ($\le 25$ words each) to preserve LLM token context
**And** it must inject the extracted sections/checklists dynamically into the mustache prompt template context before rendering
**And** it must raise a `FileNotFoundError` or clear exception if a requested skill file, section, or tag is missing.
```

### 4.2 Update to `_bmad-output/implementation-artifacts/sprint-status.yaml`
Insert the new story key under `development_status`:

```diff
   epic-2: in-progress
   2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch: done
   2-2-c4-metamodel-hierarchy-enforcement-in-private-subgraphs: review
   2-3-saam-first-fragment-scoring: backlog
   2-4-conservative-entity-deduplication-and-c4-boundary-grouping: backlog
   2-5-cross-cutting-concern-promotion-and-saam-score-calibration: backlog
+  2-6-skill-resource-bundle-and-tag-based-prompt-injection: backlog
   epic-2-retrospective: optional
```

---

## Section 5: Implementation Handoff
- **Scope Classification:** Minor (Direct execution by developer agent)
- **Handoff Recipient:** Amelia (Developer Agent)
- **Success Criteria:**
  1. `./Skills/` folder is initialized with C4 Level Mapping, Entity Extraction, Relationship Extraction, Pattern Selection, and Technology Inference guidelines in markdown with YAML frontmatter.
  2. `prompt_loader.py` resolves placeholders and dynamically injects tag-resolved sections from markdown documents.
  3. `prompt_loader.py` raises a `FileNotFoundError` or descriptive exception on invalid tag or missing files.
  4. Excerpt validation logic verifies that individual injected rules are concise ($\le 25$ words) and prints warnings/raises exceptions for violations.
  5. 100% test pass on `tests/raa/unit/test_prompt_loader.py`.
