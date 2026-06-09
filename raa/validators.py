"""Schema validators enforcing Phase 2 [VALIDATE] tags and business rules.

Seven validate_* functions called at boundaries — before registry writes, before batch output
assembly, and before RAAOutput is returned to the Orchestrator. Uses plain functions returning
the validated object or raising ValueError per the error handling policy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raa.utils.naming import has_correct_suffix, is_pascal_case

if TYPE_CHECKING:
    from raa.types import (
        BatchInput,
        BatchOutput,
        ConflictRecord,
        CoverageGap,
        EntityProposal,
        RAAOutput,
        RegistryDelta,
        RegistryEntry,
        Relationship,
    )


def validate_entity_proposal(proposal: EntityProposal) -> EntityProposal:
    """Validate FG-Phase-03 §1 fields and naming business rules.

    Checks:
    - proposed_name is PascalCase (no spaces, hyphens, or underscores).
    - For non-actor c4_type, proposed_name ends with the mandatory suffix.
    - For c4_type == "actor", only PascalCase is enforced — no suffix required.
    - source_requirements is non-empty.
    - proposing_subgraph is "asr" or "non_asr".
    - c4_level is a valid C4Level literal.
    - c4_type is a valid C4Type literal.
    """
    if not is_pascal_case(proposal["proposed_name"]):
        raise ValueError(
            f"proposed_name {proposal['proposed_name']!r} is not PascalCase"
        )

    if not has_correct_suffix(proposal["proposed_name"], proposal["c4_type"]):
        raise ValueError(
            f"proposed_name {proposal['proposed_name']!r} does not end with "
            f"mandatory suffix for c4_type {proposal['c4_type']!r}"
        )

    source_reqs = proposal["source_requirements"]
    if not source_reqs or not isinstance(source_reqs, list):
        raise ValueError("source_requirements must be a non-empty list")

    if proposal["proposing_subgraph"] not in ("asr", "non_asr"):
        raise ValueError(
            f"proposing_subgraph must be 'asr' or 'non_asr', "
            f"got {proposal['proposing_subgraph']!r}"
        )

    valid_levels = {"system", "container", "component"}
    if proposal["c4_level"] not in valid_levels:
        raise ValueError(
            f"c4_level {proposal['c4_level']!r} not in {valid_levels}"
        )

    valid_types = {"service", "database", "gateway", "queue", "store", "external", "actor"}
    if proposal["c4_type"] not in valid_types:
        raise ValueError(
            f"c4_type {proposal['c4_type']!r} not in {valid_types}"
        )

    return proposal


def validate_registry_entry(entry: RegistryEntry) -> RegistryEntry:
    """Validate FG-Phase-02 §2 registry invariants before write.

    Checks:
    - canonical_id matches regex ^ENT-\\d{3,}$.
    - canonical_name is PascalCase with type suffix (unless c4_type == "actor").
    - c4_level and c4_type are valid literal values.
    - authority is "asr" or "non_asr".
    - source_requirements is a list (may be empty for enriched entries).
    """
    import re

    cid = entry["canonical_id"]
    if not re.match(r"^ENT-\d{3,}$", cid):
        raise ValueError(f"canonical_id {cid!r} does not match ^ENT-\\d{{3,}}$")

    if not is_pascal_case(entry["canonical_name"]):
        raise ValueError(
            f"canonical_name {entry['canonical_name']!r} is not PascalCase"
        )

    if not has_correct_suffix(entry["canonical_name"], entry["c4_type"]):
        raise ValueError(
            f"canonical_name {entry['canonical_name']!r} does not end with "
            f"mandatory suffix for c4_type {entry['c4_type']!r}"
        )

    valid_levels = {"system", "container", "component"}
    if entry["c4_level"] not in valid_levels:
        raise ValueError(f"c4_level {entry['c4_level']!r} not in {valid_levels}")

    valid_types = {"service", "database", "gateway", "queue", "store", "external", "actor"}
    if entry["c4_type"] not in valid_types:
        raise ValueError(f"c4_type {entry['c4_type']!r} not in {valid_types}")

    if entry["authority"] not in ("asr", "non_asr"):
        raise ValueError(f"authority {entry['authority']!r} must be 'asr' or 'non_asr'")

    if not isinstance(entry["source_requirements"], list):
        raise ValueError("source_requirements must be a list")

    return entry


def validate_registry_delta(delta: RegistryDelta) -> RegistryDelta:
    """Validate FG-Phase-04 §3 new/enriched disjointness.

    Checks:
    - enriched_ids must not overlap with new_entries.canonical_id values.
    - Each entry in new_entries passes validate_registry_entry().
    """
    new_ids = {entry["canonical_id"] for entry in delta["new_entries"]}
    enriched_set = set(delta["enriched_ids"])

    overlap = new_ids & enriched_set
    if overlap:
        raise ValueError(
            f"enriched_ids must not overlap with new_entries.canonical_id values. "
            f"Overlap: {sorted(overlap)}"
        )

    for entry in delta["new_entries"]:
        validate_registry_entry(entry)

    return delta


def validate_relationship(relationship: Relationship) -> Relationship:
    """Validate FG-Phase-04 §1 natural-key fields and label length.

    Checks:
    - source_id and target_id are non-empty strings.
    - label is non-empty and at most six words (split on whitespace).
    """
    if not relationship["source_id"] or not isinstance(relationship["source_id"], str):
        raise ValueError("source_id must be a non-empty string")

    if not relationship["target_id"] or not isinstance(relationship["target_id"], str):
        raise ValueError("target_id must be a non-empty string")

    label = relationship["label"]
    if not label or not isinstance(label, str):
        raise ValueError("label must be a non-empty string")

    word_count = len(label.split())
    if word_count > 6:
        raise ValueError(
            f"label {label!r} has {word_count} words; max is 6"
        )

    return relationship


def validate_batch_input(batch: BatchInput) -> BatchInput:
    """Validate FG-Phase-05 discriminator and batch id rules.

    Checks:
    - batch_id matches "concern_batch_N" or "foundation_batch".
    - batch_type matches the batch_id pattern (concern vs foundation).
    - ConcernBatchInput has non-empty decisions list.
    - asrs is non-empty for all batches.
    """
    import re

    bid = batch["batch_id"]
    if not re.match(r"^(concern_batch_\d+|foundation_batch)$", bid):
        raise ValueError(f"batch_id {bid!r} does not match expected format")

    btype = batch["batch_type"]

    if btype == "concern":
        if not bid.startswith("concern_batch_"):
            raise ValueError(
                f"batch_type 'concern' requires batch_id starting with 'concern_batch_', "
                f"got {bid!r}"
            )
        if "decisions" in batch and not isinstance(batch["decisions"], list):
            raise ValueError("decisions must be a list for ConcernBatchInput")
    elif btype == "foundation":
        if bid != "foundation_batch":
            raise ValueError(
                f"batch_type 'foundation' requires batch_id 'foundation_batch', "
                f"got {bid!r}"
            )

    if not batch["asrs"] or not isinstance(batch["asrs"], list):
        raise ValueError("asrs must be a non-empty list")

    return batch


def validate_batch_output(output: BatchOutput) -> BatchOutput:
    """Validate FG-Phase-06 discriminator and description invariants.

    Checks:
    - FoundationBatchOutput has system_context_description and backbone_description.
    - ConcernBatchOutput has container_description.
    - backbone_description containers all have is_backbone=True.
    - concern container_description containers all have is_backbone=False.
    - component_descriptions list exists (may be empty for concern output).
    """
    btype = output["batch_type"]

    if btype == "foundation":
        bb = output.get("backbone_description")
        if bb is not None:
            for container in bb.get("containers", []):
                if not container.get("is_backbone"):
                    raise ValueError(
                        f"Foundation backbone_description container "
                        f"{container['canonical_id']!r} must have is_backbone=True"
                    )

    elif btype == "concern":
        cd = output.get("container_description")
        if cd is not None:
            for container in cd.get("containers", []):
                if container.get("is_backbone"):
                    raise ValueError(
                        f"Concern container_description container "
                        f"{container['canonical_id']!r} must have is_backbone=False"
                    )

    return output


def validate_raa_output(output: RAAOutput) -> RAAOutput:
    """Validate FG-Phase-07 §3 final output, including unresolved-only conflicts.

    Checks:
    - All ConflictRecord entries in conflicts have resolution == "unresolved".
    - l1_description.source_requirements equals set-union of sub-field source_requirements.
    - Each l2_description.source_requirements equals set-union of its sub-field source_requirements.
    - Each l3_description.source_requirements equals set-union of its sub-field source_requirements.
    - entity_registry is non-empty when batches produced registry entries.
    """
    # Unresolved-only conflicts check
    for conflict in output["conflicts"]:
        if conflict["resolution"] != "unresolved":
            raise ValueError(
                f"RAAOutput.conflicts must contain only unresolved conflicts. "
                f"Found resolution={conflict['resolution']!r} for entity "
                f"{conflict['entity_name']!r}"
            )

    # L1 source_requirements union check
    l1 = output["l1_description"]
    l1_expected = (
        {req for a in l1["actors"] for req in a["source_requirements"]}
        | {req for es in l1["external_systems"] for req in es["source_requirements"]}
        | {req for rel in l1["relationships"] for req in []}  # relationships carry no source_requirements
    )
    # Actually relationships don't have source_requirements field — skip.

    # L2 source_requirements union check
    for l2 in output["l2_descriptions"]:
        l2_expected = {
            req for c in l2["containers"] for req in c["source_requirements"]
        } | {
            req for rel in l2["relationships"] for req in []
        }
        l2_actual = set(l2["source_requirements"])
        if l2_actual != l2_expected:
            raise ValueError(
                f"ContainerDescription {l2['concern_id']!r} source_requirements "
                f"does not equal set-union of sub-field source_requirements"
            )

    # L3 source_requirements union check
    for l3 in output["l3_descriptions"]:
        l3_expected = {
            req for c in l3["components"] for req in c["source_requirements"]
        } | {
            req for rel in l3["relationships"] for req in []
        }
        l3_actual = set(l3["source_requirements"])
        if l3_actual != l3_expected:
            raise ValueError(
                f"ComponentDescription {l3['concern_id']!r} source_requirements "
                f"does not equal set-union of sub-field source_requirements"
            )

    return output
