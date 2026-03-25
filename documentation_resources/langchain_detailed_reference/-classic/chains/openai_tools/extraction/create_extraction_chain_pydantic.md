<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_tools/extraction/create_extraction_chain_pydantic -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_extraction\_chain\_pydantic

Creates a chain that extracts information from a passage.


```
create_extraction_chain_pydantic(
  pydantic_schemas: list[type[BaseModel]] | type[BaseModel],
  llm: BaseLanguageModel,
  system_message: str = _EXTRACTION_TEMPLATE
) -> Runnable
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pydantic_schemas`\* | `list[type[BaseModel]] | type[BaseModel]` | The schema of the entities to extract. |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `system_message` | `str` | Default:`_EXTRACTION_TEMPLATE`  The system message to use for extraction. |


