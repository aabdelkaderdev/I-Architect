<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent -->

Modulev1.2.13 (latest)●Since v1.0

# agent

Chain that takes in an input and produces an action and action input.

## Attributes

[attribute

AGENT\_DEPRECATION\_WARNING: str](/python/langchain-classic/_api/deprecation/AGENT_DEPRECATION_WARNING)[attribute

logger](/python/langchain-classic/agents/agent/logger)[attribute

NextStepOutput: list[AgentFinish | AgentAction | AgentStep]](/python/langchain-classic/agents/agent/NextStepOutput)

## Classes

[class

AgentExecutorIterator

Iterator for AgentExecutor.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator)[class

InvalidTool

Tool that is run when invalid tool name is encountered by agent.](/python/langchain-classic/agents/tools/InvalidTool)[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

BaseSingleActionAgent

Base Single Action Agent class.](/python/langchain-classic/agents/agent/BaseSingleActionAgent)[class

BaseMultiActionAgent

Base Multi Action Agent class.](/python/langchain-classic/agents/agent/BaseMultiActionAgent)[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

MultiActionAgentOutputParser

Base class for parsing agent output into agent actions/finish.

This is used for agents that can return multiple actions.](/python/langchain-classic/agents/agent/MultiActionAgentOutputParser)[class

RunnableAgent

Agent powered by Runnables.](/python/langchain-classic/agents/agent/RunnableAgent)[class

RunnableMultiActionAgent

Agent powered by Runnables.](/python/langchain-classic/agents/agent/RunnableMultiActionAgent)[class

ExceptionTool

Tool that just returns the query.](/python/langchain-classic/agents/agent/ExceptionTool)[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[deprecatedclass

AgentType

An enum for agent types.](/python/langchain-classic/agents/agent_types/AgentType)[deprecatedclass

LLMChain

Chain to run queries against LLMs.

This class is deprecated. See below for an example implementation using
LangChain runnables:

```
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(input_variables=["adjective"], template=prompt_template)
model = OpenAI()
chain = prompt | model | StrOutputParser()

chain.invoke("your adjective here")
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

LLMSingleActionAgent

Base class for single action agents.](/python/langchain-classic/agents/agent/LLMSingleActionAgent)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)

## Type Aliases

[typeAlias

RunnableAgentType](/python/langchain-classic/agents/agent/RunnableAgentType)


