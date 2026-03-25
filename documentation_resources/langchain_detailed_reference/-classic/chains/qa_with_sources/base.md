<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Question answering with sources over documents.

## Attributes

[attribute

COMBINE\_PROMPT](/python/langchain-classic/chains/qa_with_sources/map_reduce_prompt/COMBINE_PROMPT)[attribute

EXAMPLE\_PROMPT](/python/langchain-classic/chains/qa_with_sources/map_reduce_prompt/EXAMPLE_PROMPT)[attribute

QUESTION\_PROMPT](/python/langchain-classic/chains/qa_with_sources/map_reduce_prompt/QUESTION_PROMPT)

## Functions

[deprecatedfunction

load\_qa\_with\_sources\_chain

Load a question answering with sources chain.](/python/langchain-classic/chains/qa_with_sources/loading/load_qa_with_sources_chain)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

BaseCombineDocumentsChain

Base interface for chains combining documents.

Subclasses of this chain deal with combining documents in a variety of
ways. This base class exists to add some uniformity in the interface these types
of chains should expose. Namely, they expect an input key related to the documents
to use (default `input_documents`), and then also expose a method to calculate
the length of a prompt from documents (useful for outside callers to use to
determine whether it's safe to pass a list of documents into this chain or whether
that will be longer than the context length).](/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain)[deprecatedclass

MapReduceDocumentsChain

Combining documents by mapping a chain over them, then combining results.

We first call `llm_chain` on each document individually, passing in the
`page_content` and any other kwargs. This is the `map` step.

We then process the results of that `map` step in a `reduce` step. This should
likely be a ReduceDocumentsChain.](/python/langchain-classic/chains/combine_documents/map_reduce/MapReduceDocumentsChain)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

BaseQAWithSourcesChain

Question answering chain with sources over documents.](/python/langchain-classic/chains/qa_with_sources/base/BaseQAWithSourcesChain)[deprecatedclass

QAWithSourcesChain

Question answering with sources over documents.](/python/langchain-classic/chains/qa_with_sources/base/QAWithSourcesChain)


