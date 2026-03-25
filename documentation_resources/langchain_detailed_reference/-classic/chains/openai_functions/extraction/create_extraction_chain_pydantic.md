<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain_pydantic -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_extraction\_chain\_pydantic

Creates a chain that extracts information from a passage using Pydantic schema.


```
create_extraction_chain_pydantic(
  pydantic_schema: Any,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate | None = None,
  verbose: bool = False
) -> Chain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pydantic_schema`\* | `Any` | The Pydantic schema of the entities to extract. |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  The prompt to use for extraction. |
| `verbose` | `bool` | Default:`False`  Whether to run in verbose mode. In verbose mode, some intermediate logs will be printed to the console. |


