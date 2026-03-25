<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# OpenAIMultiFunctionsAgent

Agent driven by OpenAIs function powered API.


```
OpenAIMultiFunctionsAgent()
```

## Bases

`BaseMultiActionAgent`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `unknown` | This should be an instance of ChatOpenAI, specifically a model that supports using `functions`. |
| `tools`\* | `unknown` | The tools this agent has access to. |
| `prompt`\* | `unknown` | The prompt for this agent, should support agent\_scratchpad as one of the variables. For an easy way to construct this prompt, use `OpenAIMultiFunctionsAgent.create_prompt(...)` |

## Attributes

[attribute

llm: BaseLanguageModel](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/llm)[attribute

tools: Sequence[BaseTool]](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/tools)[attribute

prompt: BasePromptTemplate](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/prompt)[attribute

input\_keys: list[str]

Get input keys. Input refers to user input here.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/input_keys)[attribute

functions: list[dict]

Get the functions for the agent.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/functions)

## Methods

[method

get\_allowed\_tools

Get allowed tools.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/get_allowed_tools)[method

plan

Given input, decided what to do.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/plan)[method

aplan

Async given input, decided what to do.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/aplan)[method

create\_prompt

Create prompt for this agent.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/create_prompt)[method

from\_llm\_and\_tools

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/from_llm_and_tools)

## Inherited from[BaseMultiActionAgent](/python/langchain-classic/agents/agent/BaseMultiActionAgent)

### Attributes

[Areturn\_values: list[str]

—

Return values of the agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_values)

### Methods

[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_stopped_response)[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/dict)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/save)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseMultiActionAgent/tool_run_logging_kwargs)


