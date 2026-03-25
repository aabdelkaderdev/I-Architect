<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/base/BaseOutputParser/parse_result -->

Methodv1.2.21 (latest)●Since v0.1

# parse\_result

Parse a list of candidate model `Generation` objects into a specific format.

The return value is parsed from only the first `Generation` in the result, which
is assumed to be the highest-likelihood `Generation`.


```
parse_result(
  self,
  result: list[Generation],
  *,
  partial: bool = False
) -> T
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `result`\* | `list[Generation]` | A list of `Generation` to be parsed.  The `Generation` objects are assumed to be different candidate outputs for a single model input. |
| `partial` | `bool` | Default:`False`  Whether to parse the output as a partial result.  This is useful for parsers that can parse partial results. |


