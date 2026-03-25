<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/UsageMetadata -->

Classv1.2.21 (latest)●Since v0.2

# UsageMetadata


```
UsageMetadata()
```

## Bases

`TypedDict`

## Constructors

## Attributes



constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| input\_tokens | [int](https://docs.python.org/3/library/functions.html#int) |
| output\_tokens | [int](https://docs.python.org/3/library/functions.html#int) |
| total\_tokens | [int](https://docs.python.org/3/library/functions.html#int) |
| input\_token\_details | NotRequired[[InputTokenDetails](/python/langchain-core/messages/ai/InputTokenDetails)] |
| output\_token\_details | NotRequired[[OutputTokenDetails](/python/langchain-core/messages/ai/OutputTokenDetails)] |

[attribute

input\_tokens: int

Count of input (or prompt) tokens. Sum of all input token types.](/python/langchain-core/messages/ai/UsageMetadata/input_tokens)

[attribute

output\_tokens: int

Count of output (or completion) tokens. Sum of all output token types.](/python/langchain-core/messages/ai/UsageMetadata/output_tokens)

[attribute

total\_tokens: int

Total token count. Sum of `input_tokens` + `output_tokens`.](/python/langchain-core/messages/ai/UsageMetadata/total_tokens)

[attribute

input\_token\_details: NotRequired[InputTokenDetails]

Breakdown of input token counts.

Does *not* need to sum to full input token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/UsageMetadata/input_token_details)

[attribute

output\_token\_details: NotRequired[OutputTokenDetails]

Breakdown of output token counts.

Does *not* need to sum to full output token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/UsageMetadata/output_token_details)

Usage metadata for a message, such as token counts.

This is a standard representation of token usage that is consistent across models.

**Example:**

```
{
    "input_tokens": 350,
    "output_tokens": 240,
    "total_tokens": 590,
    "input_token_details": {
        "audio": 10,
        "cache_creation": 200,
        "cache_read": 100,
    },
    "output_token_details": {
        "audio": 10,
        "reasoning": 200,
    },
}
```

Behavior changed in `langchain-core` 0.3.9

Added `input_token_details` and `output_token_details`.

LangSmith SDK

The LangSmith SDK also has a `UsageMetadata` class. While the two share fields,
LangSmith's `UsageMetadata` has additional fields to capture cost information
used by the LangSmith platform.