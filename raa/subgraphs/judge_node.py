"""Judge node — sole decision-maker and sole writer to the Global Entity Registry.

Receives proposals from both subgraphs and the current registry snapshot, then
executes five SAAM steps (Phase 1 §8.4). Steps 1 and 2 are deterministic data
transformations — no LLM call required. Steps 3-5 use the Judge LLM with separate
structured output bindings per step (FG-Phase-20 §3.2).

LLM resolved from config["configurable"]["judge_llm"] per FG-Phase-10 §3.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from raa.registry.delta import build_delta
from raa.registry.registry import EntityRegistry
from raa.validators import (
    validate_entity_proposal,
    validate_registry_entry,
    validate_registry_delta,
)

if TYPE_CHECKING:
    from langgraph.types import RunnableConfig

    from raa.types import (
        ASREntry,
        BatchInput,
        BatchOutput,
        ConflictRecord,
        CoverageGap,
        EntityProposal,
        JudgedProposal,
        NonASREntry,
        RegistryDelta,
        RegistryEntry,
        RegistrySnapshot,
        Relationship,
    )

logger = logging.getLogger(__name__)

JUDGE_SYSTEM_TEMPLATE = "judge_system.md"
JUDGE_USER_TEMPLATE = "judge_user.md"
_L2_EXCLUDED_TYPES = {"actor", "external"}

_JUDGE_COUNTER: int = 0


def _next_ent_id() -> str:
    """Generate the next ENT-NNN canonical_id."""
    global _JUDGE_COUNTER
    _JUDGE_COUNTER += 1
    return f"ENT-{_JUDGE_COUNTER:03d}"


def _variant_for_proposal(batch_id: str, proposal: EntityProposal) -> dict:
    """Build a registry variant while omitting absent optional fields."""
    variant = {}
    technology = proposal.get("concern_technology")
    if technology:
        variant["technology"] = technology
    description_note = proposal.get("justification")
    if description_note:
        variant["description_note"] = description_note
    return {batch_id: variant} if variant else {}


def _default_classification(proposals: list[EntityProposal]) -> list[JudgedProposal]:
    """Deterministic fallback: classify every proposal as direct."""
    return [
        {
            "proposal": proposal,
            "scenario_classification": "direct",
            "satisfied_requirements": list(proposal["source_requirements"]),
            "conflicts_with": [],
        }
        for proposal in proposals
    ]


def _proposal_ref(index: int) -> str:
    """Return the stable Judge prompt reference for a proposal position."""
    return f"P{index + 1:03d}"


def _judgment_ref(judgment: dict) -> str:
    return str(judgment.get("proposal_ref", ""))


def _judgment_name(judgment: dict) -> str:
    name = str(judgment.get("proposed_name", ""))
    if name:
        return name

    proposal = judgment.get("proposal", {})
    if isinstance(proposal, dict):
        return str(proposal.get("proposed_name", ""))
    return ""


def _matched_raw_judgment(
    raw_judged: list[dict],
    proposal: EntityProposal,
    fallback_index: int,
    used_indices: set[int],
) -> dict:
    """Find the Judge annotation for a trusted proposal without trusting its copy."""
    expected_ref = _proposal_ref(fallback_index)
    for idx, raw in enumerate(raw_judged):
        if idx in used_indices:
            continue
        if _judgment_ref(raw) == expected_ref:
            used_indices.add(idx)
            return raw

    name = proposal["proposed_name"]
    for idx, raw in enumerate(raw_judged):
        if idx in used_indices:
            continue
        if _judgment_name(raw) == name:
            used_indices.add(idx)
            return raw

    if fallback_index < len(raw_judged) and fallback_index not in used_indices:
        used_indices.add(fallback_index)
        return raw_judged[fallback_index]

    return {}


def _reattach_judgment_annotations(
    base_judged: list[JudgedProposal],
    raw_judged: list[dict],
    *,
    update_classification: bool = False,
    update_satisfied: bool = False,
    update_conflicts: bool = False,
) -> list[JudgedProposal]:
    """Merge Judge annotations onto trusted proposal objects.

    The Judge LLM may omit or corrupt immutable proposal fields such as
    proposing_subgraph. Those fields always come from base_judged.
    """
    sanitized: list[JudgedProposal] = []
    used_indices: set[int] = set()

    for idx, base in enumerate(base_judged):
        raw = _matched_raw_judgment(raw_judged, base["proposal"], idx, used_indices)
        sanitized_entry: JudgedProposal = {
            "proposal": base["proposal"],
            "scenario_classification": base.get("scenario_classification", "direct"),
            "satisfied_requirements": list(base.get("satisfied_requirements", [])),
            "conflicts_with": list(base.get("conflicts_with", [])),
        }

        if update_classification:
            classification = raw.get("scenario_classification")
            if classification in ("direct", "indirect"):
                sanitized_entry["scenario_classification"] = classification

        if update_satisfied:
            reqs = raw.get("satisfied_requirements", [])
            sanitized_entry["satisfied_requirements"] = [str(req) for req in reqs]

        if update_conflicts:
            conflicts = raw.get("conflicts_with", [])
            sanitized_entry["conflicts_with"] = [str(name) for name in conflicts]

        sanitized.append(sanitized_entry)

    return sanitized


class Judge:
    """Executes five SAAM steps to evaluate proposals, resolve conflicts, and write registry entries.

    Steps 1 & 2 are deterministic — no LLM required. Steps 3-5 use the Judge LLM
    with separate structured output bindings per step (FG-Phase-20 §3.2).
    """

    def __init__(self, registry: EntityRegistry | None = None):
        self._registry = registry or EntityRegistry()

    # ── SAAM Step 1 — Scenario Development ──

    def develop_scenarios(
        self,
        batch: BatchInput,
    ) -> list[ASREntry | NonASREntry]:
        """Pre:
            - batch.asrs and batch.non_asrs contain all requirements in scope.

        Post:
            - Returns a single ordered scenario list containing every batch requirement.
            - No requirement text is modified.

        Side effects: None.
        """
        scenarios: list[ASREntry | NonASREntry] = []
        scenarios.extend(batch.get("asrs", []))
        scenarios.extend(batch.get("non_asrs", []))
        return scenarios

    # ── SAAM Step 2 — Architecture Description ──

    def describe_architecture(
        self,
        asr_proposals: list[EntityProposal],
        non_asr_proposals: list[EntityProposal],
    ) -> list[EntityProposal]:
        """Pre:
            - Inputs are validated proposal lists from the ASR and Non-ASR subgraphs.

        Post:
            - Returns the candidate architecture as ASR proposals followed by Non-ASR
              proposals, preserving provenance in proposing_subgraph.

        Side effects: None.
        """
        return list(asr_proposals) + list(non_asr_proposals)

    # ── SAAM Step 3 — Scenario Classification ──

    async def classify_scenarios(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        config: RunnableConfig,
    ) -> list[JudgedProposal]:
        """Pre:
            - `proposals` is the candidate architecture from describe_architecture().
            - config["configurable"]["judge_llm"] exists per FG-Phase-10 §1.

        Post:
            - Returns one JudgedProposal per proposal.
            - scenario_classification is "direct" when the entity is explicitly named
              or described in a source requirement's text.
            - scenario_classification is "indirect" when implied by a quality attribute
              or pattern but not explicitly stated in any requirement.

        Side effects:
            - Calls the Judge LLM. LLM is bound to a structured output model.
            - Does not write to the registry.
        """
        if not proposals:
            return []

        classification_input_count = len(proposals)
        result = await self._judge_llm_step(
            batch=batch,
            proposals=proposals,
            config=config,
            step_name="Step 3 — classification",
            output_field="classified",
        )
        raw_classified: list[dict] = []
        if isinstance(result, dict):
            raw_classified = result.get("classified", [])
        elif isinstance(result, list):
            raw_classified = result

        if classification_input_count > 0 and not raw_classified:
            logger.warning(
                "Judge classification returned empty output for %d proposals; "
                "using deterministic fallback.",
                classification_input_count,
            )
            return _default_classification(proposals)
        return _reattach_judgment_annotations(
            _default_classification(proposals),
            raw_classified,
            update_classification=True,
        )

    # ── SAAM Step 4 — Individual Scenario Evaluation ──

    def _coverage_failure_gaps(self, batch: BatchInput) -> list[CoverageGap]:
        """Return visible gaps when Judge coverage evaluation did not run."""
        return [
            {
                "requirement_id": r.get("id", ""),
                "requirement_text": r.get("text", ""),
                "batch_id": batch["batch_id"],
                "gap_reason": (
                    "Coverage evaluation failed; requirement coverage is unverified."
                ),
            }
            for r in list(batch.get("asrs", [])) + list(batch.get("non_asrs", []))
        ]

    async def evaluate_coverage(
        self,
        batch: BatchInput,
        judged: list[JudgedProposal],
        config: RunnableConfig,
    ) -> tuple[list[JudgedProposal], list[CoverageGap]]:
        """Pre:
            - `judged` contains classified proposals from Step 3.

        Post:
            - Returns updated judged proposals with satisfied_requirements populated.
            - Returns one CoverageGap for each requirement with no satisfying proposal.
            - Coverage evaluation is semantic, not keyword-only.

        Side effects:
            - Calls the Judge LLM with separate structured output binding from Step 3.
            - Does not write to the registry.
        """
        if not judged:
            gaps = [
                {
                    "requirement_id": r.get("id", ""),
                    "requirement_text": r.get("text", ""),
                    "batch_id": batch["batch_id"],
                    "gap_reason": (
                        "No proposals were submitted by either the ASR or Non-ASR "
                        "subgraph for this batch."
                    ),
                }
                for r in list(batch.get("asrs", [])) + list(batch.get("non_asrs", []))
            ]
            return ([], gaps)

        result = await self._judge_llm_step(
            batch=batch,
            proposals=[jp["proposal"] for jp in judged],
            config=config,
            step_name="Step 4 — coverage",
            output_field="coverage",
        )

        # The LLM returns a dict with judgments and gaps
        coverage_input_count = len(judged)
        coverage_evaluated = False
        if isinstance(result, dict):
            raw_judged = result.get("judged", [])
            if coverage_input_count > 0 and not raw_judged:
                logger.warning(
                    "Judge coverage returned empty judged for %d proposals; "
                    "preserving previous judged and marking coverage unverified.",
                    coverage_input_count,
                )
                updated_judged = judged
            else:
                coverage_evaluated = True
                updated_judged = _reattach_judgment_annotations(
                    judged,
                    raw_judged,
                    update_satisfied=True,
                )
            gaps = result.get("coverage_gaps", [])
            for gap in gaps:
                gap["batch_id"] = batch["batch_id"]
            if not coverage_evaluated:
                gaps = self._coverage_failure_gaps(batch)
            return (updated_judged, gaps)

        return (judged, self._coverage_failure_gaps(batch))

    # ── SAAM Step 5 — Scenario Interaction ──

    async def detect_interactions(
        self,
        batch: BatchInput,
        judged: list[JudgedProposal],
        config: RunnableConfig,
    ) -> tuple[list[JudgedProposal], list[ConflictRecord]]:
        """Pre:
            - `judged` contains coverage annotations from Step 4.

        Post:
            - Returns judged proposals with conflicts_with populated.
            - Returns ConflictRecord entries for authority conflicts and genuine conflicts.
            - Authority conflicts resolved per Phase 1 §7.4 Rule 3: ASR authority wins.
            - Entities referenced by 3+ compatible requirements are load-bearing.

        Side effects:
            - Calls the Judge LLM with separate structured output binding.
            - Does not write to the registry.
        """
        if not judged:
            return ([], [])

        result = await self._judge_llm_step(
            batch=batch,
            proposals=[jp["proposal"] for jp in judged],
            config=config,
            step_name="Step 5 — interaction",
            output_field="interactions",
        )

        interaction_input_count = len(judged)
        if isinstance(result, dict):
            raw_judged = result.get("judged", [])
            if interaction_input_count > 0 and not raw_judged:
                logger.warning(
                    "Judge interaction returned empty judged for %d proposals; "
                    "preserving previous judged.",
                    interaction_input_count,
                )
                updated_judged = judged
            else:
                updated_judged = _reattach_judgment_annotations(
                    judged,
                    raw_judged,
                    update_conflicts=True,
                )
            conflicts = result.get("conflicts", [])
            return (updated_judged, conflicts)

        return (judged, [])

    # ── FG-Phase-31: Post-SAAM Methods ──

    def deduplicate(
        self,
        judged: list[JudgedProposal],
        conflicts: list[ConflictRecord],
    ) -> list[EntityProposal]:
        """Pre:
            - SAAM Steps 3-5 have completed.
            - Naming validators (FG-Phase-14) have enforced Phase 1 §7.5.

        Post:
            - Returns surviving proposals deduplicated by exact proposed_name
              (string equality, no fuzzy matching — Phase 1 §11).
            - Compatible duplicates merge source_requirements with append_unique
              semantics (FG-Phase-01 §2).
            - ASR proposals survive same-name authority conflicts (Phase 1 §7.4 Rule 3).

        Side effects: None.
        """
        # Build set of entity names in unresolved conflicts for logging
        unresolved_names: set[str] = set()
        for c in conflicts:
            if c.get("resolution") == "unresolved":
                unresolved_names.add(c.get("entity_name", ""))

        seen: dict[str, EntityProposal] = {}
        for jp in judged:
            name = jp["proposal"]["proposed_name"]

            if name in seen:
                existing = seen[name]

                # Authority conflict: ASR wins (Phase 1 §7.4 Rule 3)
                if (jp["proposal"]["proposing_subgraph"] == "asr"
                        and existing["proposing_subgraph"] == "non_asr"):
                    # Replace non-ASR with ASR, merge source_requirements
                    asr_proposal = jp["proposal"]
                    for req_id in existing["source_requirements"]:
                        if req_id not in asr_proposal["source_requirements"]:
                            asr_proposal["source_requirements"].append(req_id)
                    seen[name] = asr_proposal
                else:
                    # Merge source_requirements (append_unique)
                    for req_id in jp["proposal"]["source_requirements"]:
                        if req_id not in existing["source_requirements"]:
                            existing["source_requirements"].append(req_id)

                if name in unresolved_names:
                    logger.info(
                        "Entity %r has unresolved conflicts; registered with conflict note.",
                        name,
                    )
            else:
                seen[name] = jp["proposal"]

        return list(seen.values())

    def derive_relationships(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        registry_snapshot: RegistrySnapshot,
    ) -> list[Relationship]:
        """Pre:
            - `proposals` are deduplicated surviving entities from deduplicate().
            - Registry lookups can resolve known canonical IDs by exact name match.

        Post:
            - Returns diagram relationships with natural key
              (source_id, target_id, label) per FG-Phase-04 §1.
            - Relationships only reference entities that will exist in the registry
              after registration/enrichment — both endpoints are guaranteed.

        Side effects: None.
        """
        # Build a lookup: proposed_name → canonical_id (new or existing)
        name_to_id: dict[str, str] = {}
        for proposal in proposals:
            name = proposal["proposed_name"]
            existing = self._registry.lookup(canonical_name=name)
            if existing is not None:
                name_to_id[name] = existing["canonical_id"]
            else:
                # New entity — assign a predictable id
                name_to_id[name] = _next_ent_id()

        relationships: list[Relationship] = []

        def make_relationship(
            source: EntityProposal,
            target: EntityProposal,
            label: str,
            description_verb: str,
        ) -> Relationship:
            return {
                "source_id": name_to_id[source["proposed_name"]],
                "target_id": name_to_id[target["proposed_name"]],
                "label": label,
                "description": (
                    f"{source['proposed_name']} {description_verb} "
                    f"{target['proposed_name']}."
                ),
            }

        # Derive system-level relationships for L1: actor → system, system → external
        actors = [p for p in proposals if p["c4_type"] == "actor"]
        externals = [p for p in proposals if p["c4_type"] == "external"]
        internal = [p for p in proposals if p["c4_type"] not in ("actor", "external")]

        for actor in actors:
            for svc in internal:
                relationships.append(
                    make_relationship(actor, svc, "uses", "interacts with")
                )

        for svc in internal:
            for ext in externals:
                relationships.append(
                    make_relationship(svc, ext, "calls", "integrates with")
                )

        databases = [p for p in proposals if p["c4_type"] == "database"]
        queues = [p for p in proposals if p["c4_type"] == "queue"]
        services = [p for p in proposals if p["c4_type"] == "service"]
        gateways = [p for p in proposals if p["c4_type"] == "gateway"]

        for svc in services:
            for db in databases:
                relationships.append(
                    make_relationship(svc, db, "persists to", "persists data to")
                )
            for queue in queues:
                relationships.append(
                    make_relationship(svc, queue, "publishes to", "publishes messages to")
                )

        for gateway in gateways:
            for svc in services:
                relationships.append(
                    make_relationship(gateway, svc, "routes to", "routes traffic to")
                )

        return relationships

    def assemble_descriptions(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        relationships: list[Relationship],
        registry_delta: RegistryDelta,
        coverage_gaps: list[CoverageGap],
        conflicts: list[ConflictRecord],
    ) -> BatchOutput:
        """Pre:
            - Registry writes for `proposals` have completed via EntityRegistry.
            - registry_delta records all new and enriched entries for this batch.

        Post:
            - Returns ConcernBatchOutput for concern batches with L2/L3 descriptions.
            - Returns FoundationBatchOutput for the Foundation batch with L1/L2 descriptions.
            - Both output types include batch_id, registry_delta, coverage_gaps, and conflicts.

        Side effects: None. The registry write is complete before this method runs.
        """
        if batch["batch_type"] == "foundation":
            return self._assemble_foundation_output(
                batch, proposals, relationships, registry_delta, coverage_gaps, conflicts
            )
        else:
            return self._assemble_concern_output(
                batch, proposals, relationships, registry_delta, coverage_gaps, conflicts
            )

    def _assemble_concern_output(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        relationships: list[Relationship],
        registry_delta: RegistryDelta,
        coverage_gaps: list[CoverageGap],
        conflicts: list[ConflictRecord],
    ) -> BatchOutput:
        """Build ConcernBatchOutput with L2 container description and L3 component descriptions."""
        from raa.types import ComponentEntry, ContainerEntry

        # Filter to non-actor, non-external entities for L2 containers
        containers: list[ContainerEntry] = []
        components: list[ComponentEntry] = []
        component_descriptions = []

        for proposal in proposals:
            if proposal["c4_type"] in _L2_EXCLUDED_TYPES:
                continue

            name = proposal["proposed_name"]
            existing = self._registry.lookup(canonical_name=name)
            cid = existing["canonical_id"] if existing else ""

            if proposal["c4_level"] == "container":
                container = {
                    "canonical_id": cid,
                    "name": name,
                    "description": proposal["description"],
                    "responsibilities": proposal["responsibilities"],
                    "is_backbone": False,
                    "source_requirements": proposal["source_requirements"],
                }
                technology = proposal.get("concern_technology")
                if technology:
                    container["technology"] = technology
                containers.append(container)

            elif proposal["c4_level"] == "component":
                component = {
                    "canonical_id": cid,
                    "name": name,
                    "description": proposal["description"],
                    "responsibilities": proposal["responsibilities"],
                    "interfaces": [],
                    "source_requirements": proposal["source_requirements"],
                }
                technology = proposal.get("concern_technology")
                if technology:
                    component["technology"] = technology
                components.append(component)

        # Build L2 source_requirements union from L2 containers only.
        container_src_reqs = sorted(set(
            req_id
            for c in containers
            for req_id in c["source_requirements"]
        ))

        container_description = {
            "concern_id": batch["batch_id"],
            "condition": batch.get("condition", ""),
            "containers": containers,
            "relationships": relationships,
            "source_requirements": container_src_reqs,
        }

        valid_parent_containers = [c for c in containers if c.get("canonical_id")]
        if components and valid_parent_containers:
            # Group components by best source-requirement overlap with a real parent.
            container_groups: dict[str, list[ComponentEntry]] = {}
            for component in components:
                comp_reqs = set(component.get("source_requirements", []))
                best_container = valid_parent_containers[0]
                best_overlap = -1
                for container in valid_parent_containers:
                    container_reqs = set(container.get("source_requirements", []))
                    overlap = len(comp_reqs & container_reqs)
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_container = container
                parent_id = best_container["canonical_id"]
                container_groups.setdefault(parent_id, []).append(component)

            component_descriptions = []
            for parent_id, grouped_components in container_groups.items():
                component_ids = {
                    component["canonical_id"]
                    for component in grouped_components
                    if component.get("canonical_id")
                }
                related_ids = {parent_id} | component_ids
                scoped_relationships = [
                    relationship for relationship in relationships
                    if (
                        relationship.get("source_id") in related_ids
                        or relationship.get("target_id") in related_ids
                    )
                ]
                component_src_reqs = sorted({
                    req_id
                    for component in grouped_components
                    for req_id in component.get("source_requirements", [])
                })
                component_descriptions.append({
                    "parent_container_id": parent_id,
                    "concern_id": batch["batch_id"],
                    "components": grouped_components,
                    "relationships": scoped_relationships,
                    "source_requirements": component_src_reqs,
                })

        output: BatchOutput = {
            "batch_id": batch["batch_id"],
            "batch_type": "concern",
            "registry_delta": registry_delta,
            "coverage_gaps": coverage_gaps,
            "conflicts": conflicts,
            "container_description": container_description,
            "component_descriptions": component_descriptions,
        }
        return output

    def _assemble_foundation_output(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        relationships: list[Relationship],
        registry_delta: RegistryDelta,
        coverage_gaps: list[CoverageGap],
        conflicts: list[ConflictRecord],
    ) -> BatchOutput:
        """Build FoundationBatchOutput with L1 system context and L2 backbone."""
        from raa.types import ActorEntry, ContainerEntry, ExternalSystemEntry

        actors: list[ActorEntry] = []
        externals: list[ExternalSystemEntry] = []
        containers: list[ContainerEntry] = []

        for proposal in proposals:
            name = proposal["proposed_name"]
            existing = self._registry.lookup(canonical_name=name)
            cid = existing["canonical_id"] if existing else ""

            if proposal["c4_type"] == "actor":
                actors.append({
                    "canonical_id": cid,
                    "name": name,
                    "description": proposal["description"],
                    "source_requirements": proposal["source_requirements"],
                })
            elif proposal["c4_type"] == "external":
                externals.append({
                    "canonical_id": cid,
                    "name": name,
                    "description": proposal["description"],
                    "source_requirements": proposal["source_requirements"],
                })
            else:
                container = {
                    "canonical_id": cid,
                    "name": name,
                    "description": proposal["description"],
                    "responsibilities": proposal["responsibilities"],
                    "is_backbone": True,
                    "source_requirements": proposal["source_requirements"],
                }
                technology = proposal.get("concern_technology")
                if technology:
                    container["technology"] = technology
                containers.append(container)

        all_src_reqs = sorted(set(
            req_id for a in actors for req_id in a["source_requirements"]
        ) | set(
            req_id for es in externals for req_id in es["source_requirements"]
        ) | set(
            req_id for c in containers for req_id in c["source_requirements"]
        ))

        system_context = {
            "system_name": "System",
            "system_description": "System derived from requirements corpus.",
            "system_boundary_description": "Boundary between system-owned responsibilities and external integrations.",
            "actors": actors,
            "external_systems": externals,
            "relationships": relationships,
            "source_requirements": all_src_reqs,
        }

        backbone = {
            "concern_id": "foundation",
            "condition": "under any circumstances",
            "containers": containers,
            "relationships": relationships,
            "source_requirements": all_src_reqs,
        }

        output: BatchOutput = {
            "batch_id": batch["batch_id"],
            "batch_type": "foundation",
            "registry_delta": registry_delta,
            "coverage_gaps": coverage_gaps,
            "conflicts": conflicts,
            "system_context_description": system_context,
            "backbone_description": backbone,
        }
        return output

    def resolve_and_register(
        self,
        batch: BatchInput,
        judged_proposals: list[JudgedProposal],
        conflicts: list[ConflictRecord],
    ) -> RegistryDelta:
        """Post-SAAM: deduplicate, determine new vs enrich, write to registry.

        Uses deduplicate() internally. Writes surviving entities to the live
        EntityRegistry per FG-Phase-18 §3 registration rules.

        Side effects: Mutates the live EntityRegistry.
        """
        surviving = self.deduplicate(judged_proposals, conflicts)

        new_entries: list[RegistryEntry] = []
        enriched_ids: list[str] = []

        for proposal in surviving:
            name = proposal["proposed_name"]
            existing = self._registry.lookup(canonical_name=name)

            if existing is not None:
                # Enrich existing entry
                cid = existing["canonical_id"]
                try:
                    self._registry.enrich(
                        cid,
                        {
                            "canonical_id": cid,
                            "canonical_name": name,
                            "c4_level": existing["c4_level"],
                            "c4_type": existing["c4_type"],
                            "source_requirements": proposal["source_requirements"],
                            "authority": existing["authority"],
                            "variants": _variant_for_proposal(batch["batch_id"], proposal),
                            "description": existing["description"],
                        },
                    )
                    enriched_ids.append(cid)
                except ValueError as exc:
                    logger.warning(
                        "Registry enrich failed for %s (batch %s): %s — rejected write, continuing",
                        name, batch["batch_id"], exc,
                    )

            else:
                cid = _next_ent_id()
                entry: RegistryEntry = {
                    "canonical_id": cid,
                    "canonical_name": name,
                    "c4_level": proposal["c4_level"],
                    "c4_type": proposal["c4_type"],
                    "source_requirements": list(proposal["source_requirements"]),
                    "authority": proposal["proposing_subgraph"],
                    "variants": _variant_for_proposal(batch["batch_id"], proposal),
                    "description": proposal["description"],
                }

                if proposal["proposed_name"] in {
                    c.get("entity_name", "") for c in conflicts
                    if c.get("resolution") == "unresolved"
                }:
                    entry["description"] += (
                        " [CONFLICT: mutually exclusive behaviours flagged for human review]"
                    )

                try:
                    validate_registry_entry(entry)
                    self._registry.register(entry)
                    new_entries.append(entry)
                except ValueError as exc:
                    logger.warning(
                        "Registry register failed for %s (batch %s): %s — rejected write, continuing",
                        name, batch["batch_id"], exc,
                    )

        self._registry.set_last_batch_id(batch["batch_id"])
        return build_delta(new_entries, enriched_ids)

    # ── Internal: Generic Judge LLM step ──

    async def _judge_llm_step(
        self,
        batch: BatchInput,
        proposals: list[EntityProposal],
        config: RunnableConfig,
        step_name: str,
        output_field: str,
    ) -> object:
        """Execute a single Judge LLM call for a SAAM step.

        LLM is resolved from config["configurable"]["judge_llm"].
        with_structured_output is bound inside this method — never at injection time.
        """
        from langchain_core.messages import HumanMessage, SystemMessage

        from raa.schemas.structured_output import (
            JudgeClassificationOutput,
            JudgeCoverageOutput,
            JudgeInteractionOutput,
            dump_structured_response,
        )
        from raa.utils.rendering import render_system_user

        # Separate ASR and Non-ASR proposals
        asr_proposals = [p for p in proposals if p["proposing_subgraph"] == "asr"]
        non_asr_proposals = [p for p in proposals if p["proposing_subgraph"] == "non_asr"]

        proposal_refs = {id(proposal): _proposal_ref(idx) for idx, proposal in enumerate(proposals)}

        # Pre-join source_requirements for Mustache (Chevron has no -last support)
        def _with_joined_src_reqs(proposals: list) -> list[dict]:
            result = []
            for idx, p in enumerate(proposals):
                entry = dict(p)
                entry["proposal_ref"] = proposal_refs.get(id(p), _proposal_ref(idx))
                reqs = entry.get("source_requirements", [])
                entry["source_requirements_joined"] = ", ".join(reqs) if reqs else ""
                result.append(entry)
            return result

        step_instructions = {
            "classified": (
                "Execute SAAM Step 3 — Scenario Classification only. "
                "For each proposal, classify it as 'direct' or 'indirect'. "
                "Return one annotation per proposal in the 'classified' field."
            ),
            "coverage": (
                "Execute SAAM Step 4 — Individual Scenario Evaluation only. "
                "For each requirement, identify which proposals satisfy it. "
                "Report requirements with no satisfying proposal as coverage gaps. "
                "Return one annotation per proposal in 'judged' and gaps in "
                "'coverage_gaps'."
            ),
            "interactions": (
                "Execute SAAM Step 5 — Scenario Interaction only. "
                "Identify proposals sharing the same name. "
                "Resolve authority conflicts (ASR wins over non-ASR). "
                "Return one annotation per proposal in 'judged' and conflicts in "
                "'conflicts'."
            ),
        }

        variables: dict = {
            "requirements": list(batch.get("asrs", [])) + list(batch.get("non_asrs", [])),
            "asr_proposals": _with_joined_src_reqs(asr_proposals),
            "non_asr_proposals": _with_joined_src_reqs(non_asr_proposals),
            "registry_snapshot": batch.get("registry_snapshot", {}),
            "step_instruction": step_instructions.get(output_field, ""),
        }

        system_prompt, user_prompt = render_system_user(
            JUDGE_SYSTEM_TEMPLATE, JUDGE_USER_TEMPLATE, variables
        )

        llm = config["configurable"]["judge_llm"]

        output_models = {
            "classified": JudgeClassificationOutput,
            "coverage": JudgeCoverageOutput,
            "interactions": JudgeInteractionOutput,
        }
        output_model = output_models[output_field]

        # Bind with_structured_output for this step.
        using_include_raw = True
        try:
            model = llm.with_structured_output(output_model, include_raw=True)
        except (TypeError, NotImplementedError):
            using_include_raw = False
            model = llm.with_structured_output(output_model)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        logger.debug("Judge %s: invoking LLM for batch %s", step_name, batch["batch_id"])
        try:
            result = await model.ainvoke(messages)
        except Exception as exc:
            if not _is_structured_output_validation_error(exc):
                raise
            logger.warning(
                "Judge %s structured output validation failed for batch %s: %s. "
                "Using deterministic fallback.",
                step_name,
                batch["batch_id"],
                exc,
            )
            return {}
        if using_include_raw and isinstance(result, dict) and "parsing_error" in result:
            parsing_error = result.get("parsing_error")
            if parsing_error is not None:
                logger.warning(
                    "Judge %s structured output parsing failed for batch %s: %s. "
                    "Using deterministic fallback.",
                    step_name,
                    batch["batch_id"],
                    parsing_error,
                )
                return {}
            parsed = result.get("parsed")
            if parsed is None:
                return {}
            return dump_structured_response(parsed)
        return dump_structured_response(result)


def _is_structured_output_validation_error(exc: Exception) -> bool:
    """Return whether an exception is a structured-output parsing/validation failure."""
    error_types = []
    try:
        from langchain_core.exceptions import OutputParserException
        error_types.append(OutputParserException)
    except ImportError:  # pragma: no cover - depends on installed langchain version
        pass

    try:
        from pydantic import ValidationError
        error_types.append(ValidationError)
    except ImportError:  # pragma: no cover - pydantic is a runtime dependency
        pass

    return bool(error_types) and isinstance(exc, tuple(error_types))
