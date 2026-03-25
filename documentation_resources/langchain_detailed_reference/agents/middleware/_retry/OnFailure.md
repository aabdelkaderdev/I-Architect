<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_retry/OnFailure -->

Typev1.2.13 (latest)●Since v1.1

# OnFailure

Type for specifying failure handling behavior.

Can be either:

- A literal action string (`'error'` or `'continue'`)
  - `'error'`: Re-raise the exception, stopping agent execution.
  - `'continue'`: Inject a message with the error details, allowing the agent to continue.
    For tool retries, a `ToolMessage` with the error details will be injected.
    For model retries, an `AIMessage` with the error details will be returned.
- A callable that takes an exception and returns a string for error message content


```
OnFailure = Literal['error', 'continue'] | Callable[[Exception], str]
```


