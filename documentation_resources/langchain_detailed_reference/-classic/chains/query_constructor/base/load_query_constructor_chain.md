<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/base/load_query_constructor_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# load\_query\_constructor\_chain

Load a query constructor chain.


```
load_query_constructor_chain(
  llm: BaseLanguageModel,
  document_contents: str,
  attribute_info: Sequence[AttributeInfo | dict],
  examples: list | None = None,
  allowed_comparators: Sequence[Comparator] = tuple(Comparator),
  allowed_operators: Sequence[Operator] = tuple(Operator),
  enable_limit: bool = False,
  schema_prompt: BasePromptTemplate | None = None,
  **kwargs: Any = {}
) -> LLMChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | BaseLanguageModel to use for the chain. |
| `document_contents`\* | `str` | The contents of the document to be queried. |
| `attribute_info`\* | `Sequence[AttributeInfo | dict]` | Sequence of attributes in the document. |
| `examples` | `list | None` | Default:`None`  Optional list of examples to use for the chain. |
| `allowed_comparators` | `Sequence[Comparator]` | Default:`tuple(Comparator)`  Sequence of allowed comparators. Defaults to all `Comparator` objects. |
| `allowed_operators` | `Sequence[Operator]` | Default:`tuple(Operator)`  Sequence of allowed operators. Defaults to all `Operator` objects. |
| `enable_limit` | `bool` | Default:`False`  Whether to enable the limit operator. |
| `schema_prompt` | `BasePromptTemplate | None` | Default:`None`  Prompt for describing query schema. Should have string input variables allowed\_comparators and allowed\_operators. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary named params to pass to LLMChain. |


