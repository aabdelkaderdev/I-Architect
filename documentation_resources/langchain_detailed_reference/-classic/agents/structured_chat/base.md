<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

FORMAT\_INSTRUCTIONS: str](/python/langchain-classic/agents/structured_chat/prompt/FORMAT_INSTRUCTIONS)[attribute

PREFIX: str](/python/langchain-classic/agents/structured_chat/prompt/PREFIX)[attribute

SUFFIX: str](/python/langchain-classic/agents/structured_chat/prompt/SUFFIX)[attribute

HUMAN\_MESSAGE\_TEMPLATE: str](/python/langchain-classic/agents/structured_chat/base/HUMAN_MESSAGE_TEMPLATE)

## Functions

[function

format\_log\_to\_str

Construct the scratchpad that lets the agent continue its thought process.](/python/langchain-classic/agents/format_scratchpad/log/format_log_to_str)[function

create\_structured\_chat\_agent

Create an agent aimed at supporting tools with multiple inputs.](/python/langchain-classic/agents/structured_chat/base/create_structured_chat_agent)

## Classes

[class

AgentOutputParser

Base class for parsing agent output into agent action/finish.](/python/langchain-classic/agents/agent/AgentOutputParser)[class

JSONAgentOutputParser

Parses tool invocations and final answers in JSON format.

Expects output to be in one of two formats.

If the output signals that an action should be taken,
should be in the below format. This will result in an AgentAction
being returned.

```
{"action": "search", "action_input": "2+2"}
```

If the output signals that a final answer should be given,
should be in the below format. This will result in an AgentFinish
being returned.

```
{"action": "Final Answer", "action_input": "4"}
```](/python/langchain-classic/agents/output_parsers/json/JSONAgentOutputParser)[class

StructuredChatOutputParserWithRetries

Output parser with retries for the structured chat agent.](/python/langchain-classic/agents/structured_chat/output_parser/StructuredChatOutputParserWithRetries)[deprecatedclass

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

StructuredChatAgent

Structured Chat Agent.](/python/langchain-classic/agents/structured_chat/base/StructuredChatAgent)


