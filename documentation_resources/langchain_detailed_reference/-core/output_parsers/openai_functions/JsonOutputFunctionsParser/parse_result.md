<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_functions/JsonOutputFunctionsParser/parse_result -->

Methodv1.2.21 (latest)●Since v0.1

# parse\_result

Parse the result of an LLM call to a JSON object.


```
parse_result(
  self,
  result: list[Generation],
  *,
  partial: bool = False
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `result`\* | `list[Generation]` | The result of the LLM call. |
| `partial` | `bool` | Default:`False`  Whether to parse partial JSON objects. |


