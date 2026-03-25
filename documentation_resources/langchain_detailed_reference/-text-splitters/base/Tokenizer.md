<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/Tokenizer -->

Classv1.1.1 (latest)●Since v0.0

# Tokenizer

Tokenizer data class.


```
Tokenizer(
  self,
  chunk_overlap: int,
  tokens_per_chunk: int,
  decode: Callable[[list[int]], str],
  encode: Callable[[str], list[int]]
)
```

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| chunk\_overlap | [int](https://docs.python.org/3/library/functions.html#int) |
| tokens\_per\_chunk | [int](https://docs.python.org/3/library/functions.html#int) |
| decode | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[list](https://docs.python.org/3/library/stdtypes.html#list)[[int](https://docs.python.org/3/library/functions.html#int)]], [str](https://docs.python.org/3/library/stdtypes.html#str)] |
| encode | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[str](https://docs.python.org/3/library/stdtypes.html#str)], [list](https://docs.python.org/3/library/stdtypes.html#list)[[int](https://docs.python.org/3/library/functions.html#int)]] |

## Attributes

[attribute

chunk\_overlap: int

Overlap in tokens between chunks](/python/langchain-text-splitters/base/Tokenizer/chunk_overlap)[attribute

tokens\_per\_chunk: int

Maximum number of tokens per chunk](/python/langchain-text-splitters/base/Tokenizer/tokens_per_chunk)[attribute

decode: Callable[[list[int]], str]

Function to decode a list of token IDs to a string](/python/langchain-text-splitters/base/Tokenizer/decode)[attribute

encode: Callable[[str], list[int]]

Function to encode a string to a list of token IDs](/python/langchain-text-splitters/base/Tokenizer/encode)


