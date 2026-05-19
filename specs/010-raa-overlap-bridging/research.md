# Research Report: Bridge Scoring and Adjacency Metrics

This report documents overlap bridging design choices.

## 1. Adjacency Metric

### Decision
Two condition groups are adjacent if the cosine similarity between their normalized centroids is greater than or equal to `0.50`.

### Rationale
Centroids are normalized unit vectors. Calculating their dot product is computationally inexpensive and accurately reflects semantic closeness of the condition clusters.

---

## 2. Multiplicative Bridging Score

### Decision
For a candidate non-ASR requirement $r$ and adjacent centroids $c_1, c_2$, the bridge score is computed as:
$$\text{Score}(r) = \text{Sim}(r, c_1) \times \text{Sim}(r, c_2)$$
Where $\text{Sim}(r, c_i)$ is the cosine similarity between the candidate and the centroid.

### Rationale
Multiplicative scoring guarantees that requirements must have positive, strong similarity to **both** clusters to qualify as a bridge. An additive score would permit a requirement strongly matching only one cluster (and unrelated to the other) to become a bridge, polluting the other cluster's context.

### Alternatives Considered
- **Additive Scoring** ($S_1 + S_2$): Rejected because a requirement matching only one centroid could qualify as a bridge.
