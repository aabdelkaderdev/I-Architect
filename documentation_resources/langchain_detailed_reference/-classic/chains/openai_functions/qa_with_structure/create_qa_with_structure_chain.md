<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_structure_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_qa\_with\_structure\_chain

Create a question answering chain with structure.

Create a question answering chain that returns an answer with sources
based on schema.


```
create_qa_with_structure_chain(
  llm: BaseLanguageModel,
  schema: dict | type[BaseModel],
  output_parser: str = 'base',
  prompt: PromptTemplate | ChatPromptTemplate | None = None,
  verbose: bool = False
) -> LLMChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | Language model to use for the chain. |
| `schema`\* | `dict | type[BaseModel]` | Pydantic schema to use for the output. |
| `output_parser` | `str` | Default:`'base'`  Output parser to use. Should be one of `'pydantic'` or `'base'`. |
| `prompt` | `PromptTemplate | ChatPromptTemplate | None` | Default:`None`  Optional prompt to use for the chain. |
| `verbose` | `bool` | Default:`False`  Whether to run the chain in verbose mode. |


