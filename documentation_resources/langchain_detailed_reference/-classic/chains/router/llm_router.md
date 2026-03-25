<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/llm_router -->

Modulev1.2.13 (latest)●Since v1.0

# llm\_router

Base classes for LLM-powered router chains.

## Classes

[class

RouterChain

Chain that outputs the name of a destination chain and the inputs to it.](/python/langchain-classic/chains/router/base/RouterChain)[class

RouterOutputParser

Parser for output of router chain in the multi-prompt chain.](/python/langchain-classic/chains/router/llm_router/RouterOutputParser)[deprecatedclass

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


