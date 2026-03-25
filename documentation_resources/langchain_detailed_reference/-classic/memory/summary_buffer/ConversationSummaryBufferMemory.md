<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationSummaryBufferMemory


```
ConversationSummaryBufferMemory()
```

## Bases

`BaseChatMemory``SummarizerMixin`

## Attributes

## Methods

## Inherited from[BaseChatMemory](/python/langchain-classic/memory/chat_memory/BaseChatMemory)

### Attributes

[Achat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)[Aoutput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/output_key)[Ainput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)[Areturn\_messages: bool](/python/langchain-classic/memory/chat_memory/BaseChatMemory/return_messages)

##



Inherited from

[SummarizerMixin](/python/langchain-classic/memory/summary/SummarizerMixin)

### Attributes

[Ahuman\_prefix: str](/python/langchain-classic/memory/summary/SummarizerMixin/human_prefix)[Aai\_prefix: str](/python/langchain-classic/memory/summary/SummarizerMixin/ai_prefix)[Allm: BaseLanguageModel](/python/langchain-classic/memory/summary/SummarizerMixin/llm)[Aprompt: BasePromptTemplate](/python/langchain-classic/memory/summary/SummarizerMixin/prompt)[Asummary\_message\_cls: type[BaseMessage]](/python/langchain-classic/memory/summary/SummarizerMixin/summary_message_cls)

### Methods

[Mpredict\_new\_summary

—

Predict a new summary based on the messages and existing summary.](/python/langchain-classic/memory/summary/SummarizerMixin/predict_new_summary)[Mapredict\_new\_summary

—

Predict a new summary based on the messages and existing summary.](/python/langchain-classic/memory/summary/SummarizerMixin/apredict_new_summary)

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

max\_token\_limit: int](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/max_token_limit)

[attribute

moving\_summary\_buffer: str](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/moving_summary_buffer)

[attribute

memory\_key: str](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/memory_key)

[attribute

buffer: str | list[BaseMessage]

String buffer of memory.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/buffer)

[attribute

memory\_variables: list[str]

Will always return list of memory variables.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/memory_variables)

[method

abuffer

Async memory buffer.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/abuffer)

[method

load\_memory\_variables

Return history buffer.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/load_memory_variables)

[method

aload\_memory\_variables

Asynchronously return key-value pairs given the text input to the chain.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/aload_memory_variables)

[method

validate\_prompt\_input\_variables

Validate that prompt input variables are consistent.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/validate_prompt_input_variables)

[method

save\_context

Save context from this conversation to buffer.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/save_context)

[method

asave\_context

Asynchronously save context from this conversation to buffer.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/asave_context)

[method

prune

Prune buffer if it exceeds max token limit.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/prune)

[method

aprune

Asynchronously prune buffer if it exceeds max token limit.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/aprune)

[method

clear

Clear memory contents.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/clear)

[method

aclear

Asynchronously clear memory contents.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory/aclear)

Buffer with summarizer for storing conversation memory.

Provides a running summary of the conversation together with the most recent
messages in the conversation under the constraint that the total number of
tokens in the conversation does not exceed a certain limit.