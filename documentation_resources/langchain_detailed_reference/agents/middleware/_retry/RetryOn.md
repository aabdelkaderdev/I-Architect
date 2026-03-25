<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_retry/RetryOn -->

Typev1.2.13 (latest)●Since v1.1

# RetryOn

Type for specifying which exceptions to retry on.

Can be either:

- A tuple of exception types to retry on (based on `isinstance` checks)
- A callable that takes an exception and returns `True` if it should be retried


```
RetryOn = tuple[type[Exception], ...] | Callable[[Exception], bool]
```


