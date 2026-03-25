<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/xml/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Attributes

[attribute

agent\_instructions: str](/python/langchain-classic/agents/xml/prompt/agent_instructions)

## Functions

[function

format\_xml

Format the intermediate steps as XML.](/python/langchain-classic/agents/format_scratchpad/xml/format_xml)[function

create\_xml\_agent

Create an agent that uses XML to format its logic.](/python/langchain-classic/agents/xml/base/create_xml_agent)

## Classes

[class

BaseSingleActionAgent

Base Single Action Agent class.](/python/langchain-classic/agents/agent/BaseSingleActionAgent)[class

XMLAgentOutputParser

Parses tool invocations and final answers from XML-formatted agent output.

This parser extracts structured information from XML tags to determine whether
an agent should perform a tool action or provide a final answer. It includes
built-in escaping support to safely handle tool names and inputs
containing XML special characters.](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser)[deprecatedclass

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

XMLAgent

Agent that uses XML tags.](/python/langchain-classic/agents/xml/base/XMLAgent)


