<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router -->

Modulev1.2.13 (latest)●Since v1.0

# router

## Classes

[class

MultiRouteChain

Use a single chain to route an input to one of multiple candidate chains.](/python/langchain-classic/chains/router/base/MultiRouteChain)[class

RouterChain

Chain that outputs the name of a destination chain and the inputs to it.](/python/langchain-classic/chains/router/base/RouterChain)[class

MultiRetrievalQAChain

Multi Retrieval QA Chain.

A multi-route chain that uses an LLM router chain to choose amongst retrieval
qa chains.](/python/langchain-classic/chains/router/multi_retrieval_qa/MultiRetrievalQAChain)[deprecatedclass

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
```](/python/langchain-classic/chains/router/llm_router/LLMRouterChain)[deprecatedclass

MultiPromptChain

A multi-route chain that uses an LLM router chain to choose amongst prompts.

This class is deprecated. See below for a replacement, which offers several
benefits, including streaming and batch support.

Below is an example implementation:

```
from operator import itemgetter
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

model = ChatOpenAI(model="gpt-4o-mini")

# Define the prompts we will route to
prompt_1 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert on animals."),
        ("human", "{input}"),
    ]
)
prompt_2 = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert on vegetables."),
        ("human", "{input}"),
    ]
)

# Construct the chains we will route to. These format the input query
# into the respective prompt, run it through a chat model, and cast
# the result to a string.
chain_1 = prompt_1 | model | StrOutputParser()
chain_2 = prompt_2 | model | StrOutputParser()

# Next: define the chain that selects which branch to route to.
# Here we will take advantage of tool-calling features to force
# the output to select one of two desired branches.
route_system = "Route the user's query to either the animal "
"or vegetable expert."
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", route_system),
        ("human", "{input}"),
    ]
)

# Define schema for output:
class RouteQuery(TypedDict):
    """Route query to destination expert."""

    destination: Literal["animal", "vegetable"]

route_chain = route_prompt | model.with_structured_output(RouteQuery)

# For LangGraph, we will define the state of the graph to hold the query,
# destination, and final answer.
class State(TypedDict):
    query: str
    destination: RouteQuery
    answer: str

# We define functions for each node, including routing the query:
async def route_query(state: State, config: RunnableConfig):
    destination = await route_chain.ainvoke(state["query"], config)
    return {"destination": destination}

# And one node for each prompt
async def prompt_1(state: State, config: RunnableConfig):
    return {"answer": await chain_1.ainvoke(state["query"], config)}

async def prompt_2(state: State, config: RunnableConfig):
    return {"answer": await chain_2.ainvoke(state["query"], config)}

# We then define logic that selects the prompt based on the classification
def select_node(state: State) -> Literal["prompt_1", "prompt_2"]:
    if state["destination"] == "animal":
        return "prompt_1"
    else:
        return "prompt_2"

# Finally, assemble the multi-prompt chain. This is a sequence of two steps:
# 1) Select "animal" or "vegetable" via the route_chain, and collect the
# answer alongside the input query.
# 2) Route the input query to chain_1 or chain_2, based on the
# selection.
graph = StateGraph(State)
graph.add_node("route_query", route_query)
graph.add_node("prompt_1", prompt_1)
graph.add_node("prompt_2", prompt_2)

graph.add_edge(START, "route_query")
graph.add_conditional_edges("route_query", select_node)
graph.add_edge("prompt_1", END)
graph.add_edge("prompt_2", END)
app = graph.compile()

result = await app.ainvoke({"query": "what color are carrots"})
print(result["destination"])
print(result["answer"])
```](/python/langchain-classic/chains/router/multi_prompt/MultiPromptChain)

## Modules

[module

multi\_prompt

Use a single chain to route an input to one of multiple llm chains.](/python/langchain-classic/chains/router/multi_prompt)[module

embedding\_router](/python/langchain-classic/chains/router/embedding_router)[module

multi\_retrieval\_prompt

Prompt for the router chain in the multi-retrieval qa chain.](/python/langchain-classic/chains/router/multi_retrieval_prompt)[module

base

Base classes for chain routing.](/python/langchain-classic/chains/router/base)[module

multi\_prompt\_prompt

Prompt for the router chain in the multi-prompt chain.](/python/langchain-classic/chains/router/multi_prompt_prompt)[module

llm\_router

Base classes for LLM-powered router chains.](/python/langchain-classic/chains/router/llm_router)[module

multi\_retrieval\_qa

Use a single chain to route an input to one of multiple retrieval qa chains.](/python/langchain-classic/chains/router/multi_retrieval_qa)


