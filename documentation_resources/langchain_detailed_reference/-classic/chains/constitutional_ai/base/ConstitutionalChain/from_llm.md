<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a chain from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  chain: LLMChain,
  critique_prompt: BasePromptTemplate = CRITIQUE_PROMPT,
  revision_prompt: BasePromptTemplate = REVISION_PROMPT,
  **kwargs: Any = {}
) -> ConstitutionalChain
```


