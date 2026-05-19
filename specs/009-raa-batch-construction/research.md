# Research Report: Centroid Calculation and Cosine Similarity Metrics

This report documents vector math implementation choices.

## 1. Centroid Calculation

### Decision
Centroids will be computed as the element-wise mathematical average of the requirement embeddings in the group. If vectors are normalized, we re-normalize the average vector to unit length (L2 normalization) so that subsequent cosine similarity searches remain simple dot products.

### Rationale
Normalizing vectors beforehand makes similarity calculations equivalent to the vector dot product:
$$\text{Similarity}(u, v) = u \cdot v$$
This avoids expensive square root operations at runtime.

### Alternatives Considered
- **Unnormalized vector averages**: Rejected because unnormalized centroid vectors would require calculating vector magnitudes during distance sorting, increasing calculation overhead.

---

## 2. Approximate Nearest Neighbor (ANN) Queries

### Decision
Read all non-ASR embeddings into a NumPy array, perform a vectorized dot product query, sort, and select top candidates.

### Rationale
For small to medium requirement counts (up to tens of thousands), performing an in-memory NumPy dot product is faster and simpler than setting up specialized vector indices (like HNSW).
