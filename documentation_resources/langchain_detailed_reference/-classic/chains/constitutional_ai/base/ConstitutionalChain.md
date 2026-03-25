<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConstitutionalChain


```
ConstitutionalChain
```

(

)

## Bases

`Chain`

## Attributes

[attribute

chain: LLMChain](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/chain)[attribute

constitutional\_principles: list[ConstitutionalPrinciple]](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/constitutional_principles)[attribute

critique\_chain: LLMChain](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/critique_chain)[attribute

revision\_chain: LLMChain](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/revision_chain)[attribute

return\_intermediate\_steps: bool](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/return_intermediate_steps)[attribute

input\_keys: list[str]](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/input_keys)[attribute

output\_keys: list[str]](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/output_keys)

## Methods

[method

get\_principles](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/get_principles)[method

from\_llm](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/from_llm)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[Atags: list[str] | None

—

Optional list of tags associated with the chain.](/python/langchain-classic/chains/base/Chain/tags)[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)[Amodel\_config](/python/langchain-classic/chains/base/Chain/model_config)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[M](/python/langchain-classic/chains/base/Chain/set_verbose)

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



Chain for applying constitutional principles.

Note

This class is deprecated. See below for a replacement implementation using
LangGraph. The benefits of this implementation are:

- Uses LLM tool calling features instead of parsing string responses;
- Support for both token-by-token and step-by-step streaming;
- Support for checkpointing and memory of chat history;
- Easier to modify or extend (e.g., with additional tools, structured responses, etc.)

Install LangGraph with:

```
pip install -U langgraph
```

```
from typing import List, Optional, Tuple

from langchain_classic.chains.constitutional_ai.prompts import (
    CRITIQUE_PROMPT,
    REVISION_PROMPT,
)
from langchain_classic.chains.constitutional_ai.models import ConstitutionalPrinciple
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

model = ChatOpenAI(model="gpt-4o-mini")

class Critique(TypedDict):
    """Generate a critique, if needed."""
    critique_needed: Annotated[bool, ..., "Whether or not a critique is needed."]
    critique: Annotated[str, ..., "If needed, the critique."]

critique_prompt = ChatPromptTemplate.from_template(
    "Critique this response according to the critique request. "
    "If no critique is needed, specify that.\n\n"
    "Query: {query}\n\n"
    "Response: {response}\n\n"
    "Critique request: {critique_request}"
)

revision_prompt = ChatPromptTemplate.from_template(
    "Revise this response according to the critique and reivsion request.\n\n"
    "Query: {query}\n\n"
    "Response: {response}\n\n"
    "Critique request: {critique_request}\n\n"
    "Critique: {critique}\n\n"
    "If the critique does not identify anything worth changing, ignore the "
    "revision request and return 'No revisions needed'. If the critique "
    "does identify something worth changing, revise the response based on "
    "the revision request.\n\n"
    "Revision Request: {revision_request}"
)

chain = model | StrOutputParser()
critique_chain = critique_prompt | model.with_structured_output(Critique)
revision_chain = revision_prompt | model | StrOutputParser()

class State(TypedDict):
    query: str
    constitutional_principles: List[ConstitutionalPrinciple]
    initial_response: str
    critiques_and_revisions: List[Tuple[str, str]]
    response: str

async def generate_response(state: State):
    """Generate initial response."""
    response = await chain.ainvoke(state["query"])
    return {"response": response, "initial_response": response}

async def critique_and_revise(state: State):
    """Critique and revise response according to principles."""
    critiques_and_revisions = []
    response = state["initial_response"]
    for principle in state["constitutional_principles"]:
        critique = await critique_chain.ainvoke(
            {
                "query": state["query"],
                "response": response,
                "critique_request": principle.critique_request,
            }
        )
        if critique["critique_needed"]:
            revision = await revision_chain.ainvoke(
                {
                    "query": state["query"],
                    "response": response,
                    "critique_request": principle.critique_request,
                    "critique": critique["critique"],
                    "revision_request": principle.revision_request,
                }
            )
            response = revision
            critiques_and_revisions.append((critique["critique"], revision))
        else:
            critiques_and_revisions.append((critique["critique"], ""))
    return {
        "critiques_and_revisions": critiques_and_revisions,
        "response": response,
    }

graph = StateGraph(State)
graph.add_node("generate_response", generate_response)
graph.add_node("critique_and_revise", critique_and_revise)

graph.add_edge(START, "generate_response")
graph.add_edge("generate_response", "critique_and_revise")
graph.add_edge("critique_and_revise", END)
app = graph.compile()
```

```
constitutional_principles=[
    ConstitutionalPrinciple(
        critique_request="Tell if this answer is good.",
        revision_request="Give a better answer.",
    )
]

query = "What is the meaning of life? Answer in 10 words or fewer."

async for step in app.astream(
    {"query": query, "constitutional_principles": constitutional_principles},
    stream_mode="values",
):
    subset = ["initial_response", "critiques_and_revisions", "response"]
    print({k: v for k, v in step.items() if k in subset})
```

**Example:**

```
from langchain_openai import OpenAI
from langchain_classic.chains import LLMChain, ConstitutionalChain
from langchain_classic.chains.constitutional_ai.models \
    import ConstitutionalPrinciple

llmodelm = OpenAI()

qa_prompt = PromptTemplate(
    template="Q: {question} A:",
    input_variables=["question"],
)
qa_chain = LLMChain(llm=model, prompt=qa_prompt)

constitutional_chain = ConstitutionalChain.from_llm(
    llm=model,
    chain=qa_chain,
    constitutional_principles=[
        ConstitutionalPrinciple(
            critique_request="Tell if this answer is good.",
            revision_request="Give a better answer.",
        )
    ],
)

constitutional_chain.run(question="What is the meaning of life?")
```

set\_verbose

—

Set the chain verbosity.

[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)

[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)

[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)

[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)

[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)

[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)

[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)

[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)

[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)

[Mapply

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

Input keys.

Output keys.

Get constitutional principles by name.

Create a chain from an LLM.