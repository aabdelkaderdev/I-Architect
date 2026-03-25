<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/xml/base/XMLAgent -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# XMLAgent

Agent that uses XML tags.


```
XMLAgent()
```

## Bases

`BaseSingleActionAgent`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `unknown` | list of tools the agent can choose from |
| `llm_chain`\* | `unknown` | The LLMChain to call to predict the next action |

## Attributes

[attribute

tools: list[BaseTool]

List of tools this agent has access to.](/python/langchain-classic/agents/xml/base/XMLAgent/tools)[attribute

llm\_chain: LLMChain

Chain to use to predict action.](/python/langchain-classic/agents/xml/base/XMLAgent/llm_chain)[attribute

input\_keys: list[str]](/python/langchain-classic/agents/xml/base/XMLAgent/input_keys)

## Methods

[method

get\_default\_prompt

Return the default prompt for the XML agent.](/python/langchain-classic/agents/xml/base/XMLAgent/get_default_prompt)[method

get\_default\_output\_parser

Return an XMLAgentOutputParser.](/python/langchain-classic/agents/xml/base/XMLAgent/get_default_output_parser)[method

plan](/python/langchain-classic/agents/xml/base/XMLAgent/plan)[method

aplan](/python/langchain-classic/agents/xml/base/XMLAgent/aplan)

## Inherited from[BaseSingleActionAgent](/python/langchain-classic/agents/agent/BaseSingleActionAgent)

### Attributes

[Areturn\_values: list[str]

—

Return values of the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_values)

### Methods

[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/get_allowed_tools)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_stopped_response)[Mfrom\_llm\_and\_tools

—

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/from_llm_and_tools)[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/dict)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/tool_run_logging_kwargs)


