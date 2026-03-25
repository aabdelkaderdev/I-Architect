<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/listwise_rerank -->

Modulev1.2.13 (latest)●Since v1.0

# listwise\_rerank

Filter that uses an LLM to rerank documents listwise and select top-k.

## Classes

[class

LLMListwiseRerank

Document compressor that uses `Zero-Shot Listwise Document Reranking`.

Adapted from: <https://arxiv.org/pdf/2305.02156.pdf>

`LLMListwiseRerank` uses a language model to rerank a list of documents based on
their relevance to a query.

Note

Requires that underlying model implement `with_structured_output`.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank)


