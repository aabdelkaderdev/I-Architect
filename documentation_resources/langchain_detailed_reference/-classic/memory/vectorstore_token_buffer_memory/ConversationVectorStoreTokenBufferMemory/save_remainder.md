<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/save_remainder -->

Methodv1.2.13 (latest)●Since v1.0

# save\_remainder

Save the remainder of the conversation buffer to the vector store.

Useful if you have made the VectorStore persistent, in which
case this can be called before the end of the session to store the
remainder of the conversation.


```
save_remainder(
    self,
) -> None
```


