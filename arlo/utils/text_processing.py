"""
Text processing utilities for the ARLO pipeline.

Handles requirement truncation and batching for LLM calls.
"""
from __future__ import annotations


def truncate_description(description: str, max_length: int = 500) -> str:
    """Truncate a requirement description to max_length characters."""
    return description[:max_length]


def batch_requirements(
    requirements: dict[str, str],
    batch_size: int = 10,
) -> list[list[dict[str, str]]]:
    """Split a requirements dict into batches of dicts with 'id' and 'description'.

    Args:
        requirements: Mapping of Requirement ID → description text.
        batch_size: Number of requirements per batch.

    Returns:
        List of batches, where each batch is a list of
        {"id": req_id, "description": truncated_text} dicts.
    """
    items = [
        {"id": req_id, "description": truncate_description(desc)}
        for req_id, desc in requirements.items()
    ]
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]
