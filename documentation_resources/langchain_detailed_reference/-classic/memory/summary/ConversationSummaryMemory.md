<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary/ConversationSummaryMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationSummaryMemory


```
ConversationSummaryMemory()
```

## Bases

`BaseChatMemory``SummarizerMixin`

## Attributes

## Methods

## Inherited from[BaseChatMemory](/python/langchain-classic/memory/chat_memory/BaseChatMemory)

### Attributes

[Achat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)[Aoutput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/output_key)[Ainput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)[Areturn\_messages: bool](/python/langchain-classic/memory/chat_memory/BaseChatMemory/return_messages)

### Methods



[Masave\_context

—

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)[Maclear

—

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/aclear)

## Inherited from[SummarizerMixin](/python/langchain-classic/memory/summary/SummarizerMixin)

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

### Methods

[Maload\_memory\_variables

—

Async return key-value pairs given the text input to the chain.](/python/langchain-classic/base_memory/BaseMemory/aload_memory_variables)[Masave\_context

—

Async save the context of this chain run to memory.](/python/langchain-classic/base_memory/BaseMemory/asave_context)[Maclear

—

Async clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/aclear)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

buffer: str](/python/langchain-classic/memory/summary/ConversationSummaryMemory/buffer)

[attribute

memory\_key: str](/python/langchain-classic/memory/summary/ConversationSummaryMemory/memory_key)

[attribute

memory\_variables: list[str]

Will always return list of memory variables.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/memory_variables)

[method

from\_messages

Create a ConversationSummaryMemory from a list of messages.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/from_messages)

[method

load\_memory\_variables

Return history buffer.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/load_memory_variables)

[method

validate\_prompt\_input\_variables

Validate that prompt input variables are consistent.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/validate_prompt_input_variables)

[method

save\_context

Save context from this conversation to buffer.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/save_context)

[method

clear

Clear memory contents.](/python/langchain-classic/memory/summary/ConversationSummaryMemory/clear)

Continually summarizes the conversation history.

The summary is updated after each conversation turn.
The implementations returns a summary of the conversation history which
can be used to provide context to the model.