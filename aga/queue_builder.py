"""Diagram queue builder — derive ordered list[DiagramSpec] from parsed RAAOutput.

Pure function: deterministic, no I/O, no LLM calls, no side effects.
"""

from __future__ import annotations

from aga.schemas import DiagramSpec, RAAOutput


def build_diagram_queue(raa: RAAOutput) -> list[DiagramSpec]:
    """Derive the ordered diagram work queue from a parsed RAAOutput.

    Queue ordering:
        1. One context diagram (from l1_description)
        2. One container diagram per l2_descriptions entry (in list order)
        3. One component diagram per l3_descriptions entry (in list order)

    Parameters
    ----------
    raa : RAAOutput
        Fully parsed RAA output (output of normalise_raa_output).

    Returns
    -------
    list[DiagramSpec]
        Ordered list of diagram specifications. Never empty.
    """
    queue: list[DiagramSpec] = []
    seen_ids: dict[str, int] = {}

    # Pass 1 — Context diagram (always exactly 1)
    l1 = raa.l1_description
    ctx_spec = DiagramSpec(
        diagram_id="ctx",
        diagram_type="context",
        label=f"System Context — {l1.system_name}",
        output_filename="ctx.png",
        source_l1=l1,
    )
    queue.append(ctx_spec)
    seen_ids["ctx"] = 1

    # Pass 2 — Container diagrams (one per L2 entry)
    for l2 in raa.l2_descriptions:
        base_id = f"cnt-{l2.concern_id}"
        diagram_id = _deduplicate(base_id, seen_ids)
        queue.append(
            DiagramSpec(
                diagram_id=diagram_id,
                diagram_type="container",
                label=f"Container Diagram — {l2.concern_id}",
                output_filename=f"{diagram_id}.png",
                source_l2=l2,
            )
        )

    # Pass 3 — Component diagrams (one per L3 entry)
    for l3 in raa.l3_descriptions:
        base_id = f"cmp-{l3.parent_container_id}-{l3.concern_id}"
        diagram_id = _deduplicate(base_id, seen_ids)
        queue.append(
            DiagramSpec(
                diagram_id=diagram_id,
                diagram_type="component",
                label=(
                    f"Component Diagram — {l3.parent_container_id}"
                    f" ({l3.concern_id})"
                ),
                output_filename=f"{diagram_id}.png",
                source_l3=l3,
            )
        )

    return queue


def _deduplicate(base_id: str, seen: dict[str, int]) -> str:
    count = seen.get(base_id, 0)
    if count == 0:
        seen[base_id] = 1
        return base_id
    seen[base_id] = count + 1
    return f"{base_id}-{count}"
