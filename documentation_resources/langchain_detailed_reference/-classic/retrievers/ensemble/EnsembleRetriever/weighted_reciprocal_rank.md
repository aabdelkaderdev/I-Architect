<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/weighted_reciprocal_rank -->

Methodv1.2.13 (latest)●Since v1.0

# weighted\_reciprocal\_rank

Perform weighted Reciprocal Rank Fusion on multiple rank lists.

You can find more details about RRF here:
<https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf>.


```
weighted_reciprocal_rank(
    self,
    doc_lists: list[list[Document]],
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `doc_lists`\* | `list[list[Document]]` | A list of rank lists, where each rank list contains unique items. |


