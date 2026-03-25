<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/multi_retrieval_qa -->

Modulev1.2.13 (latest)●Since v1.0

# multi\_retrieval\_qa

Use a single chain to route an input to one of multiple retrieval qa chains.

## Attributes

[attribute

DEFAULT\_TEMPLATE: str](/python/langchain-classic/chains/conversation/prompt/DEFAULT_TEMPLATE)[attribute

MULTI\_RETRIEVAL\_ROUTER\_TEMPLATE: str](/python/langchain-classic/chains/router/multi_retrieval_prompt/MULTI_RETRIEVAL_ROUTER_TEMPLATE)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

MultiRouteChain

Use a single chain to route an input to one of multiple candidate chains.](/python/langchain-classic/chains/router/base/MultiRouteChain)[class

RouterOutputParser

Parser for output of router chain in the multi-prompt chain.](/python/langchain-classic/chains/router/llm_router/RouterOutputParser)[class

MultiRetrievalQAChain

Multi Retrieval QA Chain.

A multi-route chain that uses an LLM router chain to choose amongst retrieval
qa chains.](/python/langchain-classic/chains/router/multi_retrieval_qa/MultiRetrievalQAChain)[deprecatedclass

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

LLMRouterChain

A router chain that uses an LLM chain to perform routing.

This class is deprecated. See below for a replacement, which offers several
benefits, including streaming and batch support.

Below is an example implementation:

```
from operator import itemgetter
from typing import Literal
from typing_extensions import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

prompt_1 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert on animals."),
        ("human", "{query}"),
    ]
)
prompt_2 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert on vegetables."),
        ("human", "{query}"),
    ]
)

chain_1 = prompt_1 | model | StrOutputParser()
chain_2 = prompt_2 | model | StrOutputParser()

route_system = "Route the user's query to either the animal "
"or vegetable expert."
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", route_system),
        ("human", "{query}"),
    ]
)

class RouteQuery(TypedDict):
    """Route query to destination."""
    destination: Literal["animal", "vegetable"]

route_chain = (
    route_prompt
    | model.with_structured_output(RouteQuery)
    | itemgetter("destination")
)

chain = {
    "destination": route_chain,  # "animal" or "vegetable"
    "query": lambda x: x["query"],  # pass through input query
} | RunnableLambda(
    # if animal, chain_1. otherwise, chain_2.
    lambda x: chain_1 if x["destination"] == "animal" else chain_2,
)

chain.invoke({"query": "what color are carrots"})
```](/python/langchain-classic/chains/router/llm_router/LLMRouterChain)


