<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory -->

Classv1.2.13 (latest)●Since v1.0

# ConversationVectorStoreTokenBufferMemory


```
ConversationVectorStoreTokenBufferMemory()
```

## Bases

[ConversationTokenBufferMemory](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory)

## Attributes

[attribute

retriever: VectorStoreRetriever](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/retriever)[attribute

memory\_key: str](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/memory_key)[attribute

previous\_history\_template: str](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/previous_history_template)[attribute

split\_chunk\_size: int](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/split_chunk_size)[attribute

memory\_retriever: VectorStoreRetrieverMemory](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/memory_retriever)

## Methods

[method

load\_memory\_variables](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/load_memory_variables)[method

save\_context](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/save_context)[method

save\_remainder](/python/langchain-classic/memory/vectorstore_token_buffer_memory/ConversationVectorStoreTokenBufferMemory/save_remainder)

## Inherited from[ConversationTokenBufferMemory](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory)

### Attributes

[Ahuman\_prefix: str](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/human_prefix)[Aai\_prefix: str](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/ai_prefix)[Allm: BaseLanguageModel](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/llm)[Amax\_token\_limit: int](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/max_token_limit)[Abuffer: Any

—

String buffer of memory.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer)[Abuffer\_as\_str: str

—

Exposes the buffer as a string in case return\_messages is False.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer_as_str)[Abuffer\_as\_messages: list[BaseMessage]

—

Exposes the buffer as a list of messages in case return\_messages is True.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer_as_messages)[Amemory\_variables: list[str]

—

Will always return list of memory variables.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/memory_variables)

## Inherited from[BaseChatMemory](/python/langchain-classic/memory/chat_memory/BaseChatMemory)

### Attributes

[Achat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)[Aoutput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/output_key)[Ainput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)[Areturn\_messages: bool](/python/langchain-classic/memory/chat_memory/BaseChatMemory/return_messages)

### Methods

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)[Amemory\_variables: list[str]

—

The string keys this memory class will add to chain inputs.](/python/langchain-classic/base_memory/BaseMemory/memory_variables)

### Methods

[Maload\_memory\_variables

—

Async return key-value pairs given the text input to the chain.](/python/langchain-classic/base_memory/BaseMemory/aload_memory_variables)[M](/python/langchain-classic/base_memory/BaseMemory/asave_context)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)



Conversation chat memory with token limit and vectordb backing.

load\_memory\_variables() will return a dict with the key "history".
It contains background information retrieved from the vector store
plus recent lines of the current conversation.

To help the LLM understand the part of the conversation stored in the
vectorstore, each interaction is timestamped and the current date and
time is also provided in the history. A side effect of this is that the
LLM will have access to the current date and time.

Initialization arguments:

This class accepts all the initialization arguments of
ConversationTokenBufferMemory, such as `llm`. In addition, it
accepts the following additional arguments

```
retriever: (required) A VectorStoreRetriever object to use
    as the vector backing store

split_chunk_size: (optional, 1000) Token chunk split size
    for long messages generated by the AI

previous_history_template: (optional) Template used to format
    the contents of the prompt history
```

Example using ChromaDB:

```
from langchain_classic.memory.token_buffer_vectorstore_memory import (
    ConversationVectorStoreTokenBufferMemory,
)
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_openai import OpenAI

embedder = HuggingFaceInstructEmbeddings(
    query_instruction="Represent the query for retrieval: "
)
chroma = Chroma(
    collection_name="demo",
    embedding_function=embedder,
    collection_metadata={"hnsw:space": "cosine"},
)

retriever = chroma.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.75,
    },
)

conversation_memory = ConversationVectorStoreTokenBufferMemory(
    return_messages=True,
    llm=OpenAI(),
    retriever=retriever,
    max_token_limit=1000,
)

conversation_memory.save_context({"Human": "Hi there"}, {"AI": "Nice to meet you!"})
conversation_memory.save_context(
    {"Human": "Nice day isn't it?"}, {"AI": "I love Wednesdays."}
)
conversation_memory.load_memory_variables({"input": "What time is it?"})
```

[Masave\_context

—

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)[Mclear

—

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/clear)[Maclear

—

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/aclear)

asave\_context

—

Async save the context of this chain run to memory.

[Mclear

—

Clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/clear)

[Maclear

—

Async clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/aclear)

M

get\_lc\_namespace

[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)

[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

Return a memory retriever from the passed retriever object.

Return history and memory buffer.

Save context from this conversation to buffer. Pruned.

Save the remainder of the conversation buffer to the vector store.

Useful if you have made the VectorStore persistent, in which
case this can be called before the end of the session to store the
remainder of the conversation.