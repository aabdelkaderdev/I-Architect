<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary/ConversationSummaryMemory/from_messages -->

Methodv1.2.13 (latest)●Since v1.0

# from\_messages

Create a ConversationSummaryMemory from a list of messages.


```
from_messages(
  cls,
  llm: BaseLanguageModel,
  chat_memory: BaseChatMessageHistory,
  *,
  summarize_step: int = 2,
  **kwargs: Any = {}
) -> ConversationSummaryMemory
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use for summarization. |
| `chat_memory`\* | `BaseChatMessageHistory` | The chat history to summarize. |
| `summarize_step` | `int` | Default:`2`  Number of messages to summarize at a time. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the class. |


