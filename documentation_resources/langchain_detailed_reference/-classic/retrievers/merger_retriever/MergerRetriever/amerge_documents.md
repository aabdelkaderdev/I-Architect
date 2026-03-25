<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/merger_retriever/MergerRetriever/amerge_documents -->

Methodv1.2.13 (latest)●Since v1.0

# amerge\_documents

Asynchronously merge the results of the retrievers.


```
amerge_documents(
  self,
  query: str,
  run_manager: AsyncCallbackManagerForRetrieverRun
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | The query to search for. |
| `run_manager`\* | `AsyncCallbackManagerForRetrieverRun` | The callback handler to use. |


