<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/llm_result/LLMResult/flatten -->

Methodv1.2.21 (latest)●Since v0.1

# flatten

Flatten generations into a single list.

Unpack `list[list[Generation]] -> list[LLMResult]` where each returned
`LLMResult` contains only a single `Generation`. If token usage information is
available, it is kept only for the `LLMResult` corresponding to the top-choice
`Generation`, to avoid over-counting of token usage downstream.


```
flatten(
    self,
) -> list[LLMResult]
```


