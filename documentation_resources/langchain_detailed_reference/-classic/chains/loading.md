<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/loading -->

Modulev1.2.13 (latest)●Since v1.0

# loading

Functionality for loading chains.

## Attributes

[attribute

URL\_BASE: str](/python/langchain-classic/chains/loading/URL_BASE)[attribute

type\_to\_loader\_dict: dict](/python/langchain-classic/chains/loading/type_to_loader_dict)

## Functions

[function

load\_llm

Import error for load\_llm.](/python/langchain-classic/chains/loading/load_llm)[function

load\_llm\_from\_config

Import error for load\_llm\_from\_config.](/python/langchain-classic/chains/loading/load_llm_from_config)[deprecatedfunction

load\_chain\_from\_config

Load chain from Config Dict.](/python/langchain-classic/chains/loading/load_chain_from_config)[deprecatedfunction

load\_chain

Unified method for loading a chain from LangChainHub or local fs.](/python/langchain-classic/chains/loading/load_chain)

## Classes

[class

APIChain

Raise an ImportError if APIChain is used without langchain\_community.](/python/langchain-classic/chains/api/base/APIChain)[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

HypotheticalDocumentEmbedder

Generate hypothetical document for query, and then embed that.

Based on <https://arxiv.org/abs/2212.10496>](/python/langchain-classic/chains/hyde/base/HypotheticalDocumentEmbedder)[class

RetrievalQAWithSourcesChain

Question-answering with sources over an index.](/python/langchain-classic/chains/qa_with_sources/retrieval/RetrievalQAWithSourcesChain)[class

VectorDBQAWithSourcesChain

Question-answering with sources over a vector database.](/python/langchain-classic/chains/qa_with_sources/vector_db/VectorDBQAWithSourcesChain)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

LLMCheckerChain

Chain for question-answering with self-verification.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain)[deprecatedclass

LLMMathChain

Chain that interprets a prompt and executes python code to do math.

Note

This class is deprecated. See below for a replacement implementation using
LangGraph. The benefits of this implementation are:

- Uses LLM tool calling features;
- Support for both token-by-token and step-by-step streaming;
- Support for checkpointing and memory of chat history;
- Easier to modify or extend
  (e.g., with additional tools, structured responses, etc.)

Install LangGraph with:

```
pip install -U langgraph
```

```
import math
from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode
import numexpr
from typing_extensions import TypedDict

@tool
def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.
```](/python/langchain-classic/chains/llm_math/base/LLMMathChain)[deprecatedclass

QAWithSourcesChain

Question answering with sources over documents.](/python/langchain-classic/chains/qa_with_sources/base/QAWithSourcesChain)[deprecatedclass

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


