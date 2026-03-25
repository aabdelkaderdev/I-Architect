<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationalChatAgent

An agent designed to hold a conversation in addition to using tools.


```
ConversationalChatAgent()
```

## Bases

`Agent`

## Attributes

[attribute

output\_parser: AgentOutputParser

Output parser for the agent.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/output_parser)[attribute

template\_tool\_response: str

Template for the tool response.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/template_tool_response)[attribute

observation\_prefix: str

Prefix to append the observation with.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/observation_prefix)[attribute

llm\_prefix: str

Prefix to append the llm call with.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/llm_prefix)

## Methods

[method

create\_prompt

Create a prompt for the agent.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/create_prompt)[method

from\_llm\_and\_tools

Construct an agent from an LLM and tools.](/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/from_llm_and_tools)

## Inherited from[Agent](/python/langchain-classic/agents/agent/Agent)

### Attributes

[Allm\_chain: LLMChain

—

LLMChain to use for agent.](/python/langchain-classic/agents/agent/Agent/llm_chain)[Aallowed\_tools: list[str] | None

—

Allowed tools for the agent. If `None`, all tools are allowed.](/python/langchain-classic/agents/agent/Agent/allowed_tools)[Areturn\_values: list[str]

—

Return values of the agent.](/python/langchain-classic/agents/agent/Agent/return_values)[Ainput\_keys: list[str]

—

Return the input keys.](/python/langchain-classic/agents/agent/Agent/input_keys)

### Methods

[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/Agent/dict)[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/Agent/get_allowed_tools)[Mplan

—

Given input, decided what to do.](/python/langchain-classic/agents/agent/Agent/plan)[Maplan

—

Async given input, decided what to do.](/python/langchain-classic/agents/agent/Agent/aplan)[Mget\_full\_inputs

—

Create the full inputs for the LLMChain from intermediate steps.](/python/langchain-classic/agents/agent/Agent/get_full_inputs)[Mvalidate\_prompt

—

Validate that prompt matches format.](/python/langchain-classic/agents/agent/Agent/validate_prompt)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/Agent/return_stopped_response)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/Agent/tool_run_logging_kwargs)

## Inherited from[BaseSingleActionAgent](/python/langchain-classic/agents/agent/BaseSingleActionAgent)

### Attributes

[Areturn\_values: list[str]

—

Return values of the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_values)[Ainput\_keys: list[str]

—

Return the input keys.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/input_keys)

### Methods

[Mget\_allowed\_tools

—

Get allowed tools.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/get_allowed_tools)[Mplan

—

Given input, decided what to do.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/plan)[Maplan

—

Async given input, decided what to do.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/aplan)[Mreturn\_stopped\_response

—

Return response when agent has been stopped due to max iterations.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/return_stopped_response)[Mdict

—

Return dictionary representation of agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/dict)[Msave

—

Save the agent.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/save)[Mtool\_run\_logging\_kwargs

—

Return logging kwargs for tool run.](/python/langchain-classic/agents/agent/BaseSingleActionAgent/tool_run_logging_kwargs)


