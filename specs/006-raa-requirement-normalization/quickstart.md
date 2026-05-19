# Quickstart: Requirement Normalization Node

This guide details how to invoke the normalization helper in the RAA pipeline.

## 1. Importing and Calling the Normalizer

The `normalize_requirement` helper takes a single raw dictionary and resolves it:

```python
from raa.utils.normalizer import normalize_requirements

# Raw ARLO inputs
asrs_raw = [
    {
        "id": 1,
        "is_architecturally_significant": True,
        "quality_attributes": ["Security"],
        "condition_text": "when under load"
    }
]

parent_requirements = {
    "R1": "The system must process payments securely."
}

# Run normalization
normalized_asrs = normalize_requirements(asrs_raw, parent_requirements, is_asr=True)
print(normalized_asrs)
# Output:
# [
#   {
#     "id": "R1",
#     "text": "The system must process payments securely.",
#     "is_asr": True,
#     "quality_attributes": ["Security"],
#     "condition_text": "when under load"
#   }
# ]
```
