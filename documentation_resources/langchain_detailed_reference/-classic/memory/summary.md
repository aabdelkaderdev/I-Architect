<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary -->

Modulev1.2.13 (latest)●Since v1.0

# summary

## Attributes

[attribute

SUMMARY\_PROMPT](/python/langchain-classic/memory/prompt/SUMMARY_PROMPT)

## Classes

[deprecatedclass

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

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)[deprecatedclass

SummarizerMixin

Mixin for summarizer.](/python/langchain-classic/memory/summary/SummarizerMixin)[deprecatedclass

ConversationSummaryMemory

Continually summarizes the conversation history.

The summary is updated after each conversation turn.
The implementations returns a summary of the conversation history which
can be used to provide context to the model.](/python/langchain-classic/memory/summary/ConversationSummaryMemory)


