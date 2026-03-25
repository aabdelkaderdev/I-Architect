<!-- Source: https://reference.langchain.com/python/langchain-core/messages/utils/filter_messages -->

Functionv1.2.21 (latest)●Since v0.2

# filter\_messages

Filter messages based on `name`, `type` or `id`.


```
filter_messages(
  messages: Iterable[MessageLikeRepresentation] | PromptValue,
  *,
  include_names: Sequence[str] | None = None,
  exclude_names: Sequence[str] | None = None,
  include_types: Sequence[str | type[BaseMessage]] | None = None,
  exclude_types: Sequence[str | type[BaseMessage]] | None = None,
  include_ids: Sequence[str] | None = None,
  exclude_ids: Sequence[str] | None = None,
  exclude_tool_calls: Sequence[str] | bool | None = None
) -> list[BaseMessage]
```

**Example:**

```
from langchain_core.messages import (
    filter_messages,
    AIMessage,
    HumanMessage,
    SystemMessage,
)

messages = [
    SystemMessage("you're a good assistant."),
    HumanMessage("what's your name", id="foo", name="example_user"),
    AIMessage("steve-o", id="bar", name="example_assistant"),
    HumanMessage(
        "what's your favorite color",
        id="baz",
    ),
    AIMessage(
        "silicon blue",
        id="blah",
    ),
]

filter_messages(
    messages,
    incl_names=("example_user", "example_assistant"),
    incl_types=("system",),
    excl_ids=("bar",),
)
```

```
[
    SystemMessage("you're a good assistant."),
    HumanMessage("what's your name", id="foo", name="example_user"),
]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `Iterable[MessageLikeRepresentation] | PromptValue` | Sequence Message-like objects to filter. |
| `include_names` | `Sequence[str] | None` | Default:`None`  Message names to include. |
| `exclude_names` | `Sequence[str] | None` | Default:`None`  Messages names to exclude. |
| `include_types` | `Sequence[str | type[BaseMessage]] | None` | Default:`None`  Message types to include. Can be specified as string names (e.g. `'system'`, `'human'`, `'ai'`, ...) or as `BaseMessage` classes (e.g. `SystemMessage`, `HumanMessage`, `AIMessage`, ...). |
| `exclude_types` | `Sequence[str | type[BaseMessage]] | None` | Default:`None`  Message types to exclude. Can be specified as string names (e.g. `'system'`, `'human'`, `'ai'`, ...) or as `BaseMessage` classes (e.g. `SystemMessage`, `HumanMessage`, `AIMessage`, ...). |
| `include_ids` | `Sequence[str] | None` | Default:`None`  Message IDs to include. |
| `exclude_ids` | `Sequence[str] | None` | Default:`None`  Message IDs to exclude. |
| `exclude_tool_calls` | `Sequence[str] | bool | None` | Default:`None`  Tool call IDs to exclude. Can be one of the following:   - `True`: All `AIMessage` objects with tool calls and all `ToolMessage`   objects will be excluded. - a sequence of tool call IDs to exclude:   - `ToolMessage` objects with the corresponding tool call ID will be     excluded.   - The `tool_calls` in the AIMessage will be updated to exclude     matching tool calls. If all `tool_calls` are filtered from an     AIMessage, the whole message is excluded. |


