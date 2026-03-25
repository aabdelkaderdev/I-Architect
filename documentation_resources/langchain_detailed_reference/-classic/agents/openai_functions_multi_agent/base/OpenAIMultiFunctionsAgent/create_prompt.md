<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/create_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# create\_prompt

Create prompt for this agent.


```
create_prompt(
  cls,
  system_message: SystemMessage | None = _NOT_SET,
  extra_prompt_messages: list[BaseMessagePromptTemplate] | None = None
) -> BasePromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `system_message` | `SystemMessage | None` | Default:`_NOT_SET`  Message to use as the system message that will be the first in the prompt. |
| `extra_prompt_messages` | `list[BaseMessagePromptTemplate] | None` | Default:`None`  Prompt messages that will be placed between the system message and the new human input. |


