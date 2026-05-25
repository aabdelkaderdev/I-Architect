"""
Runtime configuration for the RAA pipeline.

The config is unpacked from orchestrator-provided parameters
for type-safe access within nodes.
"""
from dataclasses import dataclass


@dataclass
class RAAConfig:
    """Typed representation of runtime configuration."""

    batch_size: int = 10
    coherence_threshold: float = 0.55
    residual_rebatch_pct: float = 0.15
    max_human_retries: int = 3

    @classmethod
    def from_dict(cls, d: dict) -> "RAAConfig":
        """Create from a raw config dict, ignoring unknown keys."""
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
