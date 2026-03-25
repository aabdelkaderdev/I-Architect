<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/entity -->

Modulev1.2.13 (latest)●Since v1.0

# entity

Deprecated as of LangChain v0.3.4 and will be removed in LangChain v1.0.0.

## Attributes

[attribute

ENTITY\_EXTRACTION\_PROMPT](/python/langchain-classic/memory/prompt/ENTITY_EXTRACTION_PROMPT)[attribute

ENTITY\_SUMMARIZATION\_PROMPT](/python/langchain-classic/memory/prompt/ENTITY_SUMMARIZATION_PROMPT)[attribute

logger](/python/langchain-classic/memory/entity/logger)

## Functions

[function

get\_prompt\_input\_key

Get the prompt input key.](/python/langchain-classic/memory/utils/get_prompt_input_key)

## Classes

[deprecatedclass

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

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)[deprecatedclass

BaseEntityStore

Abstract base class for Entity store.](/python/langchain-classic/memory/entity/BaseEntityStore)[deprecatedclass

InMemoryEntityStore

In-memory Entity store.](/python/langchain-classic/memory/entity/InMemoryEntityStore)[deprecatedclass

UpstashRedisEntityStore

Upstash Redis backed Entity store.

Entities get a TTL of 1 day by default, and
that TTL is extended by 3 days every time the entity is read back.](/python/langchain-classic/memory/entity/UpstashRedisEntityStore)[deprecatedclass

RedisEntityStore

Redis-backed Entity store.

Entities get a TTL of 1 day by default, and
that TTL is extended by 3 days every time the entity is read back.](/python/langchain-classic/memory/entity/RedisEntityStore)[deprecatedclass

SQLiteEntityStore

SQLite-backed Entity store with safe query construction.](/python/langchain-classic/memory/entity/SQLiteEntityStore)[deprecatedclass

ConversationEntityMemory

Entity extractor & summarizer memory.

Extracts named entities from the recent chat history and generates summaries.
With a swappable entity store, persisting entities across conversations.
Defaults to an in-memory entity store, and can be swapped out for a Redis,
SQLite, or other entity store.](/python/langchain-classic/memory/entity/ConversationEntityMemory)


