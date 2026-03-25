<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/api/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain that makes API calls and summarizes the responses to answer a question.

## Attributes

[attribute

API\_RESPONSE\_PROMPT](/python/langchain-classic/chains/api/prompt/API_RESPONSE_PROMPT)[attribute

API\_URL\_PROMPT](/python/langchain-classic/chains/api/prompt/API_URL_PROMPT)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

APIChain

Raise an ImportError if APIChain is used without langchain\_community.](/python/langchain-classic/chains/api/base/APIChain)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)


