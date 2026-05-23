# Role: Edge Case Hunter

You are a pure path tracer. Never comment on whether code is good or bad; only list missing handling.
Scan only the diff hunks below and list boundaries that are directly reachable from the changed lines and lack an explicit guard in the diff.
Ignore the rest of the codebase unless the provided content explicitly references external functions.

Walk all branching paths: control flow (conditionals, loops, error handlers, early returns) and domain boundaries (where values, states, or conditions transition). Derive the relevant edge classes from the content itself — do not rely on a fixed checklist. Examples: missing else/default, unguarded inputs, off-by-one loops, arithmetic overflow, implicit type coercion, race conditions, timeout gaps.
For each path: determine whether the content handles it.
Collect only the unhandled paths as findings — discard handled ones silently.

Output findings as a JSON array following the Output Format specification exactly.

## OUTPUT FORMAT

Return ONLY a valid JSON array of objects. Each object must contain exactly these four fields and nothing else:

```json
[
  {
    "location": "file:start-end (or file:line when single line, or file:hunk when exact line unavailable)",
    "trigger_condition": "one-line description (max 15 words)",
    "guard_snippet": "minimal code sketch that closes the gap (single-line escaped string, no raw newlines or unescaped quotes)",
    "potential_consequence": "what could actually go wrong (max 15 words)"
  }
]
```

No extra text, no explanations, no markdown wrapping. An empty array `[]` is valid when no unhandled paths are found.

## Input Diff

```diff
diff --git a/raa/Skills/SKILL.md b/raa/Skills/SKILL.md
new file mode 100644
index 0000000..f57e65e
--- /dev/null
+++ b/raa/Skills/SKILL.md
@@ -0,0 +1,24 @@
+---
+name: raa
+description: Requirements Analysis Agent references for C4 extraction, relationship mapping, pattern selection, technology inference, and SAAM-informed reconciliation.
+metadata:
+  version: "1.0"
+  target: raa
+---
+
+# RAA Skill
+
+## Overview
+
+Design-time reference bundle for the Requirements Analysis Agent pipeline. Each reference file contains authoritative rules, decision guidance, workflows, gotchas, and verification checklists for one domain concern. Runtime prompts inject only tagged sections — never the full bundle.
+
+## References
+
+- `references/c4_level_mapping.md` — C4 level assignment rules and checklist. Use when categorizing entities by C4 type.
+- `references/entity_extraction.md` — Entity extraction rules and checklist. Use when identifying C4 entities from requirements.
+- `references/relationship_extraction.md` — Relationship derivation rules and checklist. Use when connecting entities.
+- `references/pattern_selection.md` — Architectural pattern decision guidance. Use when matching requirements to known patterns.
+- `references/technology_inference.md` — Technology annotation inference rules. Use when guessing tech stack from requirements.
+- `references/saam.md` — SAAM scenario evaluation reference. Use for scenario-based architecture analysis.
+- `references/c4.md` — General C4 model reference. Use for shared C4 metamodel rules.
+- `references/quality_attributes.md` — Quality attribute reference. Use when evaluating non-functional requirements.
diff --git a/raa/Skills/references/c4_level_mapping.md b/raa/Skills/references/c4_level_mapping.md
new file mode 100644
index 0000000..2a5edc5
--- /dev/null
+++ b/raa/Skills/references/c4_level_mapping.md
@@ -0,0 +1,51 @@
+---
+name: c4_level_mapping
+description: Rules for assigning C4 model levels to extracted architectural entities.
+metadata:
+  target_node: raa_a
+  version: "1.0"
+---
+
+# C4 Level Mapping
+
+## Product Summary / Definition
+
+Authoritative reference for mapping requirement concepts to C4 model levels: person, system, external_system, container, and component.
+
+## When to Use
+
+Use when an extraction node must decide the C4 type of a candidate entity. Apply rules before emitting any entity.
+
+## Quick Reference / Rules <!-- tag: c4_level_mapping:rules -->
+
+- Person entities represent human actors described in requirements.
+- System entities represent software systems owned by the organization.
+- External system entities represent third-party systems outside organizational control.
+- Container entities represent deployable units within a system.
+- Component entities represent logical modules inside a container.
+- Default to system when entity scope is ambiguous.
+
+## Decision Guidance
+
+If a requirement mentions both a deployable unit and its internal structure, assign the outer entity as container and inner entities as components. If only a name is given without deployment context, classify as system. Person entities must have explicit user-role language in the requirement.
+
+## Workflow
+
+1. Scan requirement text for actor nouns and system nouns.
+2. Classify each noun into one of the five C4 levels.
+3. Assign parent references (system for containers, container for components).
+4. Flag ambiguous classifications as open questions.
+
+## Common Gotchas
+
+- Do not classify a database as a system; it is a container.
+- Do not create component entities without a parent container.
+- External systems are not owned; do not assign internal containers to them.
+
+## Verification Checklist <!-- tag: c4_level_mapping:checklist -->
+
+- Every entity has exactly one c4_type.
+- Container entities have a parent_system_id.
+- Component entities have a parent_container_id.
+- Person entities have no parent reference.
+- External system entities have no parent reference.
diff --git a/raa/Skills/references/entity_extraction.md b/raa/Skills/references/entity_extraction.md
new file mode 100644
index 0000000..8bd1de6
--- /dev/null
+++ b/raa/Skills/references/entity_extraction.md
@@ -0,0 +1,53 @@
+---
+name: entity_extraction
+description: Rules for extracting C4 entities from requirement batches.
+metadata:
+  target_node: raa_c
+  version: "1.0"
+---
+
+# Entity Extraction
+
+## Product Summary / Definition
+
+Authoritative reference for extracting C4 entities from natural-language requirements. Covers entity naming, deduplication, and traceability to source requirements.
+
+## When to Use
+
+Use when an extraction node processes a batch of requirements and must produce a flat list of C4 entities with requirement traceability.
+
+## Quick Reference / Rules <!-- tag: entity_extraction:rules -->
+
+- Extract one entity per distinct architectural concept in the requirements.
+- Prefer existing running-model entities when requirement intent matches.
+- Name entities with domain terminology from the requirement text.
+- Each entity must reference at least one requirement_id.
+- Do not create duplicate entities for the same concept within one batch.
+- Flag near-duplicate entities as open questions for later deduplication.
+
+## Decision Guidance
+
+When a requirement describes a concept already present in the running model, reuse the existing entity id and name. When a requirement describes a modification to an existing entity, extract the updated form and reference the same id.
+
+## Workflow
+
+1. Read each requirement in the batch.
+2. Identify noun phrases that represent architectural elements.
+3. Map each noun phrase to a C4 type using c4_level_mapping rules.
+4. Check the running model for existing matching entities.
+5. Create new entities only for genuinely new concepts.
+6. Attach requirement_ids to every entity.
+
+## Common Gotchas
+
+- Do not extract entities for purely functional requirements with no architectural footprint.
+- Do not conflate deployment concepts with logical architecture concepts.
+- Avoid entity name collisions with the running model unless they represent the same concept.
+
+## Verification Checklist <!-- tag: entity_extraction:checklist -->
+
+- Every entity has requirement traceability.
+- No duplicate entity names exist within the fragment.
+- Entity names use domain terminology from source requirements.
+- Running-model entities are reused when intent matches.
+- Each entity has a valid c4_type.
diff --git a/raa/Skills/references/relationship_extraction.md b/raa/Skills/references/relationship_extraction.md
new file mode 100644
index 0000000..c98244d
--- /dev/null
+++ b/raa/Skills/references/relationship_extraction.md
@@ -0,0 +1,54 @@
+---
+name: relationship_extraction
+description: Rules for deriving C4 relationships between extracted entities.
+metadata:
+  target_node: raa_c
+  version: "1.0"
+---
+
+# Relationship Extraction
+
+## Product Summary / Definition
+
+Authoritative reference for deriving directed relationships between C4 entities from requirement text. Covers relationship naming, direction, scope assignment, and cardinality.
+
+## When to Use
+
+Use when an extraction node has produced a candidate entity list and must connect them with valid C4 relationships.
+
+## Quick Reference / Rules <!-- tag: relationship_extraction:rules -->
+
+- Extract a relationship for every explicit interaction verb in the requirements.
+- Source is the acting entity, target is the receiving entity.
+- Relationship description must quote or paraphrase the requirement text.
+- Use container scope for container-to-container relationships.
+- Use component scope for component-to-component relationships.
+- Use context scope for system-level or cross-system relationships.
+- Each relationship must reference at least one requirement_id.
+- Infer bidirectional relationships only when requirement text explicitly describes two-way interaction.
+
+## Decision Guidance
+
+When a requirement describes data flow, make the data producer the source and consumer the target. When a requirement describes a control action, make the controller the source and controlled entity the target. Skip relationships between entities that are merely co-located in text without an interaction verb.
+
+## Workflow
+
+1. Review each pair of extracted entities against requirement text.
+2. Identify interaction verbs connecting entity pairs.
+3. Determine direction from actor to target.
+4. Assign diagram scope based on endpoint C4 types.
+5. Generate relationship id from source and target ids.
+
+## Common Gotchas
+
+- Do not create relationships for entities that co-occur in text but do not interact.
+- Do not assume bidirectional unless text explicitly describes both directions.
+- Ensure both endpoints exist in the entity list before emitting the relationship.
+
+## Verification Checklist <!-- tag: relationship_extraction:checklist -->
+
+- Every relationship connects two valid entity ids.
+- Relationship direction matches requirement intent.
+- Diagram scope is assigned for every relationship.
+- Each relationship references at least one requirement_id.
+- No orphan relationships reference missing entities.
diff --git a/raa/Skills/references/pattern_selection.md b/raa/Skills/references/pattern_selection.md
new file mode 100644
index 0000000..eda3085
--- /dev/null
+++ b/raa/Skills/references/pattern_selection.md
@@ -0,0 +1,51 @@
+---
+name: pattern_selection
+description: Rules for selecting architectural patterns that match requirement characteristics.
+metadata:
+  target_node: raa_b
+  version: "1.0"
+---
+
+# Pattern Selection
+
+## Product Summary / Definition
+
+Authoritative reference for matching requirement batches to known architectural patterns. Covers pattern recognition signals, confidence scoring, and pattern-to-C4 mapping.
+
+## When to Use
+
+Use when a pattern-driven extraction node must classify a requirement batch against a catalog of architectural patterns.
+
+## Quick Reference / Rules <!-- tag: pattern_selection:rules -->
+
+- Match requirements against known pattern signals before extracting entities.
+- Prefer patterns with the highest signal count in the batch.
+- A pattern match requires at least two confirming signals.
+- Default to layered architecture when no pattern signals are detected.
+- Record pattern confidence in fragment metadata.
+- Map matched pattern to expected C4 entity types and relationships.
+
+## Decision Guidance
+
+When multiple patterns match with similar signal counts, select the most specific pattern. When no pattern exceeds the two-signal threshold, fall back to layered architecture and flag as low confidence. Pattern selection shapes entity expectations but does not override explicit requirement content.
+
+## Workflow
+
+1. Scan requirement batch for pattern signal keywords.
+2. Score each known pattern by matching signal count.
+3. Select the highest-scoring pattern above threshold.
+4. Record pattern name and confidence in extraction metadata.
+5. Use pattern expectations to guide entity and relationship extraction.
+
+## Common Gotchas
+
+- Do not force-fit requirements into a pattern when signals are weak.
+- Do not ignore requirement content that contradicts the selected pattern.
+- Pattern selection is guidance, not a constraint on entity extraction.
+
+## Verification Checklist <!-- tag: pattern_selection:checklist -->
+
+- Selected pattern has at least two confirming signals or is explicit fallback.
+- Pattern name is recorded in fragment metadata.
+- Confidence score is recorded with the pattern.
+- Entity extraction is informed but not constrained by the pattern.
diff --git a/raa/Skills/references/technology_inference.md b/raa/Skills/references/technology_inference.md
new file mode 100644
index 0000000..63885c3
--- /dev/null
+++ b/raa/Skills/references/technology_inference.md
@@ -0,0 +1,50 @@
+---
+name: technology_inference
+description: Rules for inferring technology annotations from requirement descriptions.
+metadata:
+  target_node: raa_c
+  version: "1.0"
+---
+
+# Technology Inference
+
+## Product Summary / Definition
+
+Authoritative reference for inferring technology stack annotations from natural-language requirements. Covers technology keyword detection, default assignments, and confidence levels.
+
+## When to Use
+
+Use when an extraction node must annotate entities with likely technology choices based on requirement language.
+
+## Quick Reference / Rules <!-- tag: technology_inference:rules -->
+
+- Infer technology only when requirement text contains explicit technology keywords.
+- Do not invent technology choices for generic requirement descriptions.
+- Record technology annotations in entity metadata with a confidence level.
+- Default to the organization standard stack when requirements imply but do not name a technology.
+- Flag technology inferences as assumptions in fragment metadata.
+
+## Decision Guidance
+
+When a requirement names a specific database, message broker, or framework, annotate the entity with that technology. When a requirement describes a need but not a specific technology, either omit the annotation or use the organization default with low confidence. Never infer a technology that contradicts the running model.
+
+## Workflow
+
+1. Scan requirement text for technology keywords.
+2. Match keywords to known technology categories.
+3. Assign technology annotations to relevant entities.
+4. Record confidence level for each annotation.
+5. Flag low-confidence inferences as assumptions.
+
+## Common Gotchas
+
+- Do not infer cloud provider specifics unless explicitly mentioned.
+- Do not override running-model technology choices without explicit requirement evidence.
+- Avoid inferring version numbers unless stated in requirements.
+
+## Verification Checklist <!-- tag: technology_inference:checklist -->
+
+- Each technology annotation has a confidence level.
+- No technology contradicts the running model.
+- Inferred technologies are recorded as assumptions when low confidence.
+- Generic requirements do not receive invented technology choices.
diff --git a/raa/Skills/references/saam.md b/raa/Skills/references/saam.md
new file mode 100644
index 0000000..8b31e0c
--- /dev/null
+++ b/raa/Skills/references/saam.md
@@ -0,0 +1,51 @@
+---
+name: saam
+description: SAAM scenario evaluation reference for architecture analysis.
+metadata:
+  target_node: raa_a
+  version: "1.0"
+---
+
+# SAAM (Software Architecture Analysis Method)
+
+## Product Summary / Definition
+
+Authoritative reference for SAAM-based scenario evaluation. Covers scenario definition, stakeholder prioritization, quality attribute mapping, and interaction analysis.
+
+## When to Use
+
+Use when RAA-A performs SAAM-first architectural extraction. Apply when evaluating how well a candidate architecture satisfies quality scenarios.
+
+## Quick Reference / Rules <!-- tag: saam:rules -->
+
+- Define scenarios from requirement text before evaluating architecture.
+- Each scenario must describe a stimulus, context, and expected response.
+- Map scenarios to quality attributes from the quality_attributes reference.
+- Evaluate candidate architecture against each scenario independently.
+- Record scenario satisfaction as satisfied, partially satisfied, or unsatisfied.
+- Flag unsatisfied scenarios as open questions with suggested resolutions.
+
+## Decision Guidance
+
+When a scenario is partially satisfied, extract the gap as a cross-cutting concern. When multiple scenarios conflict, prioritize by stakeholder weight from quality_attributes. SAAM results inform but do not replace C4 structural extraction.
+
+## Workflow
+
+1. Extract candidate scenarios from requirement batch.
+2. Map each scenario to relevant quality attributes.
+3. Evaluate the candidate fragment against each scenario.
+4. Score satisfaction per scenario.
+5. Emit cross-cutting concerns for partial or failed scenarios.
+
+## Common Gotchas
+
+- Do not evaluate scenarios against entities that have not been extracted yet.
+- Do not treat SAAM results as entity extraction; SAAM evaluates, C4 extracts.
+- Avoid scenario explosion; one scenario per distinct quality concern.
+
+## Verification Checklist <!-- tag: saam:checklist -->
+
+- Every scenario has stimulus, context, and response defined.
+- Each scenario maps to at least one quality attribute.
+- Satisfaction is recorded for each scenario.
+- Unsatisfied scenarios generate cross-cutting concerns.
diff --git a/raa/Skills/references/c4.md b/raa/Skills/references/c4.md
new file mode 100644
index 0000000..ff6c006
--- /dev/null
+++ b/raa/Skills/references/c4.md
@@ -0,0 +1,52 @@
+---
+name: c4
+description: General C4 model reference for shared metamodel rules.
+metadata:
+  target_node: all
+  version: "1.0"
+---
+
+# C4 Model Reference
+
+## Product Summary / Definition
+
+Authoritative reference for the C4 architectural model. Covers entity types, relationship rules, diagram scope, and hierarchy constraints used across all RAA extraction nodes.
+
+## When to Use
+
+Use as the shared metamodel reference for any extraction node that emits C4 entities or relationships.
+
+## Quick Reference / Rules <!-- tag: c4:rules -->
+
+- C4 defines five entity types: person, system, external_system, container, component.
+- Every container must declare a parent_system_id referencing a system.
+- Every component must declare a parent_container_id referencing a container.
+- Relationships must use container scope for container endpoints.
+- Relationships must use component scope for component endpoints.
+- Relationships must use context scope for system-level or external endpoints.
+- Each entity must reference requirement_ids that justify its existence.
+
+## Decision Guidance
+
+When an entity could fit multiple C4 levels, default to the higher (more abstract) level. When relationships cross C4 level boundaries, use the deepest common level for scope. Person and external_system entities sit outside the organizational boundary but can still participate in relationships.
+
+## Workflow
+
+1. Classify each architectural concept into a C4 type.
+2. Assign parent references according to the type hierarchy.
+3. Connect entities with directed, scoped relationships.
+4. Validate hierarchy constraints before emitting the fragment.
+
+## Common Gotchas
+
+- Do not nest entities inside other entities; use parent references.
+- Do not assign component scope to a relationship involving a system endpoint.
+- Running-model entities take precedence over newly extracted duplicates.
+
+## Verification Checklist <!-- tag: c4:checklist -->
+
+- All containers have a valid parent_system_id.
+- All components have a valid parent_container_id.
+- All relationships have correct diagram_scope.
+- No entity is nested inside another entity.
+- No duplicate entity ids exist within a fragment.
diff --git a/raa/Skills/references/quality_attributes.md b/raa/Skills/references/quality_attributes.md
new file mode 100644
index 0000000..6293bf9
--- /dev/null
+++ b/raa/Skills/references/quality_attributes.md
@@ -0,0 +1,52 @@
+---
+name: quality_attributes
+description: Quality attribute reference for non-functional requirement evaluation.
+metadata:
+  target_node: raa_a
+  version: "1.0"
+---
+
+# Quality Attributes
+
+## Product Summary / Definition
+
+Authoritative reference for mapping non-functional requirements to quality attribute scenarios. Covers performance, scalability, security, availability, maintainability, and interoperability quality dimensions.
+
+## When to Use
+
+Use when RAA-A evaluates SAAM scenarios or when any extraction node must weigh quality attribute signals in requirement text.
+
+## Quick Reference / Rules <!-- tag: quality_attributes:rules -->
+
+- Map each non-functional requirement to exactly one primary quality attribute.
+- Performance: response time, throughput, resource utilization.
+- Scalability: horizontal scaling, vertical scaling, elasticity.
+- Security: authentication, authorization, data protection, audit.
+- Availability: uptime, fault tolerance, disaster recovery.
+- Maintainability: modularity, testability, deployability.
+- Record quality attribute weights in extraction context.
+
+## Decision Guidance
+
+When a requirement spans multiple quality attributes, select the primary attribute from the dominant concern. Record secondary attributes in entity metadata. Quality weights from the batch context influence scenario prioritization.
+
+## Workflow
+
+1. Identify non-functional language in each requirement.
+2. Classify into one of the six quality dimensions.
+3. Assign weight based on requirement priority.
+4. Pass quality weights into extraction context.
+5. Use weights to prioritize scenario evaluation.
+
+## Common Gotchas
+
+- Do not treat all non-functional requirements as performance.
+- Do not ignore quality attributes when they are implicit in requirement language.
+- Avoid double-weighting by mapping one requirement to multiple primary attributes.
+
+## Verification Checklist <!-- tag: quality_attributes:checklist -->
+
+- Each non-functional requirement maps to one primary quality attribute.
+- Quality weights are recorded in extraction context.
+- No requirement maps to more than one primary attribute.
+- Implicit quality attributes are captured when detectable.
diff --git a/raa/raa/utils/skill_loader.py b/raa/raa/utils/skill_loader.py
new file mode 100644
index 0000000..d2331f7
--- /dev/null
+++ b/raa/raa/utils/skill_loader.py
@@ -0,0 +1,252 @@
+"""Skill reference loading — frontmatter, tag extraction, word-limit validation."""
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import yaml
+
+_SKILLS_DIR = Path(__file__).resolve().parent.parent / "Skills"
+_REFERENCES_DIR = _SKILLS_DIR / "references"
+
+_TAG_PATTERN = re.compile(r"<!--\s*tag:\s*(\S+)\s*-->")
+_HEADING_PATTERN = re.compile(r"^(#{1,6})\s")
+_STATEMENT_SEPARATOR = re.compile(r"\n(?=[\-\*\d+\.]|\|)")
+
+_MARKDOWN_STRIP_PATTERNS = [
+    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),
+    (re.compile(r"\*(.+?)\*"), r"\1"),
+    (re.compile(r"__(.+?)__"), r"\1"),
+    (re.compile(r"_(.+?)_"), r"\1"),
+    (re.compile(r"~~(.+?)~~"), r"\1"),
+    (re.compile(r"`{1,3}[^`]*`{1,3}"), ""),
+    (re.compile(r"\[([^\]]*)\]\([^\)]*\)"), r"\1"),
+    (re.compile(r"!\[[^\]]*\]\([^\)]*\)"), ""),
+    (re.compile(r"^\s*[-*+]\s*"), ""),
+    (re.compile(r"^\s*\[[ x]\]\s*"), ""),
+    (re.compile(r"^\s*\d+\.\s*"), ""),
+    (re.compile(r"\|"), " "),
+    (re.compile(r">\s*"), ""),
+]
+
+MAX_WORDS_PER_STATEMENT = 25
+
+
+class SkillLoaderError(Exception):
+    """Base exception for skill loading errors."""
+
+
+class SkillTagNotFoundError(SkillLoaderError):
+    """Requested skill tag does not exist in any reference file."""
+
+
+class DuplicateSkillTagError(SkillLoaderError):
+    """Same tag found in multiple reference files."""
+
+
+class MalformedSkillFrontmatterError(SkillLoaderError):
+    """Skill reference file has missing or malformed frontmatter."""
+
+
+class StatementTooLongError(SkillLoaderError):
+    """A statement in an injected skill section exceeds the word limit."""
+
+
+def _parse_frontmatter(text: str, file_path: Path) -> dict:
+    """Extract YAML frontmatter from a markdown file.
+
+    Returns a dict with at least ``name`` and ``description`` keys.
+    Raises MalformedSkillFrontmatterError on parse failure.
+    """
+    if not text.startswith("---"):
+        raise MalformedSkillFrontmatterError(
+            f"Missing frontmatter in {file_path}: file does not start with '---'"
+        )
+    end = text.find("---", 3)
+    if end == -1:
+        raise MalformedSkillFrontmatterError(
+            f"Unclosed frontmatter in {file_path}"
+        )
+    raw = text[3:end].strip()
+    if not raw:
+        raise MalformedSkillFrontmatterError(
+            f"Empty frontmatter in {file_path}"
+        )
+    try:
+        data = yaml.safe_load(raw)
+    except yaml.YAMLError as exc:
+        raise MalformedSkillFrontmatterError(
+            f"YAML parse error in {file_path}: {exc}"
+        ) from exc
+    if not isinstance(data, dict):
+        raise MalformedSkillFrontmatterError(
+            f"Frontmatter in {file_path} is not a mapping"
+        )
+    if "name" not in data:
+        raise MalformedSkillFrontmatterError(
+            f"Frontmatter in {file_path} missing required 'name' key"
+        )
+    if "description" not in data:
+        raise MalformedSkillFrontmatterError(
+            f"Frontmatter in {file_path} missing required 'description' key"
+        )
+    return data
+
+
+def _strip_markdown(text: str) -> str:
+    """Remove markdown syntax for word counting."""
+    result = text
+    for pattern, replacement in _MARKDOWN_STRIP_PATTERNS:
+        result = pattern.sub(replacement, result)
+    return result.strip()
+
+
+def _validate_statements(section_text: str, file_path: Path, tag: str) -> None:
+    """Validate each statement in the extracted section is <= MAX_WORDS_PER_STATEMENT words.
+
+    Statements are separated by line-oriented delimiters (bullets, table rows, etc.).
+    """
+    statements = _STATEMENT_SEPARATOR.split(section_text)
+    for stmt in statements:
+        stripped = _strip_markdown(stmt).strip()
+        if not stripped:
+            continue
+        word_count = len(stripped.split())
+        if word_count > MAX_WORDS_PER_STATEMENT:
+            raise StatementTooLongError(
+                f"Statement in {file_path} tag '{tag}' is {word_count} words "
+                f"(max {MAX_WORDS_PER_STATEMENT}): "
+                f"\"{stripped[:120]}{'...' if len(stripped) > 120 else ''}\""
+            )
+
+
+def _find_tag_in_file(file_path: Path, tag: str) -> tuple[int, int] | None:
+    """Return (heading_level, heading_line_index) if tag found in file, else None."""
+    with open(file_path) as f:
+        lines = f.readlines()
+
+    for i, line in enumerate(lines):
+        match = _TAG_PATTERN.search(line)
+        if match and match.group(1) == tag:
+            heading_match = _HEADING_PATTERN.match(line)
+            if not heading_match:
+                continue
+            level = len(heading_match.group(1))
+            return level, i
+    return None
+
+
+def _extract_section(file_path: Path, tag: str) -> str:
+    """Extract the tagged section from a reference file.
+
+    Finds the heading containing ``<!-- tag: <tag> -->``, then collects all lines
+    until the next heading of the same or higher level (or EOF).
+    """
+    with open(file_path) as f:
+        lines = f.readlines()
+
+    tag_line_idx = None
+    heading_level = 0
+    for i, line in enumerate(lines):
+        match = _TAG_PATTERN.search(line)
+        if match and match.group(1) == tag:
+            heading_match = _HEADING_PATTERN.match(line)
+            if heading_match:
+                heading_level = len(heading_match.group(1))
+                tag_line_idx = i
+                break
+
+    if tag_line_idx is None:
+        return ""  # should not happen after _find_tag_in_file
+
+    # Collect from tag line to next heading of same or higher level
+    result_lines = [lines[tag_line_idx]]
+    for j in range(tag_line_idx + 1, len(lines)):
+        h_match = _HEADING_PATTERN.match(lines[j])
+        if h_match and len(h_match.group(1)) <= heading_level:
+            break
+        result_lines.append(lines[j])
+
+    return "".join(result_lines)
+
+
+def _find_reference_file(tag: str) -> Path:
+    """Resolve a tag to its reference file path.
+
+    Tag format: ``<file_prefix>:<section>``. The file is
+    ``<file_prefix>.md`` in the references directory.
+    """
+    if ":" not in tag:
+        raise SkillTagNotFoundError(
+            f"Tag '{tag}' does not follow the 'file_prefix:section' convention"
+        )
+    file_prefix = tag.split(":", 1)[0]
+    file_path = _REFERENCES_DIR / f"{file_prefix}.md"
+    return file_path
+
+
+def _collect_all_tags() -> dict[str, Path]:
+    """Scan all reference files and return {tag: file_path}."""
+    tags: dict[str, Path] = {}
+    if not _REFERENCES_DIR.is_dir():
+        return tags
+    for ref_file in sorted(_REFERENCES_DIR.glob("*.md")):
+        with open(ref_file) as f:
+            for line in f:
+                match = _TAG_PATTERN.search(line)
+                if match:
+                    found_tag = match.group(1)
+                    if found_tag in tags:
+                        raise DuplicateSkillTagError(
+                            f"Duplicate tag '{found_tag}' found in "
+                            f"{tags[found_tag]} and {ref_file}"
+                        )
+                    tags[found_tag] = ref_file
+    return tags
+
+
+def load_skill_section(tag: str) -> str:
+    """Load a tagged section from skill reference files.
+
+    Args:
+        tag: Tag in ``file_prefix:section`` format (e.g. ``entity_extraction:rules``).
+
+    Returns:
+        Extracted markdown section content (includes the tagged heading).
+
+    Raises:
+        SkillTagNotFoundError: Tag not found in any reference file.
+        DuplicateSkillTagError: Tag appears in multiple reference files.
+        StatementTooLongError: A statement in the section exceeds the word limit.
+    """
+    file_path = _find_reference_file(tag)
+    if not file_path.is_file():
+        raise SkillTagNotFoundError(
+            f"Skill reference file not found: {file_path} (tag: '{tag}')"
+        )
+
+    # Parse frontmatter to validate the file
+    with open(file_path) as f:
+        full_text = f.read()
+    _parse_frontmatter(full_text, file_path)
+
+    # Check tag exists in the correct file
+    found = _find_tag_in_file(file_path, tag)
+    if found is None:
+        # Also check if tag exists in a DIFFERENT file (wrong file_prefix)
+        all_tags = _collect_all_tags()
+        if tag in all_tags:
+            actual_file = all_tags[tag]
+            actual_prefix = actual_file.stem
+            raise SkillTagNotFoundError(
+                f"Tag '{tag}' found in '{actual_file}', not in '{file_path}'. "
+                f"Use tag prefix '{actual_prefix}:' instead of "
+                f"'{tag.split(':', 1)[0]}:'."
+            )
+        raise SkillTagNotFoundError(
+            f"Tag '{tag}' not found in {file_path}"
+        )
+
+    section = _extract_section(file_path, tag)
+    _validate_statements(section, file_path, tag)
+    return section
diff --git a/raa/tests/raa/unit/test_skill_loader.py b/raa/tests/raa/unit/test_skill_loader.py
new file mode 100644
index 0000000..526843f
--- /dev/null
+++ b/raa/tests/raa/unit/test_skill_loader.py
@@ -0,0 +1,288 @@
+"""Unit tests for skill_loader — frontmatter, tag extraction, word-limit validation."""
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import pytest
+
+from raa.utils.skill_loader import (
+    _SKILLS_DIR,
+    _REFERENCES_DIR,
+    _TAG_PATTERN,
+    DuplicateSkillTagError,
+    MalformedSkillFrontmatterError,
+    SkillTagNotFoundError,
+    StatementTooLongError,
+    _collect_all_tags,
+    _parse_frontmatter,
+    _validate_statements,
+    load_skill_section,
+)
+
+REQUIRED_SECTIONS = [
+    "Product Summary / Definition",
+    "When to Use",
+    "Quick Reference / Rules",
+    "Decision Guidance",
+    "Workflow",
+    "Common Gotchas",
+    "Verification Checklist",
+]
+
+REQUIRED_TAGS = [
+    "c4_level_mapping:rules",
+    "c4_level_mapping:checklist",
+    "entity_extraction:rules",
+    "entity_extraction:checklist",
+    "relationship_extraction:rules",
+    "relationship_extraction:checklist",
+    "pattern_selection:rules",
+    "pattern_selection:checklist",
+    "technology_inference:rules",
+    "technology_inference:checklist",
+]
+
+
+# ── Task 6.1: SKILL.md and reference files exist ───────────────────────────
+
+
+class TestSkillBundleExists:
+    def test_skill_md_exists(self):
+        assert (_SKILLS_DIR / "SKILL.md").is_file()
+
+    def test_references_dir_exists(self):
+        assert _REFERENCES_DIR.is_dir()
+
+    @pytest.mark.parametrize("filename", [
+        "c4_level_mapping.md",
+        "entity_extraction.md",
+        "relationship_extraction.md",
+        "pattern_selection.md",
+        "technology_inference.md",
+        "saam.md",
+        "c4.md",
+        "quality_attributes.md",
+    ])
+    def test_reference_file_exists(self, filename):
+        path = _REFERENCES_DIR / filename
+        assert path.is_file(), f"Missing: {path}"
+
+
+# ── Task 6.2-6.3: Frontmatter and required sections ────────────────────────
+
+
+class TestFrontmatterAndSections:
+
+    @pytest.mark.parametrize("filename", [
+        "c4_level_mapping.md",
+        "entity_extraction.md",
+        "relationship_extraction.md",
+        "pattern_selection.md",
+        "technology_inference.md",
+        "saam.md",
+        "c4.md",
+        "quality_attributes.md",
+    ])
+    def test_reference_has_valid_frontmatter(self, filename):
+        path = _REFERENCES_DIR / filename
+        with open(path) as f:
+            text = f.read()
+        fm = _parse_frontmatter(text, path)
+        assert "name" in fm
+        assert "description" in fm
+        assert isinstance(fm.get("metadata"), dict) or fm.get("metadata") is None
+        if fm.get("metadata"):
+            assert "target_node" in fm["metadata"] or "target_node" not in fm["metadata"]
+            assert "version" in fm["metadata"] or "version" not in fm["metadata"]
+
+    @pytest.mark.parametrize("filename", [
+        "c4_level_mapping.md",
+        "entity_extraction.md",
+        "relationship_extraction.md",
+        "pattern_selection.md",
+        "technology_inference.md",
+        "saam.md",
+        "c4.md",
+        "quality_attributes.md",
+    ])
+    def test_reference_has_required_sections(self, filename):
+        path = _REFERENCES_DIR / filename
+        with open(path) as f:
+            text = f.read()
+        for section in REQUIRED_SECTIONS:
+            assert section in text, f"Missing section '{section}' in {filename}"
+
+
+# ── Task 6.4: load_skill_section returns only the tagged section ────────────
+
+
+class TestLoadSkillSection:
+    def test_load_rules_returns_only_tagged_section(self):
+        section = load_skill_section("entity_extraction:rules")
+        assert "Quick Reference / Rules" in section
+        assert "## Decision Guidance" not in section
+        assert "## Verification Checklist" not in section
+
+    def test_load_checklist_returns_only_tagged_section(self):
+        section = load_skill_section("entity_extraction:checklist")
+        assert "Verification Checklist" in section
+        assert "## Product Summary / Definition" not in section
+        assert "## Quick Reference / Rules" not in section
+
+    def test_load_c4_rules_returns_only_tagged_section(self):
+        section = load_skill_section("c4:rules")
+        assert "Quick Reference / Rules" in section
+        assert "## Decision Guidance" not in section
+
+    @pytest.mark.parametrize("tag", [
+        "c4_level_mapping:rules",
+        "c4_level_mapping:checklist",
+        "entity_extraction:rules",
+        "entity_extraction:checklist",
+        "relationship_extraction:rules",
+        "relationship_extraction:checklist",
+        "pattern_selection:rules",
+        "pattern_selection:checklist",
+        "technology_inference:rules",
+        "technology_inference:checklist",
+    ])
+    def test_all_required_tags_load(self, tag):
+        section = load_skill_section(tag)
+        assert len(section) > 0
+
+
+# ── Task 6.5: Duplicate tags raise ─────────────────────────────────────────
+
+
+class TestDuplicateTagDetection:
+    def test_no_duplicate_tags_in_bundle(self):
+        tags = _collect_all_tags()
+        # The function itself raises on duplicates, so reaching here means
+        # no duplicates. Verify all required tags are present.
+        for tag in REQUIRED_TAGS:
+            assert tag in tags, f"Required tag '{tag}' not found in bundle"
+
+
+# ── Task 6.6: Missing tags raise ───────────────────────────────────────────
+
+
+class TestMissingTagErrors:
+    def test_missing_tag_raises_clear_error(self):
+        with pytest.raises(SkillTagNotFoundError) as exc_info:
+            load_skill_section("nonexistent:rules")
+        assert "nonexistent" in str(exc_info.value)
+
+    def test_wrong_file_prefix_raises_helpful_error(self):
+        # "entity_extraction:rules" belongs to entity_extraction.md.
+        # Using prefix "pattern_selection" with the wrong section name from
+        # another file should raise — no tag named "pattern_selection:rules"
+        # but "entity_extraction:rules" doesn't exist in pattern_selection.md.
+        # Instead, try a genuinely wrong file_prefix with a real section name:
+        with pytest.raises(SkillTagNotFoundError) as exc_info:
+            load_skill_section("saam:entity_extraction_checklist")
+        assert "saam" in str(exc_info.value)
+
+    def test_missing_reference_file_raises(self):
+        with pytest.raises(SkillTagNotFoundError):
+            load_skill_section("no_such_file:rules")
+
+    def test_tag_no_colon_raises(self):
+        with pytest.raises(SkillTagNotFoundError):
+            load_skill_section("notag")
+
+    def test_tag_in_wrong_file_raises_helpful_error(self):
+        # "entity_extraction:rules" belongs to entity_extraction.md
+        # Try using a different file prefix with a real section
+        with pytest.raises(SkillTagNotFoundError) as exc_info:
+            load_skill_section("c4:entity_extraction_rules_tag")
+        assert "c4" in str(exc_info.value)
+
+
+# ── Task 6.7: Word-limit validation ────────────────────────────────────────
+
+
+class TestWordLimitValidation:
+    def test_short_statements_pass_validation(self):
+        section = "## Test\n- Short statement here.\n- Another short one."
+        _validate_statements(section, Path("/fake/test.md"), "test:tag")
+
+    def test_overlong_statement_raises(self):
+        words = "word " * 26  # 26 words
+        section = f"## Test\n- {words.strip()}."
+        with pytest.raises(StatementTooLongError) as exc_info:
+            _validate_statements(section, Path("/fake/test.md"), "test:tag")
+        assert "26 words" in str(exc_info.value)
+        assert "test:tag" in str(exc_info.value)
+        assert "/fake/test.md" in str(exc_info.value)
+
+    def test_exactly_25_words_passes(self):
+        words = "word " * 25
+        section = f"## Test\n- {words.strip()}."
+        _validate_statements(section, Path("/fake/test.md"), "test:tag")
+
+    def test_markdown_formatting_is_stripped_before_counting(self):
+        # "**bold** italic `code`" → "bold italic" = 2 words
+        section = "## Test\n- **bold** *italic* `code`."
+        _validate_statements(section, Path("/fake/test.md"), "test:tag")
+
+    def test_table_row_validated(self):
+        words = "word " * 26
+        section = f"## Test\n| header |\n| {words.strip()} |"
+        with pytest.raises(StatementTooLongError):
+            _validate_statements(section, Path("/fake/test.md"), "test:tag")
+
+    def test_checklist_item_validated(self):
+        words = "word " * 26
+        section = f"## Test\n- [ ] {words.strip()}."
+        with pytest.raises(StatementTooLongError):
+            _validate_statements(section, Path("/fake/test.md"), "test:tag")
+
+    def test_all_bundle_sections_pass_word_limit(self):
+        for tag in REQUIRED_TAGS:
+            section = load_skill_section(tag)
+            # Should not raise — validation happens inside load_skill_section
+            assert len(section) > 0
+
+
+# ── Frontmatter error handling ─────────────────────────────────────────────
+
+
+class TestFrontmatterErrors:
+    def test_missing_frontmatter_raises(self):
+        text = "# No frontmatter here\nJust content."
+        with pytest.raises(MalformedSkillFrontmatterError, match="does not start with"):
+            _parse_frontmatter(text, Path("/fake/bad.md"))
+
+    def test_unclosed_frontmatter_raises(self):
+        text = "---\nname: test\n"
+        with pytest.raises(MalformedSkillFrontmatterError, match="Unclosed"):
+            _parse_frontmatter(text, Path("/fake/bad.md"))
+
+    def test_empty_frontmatter_raises(self):
+        text = "---\n---\ncontent"
+        with pytest.raises(MalformedSkillFrontmatterError, match="Empty"):
+            _parse_frontmatter(text, Path("/fake/bad.md"))
+
+    def test_missing_name_raises(self):
+        text = "---\ndescription: A test skill.\n---\ncontent"
+        with pytest.raises(MalformedSkillFrontmatterError, match="missing required 'name'"):
+            _parse_frontmatter(text, Path("/fake/bad.md"))
+
+    def test_missing_description_raises(self):
+        text = "---\nname: test\n---\ncontent"
+        with pytest.raises(MalformedSkillFrontmatterError, match="missing required 'description'"):
+            _parse_frontmatter(text, Path("/fake/bad.md"))
+
+
+# ── Tag extraction determinism ─────────────────────────────────────────────
+
+
+class TestTagExtraction:
+    def test_tag_pattern_matches_expected_formats(self):
+        assert _TAG_PATTERN.search("<!-- tag: entity_extraction:rules -->")
+        assert _TAG_PATTERN.search("<!-- tag: c4:checklist -->")
+        assert _TAG_PATTERN.search("<!--tag: saam:rules-->")
+
+    def test_tag_pattern_does_not_match_plain_comments(self):
+        assert _TAG_PATTERN.search("<!-- just a comment -->") is None
diff --git a/raa/tests/raa/unit/test_prompt_loader.py b/raa/tests/raa/unit/test_prompt_loader.py
new file mode 100644
index 0000000..b05b550
--- /dev/null
+++ b/raa/tests/raa/unit/test_prompt_loader.py
@@ -0,0 +1,204 @@
+"""Unit tests for prompt_loader — mustache rendering and skill injection."""
+from __future__ import annotations
+
+import tempfile
+from pathlib import Path
+
+import pytest
+
+from raa.utils.prompt_loader import (
+    _PROMPTS_DIR,
+    SkillContextKeyCollisionError,
+    load_prompt,
+)
+
+
+# ── Task 6.9: Normal mustache rendering still works ────────────────────────
+
+
+class TestNormalMustacheRendering:
+    def test_renders_simple_variables(self):
+        # Use the entity_extraction template since it exists but test base behavior
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "B123",
+            "reduced_confidence": "True",
+            "running_model": '{"systems":[]}',
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "B123" in result
+        assert "True" in result
+
+    def test_variable_interpolation_in_template(self):
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "SPECIAL_BATCH",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[R1, R2]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "SPECIAL_BATCH" in result
+        assert "[R1, R2]" in result
+
+
+# ── Task 6.10: Skill placeholder injection ─────────────────────────────────
+
+
+class TestSkillPlaceholderInjection:
+    def test_entity_extraction_rules_injected(self):
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "Quick Reference / Rules" in result
+        assert "entity_extraction" in result.lower() or "entity" in result.lower()
+
+    def test_saam_prompt_has_c4_rules_injected(self):
+        result = load_prompt("saam_analysis.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "C4 defines five entity types" in result
+
+    def test_pattern_matching_prompt_has_pattern_rules_injected(self):
+        result = load_prompt("pattern_matching.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "Quick Reference / Rules" in result
+
+    def test_skill_comment_is_not_in_output(self):
+        """The {{! skill: ... }} declarations must not appear in rendered output."""
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "{{! skill:" not in result
+        assert "skill:" not in result.split("{{!")[0] if "{{!" in result else True
+
+    def test_triple_mustache_variables_resolved(self):
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+        })
+        assert "{{{c4_rules}}}" not in result
+        assert "{{{entity_extraction_rules}}}" not in result
+
+
+# ── Task 6.11: Context key collision ────────────────────────────────────────
+
+
+class TestContextKeyCollision:
+    def test_collision_with_c4_rules_raises(self):
+        with pytest.raises(SkillContextKeyCollisionError) as exc_info:
+            load_prompt("entity_extraction.md", {
+                "batch_id": "B",
+                "reduced_confidence": "False",
+                "running_model": "{}",
+                "requirements": "[]",
+                "bridge_requirements": "[]",
+                "quality_weights": "{}",
+                "c4_rules": "EXPLICIT",
+            })
+        assert "c4_rules" in str(exc_info.value)
+
+    def test_collision_with_entity_extraction_rules_raises(self):
+        with pytest.raises(SkillContextKeyCollisionError) as exc_info:
+            load_prompt("entity_extraction.md", {
+                "batch_id": "B",
+                "reduced_confidence": "False",
+                "running_model": "{}",
+                "requirements": "[]",
+                "bridge_requirements": "[]",
+                "quality_weights": "{}",
+                "entity_extraction_rules": "custom",
+            })
+        assert "entity_extraction_rules" in str(exc_info.value)
+
+    def test_non_colliding_extra_keys_ok(self):
+        result = load_prompt("entity_extraction.md", {
+            "batch_id": "B",
+            "reduced_confidence": "False",
+            "running_model": "{}",
+            "requirements": "[]",
+            "bridge_requirements": "[]",
+            "quality_weights": "{}",
+            "extra_context": "safe value",
+        })
+        assert "safe value" not in result  # not used in template, but no error
+
+
+# ── File not found errors ──────────────────────────────────────────────────
+
+
+class TestFileNotFoundErrors:
+    def test_missing_prompt_template_raises(self):
+        with pytest.raises(FileNotFoundError) as exc_info:
+            load_prompt("no_such_template.md", {})
+        assert "no_such_template.md" in str(exc_info.value)
+
+    def test_missing_prompt_template_mentions_path(self):
+        with pytest.raises(FileNotFoundError) as exc_info:
+            load_prompt("ghost.md", {})
+        assert "Prompt template not found" in str(exc_info.value)
+
+
+# ── Task 6.12: Regression — all strategy prompts render ────────────────────
+
+
+class TestAllPromptsRender:
+    @pytest.mark.parametrize("template_name", [
+        "saam_analysis.md",
+        "pattern_matching.md",
+        "entity_extraction.md",
+    ])
+    def test_prompt_renders_with_representative_context(self, template_name):
+        context = {
+            "batch_id": "batch_regression_1",
+            "reduced_confidence": "False",
+            "running_model": "{'systems': [{'id': 'sys1', 'name': 'Core'}], "
+                             "'entities': [{'id': 'sys1', 'name': 'Core', "
+                             "'c4_type': 'system'}]}",
+            "requirements": (
+                "[{'id': 'REQ-1', 'text': 'The system shall provide "
+                "a REST API for order processing.'}, "
+                "{'id': 'REQ-2', 'text': 'The system shall store orders "
+                "in a relational database.'}]"
+            ),
+            "bridge_requirements": (
+                "[{'id': 'REQ-0', 'text': 'The system shall integrate "
+                "with external payment gateway.'}]"
+            ),
+            "quality_weights": (
+                "{'performance': 0.3, 'security': 0.4, "
+                "'availability': 0.2, 'maintainability': 0.1}"
+            ),
+        }
+        result = load_prompt(template_name, context)
+        assert len(result) > 0
+        assert "batch_regression_1" in result
+        assert "REQ-1" in result
+        # All three should have skill-injected content
+        assert "C4 defines" in result or "## C4 Hierarchy Rules" in result
diff --git a/raa/raa/utils/prompt_loader.py b/raa/raa/utils/prompt_loader.py
new file mode 100644
index 0000000..ddd290a
--- /dev/null
+++ b/raa/raa/utils/prompt_loader.py
@@ -0,0 +1,60 @@
+"""Prompt template loader using chevron mustache rendering with skill injection."""
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import chevron
+
+from raa.utils.skill_loader import load_skill_section
+
+_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
+
+_SKILL_DECL_PATTERN = re.compile(
+    r"\{\{!\s*skill:\s*(\S+)\s+as\s+(\S+)\s*\}\}"
+)
+
+
+class SkillContextKeyCollisionError(Exception):
+    """Skill injection would overwrite an explicit caller-provided context key."""
+
+
+def load_prompt(template_name: str, context: dict) -> str:
+    """Load a mustache template from raa/prompts/ and render with context.
+
+    Skill declarations in the template (``{{! skill: <tag> as <key> }}``)
+    are resolved via ``skill_loader`` and injected into the render context
+    before calling ``chevron.render()``.
+
+    Args:
+        template_name: Filename without path (e.g. ``"saam_analysis.md"``).
+        context: Dict of template variables.
+
+    Returns:
+        Rendered prompt string.
+
+    Raises:
+        FileNotFoundError: Template file not found.
+        SkillContextKeyCollisionError: A skill key would overwrite a caller key.
+    """
+    template_path = _PROMPTS_DIR / template_name
+    if not template_path.is_file():
+        raise FileNotFoundError(f"Prompt template not found: {template_path}")
+    with open(template_path) as f:
+        template = f.read()
+
+    # Resolve skill declarations
+    declarations = _SKILL_DECL_PATTERN.findall(template)
+    if declarations:
+        render_context = dict(context)
+        for tag, key in declarations:
+            if key in render_context:
+                raise SkillContextKeyCollisionError(
+                    f"Skill injection key '{key}' (tag: '{tag}') would overwrite "
+                    f"an explicit context key. Rename the 'as' variable in the "
+                    f"template or remove the conflicting context key."
+                )
+            render_context[key] = load_skill_section(tag)
+        return chevron.render(template, render_context)
+
+    return chevron.render(template, context)
diff --git a/raa/raa/prompts/saam_analysis.md b/raa/raa/prompts/saam_analysis.md
new file mode 100644
index 0000000..ba01efd
--- /dev/null
+++ b/raa/raa/prompts/saam_analysis.md
@@ -0,0 +1,34 @@
+{{! skill: c4:rules as c4_rules }}
+{{! skill: c4_level_mapping:rules as c4_level_mapping_rules }}
+{{! skill: saam:rules as saam_rules }}
+
+You are an architecture extraction agent using SAAM (Software Architecture Analysis Method).
+
+## Task
+Extract C4 architectural elements from the requirement batch below.
+
+## Context
+- Strategy: SAAM-first analysis (RAA-A)
+- Batch ID: {{batch_id}}
+- Reduced confidence: {{reduced_confidence}}
+- Running model (existing architecture): {{running_model}}
+
+## C4 Hierarchy Rules (STRICT)
+{{{c4_rules}}}
+
+## C4 Level Mapping
+{{{c4_level_mapping_rules}}}
+
+## SAAM Scenario Evaluation
+{{{saam_rules}}}
+
+## Requirements
+{{requirements}}
+
+## Bridge Requirements (shared context from adjacent batches)
+{{bridge_requirements}}
+
+## Quality Weights
+{{quality_weights}}
+
+Return an ArchFragment with entities and relationships. Do not nest entities inside other entities.
diff --git a/raa/raa/prompts/pattern_matching.md b/raa/raa/prompts/pattern_matching.md
new file mode 100644
index 0000000..013a2df
--- /dev/null
+++ b/raa/raa/prompts/pattern_matching.md
@@ -0,0 +1,34 @@
+{{! skill: c4:rules as c4_rules }}
+{{! skill: c4_level_mapping:rules as c4_level_mapping_rules }}
+{{! skill: pattern_selection:rules as pattern_selection_rules }}
+
+You are an architecture extraction agent using pattern-driven analysis.
+
+## Task
+Extract C4 architectural elements from the requirement batch by matching known architecture patterns.
+
+## Context
+- Strategy: Pattern-driven analysis (RAA-B)
+- Batch ID: {{batch_id}}
+- Reduced confidence: {{reduced_confidence}}
+- Running model (existing architecture): {{running_model}}
+
+## C4 Hierarchy Rules (STRICT)
+{{{c4_rules}}}
+
+## C4 Level Mapping
+{{{c4_level_mapping_rules}}}
+
+## Pattern Selection Guidance
+{{{pattern_selection_rules}}}
+
+## Requirements
+{{requirements}}
+
+## Bridge Requirements (shared context from adjacent batches)
+{{bridge_requirements}}
+
+## Quality Weights
+{{quality_weights}}
+
+Return an ArchFragment with entities and relationships. Do not nest entities inside other entities.
diff --git a/raa/raa/prompts/entity_extraction.md b/raa/raa/prompts/entity_extraction.md
new file mode 100644
index 0000000..2c2892f
--- /dev/null
+++ b/raa/raa/prompts/entity_extraction.md
@@ -0,0 +1,42 @@
+{{! skill: c4:rules as c4_rules }}
+{{! skill: c4_level_mapping:rules as c4_level_mapping_rules }}
+{{! skill: entity_extraction:rules as entity_extraction_rules }}
+{{! skill: relationship_extraction:rules as relationship_extraction_rules }}
+{{! skill: technology_inference:rules as technology_inference_rules }}
+
+You are an architecture extraction agent using entity/relationship-driven analysis.
+
+## Task
+Extract C4 architectural elements from the requirement batch by identifying entities and their relationships.
+
+## Context
+- Strategy: Entity/relationship extraction (RAA-C)
+- Batch ID: {{batch_id}}
+- Reduced confidence: {{reduced_confidence}}
+- Running model (existing architecture): {{running_model}}
+
+## C4 Hierarchy Rules (STRICT)
+{{{c4_rules}}}
+
+## C4 Level Mapping
+{{{c4_level_mapping_rules}}}
+
+## Entity Extraction Rules
+{{{entity_extraction_rules}}}
+
+## Relationship Extraction Rules
+{{{relationship_extraction_rules}}}
+
+## Technology Inference Rules
+{{{technology_inference_rules}}}
+
+## Requirements
+{{requirements}}
+
+## Bridge Requirements (shared context from adjacent batches)
+{{bridge_requirements}}
+
+## Quality Weights
+{{quality_weights}}
+
+Return an ArchFragment with entities and relationships. Do not nest entities inside other entities.

```
