<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter/transform_documents -->

Methodv1.1.1 (latest)●Since v0.0

# transform\_documents


```
transform_documents(
  self,
  documents: Sequence[Document],
  **kwargs: Any = {}
)
```



->

[Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)

[

[Document](/python/langchain-core/documents/Document)

]

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` |  |

Transform sequence of documents by splitting them.

The sequence of documents to split.