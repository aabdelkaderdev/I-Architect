<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_sources_chain -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_qa\_with\_sources\_chain

Create a question answering chain that returns an answer with sources.


```
create_qa_with_sources_chain(
  llm: BaseLanguageModel,
  verbose: bool = False,
  **kwargs: Any = {}
) -> LLMChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | Language model to use for the chain. |
| `verbose` | `bool` | Default:`False`  Whether to print the details of the chain |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to pass to `create_qa_with_structure_chain`. |


