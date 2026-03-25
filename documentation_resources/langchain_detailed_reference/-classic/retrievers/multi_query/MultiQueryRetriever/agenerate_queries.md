<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever/agenerate_queries -->

Methodv1.2.13 (latest)●Since v1.0

# agenerate\_queries

Generate queries based upon user input.


```
agenerate_queries(
  self,
  question: str,
  run_manager: AsyncCallbackManagerForRetrieverRun
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `question`\* | `str` | user query |
| `run_manager`\* | `AsyncCallbackManagerForRetrieverRun` | the callback handler to use. |


