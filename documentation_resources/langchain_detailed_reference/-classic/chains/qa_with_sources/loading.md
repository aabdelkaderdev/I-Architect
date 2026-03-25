<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/loading -->

Modulev1.2.13 (latest)●Since v1.0

# loading

Load question answering with sources chains.

## Attributes

[attribute

MAP\_RERANK\_PROMPT](/python/langchain-classic/chains/question_answering/map_rerank_prompt/PROMPT)

## Functions

[deprecatedfunction

load\_qa\_with\_sources\_chain

Load a question answering with sources chain.](/python/langchain-classic/chains/qa_with_sources/loading/load_qa_with_sources_chain)

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

LoadingCallable

Interface for loading the combine documents chain.](/python/langchain-classic/chains/qa_with_sources/loading/LoadingCallable)[deprecatedclass

MapReduceDocumentsChain

Combining documents by mapping a chain over them, then combining results.

We first call `llm_chain` on each document individually, passing in the
`page_content` and any other kwargs. This is the `map` step.

We then process the results of that `map` step in a `reduce` step. This should
likely be a ReduceDocumentsChain.](/python/langchain-classic/chains/combine_documents/map_reduce/MapReduceDocumentsChain)[deprecatedclass

MapRerankDocumentsChain

Combining documents by mapping a chain over them, then reranking results.

This algorithm calls an LLMChain on each input document. The LLMChain is expected
to have an OutputParser that parses the result into both an answer (`answer_key`)
and a score (`rank_key`). The answer with the highest score is then returned.](/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain)[deprecatedclass

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

RefineDocumentsChain

Combine documents by doing a first pass and then refining on more documents.

This algorithm first calls `initial_llm_chain` on the first document, passing
that first document in with the variable name `document_variable_name`, and
produces a new variable with the variable name `initial_response_name`.

Then, it loops over every remaining document. This is called the "refine" step.
It calls `refine_llm_chain`,
passing in that document with the variable name `document_variable_name`
as well as the previous response with the variable name `initial_response_name`.](/python/langchain-classic/chains/combine_documents/refine/RefineDocumentsChain)[deprecatedclass

StuffDocumentsChain

Chain that combines documents by stuffing into context.

This chain takes a list of documents and first combines them into a single string.
It does this by formatting each document into a string with the `document_prompt`
and then joining them together with `document_separator`. It then adds that new
string to the inputs with the variable name set by `document_variable_name`.
Those inputs are then passed to the `llm_chain`.](/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain)[deprecatedclass

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

## Modules

[module

map\_reduce\_prompt](/python/langchain-classic/chains/qa_with_sources/map_reduce_prompt)[module

refine\_prompts](/python/langchain-classic/chains/qa_with_sources/refine_prompts)[module

stuff\_prompt](/python/langchain-classic/chains/qa_with_sources/stuff_prompt)


