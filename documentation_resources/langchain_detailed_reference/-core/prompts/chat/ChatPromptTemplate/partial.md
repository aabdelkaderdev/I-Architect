<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate/partial -->

Methodv1.2.21 (latest)●Since v0.1

# partial

Get a new `ChatPromptTemplate` with some input variables already filled in.


```
partial(
    self,
    **kwargs: Any = {},
) -> ChatPromptTemplate
```

**Example:**

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI assistant named {name}."),
        ("human", "Hi I'm {user}"),
        ("ai", "Hi there, {user}, I'm {name}."),
        ("human", "{input}"),
    ]
)
template2 = template.partial(user="Lucy", name="R2D2")

template2.format_messages(input="hello")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to use for filling in template variables.  Ought to be a subset of the input variables. |


