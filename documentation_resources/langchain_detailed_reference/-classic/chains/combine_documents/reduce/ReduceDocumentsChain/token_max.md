<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/token_max -->

Attributev1.2.13 (latest)●Since v1.0

# token\_max

The maximum number of tokens to group documents into.

For example, if set to 3000 then documents will be grouped into chunks of no greater
than 3000 tokens before trying to combine them into a smaller chunk.


```
token_max: int = 3000
```


