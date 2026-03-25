<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/multi_prompt/MultiPromptChain/from_prompts -->

Methodv1.2.13 (latest)●Since v1.0

# from\_prompts

Convenience constructor for instantiating from destination prompts.


```
from_prompts(
  cls,
  llm: BaseLanguageModel,
  prompt_infos: list[dict[str, str]],
  default_chain: Chain | None = None,
  **kwargs: Any = {}
) -> MultiPromptChain
```


