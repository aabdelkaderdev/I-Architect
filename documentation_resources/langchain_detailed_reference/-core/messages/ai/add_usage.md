<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/add_usage -->

Functionv1.2.21 (latest)●Since v0.3

# add\_usage

Recursively add two UsageMetadata objects.


```
add_usage(
    left: UsageMetadata | None,
    right: UsageMetadata | None,
) -> UsageMetadata
```

**Example:**

```
from langchain_core.messages.ai import add_usage

left = UsageMetadata(
    input_tokens=5,
    output_tokens=0,
    total_tokens=5,
    input_token_details=InputTokenDetails(cache_read=3),
)
right = UsageMetadata(
    input_tokens=0,
    output_tokens=10,
    total_tokens=10,
    output_token_details=OutputTokenDetails(reasoning=4),
)

add_usage(left, right)
```

results in

```
UsageMetadata(
    input_tokens=5,
    output_tokens=10,
    total_tokens=15,
    input_token_details=InputTokenDetails(cache_read=3),
    output_token_details=OutputTokenDetails(reasoning=4),
)
```

Args:
left: The first `UsageMetadata` object.
right: The second `UsageMetadata` object.


