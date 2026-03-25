<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_extraction\_chain

Creates a chain that extracts information from a passage.


```
create_extraction_chain(
  schema: dict,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate | None = None,
  tags: list[str] | None = None,
  verbose: bool = False
) -> Chain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `schema`\* | `dict` | The schema of the entities to extract. |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  The prompt to use for extraction. |
| `tags` | `list[str] | None` | Default:`None`  Optional list of tags to associate with the chain. |
| `verbose` | `bool` | Default:`False`  Whether to run in verbose mode. In verbose mode, some intermediate logs will be printed to the console. |


