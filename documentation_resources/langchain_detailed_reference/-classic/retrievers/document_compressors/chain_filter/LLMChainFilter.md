<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter -->

Classv1.2.13 (latest)●Since v1.0

# LLMChainFilter


```
LLMChainFilter()
```

## Bases

`BaseDocumentCompressor`

## Attributes

## Methods



[attribute

llm\_chain: Runnable

LLM wrapper to use for filtering documents.
The chain prompt is expected to have a BooleanOutputParser.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/llm_chain)

[attribute

get\_input: Callable[[str, Document], dict]

Callable for constructing the chain input from the query and a Document.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/get_input)

[attribute

model\_config](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/model_config)

[method

compress\_documents

Filter down documents based on their relevance to the query.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/compress_documents)

[method

acompress\_documents

Filter down documents based on their relevance to the query.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/acompress_documents)

[method

from\_llm

Create a LLMChainFilter from a language model.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter/from_llm)

Filter that drops documents that aren't relevant to the query.