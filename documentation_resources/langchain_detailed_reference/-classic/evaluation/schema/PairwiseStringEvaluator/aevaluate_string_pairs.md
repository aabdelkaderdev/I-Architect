<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator/aevaluate_string_pairs -->

Methodv1.2.13 (latest)●Since v1.0

# aevaluate\_string\_pairs

Asynchronously evaluate the output string pairs.


```
aevaluate_string_pairs(
  self,
  *,
  prediction: str,
  prediction_b: str,
  reference: str | None = None,
  input: str | None = None,
  **kwargs: Any = {}
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prediction`\* | `str` | The output string from the first model. |
| `prediction_b`\* | `str` | The output string from the second model. |
| `reference` | `str | None` | Default:`None`  The expected output / reference string. |
| `input` | `str | None` | Default:`None`  The input string. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments, such as callbacks and optional reference strings. |


