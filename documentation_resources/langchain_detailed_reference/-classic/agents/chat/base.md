<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

AGENT\_DEPRECATION\_WARNING: str](/python/langchain-classic/_api/deprecation/AGENT_DEPRECATION_WARNING)[attribute

FORMAT\_INSTRUCTIONS: str](/python/langchain-classic/agents/chat/prompt/FORMAT_INSTRUCTIONS)[attribute

HUMAN\_MESSAGE: str](/python/langchain-classic/agents/chat/prompt/HUMAN_MESSAGE)[attribute

SYSTEM\_MESSAGE\_PREFIX: str](/python/langchain-classic/agents/chat/prompt/SYSTEM_MESSAGE_PREFIX)[attribute

SYSTEM\_MESSAGE\_SUFFIX: str](/python/langchain-classic/agents/chat/prompt/SYSTEM_MESSAGE_SUFFIX)

## Functions

[function

validate\_tools\_single\_input

Validate tools for single input.](/python/langchain-classic/agents/utils/validate_tools_single_input)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

ChatOutputParser

Output parser for the chat agent.](/python/langchain-classic/agents/chat/output_parser/ChatOutputParser)[deprecatedclass

Agent

Agent that calls the language model and deciding the action.

This is driven by a LLMChain. The prompt in the LLMChain MUST include
a variable called "agent\_scratchpad" where the agent can put its
intermediary work.](/python/langchain-classic/agents/agent/Agent)[deprecatedclass

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

ChatAgent

Chat Agent.](/python/langchain-classic/agents/chat/base/ChatAgent)


