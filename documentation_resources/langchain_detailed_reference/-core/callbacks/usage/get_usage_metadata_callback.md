<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/usage/get_usage_metadata_callback -->

Functionv1.2.21 (latest)●Since v0.3

# get\_usage\_metadata\_callback

Get usage metadata callback.

Get context manager for tracking usage metadata across chat model calls using
[`AIMessage.usage_metadata`](/python/langchain-core/callbacks/usage/UsageMetadataCallbackHandler/usage_metadata).


```
get_usage_metadata_callback(
  name: str = 'usage_metadata_callback'
) -> Generator[UsageMetadataCallbackHandler, None, None]
```

**Example:**

```
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import get_usage_metadata_callback

llm_1 = init_chat_model(model="openai:gpt-4o-mini")
llm_2 = init_chat_model(model="anthropic:claude-haiku-4-5-20251001")

with get_usage_metadata_callback() as cb:
    llm_1.invoke("Hello")
    llm_2.invoke("Hello")
    print(cb.usage_metadata)
```

```
{
    "gpt-4o-mini-2024-07-18": {
        "input_tokens": 8,
        "output_tokens": 10,
        "total_tokens": 18,
        "input_token_details": {"audio": 0, "cache_read": 0},
        "output_token_details": {"audio": 0, "reasoning": 0},
    },
    "claude-haiku-4-5-20251001": {
        "input_tokens": 8,
        "output_tokens": 21,
        "total_tokens": 29,
        "input_token_details": {"cache_read": 0, "cache_creation": 0},
    },
}
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | Default:`'usage_metadata_callback'`  The name of the context variable. |


