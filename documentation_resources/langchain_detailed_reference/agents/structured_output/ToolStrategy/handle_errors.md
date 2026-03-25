<!-- Source: https://reference.langchain.com/python/langchain/agents/structured_output/ToolStrategy/handle_errors -->

Attributev1.2.13 (latest)●Since v0.3

# handle\_errors

Error handling strategy for structured output via `ToolStrategy`.

- `True`: Catch all errors with default error template
- `str`: Catch all errors with this custom message
- `type[Exception]`: Only catch this exception type with default message
- `tuple[type[Exception], ...]`: Only catch these exception types with default
  message
- `Callable[[Exception], str]`: Custom function that returns error message
- `False`: No retry, let exceptions propagate


```
handle_errors: bool | str | type[Exception] | tuple[type[Exception], ...] | Callable[[Exception], str] = handle_errors
```


