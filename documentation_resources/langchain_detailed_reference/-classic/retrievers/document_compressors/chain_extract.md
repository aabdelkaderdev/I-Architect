<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_extract -->

Modulev1.2.13 (latest)●Since v1.0

# chain\_extract

DocumentFilter that uses an LLM chain to extract the relevant parts of documents.

## Attributes

[attribute

prompt\_template: str](/python/langchain-classic/retrievers/document_compressors/chain_extract_prompt/prompt_template)

## Functions

[function

default\_get\_input

Return the compression chain input.](/python/langchain-classic/retrievers/document_compressors/chain_extract/default_get_input)

## Classes

[class

NoOutputParser

Parse outputs that could return a null string of some sort.](/python/langchain-classic/retrievers/document_compressors/chain_extract/NoOutputParser)[class

LLMChainExtractor

LLM Chain Extractor.

Document compressor that uses an LLM chain to extract
the relevant parts of documents.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor)[deprecatedclass

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


