<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever/generate_queries -->

Methodv1.2.13 (latest)●Since v1.0

# generate\_queries

Generate queries based upon user input.


```
generate_queries(
  self,
  question: str,
  run_manager: CallbackManagerForRetrieverRun
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `question`\* | `str` | user query |
| `run_manager`\* | `CallbackManagerForRetrieverRun` | run manager for callbacks |


