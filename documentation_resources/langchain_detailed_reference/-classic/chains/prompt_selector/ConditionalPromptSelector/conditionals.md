<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/prompt_selector/ConditionalPromptSelector/conditionals -->

Attributev1.2.13 (latest)●Since v1.0

# conditionals

List of conditionals and prompts to use if the conditionals match.


```
conditionals: list[tuple[Callable[[BaseLanguageModel], bool], BasePromptTemplate]] = Field(
  default_factory=list
)
```


