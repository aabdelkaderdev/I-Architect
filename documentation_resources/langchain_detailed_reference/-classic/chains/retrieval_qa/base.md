<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/retrieval_qa/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain for question-answering against a vector database.

## Attributes

[attribute

PROMPT\_SELECTOR](/python/langchain-classic/chains/question_answering/stuff_prompt/PROMPT_SELECTOR)

## Functions

[deprecatedfunction

load\_qa\_chain

Load question answering chain.](/python/langchain-classic/chains/question_answering/chain/load_qa_chain)

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

BaseRetrievalQA

Base class for question-answering chains.](/python/langchain-classic/chains/retrieval_qa/base/BaseRetrievalQA)[deprecatedclass

RetrievalQA

Chain for question-answering against an index.

This class is deprecated. See below for an example implementation using
`create_retrieval_chain`:

```
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

retriever = ...  # Your retriever
model = ChatOpenAI()

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(model, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

chain.invoke({"input": query})
```](/python/langchain-classic/chains/retrieval_qa/base/RetrievalQA)[deprecatedclass

VectorDBQA

Chain for question-answering against a vector database.](/python/langchain-classic/chains/retrieval_qa/base/VectorDBQA)


