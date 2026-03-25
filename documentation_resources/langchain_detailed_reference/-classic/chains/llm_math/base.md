<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_math/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain that interprets a prompt and executes python code to do math.

## Attributes

[attribute

PROMPT](/python/langchain-classic/chains/llm_math/prompt/PROMPT)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[deprecatedclass

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
```](/python/langchain-classic/chains/llm_math/base/LLMMathChain)


