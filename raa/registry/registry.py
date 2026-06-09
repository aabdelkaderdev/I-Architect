"""Global Entity Registry — the single source of truth for what entities have been defined.

Wraps dict[str, RegistryEntry] keyed by canonical_id. Shared across all batch executions.
Subgraphs have read-only access via snapshot(). The Judge is the sole writer.

Access rules:
- Subgraphs: read-only. They propose entities but never write to the registry.
- Judge: sole writer. After resolving a batch, attempts to register each surviving entity.
- Cross-batch reads: each batch receives a frozen snapshot before it begins.
"""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raa.types import RegistryEntry, RegistrySnapshot


class EntityRegistry:
    """Append-enrichable data structure persisting across all batch executions.

    Registration rules:
    1. Name match found → enrich existing entry. Append source_requirements, merge variants.
       Never overwrite canonical_name or authority.
    2. No name match → register new entry. Authority set to proposing subgraph.
    3. Authority conflict → Judge resolves via SAAM Step 5 before registration.
       ASR-sourced wins authority; non-ASR details merged into source_requirements and variants only.
    """

    def __init__(self) -> None:
        """Initialise an empty registry with no entries and last_batch_id = 'none'."""
        self._entries: dict[str, RegistryEntry] = {}
        self._last_batch_id: str = "none"
        # Name index for O(1) name lookups
        self._name_index: dict[str, str] = {}
        # Counter for ENT-NNN ID assignment
        self._counter: int = 0

    def snapshot(self) -> RegistrySnapshot:
        """Pre: Registry may be empty (first batch).

        Post: Returns a RegistrySnapshot with entries as a deepcopy of the live dict
              and snapshot_after_batch set to the last batch_id written.

        Side effects: None (read-only). deepcopy ensures subgraph mutations to the
        snapshot do not affect the live registry.
        """
        return {
            "entries": deepcopy(self._entries),
            "snapshot_after_batch": self._last_batch_id,
        }

    def register(self, entry: RegistryEntry) -> None:
        """Pre:
            - entry.canonical_id is a new ENT-NNN not present in the registry.
            - entry.canonical_name, c4_level, c4_type, authority, description are set.

        Post:
            - Entry inserted into the live dict keyed by canonical_id.

        Side effects:
            - Mutates the live registry.

        Errors:
            - Raises ValueError if canonical_id already exists (duplicate ENT-NNN check).
            - Write access is Judge-only by convention.
        """
        cid = entry["canonical_id"]
        if cid in self._entries:
            raise ValueError(f"Duplicate canonical_id: {cid}")

        self._entries[cid] = entry
        self._name_index[entry["canonical_name"]] = cid

    def enrich(self, canonical_id: str, updates: RegistryEntry) -> None:
        """Pre: canonical_id exists in the registry.

        Post:
            - source_requirements appended (append_unique merge strategy).
            - variants merged by batch_id key (merge_by_key merge strategy).
            - description is never overwritten — Phase 1 §7.4 Rule 1.

        Side effects: Mutates the live registry entry in place.

        Errors: Raises ValueError if caller attempts to change canonical_name or authority.
        """
        if canonical_id not in self._entries:
            raise ValueError(f"Entity not found: {canonical_id}")

        existing = self._entries[canonical_id]

        # Reject immutable field changes
        if updates["canonical_name"] != existing["canonical_name"]:
            raise ValueError(
                f"Cannot change canonical_name from {existing['canonical_name']!r} "
                f"to {updates['canonical_name']!r} — field is immutable"
            )
        if updates["authority"] != existing["authority"]:
            raise ValueError(
                f"Cannot change authority from {existing['authority']!r} "
                f"to {updates['authority']!r} — field is immutable"
            )

        # append_unique source_requirements
        existing_reqs = set(existing["source_requirements"])
        for req_id in updates.get("source_requirements", []):
            if req_id not in existing_reqs:
                existing["source_requirements"].append(req_id)
                existing_reqs.add(req_id)

        # merge_by_key variants
        for batch_id, variant in updates.get("variants", {}).items():
            existing["variants"][batch_id] = variant

    def lookup(
        self,
        canonical_id: str | None = None,
        canonical_name: str | None = None,
    ) -> RegistryEntry | None:
        """Pre: At least one lookup key is supplied.

        Post: Returns the matching RegistryEntry, or None.
            - canonical_id lookup is preferred (O(1) dict access) when both keys are supplied.
            - canonical_name lookup uses exact string equality only (O(1) via name index).
              No fuzzy matching — naming is enforced by LLM prompts and output parsers.
        Side effects: None.
        """
        if canonical_id is not None:
            return self._entries.get(canonical_id)

        if canonical_name is not None:
            cid = self._name_index.get(canonical_name)
            if cid is not None:
                return self._entries.get(cid)
            return None

        return None

    def _next_id(self) -> str:
        """Generate the next ENT-NNN canonical_id."""
        self._counter += 1
        return f"ENT-{self._counter:03d}"

    def set_last_batch_id(self, batch_id: str) -> None:
        """Record the batch_id of the last batch that wrote to this registry."""
        self._last_batch_id = batch_id

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, canonical_id: str) -> bool:
        return canonical_id in self._entries
