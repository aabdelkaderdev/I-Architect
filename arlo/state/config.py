"""
Experiment configuration for the ARLO pipeline.

The experiment_config dict from ARLOInput is unpacked here
for type-safe access within nodes.
"""
from dataclasses import dataclass, field


@dataclass
class ExperimentConfig:
    """Typed representation of the experiment_config dict."""

    mode: str = "stringent"            # "stringent" or "lax"
    optimizer: str = "ILP"             # "ILP" or "Greedy"
    batch_size: int = 10               # Requirements per LLM batch
    max_sat_retries: int = 3           # Max retries for satisfiable group parsing

    @classmethod
    def from_dict(cls, d: dict) -> "ExperimentConfig":
        """Create from the raw experiment_config dict in state."""
        return cls(
            mode=d.get("mode", "stringent"),
            optimizer=d.get("optimizer", "ILP"),
            batch_size=d.get("batch_size", 10),
            max_sat_retries=d.get("max_sat_retries", 3),
        )
