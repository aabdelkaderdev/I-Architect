<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/multi_prompt/MultiPromptChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# MultiPromptChain


```
MultiPromptChain
```

(

)

## Bases

`MultiRouteChain`

## Attributes

[attribute

output\_keys: list[str]](/python/langchain-classic/chains/router/multi_prompt/MultiPromptChain/output_keys)

## Methods

[method

from\_prompts](/python/langchain-classic/chains/router/multi_prompt/MultiPromptChain/from_prompts)

## Inherited from[MultiRouteChain](/python/langchain-classic/chains/router/base/MultiRouteChain)

### Attributes

[Arouter\_chain: RouterChain

—

Chain that routes inputs to destination chains.](/python/langchain-classic/chains/router/base/MultiRouteChain/router_chain)[Adestination\_chains: Mapping[str, Chain]

—

Chains that return final answer to inputs.](/python/langchain-classic/chains/router/base/MultiRouteChain/destination_chains)[Adefault\_chain: Chain

—

Default chain to use when none of the destination chains are suitable.](/python/langchain-classic/chains/router/base/MultiRouteChain/default_chain)[Asilent\_errors: bool

—

If `True`, use default\_chain when an invalid destination name is provided.](/python/langchain-classic/chains/router/base/MultiRouteChain/silent_errors)[Amodel\_config](/python/langchain-classic/chains/router/base/MultiRouteChain/model_config)[Ainput\_keys: list[str]

—

Will be whatever keys the router chain prompt expects.](/python/langchain-classic/chains/router/base/MultiRouteChain/input_keys)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[A](/python/langchain-classic/chains/base/Chain/tags)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)



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
```

tags

: list[str] | None

—

Optional list of tags associated with the chain.

[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)

[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

[Amodel\_config](/python/langchain-classic/chains/base/Chain/model_config)

[Ainput\_keys: list[str]

—

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[Mset\_verbose

—

Set the chain verbosity.](/python/langchain-classic/chains/base/Chain/set_verbose)[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

M

configurable\_alternatives

M

get\_lc\_namespace

[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)

[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)[Mpick](/python/langchain-core/runnables/base/Runnable/pick)[Massign](/python/langchain-core/runnables/base/Runnable/assign)[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/Runnable/stream)[Mastream](/python/langchain-core/runnables/base/Runnable/astream)[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)[Mbind](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)[Mmap](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)

Convenience constructor for instantiating from destination prompts.