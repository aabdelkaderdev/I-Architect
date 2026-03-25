<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a LLMListwiseRerank document compressor from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  *,
  prompt: BasePromptTemplate | None = None,
  **kwargs: Any = {}
) -> LLMListwiseRerank
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use for filtering. **Must implement BaseLanguageModel.with\_structured\_output().** |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  The prompt to use for the filter. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the constructor. |


