<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError -->

Classv1.2.13 (latest)●Since v1.0

# ModelCallLimitExceededError

Exception raised when model call limits are exceeded.

This exception is raised when the configured exit behavior is `'error'` and either
the thread or run model call limit has been exceeded.


```
ModelCallLimitExceededError(
  self,
  thread_count: int,
  run_count: int,
  thread_limit: int | None,
  run_limit: int | None
)
```

## Bases

`Exception`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `thread_count`\* | `int` | Current thread model call count. |
| `run_count`\* | `int` | Current run model call count. |
| `thread_limit`\* | `int | None` | Thread model call limit (if set). |
| `run_limit`\* | `int | None` | Run model call limit (if set). |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| thread\_count | [int](https://docs.python.org/3/library/functions.html#int) |
| run\_count | [int](https://docs.python.org/3/library/functions.html#int) |
| thread\_limit | [int](https://docs.python.org/3/library/functions.html#int) | None |
| run\_limit | [int](https://docs.python.org/3/library/functions.html#int) | None |

## Attributes

[attribute

thread\_count: thread\_count](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError/thread_count)[attribute

run\_count: run\_count](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError/run_count)[attribute

thread\_limit: thread\_limit](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError/thread_limit)[attribute

run\_limit: run\_limit](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError/run_limit)


