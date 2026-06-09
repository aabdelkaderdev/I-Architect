"""RegistryDelta construction and non-overlap validation. FG-Phase-04 §3."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raa.types import RegistryDelta, RegistryEntry


def build_delta(
    new_entries: list[RegistryEntry],
    enriched_ids: list[str],
) -> RegistryDelta:
    """Construct a RegistryDelta from new entries and enriched canonical_ids.

    Pre:
        - enriched_ids must not overlap with new_entries.canonical_id values.
        - Each entry in new_entries passes validate_registry_entry().

    Post: Returns a validated RegistryDelta.

    Errors: Raises ValueError if enriched_ids overlaps with new entry IDs.
    """
    new_ids = {entry["canonical_id"] for entry in new_entries}
    enriched_set = set(enriched_ids)

    overlap = new_ids & enriched_set
    if overlap:
        raise ValueError(
            f"RegistryDelta invariant violation: enriched_ids must not overlap "
            f"with new_entries.canonical_id values. Overlap: {sorted(overlap)}"
        )

    return {
        "new_entries": list(new_entries),
        "enriched_ids": list(enriched_ids),
    }
