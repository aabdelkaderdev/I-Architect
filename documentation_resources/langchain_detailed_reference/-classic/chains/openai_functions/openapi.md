<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/openapi -->

Modulev1.2.13 (latest)●Since v1.0

# openapi

## Functions

[function

openapi\_spec\_to\_openai\_fn

OpenAPI spec to OpenAI function JSON Schema.

Convert a valid OpenAPI spec to the JSON Schema format expected for OpenAI
functions.](/python/langchain-classic/chains/openai_functions/openapi/openapi_spec_to_openai_fn)[deprecatedfunction

get\_openapi\_chain

Create a chain for querying an API from a OpenAPI spec.](/python/langchain-classic/chains/openai_functions/openapi/get_openapi_chain)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

SequentialChain

Chain where the outputs of one chain feed directly into next.](/python/langchain-classic/chains/sequential/SequentialChain)[class

SimpleRequestChain

Chain for making a simple request to an API endpoint.](/python/langchain-classic/chains/openai_functions/openapi/SimpleRequestChain)[deprecatedclass

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


