<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/generate_chain -->

Modulev1.2.13 (latest)●Since v1.0

# generate\_chain

LLM Chain for generating examples for question answering.

## Attributes

[attribute

PROMPT](/python/langchain-classic/evaluation/qa/generate_prompt/PROMPT)

## Classes

[class

RegexParser

Parse the output of an LLM call using a regex.](/python/langchain-classic/output_parsers/regex/RegexParser)[class

QAGenerateChain

LLM Chain for generating examples for question answering.](/python/langchain-classic/evaluation/qa/generate_chain/QAGenerateChain)[deprecatedclass

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


