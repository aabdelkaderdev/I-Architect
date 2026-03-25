<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/qa_with_structure -->

Modulev1.2.13 (latest)●Since v1.0

# qa\_with\_structure

## Functions

[function

get\_llm\_kwargs

Return the kwargs for the LLMChain constructor.](/python/langchain-classic/chains/openai_functions/utils/get_llm_kwargs)[deprecatedfunction

create\_qa\_with\_structure\_chain

Create a question answering chain with structure.

Create a question answering chain that returns an answer with sources
based on schema.](/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_structure_chain)[deprecatedfunction

create\_qa\_with\_sources\_chain

Create a question answering chain that returns an answer with sources.](/python/langchain-classic/chains/openai_functions/qa_with_structure/create_qa_with_sources_chain)

## Classes

[class

AnswerWithSources

An answer to the question, with sources.](/python/langchain-classic/chains/openai_functions/qa_with_structure/AnswerWithSources)[deprecatedclass

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


