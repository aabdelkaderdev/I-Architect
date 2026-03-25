<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/extras -->

Attributev1.2.21 (latest)●Since v1.2

# extras

Optional provider-specific extra fields for the tool.

This is used to pass provider-specific configuration that doesn't fit into
standard tool fields.


```
extras: dict[str, Any] | None = None
```

**Example:**

Anthropic-specific fields like [`cache_control`](https://docs.langchain.com/oss/python/integrations/chat/anthropic#prompt-caching),
[`defer_loading`](https://docs.langchain.com/oss/python/integrations/chat/anthropic#tool-search),
or `input_examples`.

```
@tool(extras={"defer_loading": True, "cache_control": {"type": "ephemeral"}})
def my_tool(x: str) -> str:
    return x
```


