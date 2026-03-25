<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/collapse_documents_chain -->

Attributev1.2.13 (latest)●Since v1.0

# collapse\_documents\_chain

Chain to use to collapse documents if needed until they can all fit.
If `None`, will use the `combine_documents_chain`.

This is typically a `StuffDocumentsChain`.


```
collapse_documents_chain: BaseCombineDocumentsChain | None = None
```


