<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/ToolException -->

Classv1.2.21 (latest)●Since v0.2

# ToolException

Exception thrown when a tool execution error occurs.

This exception allows tools to signal errors without stopping the agent.

The error is handled according to the tool's `handle_tool_error` setting, and the
result is returned as an observation to the agent.


```
ToolException()
```

## Bases

`Exception`


