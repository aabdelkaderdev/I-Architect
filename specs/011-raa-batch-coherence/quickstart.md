# Quickstart: RAA Batch Coherence Gate

This guide explains how to calculate batch coherence and implement deterministic splitting.

## 1. Coherence Scoring

```python
import numpy as np

def compute_coherence(vectors: list[list[float]], centroid: list[float]) -> float:
    if len(vectors) <= 2:
        return 1.0  # Small batches pass automatically
    
    vec_arr = np.array(vectors)
    cent_arr = np.array(centroid)
    
    # Average cosine similarity
    similarities = np.dot(vec_arr, cent_arr)
    return float(np.mean(similarities))
```

## 2. Deterministic K-Means Split (K=2)

```python
def split_batch_vectors(vectors: list[list[float]]) -> tuple[list[int], list[int]]:
    arr = np.array(vectors)
    n = len(arr)
    
    # 1. Deterministic centroid seed: find the two furthest vectors
    sim_matrix = np.dot(arr, arr.T)
    min_idx = np.unravel_index(np.argmin(sim_matrix), sim_matrix.shape)
    
    c1 = arr[min_idx[0]]
    c2 = arr[min_idx[1]]
    
    # 2. Iterate assignments
    for _ in range(10):
        # Assign to nearest centroid
        s1 = np.dot(arr, c1)
        s2 = np.dot(arr, c2)
        
        labels = np.where(s1 >= s2, 0, 1)
        
        # Recalculate centroids
        idx1 = np.where(labels == 0)[0]
        idx2 = np.where(labels == 1)[0]
        
        if len(idx1) == 0 or len(idx2) == 0:
            break
            
        c1_new = np.mean(arr[idx1], axis=0)
        c2_new = np.mean(arr[idx2], axis=0)
        
        c1 = c1_new / np.linalg.norm(c1_new)
        c2 = c2_new / np.linalg.norm(c2_new)
        
    return idx1.tolist(), idx2.tolist()
```
