<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/arank_fusion -->

Methodv1.2.13 (latest)●Since v1.0

# arank\_fusion

Rank fusion.

Asynchronously retrieve the results of the retrievers
and use rank\_fusion\_func to get the final result.


```
arank_fusion(
  self,
  query: str,
  run_manager: AsyncCallbackManagerForRetrieverRun,
  *,
  config: RunnableConfig | None = None
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | The query to search for. |
| `run_manager`\* | `AsyncCallbackManagerForRetrieverRun` | The callback handler to use. |
| `config` | `RunnableConfig | None` | Default:`None`  Optional configuration for the retrievers. |


