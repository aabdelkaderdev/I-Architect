<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/ModelCallResult -->

Typev1.2.13 (latest)●Since v1.0

# ModelCallResult

`TypeAlias` for model call handler return value.

Middleware can return either:

- `ModelResponse`: Full response with messages and optional structured output
- `AIMessage`: Simplified return for simple use cases
- `ExtendedModelResponse`: Response with an optional `Command` for additional state updates
  `goto`, `resume`, and `graph` are not yet supported on these commands.
  A `NotImplementedError` will be raised if you try to use them.


```
ModelCallResult: TypeAlias = 'ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]'
```


