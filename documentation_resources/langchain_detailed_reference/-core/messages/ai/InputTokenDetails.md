<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/InputTokenDetails -->

Classv1.2.21 (latest)●Since v0.3

# InputTokenDetails


```
InputTokenDetails()
```

## Bases

`TypedDict`

## Constructors

## Attributes



constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| audio | [int](https://docs.python.org/3/library/functions.html#int) |
| cache\_creation | [int](https://docs.python.org/3/library/functions.html#int) |
| cache\_read | [int](https://docs.python.org/3/library/functions.html#int) |

[attribute

audio: int

Audio input tokens.](/python/langchain-core/messages/ai/InputTokenDetails/audio)

[attribute

cache\_creation: int

Input tokens that were cached and there was a cache miss.

Since there was a cache miss, the cache was created from these tokens.](/python/langchain-core/messages/ai/InputTokenDetails/cache_creation)

[attribute

cache\_read: int

Input tokens that were cached and there was a cache hit.

Since there was a cache hit, the tokens were read from the cache. More precisely,
the model state given these tokens was read from the cache.](/python/langchain-core/messages/ai/InputTokenDetails/cache_read)

Breakdown of input token counts.

Does *not* need to sum to full input token count. Does *not* need to have all keys.

**Example:**

```
{
    "audio": 10,
    "cache_creation": 200,
    "cache_read": 100,
}
```

May also hold extra provider-specific keys.