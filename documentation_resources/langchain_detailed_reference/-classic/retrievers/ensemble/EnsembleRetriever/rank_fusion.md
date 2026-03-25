<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/rank_fusion -->

Methodv1.2.13 (latest)●Since v1.0

# rank\_fusion

Rank fusion.

Retrieve the results of the retrievers and use rank\_fusion\_func to get
the final result.


```
rank_fusion(
  self,
  query: str,
  run_manager: CallbackManagerForRetrieverRun,
  *,
  config: RunnableConfig | None = None
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | The query to search for. |
| `run_manager`\* | `CallbackManagerForRetrieverRun` | The callback handler to use. |
| `config` | `RunnableConfig | None` | Default:`None`  Optional configuration for the retrievers. |


