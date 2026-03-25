<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage/pretty_repr -->

Methodv1.2.21 (latest)●Since v0.1

# pretty\_repr

Return a pretty representation of the message for display.


```
pretty_repr(
    self,
    html: bool = False,
) -> str
```

**Example:**

```
from langchain_core.messages import AIMessage

msg = AIMessage(
    content="Let me check the weather.",
    tool_calls=[
        {"name": "get_weather", "args": {"city": "Paris"}, "id": "1"}
    ],
)
```

Results in:

```
>>> print(msg.pretty_repr())
================================== Ai Message ==================================

Let me check the weather.
Tool Calls:
  get_weather (1)
 Call ID: 1
  Args:
    city: Paris
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `html` | `bool` | Default:`False`  Whether to return an HTML-formatted string. |


