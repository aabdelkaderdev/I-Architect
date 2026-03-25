<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/retry/RunnableRetry/retry_exception_types -->

Attributev1.2.21 (latest)●Since v0.1

# retry\_exception\_types

The exception types to retry on. By default all exceptions are retried.

In general you should only retry on exceptions that are likely to be
transient, such as network errors.

Good exceptions to retry are all server errors (5xx) and selected client
errors (4xx) such as 429 Too Many Requests.


```
retry_exception_types: tuple[type[BaseException], ...] = (Exception,)
```


