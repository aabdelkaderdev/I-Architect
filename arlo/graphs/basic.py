"""
BasicArlo experiment graph.

This is the simplest ARLO experiment: a single pass through the
core pipeline with no removal loops or sensitivity analysis.
"""
from __future__ import annotations

from .core import build_arlo_subgraph


def build_basic_arlo():
    """Build the BasicArlo experiment graph (uncompiled).

    This is identical to the core pipeline — no additional wiring needed.
    The caller compiles with a checkpointer.
    """
    return build_arlo_subgraph()
