# Research Report: Requirement Normalization Implementation

This report documents the implementation choices for the RAA requirement normalization.

## 1. Key Resolution and Error Boundaries

### Decision
The normalizer must raise a clear, descriptive `KeyError` if a requirement ID returned by ARLO cannot be found in the parent pipeline's `requirements` dictionary.

### Rationale
Failing fast prevents bad data from propagating downstream. If a requirement description is missing, its embedding will be incorrect, leading to invalid clusters and poor strategy generation.

### Alternatives Considered
- **Defaulting to empty text**: Rejected because empty requirements would create duplicate embeddings at the origin and corrupt the cosine similarity search space.

---

## 2. Key Conversion Schema

### Decision
Always map raw integer IDs to string IDs using the `R{id}` template format (e.g. `1` -> `"R1"`).

### Rationale
Positional integers from ARLO must be matched with string identifiers (such as `"R1"`, `"R2"`) in the parent system. Standardizing on strings avoids type mismatch bugs during dictionary key lookups.
