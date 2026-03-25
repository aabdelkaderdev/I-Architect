<!-- Source: https://reference.langchain.com/python/langchain-core/rate_limiters/InMemoryRateLimiter/aacquire -->

Methodv1.2.21 (latest)●Since v0.2

# aacquire

Attempt to acquire a token from the rate limiter. Async version.

This method blocks until the required tokens are available if `blocking`
is set to `True`.

If `blocking` is set to `False`, the method will immediately return the result
of the attempt to acquire the tokens.


```
aacquire(
    self,
    *,
    blocking: bool = True,
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `blocking` | `bool` | Default:`True`  If `True`, the method will block until the tokens are available. If `False`, the method will return immediately with the result of the attempt. |


