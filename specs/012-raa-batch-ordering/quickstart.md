# Quickstart: RAA Batch Queue Ordering

This guide demonstrates how to calculate sorting scores and order the batch execution queue.

## 1. Score Calculation

```python
RISK_MAPPING = {
    "security": 4,
    "reliability": 3,
    "performance": 2,
    "usability": 1
}

def calculate_batch_score(batch: dict, strategy: str) -> float:
    if strategy == "asr_count":
        return float(len(batch["asr_ids"]))
        
    elif strategy == "quality_weight":
        # Sum of quality weights
        return float(sum(req.get("weight", 1.0) for req in batch["asr_requirements"]))
        
    else:  # risk_first
        # Max risk priority score
        risks = [RISK_MAPPING.get(req.get("quality_attribute", "").lower(), 0) 
                 for req in batch["asr_requirements"]]
        return float(max(risks) if risks else 0.0)
```

## 2. Queue Sorting with Tie-Breaking

```python
def sort_batch_queue(batches: list[dict], strategy: str = "risk_first") -> list[dict]:
    # Annotate with scores
    for batch in batches:
        score = calculate_batch_score(batch, strategy)
        batch["sorting_metadata"] = {
            "score": score,
            "strategy": strategy,
            "tie_breaker": batch["group_id"]
        }
        
    # Sort descending by score, ascending by group_id (lexicographical tie-breaker)
    sorted_batches = sorted(
        batches,
        key=lambda x: (-x["sorting_metadata"]["score"], x["sorting_metadata"]["tie_breaker"])
    )
    return sorted_batches
```
