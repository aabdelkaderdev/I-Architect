"""
K-Means clustering of ASR embeddings (scikit-learn).

Groups ASRs by condition similarity to enable condition-group formation.
"""
from __future__ import annotations

from arlo.state.schemas import ARLOState


def cluster_conditions(state: ARLOState) -> dict:
    """Node: Cluster ASR embeddings via K-Means.
    Reads: embeddings, asrs
    Writes: cluster_assignments
    """
    embeddings = state["embeddings"]
    if not embeddings:
        return {"cluster_assignments": []}

    from sklearn.cluster import KMeans
    import numpy as np

    X = np.array(embeddings)
    n = len(embeddings)

    if n == 1:
        return {"cluster_assignments": [0]}

    def calculate_wcss(X: np.ndarray, centroids: np.ndarray, labels: np.ndarray) -> float:
        """Standard within-cluster sum of squared Euclidean distances."""
        wcss = 0.0
        for i, label in enumerate(labels):
            diff = X[i] - centroids[label]
            wcss += float(np.dot(diff, diff))

        return wcss

    def find_elbow_offset(wcss_list: list[float]) -> int:
        """Return a 0-based offset from k_start, or 0 for short sweeps."""
        if len(wcss_list) <= 2:
            return 0

        diffs = [wcss_list[i - 1] - wcss_list[i] for i in range(1, len(wcss_list))]
        return max(range(len(diffs)), key=lambda i: diffs[i])

    # ── sweep k from n//10 to n//5 (inclusive) ───────────────────────────────
    k_start = n // 10
    k_end   = n // 5

    # Guard: need at least one valid k (≥ 1 and < n)
    k_start = max(k_start, 1)
    k_end   = max(k_end, k_start)
    k_end   = min(k_end, n - 1)

    wcss_scores: list[float] = []
    for k in range(k_start, k_end + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        km.fit(X)
        score = calculate_wcss(X, km.cluster_centers_, km.labels_)
        wcss_scores.append(score)

    optimal_k = k_start + find_elbow_offset(wcss_scores)
    optimal_k = max(1, min(optimal_k, n - 1))   # clamp to valid range

    # ── final fit ────────────────────────────────────────────────────────────
    final_km = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
    final_km.fit(X)
    raw_labels: np.ndarray = final_km.labels_   # shape (n,)

    # ── reassign sequential IDs while preserving ASR positional alignment ─────
    raw_label_list = raw_labels.tolist()

    # Assign a sequential cluster ID to each unique raw label in sorted order,
    # then map back so cluster_assignments[i] corresponds to asrs[i].
    unique_labels = sorted(set(raw_label_list))
    label_to_id   = {label: cid for cid, label in enumerate(unique_labels)}
    adjusted      = [label_to_id[label] for label in raw_label_list]

    return {"cluster_assignments": adjusted}
