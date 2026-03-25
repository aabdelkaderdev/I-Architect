<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/base/BaseQAWithSourcesChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Construct the chain from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  document_prompt: BasePromptTemplate = EXAMPLE_PROMPT,
  question_prompt: BasePromptTemplate = QUESTION_PROMPT,
  combine_prompt: BasePromptTemplate = COMBINE_PROMPT,
  **kwargs: Any = {}
) -> BaseQAWithSourcesChain
```


