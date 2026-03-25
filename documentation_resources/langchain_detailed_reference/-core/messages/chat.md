<!-- Source: https://reference.langchain.com/python/langchain-core/messages/chat -->

Modulev1.2.21 (latest)●Since v0.1

# chat

Chat Message.

## Functions

[function

merge\_content

Merge multiple message contents.](/python/langchain-core/messages/base/merge_content)[function

merge\_dicts

Merge dictionaries.

Merge many dicts, handling specific scenarios where a key exists in both
dictionaries but has a value of `None` in `'left'`. In such cases, the method uses
the value from `'right'` for that key in the merged dictionary.](/python/langchain-core/utils/_merge/merge_dicts)

## Classes

[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseMessageChunk

Message chunk, which can be concatenated with other Message chunks.](/python/langchain-core/messages/base/BaseMessageChunk)[class

ChatMessage

Message that can be assigned an arbitrary speaker (i.e. role).](/python/langchain-core/messages/chat/ChatMessage)[class

ChatMessageChunk

Chat Message chunk.](/python/langchain-core/messages/chat/ChatMessageChunk)


