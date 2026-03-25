<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/extraction -->

Modulev1.2.13 (latest)●Since v1.0

# extraction

## Functions

[function

get\_llm\_kwargs

Return the kwargs for the LLMChain constructor.](/python/langchain-classic/chains/openai_functions/utils/get_llm_kwargs)[deprecatedfunction

create\_extraction\_chain

Creates a chain that extracts information from a passage.](/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain)[deprecatedfunction

create\_extraction\_chain\_pydantic

Creates a chain that extracts information from a passage using Pydantic schema.](/python/langchain-classic/chains/openai_functions/extraction/create_extraction_chain_pydantic)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[deprecatedclass

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


