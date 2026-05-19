# Quickstart: RAA Overlap Bridging

This guide demonstrates how to calculate bridging scores and inject bridge requirements.

## 1. Adjacency Check

```python
import numpy as np

def are_adjacent(c1: list[float], c2: list[float], threshold: float = 0.50) -> bool:
    c1_arr = np.array(c1)
    c2_arr = np.array(c2)
    return float(np.dot(c1_arr, c2_arr)) >= threshold
```

## 2. Multiplicative Bridging Score

```python
def score_and_select_bridges(
    c1: list[float], 
    c2: list[float], 
    non_asrs: list[dict]
) -> list[str]:
    c1_arr = np.array(c1)
    c2_arr = np.array(c2)
    
    candidates = []
    for req in non_asrs:
        vec = np.array(req["vector"])
        s1 = float(np.dot(vec, c1_arr))
        s2 = float(np.dot(vec, c2_arr))
        
        # Must have positive relevance to both
        if s1 > 0 and s2 > 0:
            bridge_score = s1 * s2
            candidates.append((req["id"], bridge_score))
            
    # Sort descending by bridge score
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 1-3 requirement IDs
    return [item[0] for item in candidates[:3]]
```
