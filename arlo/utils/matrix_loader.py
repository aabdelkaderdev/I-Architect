"""
Quality–architecture pattern matrix loader.

The matrix is a nested dict mapping quality attributes to architecture
patterns with integer scores. It is pre-loaded by the parent pipeline
and passed into ARLO via ARLOInput.matrix.
"""
import json
from pathlib import Path


def load_matrix_from_json(path: str | Path) -> dict[str, dict[str, int]]:
    """Load the quality–architecture matrix from a JSON file.

    Expected format:
    {
        "Performance": {"Caching": 3, "Load Balancing": 2, ...},
        "Security": {"Encryption": 3, "Firewall": 1, ...},
        ...
    }
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)
