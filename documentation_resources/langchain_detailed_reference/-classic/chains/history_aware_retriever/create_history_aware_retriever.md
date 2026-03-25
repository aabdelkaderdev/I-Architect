<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/history_aware_retriever/create_history_aware_retriever -->

Functionv1.2.13 (latest)●Since v1.0

# create\_history\_aware\_retriever

Create a chain that takes conversation history and returns documents.

If there is no `chat_history`, then the `input` is just passed directly to the
retriever. If there is `chat_history`, then the prompt and LLM will be used
to generate a search query. That search query is then passed to the retriever.


```
create_history_aware_retriever(
  llm: LanguageModelLike,
  retriever: RetrieverLike,
  prompt: BasePromptTemplate
) -> RetrieverOutputLike
```

**Example:**

```
# pip install -U langchain langchain-community

from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_history_aware_retriever
from langchain_classic import hub

rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
model = ChatOpenAI()
retriever = ...
chat_retriever_chain = create_history_aware_retriever(
    model, retriever, rephrase_prompt
)

chain.invoke({"input": "...", "chat_history": })
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `LanguageModelLike` | Language model to use for generating a search term given chat history |
| `retriever`\* | `RetrieverLike` | `RetrieverLike` object that takes a string as input and outputs a list of `Document` objects. |
| `prompt`\* | `BasePromptTemplate` | The prompt used to generate the search query for the retriever. |


