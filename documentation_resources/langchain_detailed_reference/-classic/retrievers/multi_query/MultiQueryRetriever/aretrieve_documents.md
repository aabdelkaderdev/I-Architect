<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever/aretrieve_documents -->

Methodv1.2.13 (latest)●Since v1.0

# aretrieve\_documents

Run all LLM generated queries.


```
aretrieve_documents(
  self,
  queries: list[str],
  run_manager: AsyncCallbackManagerForRetrieverRun
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `queries`\* | `list[str]` | query list |
| `run_manager`\* | `AsyncCallbackManagerForRetrieverRun` | the callback handler to use |


