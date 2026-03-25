<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/from_messages -->

Methodv1.2.21 (latest)●Since v0.1

# from\_messages

Create a chat prompt template from a variety of message formats.


```
from_messages(
  cls,
  messages: Sequence[MessageLikeRepresentation],
  template_format: PromptTemplateFormat = 'f-string'
) -> ChatPromptTemplate
```

Args:
messages: Sequence of message representations.

```
A message can be represented using the following formats:

1. `BaseMessagePromptTemplate`
2. `BaseMessage`
3. 2-tuple of `(message type, template)`; e.g.,
    `('human', '{user_input}')`
4. 2-tuple of `(message class, template)`
5. A string which is shorthand for `('human', template)`; e.g.,
    `'{user_input}'`
```

template\_format: Format of the template.


