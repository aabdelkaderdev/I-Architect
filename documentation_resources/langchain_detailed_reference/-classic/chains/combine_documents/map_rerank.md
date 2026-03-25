<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/map_rerank -->

Modulev1.2.13 (latest)●Since v1.0

# map\_rerank

Combining documents by mapping a chain over them first, then reranking results.

## Classes

[class

BaseCombineDocumentsChain

Base interface for chains combining documents.

Subclasses of this chain deal with combining documents in a variety of
ways. This base class exists to add some uniformity in the interface these types
of chains should expose. Namely, they expect an input key related to the documents
to use (default `input_documents`), and then also expose a method to calculate
the length of a prompt from documents (useful for outside callers to use to
determine whether it's safe to pass a list of documents into this chain or whether
that will be longer than the context length).](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)[class

RegexParser

Parse the output of an LLM call using a regex.](/python/langchain-classic/output_parsers/regex/RegexParser)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

MapRerankDocumentsChain

Combining documents by mapping a chain over them, then reranking results.

This algorithm calls an LLMChain on each input document. The LLMChain is expected
to have an OutputParser that parses the result into both an answer (`answer_key`)
and a score (`rank_key`). The answer with the highest score is then returned.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain)


