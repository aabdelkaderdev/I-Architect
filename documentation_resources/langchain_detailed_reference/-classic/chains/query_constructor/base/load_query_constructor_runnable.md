<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/base/load_query_constructor_runnable -->

Functionv1.2.13 (latest)●Since v1.0

# load\_query\_constructor\_runnable

Load a query constructor runnable chain.


```
load_query_constructor_runnable(
  llm: BaseLanguageModel,
  document_contents: str,
  attribute_info: Sequence[AttributeInfo | dict],
  *,
  examples: Sequence | None = None,
  allowed_comparators: Sequence[Comparator] = tuple(Comparator),
  allowed_operators: Sequence[Operator] = tuple(Operator),
  enable_limit: bool = False,
  schema_prompt: BasePromptTemplate | None = None,
  fix_invalid: bool = False,
  **kwargs: Any = {}
) -> Runnable
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | BaseLanguageModel to use for the chain. |
| `document_contents`\* | `str` | Description of the page contents of the document to be queried. |
| `attribute_info`\* | `Sequence[AttributeInfo | dict]` | Sequence of attributes in the document. |
| `examples` | `Sequence | None` | Default:`None`  Optional list of examples to use for the chain. |
| `allowed_comparators` | `Sequence[Comparator]` | Default:`tuple(Comparator)`  Sequence of allowed comparators. Defaults to all `Comparator` objects. |
| `allowed_operators` | `Sequence[Operator]` | Default:`tuple(Operator)`  Sequence of allowed operators. Defaults to all `Operator` objects. |
| `enable_limit` | `bool` | Default:`False`  Whether to enable the limit operator. |
| `schema_prompt` | `BasePromptTemplate | None` | Default:`None`  Prompt for describing query schema. Should have string input variables allowed\_comparators and allowed\_operators. |
| `fix_invalid` | `bool` | Default:`False`  Whether to fix invalid filter directives by ignoring invalid operators, comparators and attributes. |
| `kwargs` | `Any` | Default:`{}`  Additional named params to pass to FewShotPromptTemplate init. |


