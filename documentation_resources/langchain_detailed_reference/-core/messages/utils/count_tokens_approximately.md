<!-- Source: https://reference.langchain.com/python/langchain-core/messages/utils/count_tokens_approximately -->

Functionv1.2.21 (latest)●Since v0.3

# count\_tokens\_approximately

Approximate the total number of tokens in messages.

The token count includes stringified message content, role, and (optionally) name.

- For AI messages, the token count also includes stringified tool calls.
- For tool messages, the token count also includes the tool call ID.
- For multimodal messages with images, applies a fixed token penalty per image
  instead of counting base64-encoded characters.
- If tools are provided, the token count also includes stringified tool schemas.


```
count_tokens_approximately(
  messages: Iterable[MessageLikeRepresentation],
  *,
  chars_per_token: float = 4.0,
  extra_tokens_per_message: float = 3.0,
  count_name: bool = True,
  tokens_per_image: int = 85,
  use_usage_metadata_scaling: bool = False,
  tools: list[BaseTool | dict[str, Any]] | None = None
) -> int
```

**Note:**

This is a simple approximation that may not match the exact token count used by
specific models. For accurate counts, use model-specific tokenizers.

For multimodal messages containing images, a fixed token penalty is applied
per image instead of counting base64-encoded characters, which provides a
more realistic approximation.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `Iterable[MessageLikeRepresentation]` | List of messages to count tokens for. |
| `chars_per_token` | `float` | Default:`4.0`  Number of characters per token to use for the approximation. One token corresponds to ~4 chars for common English text. You can also specify `float` values for more fine-grained control. [See more here](https://platform.openai.com/tokenizer). |
| `extra_tokens_per_message` | `float` | Default:`3.0`  Number of extra tokens to add per message, e.g. special tokens, including beginning/end of message. You can also specify `float` values for more fine-grained control. [See more here](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb). |
| `count_name` | `bool` | Default:`True`  Whether to include message names in the count. |
| `tokens_per_image` | `int` | Default:`85`  Fixed token cost per image (default: 85, aligned with OpenAI's low-resolution image token cost). |
| `use_usage_metadata_scaling` | `bool` | Default:`False`  If True, and all AI messages have consistent `response_metadata['model_provider']`, scale the approximate token count using the **most recent** AI message that has `usage_metadata['total_tokens']`. The scaling factor is: `AI_total_tokens / approx_tokens_up_to_that_AI_message` |
| `tools` | `list[BaseTool | dict[str, Any]] | None` | Default:`None`  List of tools to include in the token count. Each tool can be either a `BaseTool` instance or a dict representing a tool schema. `BaseTool` instances are converted to OpenAI tool format before counting. |


