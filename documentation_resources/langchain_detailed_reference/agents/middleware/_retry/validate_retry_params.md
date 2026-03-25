<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_retry/validate_retry_params -->

Functionv1.2.13 (latest)●Since v1.1

# validate\_retry\_params

Validate retry parameters.


```
validate_retry_params(
  max_retries: int,
  initial_delay: float,
  max_delay: float,
  backoff_factor: float
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `max_retries`\* | `int` | Maximum number of retry attempts. |
| `initial_delay`\* | `float` | Initial delay in seconds before first retry. |
| `max_delay`\* | `float` | Maximum delay in seconds between retries. |
| `backoff_factor`\* | `float` | Multiplier for exponential backoff. |


