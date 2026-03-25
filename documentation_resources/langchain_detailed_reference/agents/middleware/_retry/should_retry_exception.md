<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_retry/should_retry_exception -->

Functionv1.2.13 (latest)●Since v1.1

# should\_retry\_exception

Check if an exception should trigger a retry.


```
should_retry_exception(
    exc: Exception,
    retry_on: RetryOn,
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `exc`\* | `Exception` | The exception that occurred. |
| `retry_on`\* | `RetryOn` | Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried. |


