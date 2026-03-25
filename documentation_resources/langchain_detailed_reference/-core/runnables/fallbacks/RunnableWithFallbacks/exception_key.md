<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/exception_key -->

Attributev1.2.21 (latest)●Since v0.1

# exception\_key

If `string` is specified then handled exceptions will be passed to fallbacks as
part of the input under the specified key.

If `None`, exceptions will not be passed to fallbacks.

If used, the base `Runnable` and its fallbacks must accept a dictionary as input.


```
exception_key: str | None = None
```


