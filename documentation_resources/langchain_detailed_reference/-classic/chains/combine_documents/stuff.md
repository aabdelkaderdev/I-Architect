<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/stuff -->

Modulev1.2.13 (latest)●Since v1.0

# stuff

Chain that combines documents by stuffing into context.

## Attributes

[attribute

DEFAULT\_DOCUMENT\_PROMPT](/python/langchain-classic/chains/combine_documents/base/DEFAULT_DOCUMENT_PROMPT)[attribute

DEFAULT\_DOCUMENT\_SEPARATOR: str](/python/langchain-classic/chains/combine_documents/base/DEFAULT_DOCUMENT_SEPARATOR)[attribute

DOCUMENTS\_KEY: str](/python/langchain-classic/chains/combine_documents/base/DOCUMENTS_KEY)

## Functions

[function

create\_stuff\_documents\_chain

Create a chain for passing a list of Documents to a model.](/python/langchain-classic/chains/combine_documents/stuff/create_stuff_documents_chain)

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

StuffDocumentsChain

Chain that combines documents by stuffing into context.

This chain takes a list of documents and first combines them into a single string.
It does this by formatting each document into a string with the `document_prompt`
and then joining them together with `document_separator`. It then adds that new
string to the inputs with the variable name set by `document_variable_name`.
Those inputs are then passed to the `llm_chain`.](/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain)


