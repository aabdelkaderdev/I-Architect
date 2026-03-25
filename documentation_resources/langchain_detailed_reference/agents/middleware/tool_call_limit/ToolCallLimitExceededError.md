<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError -->

Classv1.2.13 (latest)●Since v1.0

# ToolCallLimitExceededError

Exception raised when tool call limits are exceeded.

This exception is raised when the configured exit behavior is `'error'` and either
the thread or run tool call limit has been exceeded.


```
ToolCallLimitExceededError(
  self,
  thread_count: int,
  run_count: int,
  thread_limit: int | None,
  run_limit: int | None,
  tool_name: str | None = None
)
```

## Bases

`Exception`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `thread_count`\* | `int` | Current thread tool call count. |
| `run_count`\* | `int` | Current run tool call count. |
| `thread_limit`\* | `int | None` | Thread tool call limit (if set). |
| `run_limit`\* | `int | None` | Run tool call limit (if set). |
| `tool_name` | `str | None` | Default:`None`  Tool name being limited (if specific tool), or None for all tools. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| thread\_count | [int](https://docs.python.org/3/library/functions.html#int) |
| run\_count | [int](https://docs.python.org/3/library/functions.html#int) |
| thread\_limit | [int](https://docs.python.org/3/library/functions.html#int) | None |
| run\_limit | [int](https://docs.python.org/3/library/functions.html#int) | None |
| tool\_name | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |

## Attributes

[attribute

thread\_count: thread\_count](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError/thread_count)[attribute

run\_count: run\_count](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError/run_count)[attribute

thread\_limit: thread\_limit](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError/thread_limit)[attribute

run\_limit: run\_limit](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError/run_limit)[attribute

tool\_name: tool\_name](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError/tool_name)


