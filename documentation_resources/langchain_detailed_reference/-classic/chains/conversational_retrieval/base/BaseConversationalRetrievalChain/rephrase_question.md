<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversational_retrieval/base/BaseConversationalRetrievalChain/rephrase_question -->

Attributev1.2.13 (latest)●Since v1.0

# rephrase\_question

Whether or not to pass the new generated question to the combine\_docs\_chain.
If `True`, will pass the new generated question along.
If `False`, will only use the new generated question for retrieval and pass the
original question along to the combine\_docs\_chain.


```
rephrase_question: bool = True
```


