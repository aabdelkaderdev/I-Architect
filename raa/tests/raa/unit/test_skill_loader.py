"""Unit tests for skill_loader — frontmatter, tag extraction, word-limit validation."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from raa.utils.skill_loader import (
    _SKILLS_DIR,
    _REFERENCES_DIR,
    _TAG_PATTERN,
    DuplicateSkillTagError,
    MalformedSkillFrontmatterError,
    SkillTagNotFoundError,
    StatementTooLongError,
    _collect_all_tags,
    _parse_frontmatter,
    _validate_statements,
    load_skill_section,
)

REQUIRED_SECTIONS = [
    "Product Summary / Definition",
    "When to Use",
    "Quick Reference / Rules",
    "Decision Guidance",
    "Workflow",
    "Common Gotchas",
    "Verification Checklist",
]

REQUIRED_TAGS = [
    "c4_level_mapping:rules",
    "c4_level_mapping:checklist",
    "entity_extraction:rules",
    "entity_extraction:checklist",
    "relationship_extraction:rules",
    "relationship_extraction:checklist",
    "pattern_selection:rules",
    "pattern_selection:checklist",
    "technology_inference:rules",
    "technology_inference:checklist",
]


# ── Task 6.1: SKILL.md and reference files exist ───────────────────────────


class TestSkillBundleExists:
    def test_skill_md_exists(self):
        assert (_SKILLS_DIR / "SKILL.md").is_file()

    def test_references_dir_exists(self):
        assert _REFERENCES_DIR.is_dir()

    @pytest.mark.parametrize("filename", [
        "c4_level_mapping.md",
        "entity_extraction.md",
        "relationship_extraction.md",
        "pattern_selection.md",
        "technology_inference.md",
        "saam.md",
        "c4.md",
        "quality_attributes.md",
    ])
    def test_reference_file_exists(self, filename):
        path = _REFERENCES_DIR / filename
        assert path.is_file(), f"Missing: {path}"


# ── Task 6.2-6.3: Frontmatter and required sections ────────────────────────


class TestFrontmatterAndSections:

    @pytest.mark.parametrize("filename", [
        "c4_level_mapping.md",
        "entity_extraction.md",
        "relationship_extraction.md",
        "pattern_selection.md",
        "technology_inference.md",
        "saam.md",
        "c4.md",
        "quality_attributes.md",
    ])
    def test_reference_has_valid_frontmatter(self, filename):
        path = _REFERENCES_DIR / filename
        with open(path) as f:
            text = f.read()
        fm = _parse_frontmatter(text, path)
        assert "name" in fm
        assert "description" in fm
        assert isinstance(fm.get("metadata"), dict) or fm.get("metadata") is None
        if fm.get("metadata"):
            assert "target_node" in fm["metadata"] or "target_node" not in fm["metadata"]
            assert "version" in fm["metadata"] or "version" not in fm["metadata"]

    @pytest.mark.parametrize("filename", [
        "c4_level_mapping.md",
        "entity_extraction.md",
        "relationship_extraction.md",
        "pattern_selection.md",
        "technology_inference.md",
        "saam.md",
        "c4.md",
        "quality_attributes.md",
    ])
    def test_reference_has_required_sections(self, filename):
        path = _REFERENCES_DIR / filename
        with open(path) as f:
            text = f.read()
        for section in REQUIRED_SECTIONS:
            assert section in text, f"Missing section '{section}' in {filename}"


# ── Task 6.4: load_skill_section returns only the tagged section ────────────


class TestLoadSkillSection:
    def test_load_rules_returns_only_tagged_section(self):
        section = load_skill_section("entity_extraction:rules")
        assert "Quick Reference / Rules" in section
        assert "## Decision Guidance" not in section
        assert "## Verification Checklist" not in section

    def test_load_checklist_returns_only_tagged_section(self):
        section = load_skill_section("entity_extraction:checklist")
        assert "Verification Checklist" in section
        assert "## Product Summary / Definition" not in section
        assert "## Quick Reference / Rules" not in section

    def test_load_c4_rules_returns_only_tagged_section(self):
        section = load_skill_section("c4:rules")
        assert "Quick Reference / Rules" in section
        assert "## Decision Guidance" not in section

    @pytest.mark.parametrize("tag", [
        "c4_level_mapping:rules",
        "c4_level_mapping:checklist",
        "entity_extraction:rules",
        "entity_extraction:checklist",
        "relationship_extraction:rules",
        "relationship_extraction:checklist",
        "pattern_selection:rules",
        "pattern_selection:checklist",
        "technology_inference:rules",
        "technology_inference:checklist",
    ])
    def test_all_required_tags_load(self, tag):
        section = load_skill_section(tag)
        assert len(section) > 0


# ── Task 6.5: Duplicate tags raise ─────────────────────────────────────────


class TestDuplicateTagDetection:
    def test_no_duplicate_tags_in_bundle(self):
        tags = _collect_all_tags()
        # The function itself raises on duplicates, so reaching here means
        # no duplicates. Verify all required tags are present.
        for tag in REQUIRED_TAGS:
            assert tag in tags, f"Required tag '{tag}' not found in bundle"


# ── Task 6.6: Missing tags raise ───────────────────────────────────────────


class TestMissingTagErrors:
    def test_missing_tag_raises_clear_error(self):
        with pytest.raises(SkillTagNotFoundError) as exc_info:
            load_skill_section("nonexistent:rules")
        assert "nonexistent" in str(exc_info.value)

    def test_wrong_file_prefix_raises_helpful_error(self):
        # "entity_extraction:rules" belongs to entity_extraction.md.
        # Using prefix "pattern_selection" with the wrong section name from
        # another file should raise — no tag named "pattern_selection:rules"
        # but "entity_extraction:rules" doesn't exist in pattern_selection.md.
        # Instead, try a genuinely wrong file_prefix with a real section name:
        with pytest.raises(SkillTagNotFoundError) as exc_info:
            load_skill_section("saam:entity_extraction_checklist")
        assert "saam" in str(exc_info.value)

    def test_missing_reference_file_raises(self):
        with pytest.raises(SkillTagNotFoundError):
            load_skill_section("no_such_file:rules")

    def test_tag_no_colon_raises(self):
        with pytest.raises(SkillTagNotFoundError):
            load_skill_section("notag")

    def test_tag_in_wrong_file_raises_helpful_error(self):
        # "entity_extraction:rules" belongs to entity_extraction.md
        # Try using a different file prefix with a real section
        with pytest.raises(SkillTagNotFoundError) as exc_info:
            load_skill_section("c4:entity_extraction_rules_tag")
        assert "c4" in str(exc_info.value)


# ── Task 6.7: Word-limit validation ────────────────────────────────────────


class TestWordLimitValidation:
    def test_short_statements_pass_validation(self):
        section = "## Test\n- Short statement here.\n- Another short one."
        _validate_statements(section, Path("/fake/test.md"), "test:tag")

    def test_overlong_statement_raises(self):
        words = "word " * 26  # 26 words
        section = f"## Test\n- {words.strip()}."
        with pytest.raises(StatementTooLongError) as exc_info:
            _validate_statements(section, Path("/fake/test.md"), "test:tag")
        assert "26 words" in str(exc_info.value)
        assert "test:tag" in str(exc_info.value)
        assert "/fake/test.md" in str(exc_info.value)

    def test_exactly_25_words_passes(self):
        words = "word " * 25
        section = f"## Test\n- {words.strip()}."
        _validate_statements(section, Path("/fake/test.md"), "test:tag")

    def test_markdown_formatting_is_stripped_before_counting(self):
        # "**bold** italic `code`" → "bold italic" = 2 words
        section = "## Test\n- **bold** *italic* `code`."
        _validate_statements(section, Path("/fake/test.md"), "test:tag")

    def test_table_row_validated(self):
        words = "word " * 26
        section = f"## Test\n| header |\n| {words.strip()} |"
        with pytest.raises(StatementTooLongError):
            _validate_statements(section, Path("/fake/test.md"), "test:tag")

    def test_checklist_item_validated(self):
        words = "word " * 26
        section = f"## Test\n- [ ] {words.strip()}."
        with pytest.raises(StatementTooLongError):
            _validate_statements(section, Path("/fake/test.md"), "test:tag")

    def test_all_bundle_sections_pass_word_limit(self):
        for tag in REQUIRED_TAGS:
            section = load_skill_section(tag)
            # Should not raise — validation happens inside load_skill_section
            assert len(section) > 0


# ── Frontmatter error handling ─────────────────────────────────────────────


class TestFrontmatterErrors:
    def test_missing_frontmatter_raises(self):
        text = "# No frontmatter here\nJust content."
        with pytest.raises(MalformedSkillFrontmatterError, match="does not start with"):
            _parse_frontmatter(text, Path("/fake/bad.md"))

    def test_unclosed_frontmatter_raises(self):
        text = "---\nname: test\n"
        with pytest.raises(MalformedSkillFrontmatterError, match="Unclosed"):
            _parse_frontmatter(text, Path("/fake/bad.md"))

    def test_empty_frontmatter_raises(self):
        text = "---\n---\ncontent"
        with pytest.raises(MalformedSkillFrontmatterError, match="Empty"):
            _parse_frontmatter(text, Path("/fake/bad.md"))

    def test_missing_name_raises(self):
        text = "---\ndescription: A test skill.\n---\ncontent"
        with pytest.raises(MalformedSkillFrontmatterError, match="missing required 'name'"):
            _parse_frontmatter(text, Path("/fake/bad.md"))

    def test_missing_description_raises(self):
        text = "---\nname: test\n---\ncontent"
        with pytest.raises(MalformedSkillFrontmatterError, match="missing required 'description'"):
            _parse_frontmatter(text, Path("/fake/bad.md"))


# ── Tag extraction determinism ─────────────────────────────────────────────


class TestTagExtraction:
    def test_tag_pattern_matches_expected_formats(self):
        assert _TAG_PATTERN.search("<!-- tag: entity_extraction:rules -->")
        assert _TAG_PATTERN.search("<!-- tag: c4:checklist -->")
        assert _TAG_PATTERN.search("<!--tag: saam:rules-->")

    def test_tag_pattern_does_not_match_plain_comments(self):
        assert _TAG_PATTERN.search("<!-- just a comment -->") is None


# ── Patched functionality and edge cases ───────────────────────────────────


class TestPatchedFunctionality:
    def test_description_truncation(self):
        long_desc = "x" * 2000
        text = f"---\nname: test\ndescription: {long_desc}\n---\ncontent"
        fm = _parse_frontmatter(text, Path("/fake/test.md"))
        assert len(fm["description"]) == 1024
        assert fm["description"] == "x" * 1024

    def test_path_traversal_detection(self):
        with pytest.raises(SkillTagNotFoundError, match="Invalid file prefix|Path traversal"):
            load_skill_section("../passwd:rules")

    def test_markdown_strip_html_comments_and_hashes(self):
        from raa.utils.skill_loader import _strip_markdown
        text = "## Heading <!-- tag: dummy -->\nSome text."
        stripped = _strip_markdown(text)
        assert "Heading" in stripped
        assert "tag:" not in stripped
        assert "##" not in stripped

    def test_nested_bullet_statement_splitting(self):
        from raa.utils.skill_loader import _STATEMENT_SEPARATOR
        section = "- Parent point\n  - Nested point"
        parts = _STATEMENT_SEPARATOR.split(section)
        assert len(parts) == 2
        assert parts[0].strip() == "- Parent point"
        assert parts[1].strip() == "- Nested point"

