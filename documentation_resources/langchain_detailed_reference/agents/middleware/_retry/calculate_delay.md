<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_retry/calculate_delay -->

Functionv1.2.13 (latest)●Since v1.1

# calculate\_delay

Calculate delay for a retry attempt with exponential backoff and optional jitter.


```
calculate_delay(
  retry_number: int,
  *,
  backoff_factor: float,
  initial_delay: float,
  max_delay: float,
  jitter: bool
) -> float
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retry_number`\* | `int` | The retry attempt number (0-indexed). |
| `backoff_factor`\* | `float` | Multiplier for exponential backoff.  Set to `0.0` for constant delay. |
| `initial_delay`\* | `float` | Initial delay in seconds before first retry. |
| `max_delay`\* | `float` | Maximum delay in seconds between retries.  Caps exponential backoff growth. |
| `jitter`\* | `bool` | Whether to add random jitter to delay to avoid thundering herd. |


