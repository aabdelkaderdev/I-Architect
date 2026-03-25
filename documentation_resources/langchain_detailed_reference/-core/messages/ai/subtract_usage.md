<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/subtract_usage -->

Functionv1.2.21 (latest)●Since v0.3

# subtract\_usage

Recursively subtract two `UsageMetadata` objects.

Token counts cannot be negative so the actual operation is `max(left - right, 0)`.


```
subtract_usage(
    left: UsageMetadata | None,
    right: UsageMetadata | None,
) -> UsageMetadata
```

**Example:**

```
from langchain_core.messages.ai import subtract_usage

left = UsageMetadata(
    input_tokens=5,
    output_tokens=10,
    total_tokens=15,
    input_token_details=InputTokenDetails(cache_read=4),
)
right = UsageMetadata(
    input_tokens=3,
    output_tokens=8,
    total_tokens=11,
    output_token_details=OutputTokenDetails(reasoning=4),
)

subtract_usage(left, right)
```

results in

```
UsageMetadata(
    input_tokens=2,
    output_tokens=2,
    total_tokens=4,
    input_token_details=InputTokenDetails(cache_read=4),
    output_token_details=OutputTokenDetails(reasoning=0),
)
```

Args:
left: The first `UsageMetadata` object.
right: The second `UsageMetadata` object.


