<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors -->

Modulev1.2.13 (latest)●Since v1.0

# document\_compressors

## Classes

[class

DocumentCompressorPipeline

Document compressor that uses a pipeline of Transformers.](/python/langchain-classic/retrievers/document_compressors/base/DocumentCompressorPipeline)[class

LLMChainExtractor

LLM Chain Extractor.

Document compressor that uses an LLM chain to extract
the relevant parts of documents.](/python/langchain-classic/retrievers/document_compressors/chain_extract/LLMChainExtractor)[class

LLMChainFilter

Filter that drops documents that aren't relevant to the query.](/python/langchain-classic/retrievers/document_compressors/chain_filter/LLMChainFilter)[class

CrossEncoderReranker

Document compressor that uses CrossEncoder for reranking.](/python/langchain-classic/retrievers/document_compressors/cross_encoder_rerank/CrossEncoderReranker)[class

EmbeddingsFilter

Embeddings Filter.

Document compressor that uses embeddings to drop documents unrelated to the query.](/python/langchain-classic/retrievers/document_compressors/embeddings_filter/EmbeddingsFilter)[class

LLMListwiseRerank

Document compressor that uses `Zero-Shot Listwise Document Reranking`.

Adapted from: <https://arxiv.org/pdf/2305.02156.pdf>

`LLMListwiseRerank` uses a language model to rerank a list of documents based on
their relevance to a query.

Note

Requires that underlying model implement `with_structured_output`.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank)[deprecatedclass

CohereRerank

Document compressor that uses `Cohere Rerank API`.](/python/langchain-classic/retrievers/document_compressors/cohere_rerank/CohereRerank)

## Modules

[module

listwise\_rerank

Filter that uses an LLM to rerank documents listwise and select top-k.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank)[module

cross\_encoder](/python/langchain-classic/retrievers/document_compressors/cross_encoder)[module

chain\_extract\_prompt](/python/langchain-classic/retrievers/document_compressors/chain_extract_prompt)[module

base](/python/langchain-classic/retrievers/document_compressors/base)[module

embeddings\_filter](/python/langchain-classic/retrievers/document_compressors/embeddings_filter)[module

cohere\_rerank](/python/langchain-classic/retrievers/document_compressors/cohere_rerank)[module

flashrank\_rerank](/python/langchain-classic/retrievers/document_compressors/flashrank_rerank)[module

chain\_filter

Filter that uses an LLM to drop documents that aren't relevant to the query.](/python/langchain-classic/retrievers/document_compressors/chain_filter)[module

chain\_filter\_prompt](/python/langchain-classic/retrievers/document_compressors/chain_filter_prompt)[module

cross\_encoder\_rerank](/python/langchain-classic/retrievers/document_compressors/cross_encoder_rerank)[module

chain\_extract

DocumentFilter that uses an LLM chain to extract the relevant parts of documents.](/python/langchain-classic/retrievers/document_compressors/chain_extract)


