# Quickstart: RAA Batch Construction

This guide explains how to construct condition-group anchored requirement batches.

```python
from raa.nodes.batch_construction import construct_batches
```

## 1. Centroid Math Implementation

```python
import numpy as np

def calculate_centroid(vectors: list[list[float]]) -> list[float]:
    arr = np.array(vectors)
    avg = np.mean(arr, axis=0)
    # L2 normalize
    norm = np.linalg.norm(avg)
    if norm == 0:
        return avg.tolist()
    return (avg / norm).tolist()
```

## 2. Cosine Similarity Filter

```python
def filter_non_asrs(centroid: list[float], non_asr_records: list[dict]) -> list[dict]:
    centroid_arr = np.array(centroid)
    results = []
    
    for record in non_asr_records:
        vec = np.array(record["vector"])
        similarity = float(np.dot(centroid_arr, vec))
        if similarity >= 0.65:
            results.append({
                "id": record["id"],
                "text": record["text"],
                "similarity": similarity
            })
            
    # Sort and cap at 10 candidates
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:10]
```
