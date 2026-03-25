<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/collapse_max_retries -->

Attributev1.2.13 (latest)●Since v1.0

# collapse\_max\_retries

The maximum number of retries to collapse documents to fit `token_max`.

If `None`, it will keep trying to collapse documents to fit `token_max`.

Otherwise, after it reaches the max number, it will throw an error.


```
collapse_max_retries: int | None = None
```


