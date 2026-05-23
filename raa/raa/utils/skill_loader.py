"""Skill reference loading — frontmatter, tag extraction, word-limit validation."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

_SKILLS_DIR = Path(__file__).resolve().parent.parent / "Skills"
_REFERENCES_DIR = _SKILLS_DIR / "references"

_TAG_PATTERN = re.compile(r"<!--\s*tag:\s*(\S+)\s*-->")
_HEADING_PATTERN = re.compile(r"^(#{1,6})\s")
_STATEMENT_SEPARATOR = re.compile(r"\n(?=\s*[\-\*\d+\.]|\|)")

_MARKDOWN_STRIP_PATTERNS = [
    (re.compile(r"<!--.*?-->", re.DOTALL), ""),
    (re.compile(r"^(#{1,6})\s", re.MULTILINE), ""),
    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),
    (re.compile(r"\*(.+?)\*"), r"\1"),
    (re.compile(r"__(.+?)__"), r"\1"),
    (re.compile(r"_(.+?)_"), r"\1"),
    (re.compile(r"~~(.+?)~~"), r"\1"),
    (re.compile(r"`{1,3}[^`]*`{1,3}"), ""),
    (re.compile(r"\[([^\]]*)\]\([^\)]*\)"), r"\1"),
    (re.compile(r"!\[[^\]]*\]\([^\)]*\)"), ""),
    (re.compile(r"^\s*[-*+]\s*"), ""),
    (re.compile(r"^\s*\[[ x]\]\s*"), ""),
    (re.compile(r"^\s*\d+\.\s*"), ""),
    (re.compile(r"\|"), " "),
    (re.compile(r">\s*"), ""),
]

MAX_WORDS_PER_STATEMENT = 25

# Global caches for optimization
_TAG_TO_FILE_CACHE: dict[str, Path] | None = None
_FILE_CONTENT_CACHE: dict[Path, str] = {}


class SkillLoaderError(Exception):
    """Base exception for skill loading errors."""


class SkillTagNotFoundError(SkillLoaderError):
    """Requested skill tag does not exist in any reference file."""


class DuplicateSkillTagError(SkillLoaderError):
    """Same tag found in multiple reference files."""


class MalformedSkillFrontmatterError(SkillLoaderError):
    """Skill reference file has missing or malformed frontmatter."""


class StatementTooLongError(SkillLoaderError):
    """A statement in an injected skill section exceeds the word limit."""


def _parse_frontmatter(text: str, file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.

    Returns a dict with at least ``name`` and ``description`` keys.
    Raises MalformedSkillFrontmatterError on parse failure.
    """
    if not text.startswith("---"):
        raise MalformedSkillFrontmatterError(
            f"Missing frontmatter in {file_path}: file does not start with '---'"
        )
    end = text.find("---", 3)
    if end == -1:
        raise MalformedSkillFrontmatterError(
            f"Unclosed frontmatter in {file_path}"
        )
    raw = text[3:end].strip()
    if not raw:
        raise MalformedSkillFrontmatterError(
            f"Empty frontmatter in {file_path}"
        )
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise MalformedSkillFrontmatterError(
            f"YAML parse error in {file_path}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise MalformedSkillFrontmatterError(
            f"Frontmatter in {file_path} is not a mapping"
        )
    if "name" not in data:
        raise MalformedSkillFrontmatterError(
            f"Frontmatter in {file_path} missing required 'name' key"
        )
    if "description" not in data:
        raise MalformedSkillFrontmatterError(
            f"Frontmatter in {file_path} missing required 'description' key"
        )
    desc = data.get("description", "")
    if not isinstance(desc, str):
        raise MalformedSkillFrontmatterError("description must be a string")
    if len(desc) > 1024:
        data["description"] = desc[:1024]
    return data


def _strip_markdown(text: str) -> str:
    """Remove markdown syntax for word counting."""
    result = text
    for pattern, replacement in _MARKDOWN_STRIP_PATTERNS:
        result = pattern.sub(replacement, result)
    return result.strip()


def _validate_statements(section_text: str, file_path: Path, tag: str) -> None:
    """Validate each statement in the extracted section is <= MAX_WORDS_PER_STATEMENT words.

    Statements are separated by line-oriented delimiters (bullets, table rows, etc.).
    """
    statements = _STATEMENT_SEPARATOR.split(section_text)
    for stmt in statements:
        stripped = _strip_markdown(stmt).strip()
        if not stripped:
            continue
        word_count = len(stripped.split())
        if word_count > MAX_WORDS_PER_STATEMENT:
            raise StatementTooLongError(
                f"Statement in {file_path} tag '{tag}' is {word_count} words "
                f"(max {MAX_WORDS_PER_STATEMENT}): "
                f"\"{stripped[:120]}{'...' if len(stripped) > 120 else ''}\""
            )


def _find_tag_in_file(file_text: str, tag: str) -> tuple[int, int] | None:
    """Return (heading_level, heading_line_index) if tag found in file text, else None."""
    lines = file_text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        match = _TAG_PATTERN.search(line)
        if match and match.group(1) == tag:
            heading_match = _HEADING_PATTERN.match(line)
            if not heading_match:
                continue
            level = len(heading_match.group(1))
            return level, i
    return None


def _extract_section(file_text: str, tag: str) -> str:
    """Extract the tagged section from a reference file's content.

    Finds the heading containing ``<!-- tag: <tag> -->``, then collects all lines
    until the next heading of the same or higher level (or EOF).
    """
    lines = file_text.splitlines(keepends=True)
    tag_line_idx = None
    heading_level = 0
    for i, line in enumerate(lines):
        match = _TAG_PATTERN.search(line)
        if match and match.group(1) == tag:
            heading_match = _HEADING_PATTERN.match(line)
            if heading_match:
                heading_level = len(heading_match.group(1))
                tag_line_idx = i
                break

    if tag_line_idx is None:
        return ""

    # Collect from tag line to next heading of same or higher level
    result_lines = [lines[tag_line_idx]]
    for j in range(tag_line_idx + 1, len(lines)):
        h_match = _HEADING_PATTERN.match(lines[j])
        if h_match and len(h_match.group(1)) <= heading_level:
            break
        result_lines.append(lines[j])

    return "".join(result_lines)


def _find_reference_file(tag: str) -> Path:
    """Resolve a tag to its reference file path.

    Tag format: ``<file_prefix>:<section>``. The file is
    ``<file_prefix>.md`` in the references directory.
    """
    if ":" not in tag:
        raise SkillTagNotFoundError(
            f"Tag '{tag}' does not follow the 'file_prefix:section' convention"
        )
    file_prefix = tag.split(":", 1)[0]
    if not re.match(r"^[a-zA-Z0-9_]+$", file_prefix):
        raise SkillTagNotFoundError(
            f"Invalid file prefix '{file_prefix}' in tag '{tag}'"
        )
    file_path = (_REFERENCES_DIR / f"{file_prefix}.md").resolve()
    # Path traversal validation
    if not str(file_path).startswith(str(_REFERENCES_DIR.resolve())):
        raise SkillTagNotFoundError(
            f"Path traversal detected in tag prefix '{file_prefix}'"
        )
    return file_path


def _collect_all_tags() -> dict[str, Path]:
    """Scan all reference files and return {tag: file_path}."""
    tags: dict[str, Path] = {}
    if not _REFERENCES_DIR.is_dir():
        return tags
    for ref_file in sorted(_REFERENCES_DIR.glob("*.md")):
        # Check size limit on scan
        if ref_file.stat().st_size > 10 * 1024 * 1024:
            continue
        if ref_file not in _FILE_CONTENT_CACHE:
            try:
                with open(ref_file) as f:
                    _FILE_CONTENT_CACHE[ref_file] = f.read()
            except IOError:
                continue
        content = _FILE_CONTENT_CACHE[ref_file]
        for line in content.splitlines():
            match = _TAG_PATTERN.search(line)
            if match:
                found_tag = match.group(1)
                if found_tag in tags:
                    raise DuplicateSkillTagError(
                        f"Duplicate tag '{found_tag}' found in "
                        f"{tags[found_tag]} and {ref_file}"
                    )
                tags[found_tag] = ref_file
    return tags


def _get_tag_to_file_map() -> dict[str, Path]:
    """Retrieve or build tag-to-file mapping with duplicate check."""
    global _TAG_TO_FILE_CACHE
    if _TAG_TO_FILE_CACHE is None:
        _TAG_TO_FILE_CACHE = _collect_all_tags()
    return _TAG_TO_FILE_CACHE


def load_skill_section(tag: str) -> str:
    """Load a tagged section from skill reference files.

    Args:
        tag: Tag in ``file_prefix:section`` format (e.g. ``entity_extraction:rules``).

    Returns:
        Extracted markdown section content (includes the tagged heading).

    Raises:
        SkillTagNotFoundError: Tag not found in any reference file.
        DuplicateSkillTagError: Tag appears in multiple reference files.
        StatementTooLongError: A statement in the section exceeds the word limit.
    """
    # Eagerly initialize/check for duplicates across the entire bundle
    all_tags = _get_tag_to_file_map()

    file_path = _find_reference_file(tag)
    if not file_path.is_file():
        raise SkillTagNotFoundError(
            f"Skill reference file not found: {file_path} (tag: '{tag}')"
        )

    # Verify file size limit (10 MB)
    if file_path.stat().st_size > 10 * 1024 * 1024:
        raise SkillLoaderError(
            f"Skill reference file {file_path} exceeds the 10 MB size limit"
        )

    # Parse frontmatter using the cache
    if file_path not in _FILE_CONTENT_CACHE:
        with open(file_path) as f:
            _FILE_CONTENT_CACHE[file_path] = f.read()
    full_text = _FILE_CONTENT_CACHE[file_path]

    _parse_frontmatter(full_text, file_path)

    # Check tag exists in the correct file
    found = _find_tag_in_file(full_text, tag)
    if found is None:
        # Also check if tag exists in a DIFFERENT file (wrong file_prefix)
        if tag in all_tags:
            actual_file = all_tags[tag]
            actual_prefix = actual_file.stem
            raise SkillTagNotFoundError(
                f"Tag '{tag}' found in '{actual_file}', not in '{file_path}'. "
                f"Use tag prefix '{actual_prefix}:' instead of "
                f"'{tag.split(':', 1)[0]}:'."
            )
        raise SkillTagNotFoundError(
            f"Tag '{tag}' not found in {file_path}"
        )

    section = _extract_section(full_text, tag)
    _validate_statements(section, file_path, tag)
    return section
