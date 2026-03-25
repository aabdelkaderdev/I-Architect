<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_toolkits -->

Modulev1.2.13 (latest)●Since v1.0

# agent\_toolkits

Agent toolkits contain integrations with various resources and services.

LangChain has a large ecosystem of integrations with various external resources
like local and remote file systems, APIs and databases.

These integrations allow developers to create versatile applications that combine the
power of LLMs with the ability to access, interact with and manipulate external
resources.

When developing an application, developers should inspect the capabilities and
permissions of the tools that underlie the given agent toolkit, and determine
whether permissions of the given toolkit are appropriate for the application.

See <https://docs.langchain.com/oss/python/security-policy> for more information.

## Attributes

[attribute

DEPRECATED\_AGENTS: list](/python/langchain-classic/agents/agent_toolkits/DEPRECATED_AGENTS)[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/agents/agent_toolkits/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)[function

create\_conversational\_retrieval\_agent

A convenience method for creating a conversational retrieval agent.](/python/langchain-classic/agents/agent_toolkits/conversational_retrieval/openai_functions/create_conversational_retrieval_agent)[deprecatedfunction

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

VectorStoreInfo

Information about a `VectorStore`.](/python/langchain-classic/agents/agent_toolkits/vectorstore/toolkit/VectorStoreInfo)[class

VectorStoreRouterToolkit

Toolkit for routing between Vector Stores.](/python/langchain-classic/agents/agent_toolkits/vectorstore/toolkit/VectorStoreRouterToolkit)[class

VectorStoreToolkit

Toolkit for interacting with a `VectorStore`.](/python/langchain-classic/agents/agent_toolkits/vectorstore/toolkit/VectorStoreToolkit)

## Modules

[module

base](/python/langchain-classic/agents/agent_toolkits/base)[module

azure\_cognitive\_services](/python/langchain-classic/agents/agent_toolkits/azure_cognitive_services)[module

gmail

Gmail toolkit.](/python/langchain-classic/agents/agent_toolkits/gmail)[module

python](/python/langchain-classic/agents/agent_toolkits/python)[module

office365

Office365 toolkit.](/python/langchain-classic/agents/agent_toolkits/office365)[module

jira

Jira Toolkit.](/python/langchain-classic/agents/agent_toolkits/jira)[module

playwright

Playwright browser toolkit.](/python/langchain-classic/agents/agent_toolkits/playwright)[module

github

GitHub Toolkit.](/python/langchain-classic/agents/agent_toolkits/github)[module

file\_management

Local file management toolkit.](/python/langchain-classic/agents/agent_toolkits/file_management)[module

spark\_sql

Spark SQL agent.](/python/langchain-classic/agents/agent_toolkits/spark_sql)[module

openapi

OpenAPI spec agent.](/python/langchain-classic/agents/agent_toolkits/openapi)[module

vectorstore

Agent toolkit for interacting with vector stores.](/python/langchain-classic/agents/agent_toolkits/vectorstore)[module

steam

Steam Toolkit.](/python/langchain-classic/agents/agent_toolkits/steam)[module

powerbi

Power BI agent.](/python/langchain-classic/agents/agent_toolkits/powerbi)[module

nasa

NASA Toolkit.](/python/langchain-classic/agents/agent_toolkits/nasa)[module

multion

MultiOn Toolkit.](/python/langchain-classic/agents/agent_toolkits/multion)[module

conversational\_retrieval](/python/langchain-classic/agents/agent_toolkits/conversational_retrieval)[module

gitlab

GitLab Toolkit.](/python/langchain-classic/agents/agent_toolkits/gitlab)[module

sql

SQL agent.](/python/langchain-classic/agents/agent_toolkits/sql)[module

zapier

Zapier Toolkit.](/python/langchain-classic/agents/agent_toolkits/zapier)[module

pandas](/python/langchain-classic/agents/agent_toolkits/pandas)[module

amadeus](/python/langchain-classic/agents/agent_toolkits/amadeus)[module

ainetwork

AINetwork toolkit.](/python/langchain-classic/agents/agent_toolkits/ainetwork)[module

slack

Slack toolkit.](/python/langchain-classic/agents/agent_toolkits/slack)[module

clickup](/python/langchain-classic/agents/agent_toolkits/clickup)[module

xorbits](/python/langchain-classic/agents/agent_toolkits/xorbits)[module

nla](/python/langchain-classic/agents/agent_toolkits/nla)[module

csv](/python/langchain-classic/agents/agent_toolkits/csv)[module

json

Json agent.](/python/langchain-classic/agents/agent_toolkits/json)[module

spark](/python/langchain-classic/agents/agent_toolkits/spark)


