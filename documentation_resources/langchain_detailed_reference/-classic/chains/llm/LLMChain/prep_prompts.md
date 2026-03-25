<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm/LLMChain/prep_prompts -->

Methodv1.2.13 (latest)●Since v1.0

# prep\_prompts

Prepare prompts from inputs.


```
prep_prompts(
  self,
  input_list: list[dict[str, Any]],
  run_manager: CallbackManagerForChainRun | None = None
) -> tuple[list[PromptValue], list[str] | None]
```


