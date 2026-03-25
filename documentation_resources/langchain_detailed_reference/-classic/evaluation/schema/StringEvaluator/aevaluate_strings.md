<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings -->

Methodv1.2.13 (latest)●Since v1.0

# aevaluate\_strings

Asynchronously evaluate Chain or LLM output, based on optional input and label.


```
aevaluate_strings(
  self,
  *,
  prediction: str,
  reference: str | None = None,
  input: str | None = None,
  **kwargs: Any = {}
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prediction`\* | `str` | The LLM or chain prediction to evaluate. |
| `reference` | `str | None` | Default:`None`  The reference label to evaluate against. |
| `input` | `str | None` | Default:`None`  The input to consider during evaluation. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments, including callbacks, tags, etc. |


