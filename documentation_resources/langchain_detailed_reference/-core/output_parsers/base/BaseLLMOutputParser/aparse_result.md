<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/base/BaseLLMOutputParser/aparse_result -->

Methodv1.2.21 (latest)●Since v0.1

# aparse\_result

Parse a list of candidate model `Generation` objects into a specific format.


```
aparse_result(
  self,
  result: list[Generation],
  *,
  partial: bool = False
) -> T
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `result`\* | `list[Generation]` | A list of `Generation` to be parsed.  The Generations are assumed to be different candidate outputs for a single model input. |
| `partial` | `bool` | Default:`False`  Whether to parse the output as a partial result.  This is useful for parsers that can parse partial results. |


