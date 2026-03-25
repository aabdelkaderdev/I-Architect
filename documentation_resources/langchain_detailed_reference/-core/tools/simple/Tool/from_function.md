<!-- Source: https://reference.langchain.com/python/langchain-core/tools/simple/Tool/from_function -->

Methodv1.2.21 (latest)●Since v0.2

# from\_function

Initialize tool from a function.


```
from_function(
  cls,
  func: Callable | None,
  name: str,
  description: str,
  return_direct: bool = False,
  args_schema: ArgsSchema | None = None,
  coroutine: Callable[..., Awaitable[Any]] | None = None,
  **kwargs: Any = {}
) -> Tool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `func`\* | `Callable | None` | The function to create the tool from. |
| `name`\* | `str` | The name of the tool. |
| `description`\* | `str` | The description of the tool. |
| `return_direct` | `bool` | Default:`False`  Whether to return the output directly. |
| `args_schema` | `ArgsSchema | None` | Default:`None`  The schema of the tool's input arguments. |
| `coroutine` | `Callable[..., Awaitable[Any]] | None` | Default:`None`  The asynchronous version of the function. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the tool. |


