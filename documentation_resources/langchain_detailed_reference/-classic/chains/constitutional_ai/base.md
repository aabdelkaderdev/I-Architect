<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain for applying constitutional principles to the outputs of another chain.

## Attributes

[attribute

PRINCIPLES: dict[str, ConstitutionalPrinciple]](/python/langchain-classic/chains/constitutional_ai/principles/PRINCIPLES)[attribute

CRITIQUE\_PROMPT](/python/langchain-classic/chains/constitutional_ai/prompts/CRITIQUE_PROMPT)[attribute

REVISION\_PROMPT](/python/langchain-classic/chains/constitutional_ai/prompts/REVISION_PROMPT)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

ConstitutionalPrinciple

Class for a constitutional principle.](/python/langchain-classic/chains/constitutional_ai/models/ConstitutionalPrinciple)[deprecatedclass

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

ConstitutionalChain

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
```](/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain)


