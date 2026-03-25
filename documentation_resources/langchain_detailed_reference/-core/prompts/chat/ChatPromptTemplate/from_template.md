<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/from_template -->

Methodv1.2.21 (latest)●Since v0.1

# from\_template

Create a chat prompt template from a template string.

Creates a chat template consisting of a single message assumed to be from the
human.


```
from_template(
  cls,
  template: str,
  **kwargs: Any = {}
) -> ChatPromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | Template string |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to pass to the constructor. |


