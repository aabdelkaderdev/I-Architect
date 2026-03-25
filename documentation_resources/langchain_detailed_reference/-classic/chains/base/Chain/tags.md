<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/tags -->

Attributev1.2.13 (latest)●Since v1.0

# tags

Optional list of tags associated with the chain.
These tags will be associated with each call to this chain,
and passed as arguments to the handlers defined in `callbacks`.
You can use these to eg identify a specific instance of a chain with its use case.


```
tags: list[str] | None = None
```


