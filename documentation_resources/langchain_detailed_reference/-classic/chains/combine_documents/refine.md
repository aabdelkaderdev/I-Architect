<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/refine -->

Modulev1.2.13 (latest)●Since v1.0

# refine

Combine documents by doing a first pass and then refining on more documents.

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

RefineDocumentsChain

Combine documents by doing a first pass and then refining on more documents.

This algorithm first calls `initial_llm_chain` on the first document, passing
that first document in with the variable name `document_variable_name`, and
produces a new variable with the variable name `initial_response_name`.

Then, it loops over every remaining document. This is called the "refine" step.
It calls `refine_llm_chain`,
passing in that document with the variable name `document_variable_name`
as well as the previous response with the variable name `initial_response_name`.](/python/langchain-classic/chains/combine_documents/refine/RefineDocumentsChain)


