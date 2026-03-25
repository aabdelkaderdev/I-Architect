<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ExitBehavior -->

Attributev1.2.13 (latest)●Since v1.0

# ExitBehavior

How to handle execution when tool call limits are exceeded.

- `'continue'`: Block exceeded tools with error messages, let other tools continue
  (default)
- `'error'`: Raise a `ToolCallLimitExceededError` exception
- `'end'`: Stop execution immediately, injecting a `ToolMessage` and an `AIMessage` for
  the single tool call that exceeded the limit. Raises `NotImplementedError` if there
  are other pending tool calls (due to parallel tool calling).


```
ExitBehavior = Literal['continue', 'error', 'end']
```


