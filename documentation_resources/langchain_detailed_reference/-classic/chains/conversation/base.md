<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversation/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain that carries on a conversation and calls an LLM.

## Attributes

[attribute

PROMPT](/python/langchain-classic/chains/conversation/prompt/PROMPT)

## Classes

[deprecatedclass

BaseMemory

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.](/python/langchain-classic/base_memory/BaseMemory)[deprecatedclass

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

ConversationBufferMemory

A basic memory implementation that simply stores the conversation history.

This stores the entire conversation history in memory without any
additional processing.

Note that additional processing may be required in some situations when the
conversation history is too large to fit in the context window of the model.](/python/langchain-classic/memory/buffer/ConversationBufferMemory)[deprecatedclass

ConversationChain

Chain to have a conversation and load context from memory.

This class is deprecated in favor of `RunnableWithMessageHistory`. Please refer
to this tutorial for more detail: <https://python.langchain.com/docs/tutorials/chatbot/>

`RunnableWithMessageHistory` offers several benefits, including:

- Stream, batch, and async support;
- More flexible memory handling, including the ability to manage memory
  outside the chain;
- Support for multiple threads.

Below is a minimal implementation, analogous to using `ConversationChain` with
the default `ConversationBufferMemory`:

```
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}  # memory is maintained outside the chain

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

chain = RunnableWithMessageHistory(model, get_session_history)
chain.invoke(
    "Hi I'm Bob.",
    config={"configurable": {"session_id": "1"}},
)  # session_id determines thread
```

Memory objects can also be incorporated into the `get_session_history` callable:

```
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}  # memory is maintained outside the chain

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    memory = ConversationBufferWindowMemory(
        chat_memory=store[session_id],
        k=3,
        return_messages=True,
    )
    assert len(memory.memory_variables) == 1
    key = memory.memory_variables[0]
    messages = memory.load_memory_variables({})[key]
    store[session_id] = InMemoryChatMessageHistory(messages=messages)
    return store[session_id]

model = ChatOpenAI(model="gpt-3.5-turbo-0125")

chain = RunnableWithMessageHistory(model, get_session_history)
chain.invoke(
    "Hi I'm Bob.",
    config={"configurable": {"session_id": "1"}},
)  # session_id determines thread
```](/python/langchain-classic/chains/conversation/base/ConversationChain)


