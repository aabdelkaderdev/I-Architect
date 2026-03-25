<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/ConversationalRetrievalChain/max_tokens_limit -->

Attributev1.2.13 (latest)●Since v1.0

# max\_tokens\_limit

If set, enforces that the documents returned are less than this limit.

This is only enforced if `combine_docs_chain` is of type StuffDocumentsChain.


```
max_tokens_limit: int | None = None
```


