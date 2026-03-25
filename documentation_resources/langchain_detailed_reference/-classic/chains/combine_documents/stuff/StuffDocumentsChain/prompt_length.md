<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain/prompt_length -->

Methodv1.2.13 (latest)●Since v1.0

# prompt\_length

Return the prompt length given the documents passed in.

This can be used by a caller to determine whether passing in a list
of documents would exceed a certain prompt length. This useful when
trying to ensure that the size of a prompt remains below a certain
context limit.


```
prompt_length(
  self,
  docs: list[Document],
  **kwargs: Any = {}
) -> int | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | a list of documents to use to calculate the total prompt length. |
| `**kwargs` | `Any` | Default:`{}`  additional parameters to use to get inputs to LLMChain. |


