"""Unit tests for prompt_loader — mustache rendering and skill injection."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from raa.utils.prompt_loader import (
    _PROMPTS_DIR,
    SkillContextKeyCollisionError,
    load_prompt,
)


# ── Task 6.9: Normal mustache rendering still works ────────────────────────


class TestNormalMustacheRendering:
    def test_renders_simple_variables(self):
        # Use the entity_extraction template since it exists but test base behavior
        result = load_prompt("entity_extraction.md", {
            "batch_id": "B123",
            "reduced_confidence": "True",
            "running_model": '{"systems":[]}',
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "B123" in result
        assert "True" in result

    def test_variable_interpolation_in_template(self):
        result = load_prompt("entity_extraction.md", {
            "batch_id": "SPECIAL_BATCH",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[R1, R2]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "SPECIAL_BATCH" in result
        assert "[R1, R2]" in result


# ── Task 6.10: Skill placeholder injection ─────────────────────────────────


class TestSkillPlaceholderInjection:
    def test_entity_extraction_rules_injected(self):
        result = load_prompt("entity_extraction.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "Quick Reference / Rules" in result
        assert "entity_extraction" in result.lower() or "entity" in result.lower()

    def test_saam_prompt_has_c4_rules_injected(self):
        result = load_prompt("saam_analysis.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "C4 defines five entity types" in result

    def test_pattern_matching_prompt_has_pattern_rules_injected(self):
        result = load_prompt("pattern_matching.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "Quick Reference / Rules" in result

    def test_skill_comment_is_not_in_output(self):
        """The {{! skill: ... }} declarations must not appear in rendered output."""
        result = load_prompt("entity_extraction.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "{{! skill:" not in result
        assert "skill:" not in result.split("{{!")[0] if "{{!" in result else True

    def test_triple_mustache_variables_resolved(self):
        result = load_prompt("entity_extraction.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
        })
        assert "{{{c4_rules}}}" not in result
        assert "{{{entity_extraction_rules}}}" not in result


# ── Task 6.11: Context key collision ────────────────────────────────────────


class TestContextKeyCollision:
    def test_collision_with_c4_rules_raises(self):
        with pytest.raises(SkillContextKeyCollisionError) as exc_info:
            load_prompt("entity_extraction.md", {
                "batch_id": "B",
                "reduced_confidence": "False",
                "running_model": "{}",
                "requirements": "[]",
                "bridge_requirements": "[]",
                "quality_weights": "{}",
                "c4_rules": "EXPLICIT",
            })
        assert "c4_rules" in str(exc_info.value)

    def test_collision_with_entity_extraction_rules_raises(self):
        with pytest.raises(SkillContextKeyCollisionError) as exc_info:
            load_prompt("entity_extraction.md", {
                "batch_id": "B",
                "reduced_confidence": "False",
                "running_model": "{}",
                "requirements": "[]",
                "bridge_requirements": "[]",
                "quality_weights": "{}",
                "entity_extraction_rules": "custom",
            })
        assert "entity_extraction_rules" in str(exc_info.value)

    def test_non_colliding_extra_keys_ok(self):
        result = load_prompt("entity_extraction.md", {
            "batch_id": "B",
            "reduced_confidence": "False",
            "running_model": "{}",
            "requirements": "[]",
            "bridge_requirements": "[]",
            "quality_weights": "{}",
            "extra_context": "safe value",
        })
        assert "safe value" not in result  # not used in template, but no error


# ── File not found errors ──────────────────────────────────────────────────


class TestFileNotFoundErrors:
    def test_missing_prompt_template_raises(self):
        with pytest.raises(FileNotFoundError) as exc_info:
            load_prompt("no_such_template.md", {})
        assert "no_such_template.md" in str(exc_info.value)

    def test_missing_prompt_template_mentions_path(self):
        with pytest.raises(FileNotFoundError) as exc_info:
            load_prompt("ghost.md", {})
        assert "Prompt template not found" in str(exc_info.value)


# ── Task 6.12: Regression — all strategy prompts render ────────────────────


class TestAllPromptsRender:
    @pytest.mark.parametrize("template_name", [
        "saam_analysis.md",
        "pattern_matching.md",
        "entity_extraction.md",
    ])
    def test_prompt_renders_with_representative_context(self, template_name):
        context = {
            "batch_id": "batch_regression_1",
            "reduced_confidence": "False",
            "running_model": "{'systems': [{'id': 'sys1', 'name': 'Core'}], "
                             "'entities': [{'id': 'sys1', 'name': 'Core', "
                             "'c4_type': 'system'}]}",
            "requirements": (
                "[{'id': 'REQ-1', 'text': 'The system shall provide "
                "a REST API for order processing.'}, "
                "{'id': 'REQ-2', 'text': 'The system shall store orders "
                "in a relational database.'}]"
            ),
            "bridge_requirements": (
                "[{'id': 'REQ-0', 'text': 'The system shall integrate "
                "with external payment gateway.'}]"
            ),
            "quality_weights": (
                "{'performance': 0.3, 'security': 0.4, "
                "'availability': 0.2, 'maintainability': 0.1}"
            ),
        }
        result = load_prompt(template_name, context)
        assert len(result) > 0
        assert "batch_regression_1" in result
        assert "REQ-1" in result
        # All three should have skill-injected content
        assert "C4 defines" in result or "## C4 Hierarchy Rules" in result
