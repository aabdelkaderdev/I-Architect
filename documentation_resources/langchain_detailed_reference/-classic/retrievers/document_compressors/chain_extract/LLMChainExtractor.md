<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor -->

Classv1.2.13 (latest)●Since v1.0

# LLMChainExtractor


```
LLMChainExtractor()
```

## Bases

`BaseDocumentCompressor`

## Attributes

## Methods



[attribute

llm\_chain: Runnable

LLM wrapper to use for compressing documents.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/llm_chain)

[attribute

get\_input: Callable[[str, Document], dict]

Callable for constructing the chain input from the query and a Document.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/get_input)

[attribute

model\_config](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/model_config)

[method

compress\_documents

Compress page content of raw documents.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/compress_documents)

[method

acompress\_documents

Compress page content of raw documents asynchronously.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/acompress_documents)

[method

from\_llm

Initialize from LLM.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor/from_llm)

LLM Chain Extractor.

Document compressor that uses an LLM chain to extract
the relevant parts of documents.