<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/map_reduce/MapReduceDocumentsChain/acombine_docs -->

Methodv1.2.13 (latest)●Since v1.0

# acombine\_docs

Combine documents in a map reduce manner.

Combine by mapping first chain over all documents, then reducing the results.
This reducing can be done recursively if needed (if there are many documents).


```
acombine_docs(
  self,
  docs: list[Document],
  token_max: int | None = None,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> tuple[str, dict]
```


