<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/in_memory/InMemoryVectorStore/load -->

Methodv1.2.21 (latest)●Since v0.2

# load

Load a vector store from a file.


```
load(
  cls,
  path: str,
  embedding: Embeddings,
  **kwargs: Any = {}
) -> InMemoryVectorStore
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `path`\* | `str` | The path to load the vector store from. |
| `embedding`\* | `Embeddings` | The embedding to use. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the constructor. |


