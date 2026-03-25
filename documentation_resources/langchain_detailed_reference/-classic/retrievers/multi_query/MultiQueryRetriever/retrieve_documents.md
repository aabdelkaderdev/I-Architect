<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever/retrieve_documents -->

Methodv1.2.13 (latest)●Since v1.0

# retrieve\_documents

Run all LLM generated queries.


```
retrieve_documents(
  self,
  queries: list[str],
  run_manager: CallbackManagerForRetrieverRun
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `queries`\* | `list[str]` | query list |
| `run_manager`\* | `CallbackManagerForRetrieverRun` | run manager for callbacks |


