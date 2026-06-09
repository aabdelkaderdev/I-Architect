"""Tests for Mustache template rendering. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.utils.rendering import load_template, render_prompt, render_system_user


class TestRendering:
    def test_load_template(self):
        """load_template reads a template file from raa/prompts/."""
        content = load_template("naming_convention.md")
        assert isinstance(content, str)
        assert len(content) > 0
        assert "PascalCase" in content

    def test_render_prompt(self):
        """render_prompt substitutes Mustache variables."""
        # Use a template we know has no partials
        rendered = render_prompt("non_asr_subgraph_system.md", {})
        assert isinstance(rendered, str)
        assert "functional analyst" in rendered

    def test_render_system_user(self):
        """render_system_user returns a (system, user) tuple."""
        sys_p, usr_p = render_system_user(
            "non_asr_subgraph_system.md",
            "non_asr_subgraph_user.md",
            {
                "non_asrs": [{"id": "REQ-010", "text": "Export data as CSV"}],
                "registry_snapshot": {"entries": {}},
            },
        )
        assert isinstance(sys_p, str)
        assert isinstance(usr_p, str)
        assert len(sys_p) > 0
        assert len(usr_p) > 0
        assert "REQ-010" in usr_p

    def test_template_cache(self):
        """Repeated loads hit the in-memory cache."""
        from raa.utils.rendering import _cache

        before = len(_cache)
        load_template("naming_convention.md")
        after_first = len(_cache)

        # Second load should not add to cache
        load_template("naming_convention.md")
        after_second = len(_cache)

        assert after_first > before or after_first > 0  # at least cached now
        assert after_second == after_first  # no new cache entry added
