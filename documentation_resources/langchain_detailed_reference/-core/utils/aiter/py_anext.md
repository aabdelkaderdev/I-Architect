<!-- Source: https://reference.langchain.com/python/langchain-core/utils/aiter/py_anext -->

Functionv1.2.21 (latest)●Since v0.1Deprecated

# py\_anext

Pure-Python implementation of `anext()` for testing purposes.

Closely matches the builtin `anext()` C implementation.

Can be used to compare the built-in implementation of the inner coroutines machinery
to C-implementation of `__anext__()` and `send()` or `throw()` on the returned
generator.


```
py_anext(
  iterator: AsyncIterator[T],
  default: T | Any = _no_default
) -> Awaitable[T | Any | None]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `iterator`\* | `AsyncIterator[T]` | The async iterator to advance. |
| `default` | `T | Any` | Default:`_no_default`  The value to return if the iterator is exhausted.  If not provided, a `StopAsyncIteration` exception is raised. |


