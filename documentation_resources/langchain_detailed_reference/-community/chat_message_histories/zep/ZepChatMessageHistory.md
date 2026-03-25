<!-- Source: https://reference.langchain.com/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory -->

Classv0.4.1 (latest)●Since v0.3

# ZepChatMessageHistory


```
ZepChatMessageHistory(
  self,
  session_id: str,
  url: str = 'http://localhost:8000',
  api_key: Optional
```

## Bases

`BaseChatMessageHistory`

## Constructors

## Attributes

## Methods

## Inherited from[BaseChatMessageHistory](/python/langchain-core/chat_history/BaseChatMessageHistory)(langchain\_core)

### Methods

[Maget\_messages](/python/langchain-core/chat_history/BaseChatMessageHistory/aget_messages)



[

[str](https://docs.python.org/3/library/stdtypes.html#str)

]

=

None

)

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| session\_id | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| url | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| api\_key | [Optional](https://docs.python.org/3/library/typing.html#typing.Optional)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |

[attribute

zep\_client](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/zep_client)

[attribute

session\_id: session\_id](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/session_id)

[attribute

messages: List[BaseMessage]](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/messages)

[attribute

zep\_messages: List[Message]](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/zep_messages)

[attribute

zep\_summary: Optional[str]](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/zep_summary)

[method

add\_user\_message](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/add_user_message)

[method

add\_ai\_message](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/add_ai_message)

[method

add\_message](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/add_message)

[method

add\_messages](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/add_messages)

[method

aadd\_messages](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/aadd_messages)

[method

search](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/search)

[method

clear](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/clear)

[method

aclear](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory/aclear)

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
<https://github.com/getzep/zep-python>

Retrieve messages from Zep memory

Retrieve summary from Zep memory

Retrieve summary from Zep memory

Convenience method for adding a human message string to the store.

Convenience method for adding an AI message string to the store.

Append the message to the Zep memory history

Append the messages to the Zep memory history

Append the messages to the Zep memory history asynchronously

Search Zep memory for messages matching the query

Clear session memory from Zep. Note that Zep is long-term storage for memory
and this is not advised unless you have specific data retention requirements.

Clear session memory from Zep asynchronously.
Note that Zep is long-term storage for memory and this is not advised
unless you have specific data retention requirements.