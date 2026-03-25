<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_toolkits/vectorstore/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

VectorStore agent.

## Attributes

[attribute

PREFIX: str](/python/langchain-classic/agents/agent_toolkits/vectorstore/prompt/PREFIX)[attribute

ROUTER\_PREFIX: str](/python/langchain-classic/agents/agent_toolkits/vectorstore/prompt/ROUTER_PREFIX)

## Functions

[deprecatedfunction

create\_vectorstore\_agent

Construct a VectorStore agent from an LLM and tools.

Note

This class is deprecated. See below for a replacement that uses tool
calling methods and LangGraph. Install LangGraph with:

```
pip install -U langgraph
```

```
from langchain_core.tools import create_retriever_tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

vector_store = InMemoryVectorStore.from_texts(
    [
        "Dogs are great companions, known for their loyalty and friendliness.",
        "Cats are independent pets that often enjoy their own space.",
    ],
    OpenAIEmbeddings(),
)

tool = create_retriever_tool(
    vector_store.as_retriever(),
    "pet_information_retriever",
    "Fetches information about pets.",
)

agent = create_react_agent(model, [tool])

for step in agent.stream(
    {"messages": [("human", "What are dogs known for?")]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```](/python/langchain-classic/agents/agent_toolkits/vectorstore/base/create_vectorstore_agent)[deprecatedfunction

create\_vectorstore\_router\_agent

Construct a VectorStore router agent from an LLM and tools.

Note

This class is deprecated. See below for a replacement that uses tool calling
methods and LangGraph. Install LangGraph with:

```
pip install -U langgraph
```

```
from langchain_core.tools import create_retriever_tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.prebuilt import create_react_agent

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

pet_vector_store = InMemoryVectorStore.from_texts(
    [
        "Dogs are great companions, known for their loyalty and friendliness.",
        "Cats are independent pets that often enjoy their own space.",
    ],
    OpenAIEmbeddings(),
)

food_vector_store = InMemoryVectorStore.from_texts(
    [
        "Carrots are orange and delicious.",
        "Apples are red and delicious.",
    ],
    OpenAIEmbeddings(),
)

tools = [
    create_retriever_tool(
        pet_vector_store.as_retriever(),
        "pet_information_retriever",
        "Fetches information about pets.",
    ),
    create_retriever_tool(
        food_vector_store.as_retriever(),
        "food_information_retriever",
        "Fetches information about food.",
    ),
]

agent = create_react_agent(model, tools)

for step in agent.stream(
    {"messages": [("human", "Tell me about carrots.")]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```](/python/langchain-classic/agents/agent_toolkits/vectorstore/base/create_vectorstore_router_agent)

## Classes

[class

AgentExecutor

Agent that is using tools.](/python/langchain-classic/agents/agent/AgentExecutor)[class

VectorStoreRouterToolkit

Toolkit for routing between Vector Stores.](/python/langchain-classic/agents/agent_toolkits/vectorstore/toolkit/VectorStoreRouterToolkit)[class

VectorStoreToolkit

Toolkit for interacting with a `VectorStore`.](/python/langchain-classic/agents/agent_toolkits/vectorstore/toolkit/VectorStoreToolkit)[deprecatedclass

ZeroShotAgent

Agent for the MRKL chain.](/python/langchain-classic/agents/mrkl/base/ZeroShotAgent)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)


