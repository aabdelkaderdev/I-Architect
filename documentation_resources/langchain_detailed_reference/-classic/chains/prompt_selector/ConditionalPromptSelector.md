<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/prompt_selector/ConditionalPromptSelector -->

Classv1.2.13 (latest)●Since v1.0

# ConditionalPromptSelector

Prompt collection that goes through conditionals.


```
ConditionalPromptSelector()
```

## Bases

`BasePromptSelector`

## Attributes

[attribute

default\_prompt: BasePromptTemplate

Default prompt to use if no conditionals match.](/python/langchain-classic/chains/prompt_selector/ConditionalPromptSelector/default_prompt)[attribute

conditionals: list[tuple[Callable[[BaseLanguageModel], bool], BasePromptTemplate]]

List of conditionals and prompts to use if the conditionals match.](/python/langchain-classic/chains/prompt_selector/ConditionalPromptSelector/conditionals)

## Methods

[method

get\_prompt

Get default prompt for a language model.](/python/langchain-classic/chains/prompt_selector/ConditionalPromptSelector/get_prompt)


