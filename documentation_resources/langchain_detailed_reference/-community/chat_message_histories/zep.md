<!-- Source: https://reference.langchain.com/python/langchain-community/chat_message_histories/zep -->

Modulev0.4.1 (latest)●Since v0.3

# zep

## Attributes

[attribute

logger](/python/langchain-community/chat_message_histories/zep/logger)

## Classes

[class

SearchScope

Scope for the document search. Messages or Summaries?](/python/langchain-community/chat_message_histories/zep/SearchScope)[class

SearchType

Enumerator of the types of search to perform.](/python/langchain-community/chat_message_histories/zep/SearchType)[class

ZepChatMessageHistory

Chat message history that uses Zep as a backend.

Recommended usage::

```
# Set up Zep Chat History
zep_chat_history = ZepChatMessageHistory(
    session_id=session_id,
    url=ZEP_API_URL,
    api_key=<your_api_key>,
)

# Use a standard ConversationBufferMemory to encapsulate the Zep chat history
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=zep_chat_history
)
```

Zep provides long-term conversation storage for LLM apps. The server stores,
summarizes, embeds, indexes, and enriches conversational AI chat
histories, and exposes them via simple, low-latency APIs.

For server installation instructions and more, see:
<https://docs.getzep.com/deployment/quickstart/>

This class is a thin wrapper around the zep-python package. Additional
Zep functionality is exposed via the `zep_summary` and `zep_messages`
properties.

For more information on the zep-python package, see:
<https://github.com/getzep/zep-python>](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory)


