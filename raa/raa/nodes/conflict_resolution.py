"""
Conflict resolution node (Story 3.3).

Applies human answers authoritatively to override pre-computed suggestions,
parses free-text overrides via LLM into C4 structural modifications,
validates changes against C4 metamodel rules, and resolves assumption flags.
"""
from __future__ import annotations

import json
from typing import Any, Literal

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field, ValidationError

from raa.state.models import C4Entity, C4Relationship, OpenQuestion, ArchFragment
from raa.state.schemas import RAAState
from raa.utils.c4_validator import enforce_fragment_hierarchy
from raa.utils.prompt_loader import load_prompt


# ── Structured LLM Output Model ─────────────────────────────────────────────


class EntityModification(BaseModel):
    entity_id: str
    action: Literal["update_parent", "update_name", "merge", "delete", "update_technology"]
    new_parent_system_id: str | None = None
    new_parent_container_id: str | None = None
    new_name: str | None = None
    target_entity_id: str | None = None
    new_technology: str | None = None


class RelationshipModification(BaseModel):
    action: Literal["add", "remove", "update_endpoints"]
    source_id: str | None = None
    target_id: str | None = None
    description: str = ""
    relationship_id: str | None = None
    new_source_id: str | None = None
    new_target_id: str | None = None



class HumanOverrideInstructions(BaseModel):
    entity_modifications: list[EntityModification] = Field(default_factory=list)
    relationship_modifications: list[RelationshipModification] = Field(default_factory=list)


# ── Answer Normalization ────────────────────────────────────────────────────


def _normalize_answers(human_answers: Any) -> dict[str, str]:
    """Normalize human_answers from various formats into a flat {question_id: answer_text} dict.

    Handles:
    - Flat dict: ``{"q_0": "approve", "q_1": "reject"}``
    - List-style: ``{"answers": [{"question_id": "q_0", "answer": "approve"}]}``
    - Nested dict: ``{"answers": {"q_0": "approve"}}``
    """
    if human_answers is None:
        return {}

    if isinstance(human_answers, dict):
        # Check for list-style: {"answers": [{"question_id": ..., "answer": ...}]}
        answers_list = human_answers.get("answers")
        if isinstance(answers_list, list):
            result: dict[str, str] = {}
            for item in answers_list:
                if isinstance(item, dict):
                    qid = item.get("question_id", "")
                    ans = item.get("answer", "")
                    if qid:
                        result[str(qid)] = str(ans)
            return result

        # Check for nested dict: {"answers": {"q_0": "text"}}
        if isinstance(answers_list, dict):
            return {str(k): str(v) for k, v in answers_list.items()}

        # Assume flat dict: keys are question IDs
        # Filter out non-question-id keys (like "answers" itself when it's not dict/list)
        result = {}
        for k, v in human_answers.items():
            if k == "answers" and not isinstance(v, (dict, list)):
                continue
            if isinstance(v, (str, int, float, bool)):
                result[str(k)] = str(v)
        return result

    return {}


# ── Question/Answer Mapping ──────────────────────────────────────────────────


def _map_answers_to_questions(
    answers: dict[str, str],
    open_questions: list[dict],
) -> tuple[list[dict], set[str]]:
    """Map human answers to matching OpenQuestions.

    Returns (updated_questions, resolved_entity_ids).
    """
    resolved_entity_ids: set[str] = set()

    for i, q in enumerate(open_questions):
        qid = q.get("id") or f"q_{i}_{q.get('question_type') or q.get('type') or 'unknown'}"

        if qid in answers:
            q["resolution"] = answers[qid]
            q["assumption_flag"] = False

            # Collect referenced entity IDs
            id_keys = ("entity_a_id", "entity_b_id", "entity_id", "promoted_component_id")
            for key in id_keys:
                val = q.get(key)
                if val and isinstance(val, str):
                    resolved_entity_ids.add(val)
            # Also scan context
            ctx = q.get("context") or {}
            if isinstance(ctx, dict):
                for key in id_keys:
                    val = ctx.get(key)
                    if val and isinstance(val, str):
                        resolved_entity_ids.add(val)

    return open_questions, resolved_entity_ids



# ── Arch Model Overrides ─────────────────────────────────────────────────────


def _apply_answer_overrides(
    arch_model: dict,
    resolved_entity_ids: set[str],
) -> dict:
    """Clear assumption flags on entities resolved by human answers."""
    model = {
        "entities": [dict(e) for e in (arch_model.get("entities") or [])],
        "relationships": [dict(r) for r in (arch_model.get("relationships") or [])],
        "boundary_groups": list(arch_model.get("boundary_groups") or []),
        "cross_cutting_candidates": list(arch_model.get("cross_cutting_candidates") or []),
        "assumption_flags": list(arch_model.get("assumption_flags") or []),
    }

    for entity in model["entities"]:
        if entity.get("id") in resolved_entity_ids:
            meta = dict(entity.get("metadata") or {})
            meta["assumption_flag"] = False
            meta["assumed"] = False
            entity["metadata"] = meta

    # Remove resolved entity IDs from assumption_flags
    assumption_flags: list[str] = model["assumption_flags"]
    model["assumption_flags"] = [f for f in assumption_flags if f not in resolved_entity_ids]

    return model


# ── LLM Interpreter ──────────────────────────────────────────────────────────


def _build_arch_model_context(arch_model: dict, max_entities: int = 20) -> str:
    """Build a compact text summary of the arch model for the LLM prompt."""
    entities = (arch_model.get("entities") or [])[:max_entities]
    relationships = (arch_model.get("relationships") or [])[:max_entities]

    lines = ["## Entities"]
    for e in entities:
        lines.append(
            f"- {e.get('id')}: {e.get('name')} (type={e.get('c4_type')}, "
            f"parent_system={e.get('parent_system_id')}, "
            f"parent_container={e.get('parent_container_id')})"
        )

    lines.append("## Relationships")
    for r in relationships:
        lines.append(
            f"- {r.get('id')}: {r.get('source_id')} -> {r.get('target_id')} "
            f"({r.get('description', '')})"
        )

    return "\n".join(lines)


def _parse_human_override(
    human_answer: str,
    arch_model: dict,
    config: RunnableConfig | None,
) -> HumanOverrideInstructions:
    """Use the judge LLM to parse free-text human directions into C4 structural actions.

    Returns empty instructions if:
    - No judge_llm is configured
    - The human_answer is empty/whitespace
    - The LLM call fails
    """
    answer = (human_answer or "").strip()
    if not answer:
        return HumanOverrideInstructions()

    # Try to get the judge LLM from config
    judge_llm = None
    if config is not None:
        if isinstance(config, dict):
            cfg = config.get("configurable") or {}
        else:
            cfg = getattr(config, "configurable", None) or {}
        judge_llm = cfg.get("judge_llm")

    if judge_llm is None:
        return HumanOverrideInstructions()

    try:
        prompt = load_prompt("parse_human_override", {
            "human_answer": answer,
            "arch_model_context": _build_arch_model_context(arch_model),
        })

        structured_llm = judge_llm.with_structured_output(HumanOverrideInstructions)
        result = structured_llm.invoke(prompt)
        return result
    except (ValidationError, json.JSONDecodeError, Exception):
        return HumanOverrideInstructions()


# ── Structural Modification Application ──────────────────────────────────────


def _apply_structural_modifications(
    arch_model: dict,
    instructions: HumanOverrideInstructions,
) -> dict:
    """Apply parsed structural modifications to the arch model.

    Returns a new model dict — never mutates input.
    """
    model = {
        "entities": [dict(e) for e in (arch_model.get("entities") or [])],
        "relationships": [dict(r) for r in (arch_model.get("relationships") or [])],
        "boundary_groups": list(arch_model.get("boundary_groups") or []),
        "cross_cutting_candidates": list(arch_model.get("cross_cutting_candidates") or []),
        "assumption_flags": list(arch_model.get("assumption_flags") or []),
    }

    entity_by_id = {e.get("id", ""): e for e in model["entities"]}

    for mod in instructions.entity_modifications:
        eid = mod.entity_id
        if eid not in entity_by_id:
            continue

        entity = entity_by_id[eid]

        if mod.action == "update_parent":
            if mod.new_parent_system_id is not None:
                entity["parent_system_id"] = mod.new_parent_system_id
            if mod.new_parent_container_id is not None:
                entity["parent_container_id"] = mod.new_parent_container_id

        elif mod.action == "update_name":
            if mod.new_name:
                entity["name"] = mod.new_name

        elif mod.action == "update_technology":
            entity["technology"] = mod.new_technology or ""

        elif mod.action == "merge":
            target_id = mod.target_entity_id
            if target_id and target_id in entity_by_id:
                target = entity_by_id[target_id]
                req_ids = sorted(set(
                    (entity.get("requirement_ids") or []) +
                    (target.get("requirement_ids") or [])
                ))
                target["requirement_ids"] = req_ids
                # Remove source entity
                model["entities"] = [e for e in model["entities"] if e.get("id") != eid]
                # Rewrite relationships pointing to/from merged entity to target_id
                for r in model["relationships"]:
                    if r.get("source_id") == eid:
                        r["source_id"] = target_id
                    if r.get("target_id") == eid:
                        r["target_id"] = target_id
                # Filter out self-relationships after merge
                model["relationships"] = [
                    r for r in model["relationships"]
                    if r.get("source_id") != r.get("target_id")
                ]

        elif mod.action == "delete":
            model["entities"] = [e for e in model["entities"] if e.get("id") != eid]
            model["relationships"] = [
                r for r in model["relationships"]
                if r.get("source_id") != eid and r.get("target_id") != eid
            ]


    # Apply relationship modifications
    for mod in instructions.relationship_modifications:
        if mod.action == "add":
            rel_id = f"rel_human_{mod.source_id}_{mod.target_id}"
            model["relationships"].append({
                "id": rel_id,
                "source_id": mod.source_id or "",
                "target_id": mod.target_id or "",
                "description": mod.description or "",
                "relationship_type": "uses",
                "diagram_scope": "",
                "metadata": {"source": "human_override"},
            })

        elif mod.action == "remove":
            rid = mod.relationship_id
            model["relationships"] = [
                r for r in model["relationships"] if r.get("id") != rid
            ]

        elif mod.action == "update_endpoints":
            rid = mod.relationship_id
            for rel in model["relationships"]:
                if rel.get("id") == rid:
                    if mod.new_source_id is not None:
                        rel["source_id"] = mod.new_source_id
                    if mod.new_target_id is not None:
                        rel["target_id"] = mod.new_target_id

    return model


# ── Validation ───────────────────────────────────────────────────────────────


def _validate_and_fallback(
    original_model: dict,
    modified_model: dict,
    human_answer: str,
) -> tuple[dict, list[dict]]:
    """Validate structural modifications against C4 metamodel rules.

    Builds a temporary ArchFragment from the modifications and runs
    ``enforce_fragment_hierarchy``. On failure, logs a ``scope_conflict``
    open question and reverts to the original model.

    Returns (final_model, open_questions).
    """
    # Find which entities were added or modified
    orig_ids = {e.get("id") for e in (original_model.get("entities") or [])}
    mod_entities_raw = modified_model.get("entities") or []

    # Build modified entities as C4Entity objects
    modified_entities: list[C4Entity] = []
    for e in mod_entities_raw:
        try:
            modified_entities.append(C4Entity.model_validate(e))
        except ValidationError:
            continue

    # Build relationships
    modified_relationships: list[C4Relationship] = []
    for r in (modified_model.get("relationships") or []):
        try:
            modified_relationships.append(C4Relationship.model_validate(r))
        except ValidationError:
            continue

    fragment = ArchFragment(
        entities=modified_entities,
        relationships=modified_relationships,
        cross_cutting_candidates=modified_model.get("cross_cutting_candidates") or [],
        assumption_flags=modified_model.get("assumption_flags") or [],
    )

    try:
        cleaned, questions = enforce_fragment_hierarchy(
            fragment,
            original_model,
            batch_id="human_override",
            strategy="human",
        )

        # Check for hierarchy conflict or orphan issues
        critical_issues = [
            q for q in questions
            if q.get("reason") in (
                "orphan_container", "orphan_component",
                "unresolved_relationship_endpoint",
            )
        ]

        if critical_issues:
            scope_conflict = {
                "question_type": "scope_conflict",
                "description": (
                    f"Human override caused structural validation failure: "
                    f"{len(critical_issues)} C4 hierarchy violation(s). "
                    f"Original instruction: '{human_answer[:200]}'. "
                    f"Changes reverted to safe state."
                ),
                "source": "conflict_resolution",
                "severity": "high",
                "validation_details": [
                    {"reason": q.get("reason"), "detail": q.get("suggested_resolution")}
                    for q in critical_issues
                ],
            }
            return dict(original_model), [scope_conflict]

        # Merge cleaned fragment entities back
        result = dict(modified_model)
        result["entities"] = [e.model_dump() for e in cleaned.entities]
        result["relationships"] = [r.model_dump() for r in cleaned.relationships]
        return result, []

    except Exception:
        scope_conflict = {
            "question_type": "scope_conflict",
            "description": (
                f"Human override caused unexpected validation error. "
                f"Original instruction: '{human_answer[:200]}'. "
                f"Changes reverted to safe state."
            ),
            "source": "conflict_resolution",
            "severity": "high",
        }
        return dict(original_model), [scope_conflict]


# ── Main Node ────────────────────────────────────────────────────────────────


def conflict_resolution(
    state: RAAState,
    config: RunnableConfig | None = None,
) -> dict:
    """Apply human answers authoritatively to override pre-computed suggestions.

    1. Normalizes ``human_answers`` from various formats to a flat dict.
    2. Maps answers to matching ``OpenQuestion`` entries, updating
       ``resolution`` and clearing ``assumption_flag``.
    3. Applies overrides to ``arch_model`` entities (resets assumption flags).
    4. Parses free-text human overrides via the judge LLM into C4 structural
       modifications (entity parent changes, merges, relationship edits).
    5. Validates structural modifications against C4 metamodel rules.
       On failure, logs ``scope_conflict`` and reverts to the safe state.

    Args:
        state: Full RAA state with ``human_answers``, ``open_questions``,
            and ``arch_model`` channels.
        config: LangGraph RunnableConfig with optional ``judge_llm`` in
            configurable.

    Returns:
        dict with keys: ``open_questions``, ``arch_model``.
    """
    human_answers = state.get("human_answers") or {}
    open_questions: list[dict] = list(state.get("open_questions") or [])
    arch_model: dict = state.get("arch_model") or {}

    # 1. Normalize answers
    answers = _normalize_answers(human_answers)

    # 2. Map answers to questions
    updated_questions, resolved_entity_ids = _map_answers_to_questions(
        answers, open_questions,
    )

    # 3. Apply overrides to arch_model entities
    arch_model = _apply_answer_overrides(arch_model, resolved_entity_ids)

    # 4. LLM interpreter: parse free-text human answers into structural modifications
    all_instructions = HumanOverrideInstructions()
    for answer_text in answers.values():
        instructions = _parse_human_override(answer_text, arch_model, config)
        all_instructions.entity_modifications.extend(instructions.entity_modifications)
        all_instructions.relationship_modifications.extend(instructions.relationship_modifications)

    new_open_questions: list[dict] = []

    # 5. Apply + validate structural modifications
    if all_instructions.entity_modifications or all_instructions.relationship_modifications:
        modified_model = _apply_structural_modifications(arch_model, all_instructions)
        combined_answers = "; ".join(answers.values())
        arch_model, validation_questions = _validate_and_fallback(
            arch_model, modified_model, combined_answers,
        )
        new_open_questions.extend(validation_questions)

    # Since open_questions is append-only in the state schema (Annotated[list, add]),
    # returning updated_questions would concatenate the entire list and duplicate it.
    # We only return new_open_questions to append newly generated questions,
    # as existing questions are already updated in-place.
    return {
        "open_questions": new_open_questions,
        "arch_model": arch_model,
    }

