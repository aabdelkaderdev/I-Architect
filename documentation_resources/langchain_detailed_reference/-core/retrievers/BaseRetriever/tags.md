<!-- Source: https://reference.langchain.com/python/langchain-core/retrievers/BaseRetriever/tags -->

Attributev1.2.21 (latest)●Since v0.1

# tags

Optional list of tags associated with the retriever.

These tags will be associated with each call to this retriever,
and passed as arguments to the handlers defined in `callbacks`.

You can use these to eg identify a specific instance of a retriever with its
use case.


```
tags: list[str] | None = None
```


