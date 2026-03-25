<!-- Source: https://reference.langchain.com/python/langchain-core/messages/utils/merge_message_runs -->

Functionv1.2.21 (latest)●Since v0.2

# merge\_message\_runs

Merge consecutive Messages of the same type.

Note

`ToolMessage` objects are not merged, as each has a distinct tool call id that
can't be merged.


```
merge_message_runs(
  messages: Iterable[MessageLikeRepresentation] | PromptValue,
  *,
  chunk_separator: str = '\n'
) -> list[BaseMessage]
```

**Example:**

```
from langchain_core.messages import (
    merge_message_runs,
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolCall,
)

messages = [
    SystemMessage("you're a good assistant."),
    HumanMessage(
        "what's your favorite color",
        id="foo",
    ),
    HumanMessage(
        "wait your favorite food",
        id="bar",
    ),
    AIMessage(
        "my favorite colo",
        tool_calls=[
            ToolCall(
                name="blah_tool", args={"x": 2}, id="123", type="tool_call"
            )
        ],
        id="baz",
    ),
    AIMessage(
        [{"type": "text", "text": "my favorite dish is lasagna"}],
        tool_calls=[
            ToolCall(
                name="blah_tool",
                args={"x": -10},
                id="456",
                type="tool_call",
            )
        ],
        id="blur",
    ),
]

merge_message_runs(messages)
```

```
[
    SystemMessage("you're a good assistant."),
    HumanMessage(
        "what's your favorite color\\n"
        "wait your favorite food", id="foo",
    ),
    AIMessage(
        [
            "my favorite colo",
            {"type": "text", "text": "my favorite dish is lasagna"}
        ],
        tool_calls=[
            ToolCall({
                "name": "blah_tool",
                "args": {"x": 2},
                "id": "123",
                "type": "tool_call"
            }),
            ToolCall({
                "name": "blah_tool",
                "args": {"x": -10},
                "id": "456",
                "type": "tool_call"
            })
        ]
        id="baz"
    ),
]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `Iterable[MessageLikeRepresentation] | PromptValue` | Sequence Message-like objects to merge. |
| `chunk_separator` | `str` | Default:`'\n'`  Specify the string to be inserted between message chunks. |


