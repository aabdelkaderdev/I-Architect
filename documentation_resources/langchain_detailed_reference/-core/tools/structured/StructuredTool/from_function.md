<!-- Source: https://reference.langchain.com/python/langchain-core/tools/structured/StructuredTool/from_function -->

Methodv1.2.21 (latest)●Since v0.2

# from\_function

Create tool from a given function.

A classmethod that helps to create a tool from a function.


```
from_function(
  cls,
  func: Callable | None = None,
  coroutine: Callable[..., Awaitable[Any]] | None = None,
  name: str | None = None,
  description: str | None = None,
  return_direct: bool = False,
  args_schema: ArgsSchema | None = None,
  infer_schema: bool = True,
  *,
  response_format: Literal['content', 'content_and_artifact'] = 'content',
  parse_docstring: bool = False,
  error_on_invalid_docstring: bool = False,
  **kwargs: Any = {}
) -> StructuredTool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `func` | `Callable | None` | Default:`None`  The function from which to create a tool. |
| `coroutine` | `Callable[..., Awaitable[Any]] | None` | Default:`None`  The async function from which to create a tool. |
| `name` | `str | None` | Default:`None`  The name of the tool.  Defaults to the function name. |
| `description` | `str | None` | Default:`None`  The description of the tool.  Defaults to the function docstring. |
| `return_direct` | `bool` | Default:`False`  Whether to return the result directly or as a callback. |
| `args_schema` | `ArgsSchema | None` | Default:`None`  The schema of the tool's input arguments. |
| `infer_schema` | `bool` | Default:`True`  Whether to infer the schema from the function's signature. |
| `response_format` | `Literal['content', 'content_and_artifact']` | Default:`'content'`  The tool response format.  If `'content'` then the output of the tool is interpreted as the contents of a `ToolMessage`. If `'content_and_artifact'` then the output is expected to be a two-tuple corresponding to the `(content, artifact)` of a `ToolMessage`. |
| `parse_docstring` | `bool` | Default:`False`  If `infer_schema` and `parse_docstring`, will attempt to parse parameter descriptions from Google Style function docstrings. |
| `error_on_invalid_docstring` | `bool` | Default:`False`  if `parse_docstring` is provided, configure whether to raise `ValueError` on invalid Google Style docstrings. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the tool |


