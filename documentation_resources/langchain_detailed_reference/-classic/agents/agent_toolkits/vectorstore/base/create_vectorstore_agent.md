<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_toolkits/vectorstore/base/create_vectorstore_agent -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# create\_vectorstore\_agent

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
```


```
create_vectorstore_agent(
  llm: BaseLanguageModel,
  toolkit: VectorStoreToolkit,
  callback_manager: BaseCallbackManager | None = None,
  prefix: str = PREFIX,
  verbose: bool = False,
  agent_executor_kwargs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> AgentExecutor
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | LLM that will be used by the agent |
| `toolkit`\* | `VectorStoreToolkit` | Set of tools for the agent |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  Object to handle the callback |
| `prefix` | `str` | Default:`PREFIX`  The prefix prompt for the agent. |
| `verbose` | `bool` | Default:`False`  If you want to see the content of the scratchpad. |
| `agent_executor_kwargs` | `dict[str, Any] | None` | Default:`None`  If there is any other parameter you want to send to the agent. |
| `kwargs` | `Any` | Default:`{}`  Additional named parameters to pass to the `ZeroShotAgent`. |


