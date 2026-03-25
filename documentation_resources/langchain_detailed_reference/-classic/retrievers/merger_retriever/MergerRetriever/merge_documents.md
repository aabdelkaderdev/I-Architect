<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/merger_retriever/MergerRetriever/merge_documents -->

Methodv1.2.13 (latest)●Since v1.0

# merge\_documents

Merge the results of the retrievers.


```
merge_documents(
  self,
  query: str,
  run_manager: CallbackManagerForRetrieverRun
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | The query to search for. |
| `run_manager`\* | `CallbackManagerForRetrieverRun` | The callback handler to use. |


