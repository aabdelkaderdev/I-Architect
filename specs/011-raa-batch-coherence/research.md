# Research Report: Deterministic Batch Clustering and Cohesion Metrics

This report documents batch splitting implementation choices.

## 1. Deterministic 2-Way Clustering

### Decision
Implement K-Means (K=2) using pure NumPy. To ensure the clustering is 100% deterministic (reproducible across runs and machines), initialize the centroids using the two requirements in the batch that have the lowest cosine similarity (greatest distance) to each other.

### Rationale
Standard K-Means uses random initializations, which could produce different sub-batches across runs. Selecting the two most distant points as starting centroids is fully deterministic, stable, and semantically logical for splitting drifting clusters.

### Alternatives Considered
- **Scikit-learn KMeans**: Rejected because importing a heavy machine learning library adds unnecessary overhead, and configuring it for perfect cross-platform determinism is brittle.

---

## 2. Coherence Metric Implementation

### Decision
Calculate the average of the cosine similarities between every vector in the batch and the batch's normalized centroid vector.

### Rationale
Cosine similarity is bounded and scale-invariant. The threshold of 0.55 acts as a reliable filter for semantic cohesion.
