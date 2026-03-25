<!-- Source: https://reference.langchain.com/python/langchain-classic/model_laboratory/ModelLaboratory/compare -->

Methodv1.2.13 (latest)●Since v1.0

# compare

Compare model outputs on an input text.

If a prompt was provided with starting the laboratory, then this text will be
fed into the prompt. If no prompt was provided, then the input text is the
entire prompt.


```
compare(
    self,
    text: str,
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | input text to run all models on. |


