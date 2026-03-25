<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/hyde/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Hypothetical Document Embeddings.

<https://arxiv.org/abs/2212.10496>

## Attributes

[attribute

PROMPT\_MAP: dict](/python/langchain-classic/chains/hyde/prompts/PROMPT_MAP)[attribute

logger](/python/langchain-classic/chains/hyde/base/logger)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

HypotheticalDocumentEmbedder

Generate hypothetical document for query, and then embed that.

Based on <https://arxiv.org/abs/2212.10496>](/python/langchain-classic/chains/hyde/base/HypotheticalDocumentEmbedder)[deprecatedclass

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


