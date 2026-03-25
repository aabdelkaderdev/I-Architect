<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage/pretty_repr -->

Methodv1.2.21 (latest)●Since v0.1

# pretty\_repr

Get a pretty representation of the message.


```
pretty_repr(
    self,
    html: bool = False,
) -> str
```

**Example:**

```
from langchain_core.messages import HumanMessage

msg = HumanMessage(content="What is the capital of France?")
print(msg.pretty_repr())
```

Results in:

```
================================ Human Message =================================

What is the capital of France?
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `html` | `bool` | Default:`False`  Whether to format the message as HTML. If `True`, the message will be formatted with HTML tags. |


