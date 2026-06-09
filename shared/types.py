from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

C4Level = Literal["system", "container", "component"]

C4Type = Literal[
    "service", "database", "gateway", "queue", "store", "external", "actor"
]


class ConcernDefinition(TypedDict):
    concern_id: str
    # [MERGE: never]
    # Format: "CCG-NNN" (zero-padded). Assigned by the Concern Clustering Graph (CCG).

    nominal_condition: str
    # [MERGE: overwrite]
    # The condition under which this concern is operational.
    # Example: "when traffic exceeds 10,000 concurrent users".


class EntityProposal(TypedDict):
    """Ephemeral subgraph output emitted by ASR and Non-ASR subgraphs. Never persisted directly."""

    proposed_name: str
    # PascalCase name with mandatory type suffix (Phase 1 §7.5), pre-validated by the output parser.
    # Becomes canonical_name in the registry if accepted; discarded entirely if rejected.
    # [VALIDATE] PascalCase + type suffix (unless c4_type == "actor").

    c4_level: C4Level

    c4_type: C4Type

    description: str
    # One-to-two sentence description. Becomes the initial canonical description if accepted.
    # [VALIDATE] 1-2 sentences.

    responsibilities: list[str]
    # Ordered list of what this entity does within its C4 scope.
    # Used by the Judge in SAAM Step 5 to identify load-bearing entities.

    source_requirements: list[str]
    # IDs of requirements in this batch justifying the proposal.
    # [VALIDATE] Must be non-empty. Output parser rejects empty lists (Phase 1 §5).

    proposing_subgraph: Literal["asr", "non_asr"]
    # Maps directly to authority in the registry upon acceptance.
    # In an authority conflict, asr wins; non_asr source_requirements are merged only (Phase 1 §7.4 Rule 3).

    concern_technology: NotRequired[str]
    # Technology scoped to this batch's concern; stored as a variant keyed by batch_id on acceptance.
    # Omitted for actors and technology-agnostic entities.

    justification: str
    # Subgraph's reasoning evaluated by the Judge during SAAM. Not persisted; discarded after evaluation.


class JudgedProposal(TypedDict):
    """Judge's internal working state during SAAM. Never emitted externally; discarded after the batch completes."""

    proposal: EntityProposal
    # The original subgraph proposal, unmodified.

    scenario_classification: Literal["direct", "indirect"]
    # SAAM Step 3. Assigned exclusively by the Judge.
    # direct   → entity is explicitly named or described in a source requirement.
    # indirect → entity is implied by a quality attribute or architectural pattern.

    satisfied_requirements: list[str]
    # Requirement IDs this proposal satisfies (SAAM Step 4).

    conflicts_with: list[str]
    # proposed_names of proposals conflicting with this one (SAAM Step 5).
    # Includes authority conflicts; resolved per Phase 1 §7.4 Rule 3 before registration.
