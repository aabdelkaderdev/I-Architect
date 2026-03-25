<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/map_reduce -->

Modulev1.2.13 (latest)●Since v1.0

# map\_reduce

Combining documents by mapping a chain over them first, then combining results.

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
that will be longer than the context length).](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)[deprecatedclass

ReduceDocumentsChain

Combine documents by recursively reducing them.

This involves

- `combine_documents_chain`
- `collapse_documents_chain`

`combine_documents_chain` is ALWAYS provided. This is final chain that is called.

We pass all previous results to this chain, and the output of this chain is
returned as a final result.

`collapse_documents_chain` is used if the documents passed in are too many to all
be passed to `combine_documents_chain` in one go. In this case,
`collapse_documents_chain` is called recursively on as big of groups of documents
as are allowed.](/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain)[deprecatedclass

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

MapReduceDocumentsChain

Combining documents by mapping a chain over them, then combining results.

We first call `llm_chain` on each document individually, passing in the
`page_content` and any other kwargs. This is the `map` step.

We then process the results of that `map` step in a `reduce` step. This should
likely be a ReduceDocumentsChain.](/python/langchain-classic/chains/combine_documents/map_reduce/MapReduceDocumentsChain)


