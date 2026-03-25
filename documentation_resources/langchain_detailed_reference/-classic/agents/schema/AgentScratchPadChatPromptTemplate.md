<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/schema/AgentScratchPadChatPromptTemplate -->

Classv1.2.13 (latest)●Since v1.0

# AgentScratchPadChatPromptTemplate


```
AgentScratchPadChatPromptTemplate()
```

## Bases

`ChatPromptTemplate`

## Methods

## Inherited from[ChatPromptTemplate](/python/langchain-core/prompts/chat/ChatPromptTemplate)(langchain\_core)

### Attributes

[Amessages](/python/langchain-core/prompts/chat/ChatPromptTemplate/messages)[Avalidate\_template](/python/langchain-core/prompts/chat/ChatPromptTemplate/validate_template)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/prompts/chat/ChatPromptTemplate/get_lc_namespace)[Mvalidate\_input\_variables](/python/langchain-core/prompts/chat/ChatPromptTemplate/validate_input_variables)



M

from\_template

[Mfrom\_messages](/python/langchain-core/prompts/chat/ChatPromptTemplate/from_messages)

[Mformat\_messages](/python/langchain-core/prompts/chat/ChatPromptTemplate/format_messages)

[Maformat\_messages](/python/langchain-core/prompts/chat/ChatPromptTemplate/aformat_messages)

[Mpartial](/python/langchain-core/prompts/chat/ChatPromptTemplate/partial)

[Mappend](/python/langchain-core/prompts/chat/ChatPromptTemplate/append)

[Mextend](/python/langchain-core/prompts/chat/ChatPromptTemplate/extend)

[Msave](/python/langchain-core/prompts/chat/ChatPromptTemplate/save)

[Mpretty\_repr](/python/langchain-core/prompts/chat/ChatPromptTemplate/pretty_repr)

## Inherited from[BaseChatPromptTemplate](/python/langchain-core/prompts/chat/BaseChatPromptTemplate)(langchain\_core)

### Attributes

[Alc\_attributes](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/lc_attributes)

### Methods

[Mformat](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/format)[Maformat](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/aformat)[Mformat\_prompt](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/format_prompt)[Maformat\_prompt](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/aformat_prompt)[Mformat\_messages](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/format_messages)[Maformat\_messages](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/aformat_messages)[Mpretty\_repr](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/pretty_repr)[Mpretty\_print](/python/langchain-core/prompts/chat/BaseChatPromptTemplate/pretty_print)

## Inherited from[BasePromptTemplate](/python/langchain-core/prompts/base/BasePromptTemplate)(langchain\_core)

### Attributes

[Ainput\_variables](/python/langchain-core/prompts/base/BasePromptTemplate/input_variables)[Aoptional\_variables](/python/langchain-core/prompts/base/BasePromptTemplate/optional_variables)[Ainput\_types](/python/langchain-core/prompts/base/BasePromptTemplate/input_types)[Aoutput\_parser](/python/langchain-core/prompts/base/BasePromptTemplate/output_parser)[Apartial\_variables](/python/langchain-core/prompts/base/BasePromptTemplate/partial_variables)[Ametadata](/python/langchain-core/prompts/base/BasePromptTemplate/metadata)[Atags](/python/langchain-core/prompts/base/BasePromptTemplate/tags)[Amodel\_config](/python/langchain-core/prompts/base/BasePromptTemplate/model_config)[AOutputType](/python/langchain-core/prompts/base/BasePromptTemplate/OutputType)

### Methods

[Mvalidate\_variable\_names](/python/langchain-core/prompts/base/BasePromptTemplate/validate_variable_names)[Mget\_lc\_namespace](/python/langchain-core/prompts/base/BasePromptTemplate/get_lc_namespace)[Mget\_input\_schema](/python/langchain-core/prompts/base/BasePromptTemplate/get_input_schema)[Minvoke](/python/langchain-core/prompts/base/BasePromptTemplate/invoke)[Mainvoke](/python/langchain-core/prompts/base/BasePromptTemplate/ainvoke)[Mformat\_prompt](/python/langchain-core/prompts/base/BasePromptTemplate/format_prompt)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[method

is\_lc\_serializable](/python/langchain-classic/agents/schema/AgentScratchPadChatPromptTemplate/is_lc_serializable)

Chat prompt template for the agent scratchpad.

[Maformat\_prompt](/python/langchain-core/prompts/base/BasePromptTemplate/aformat_prompt)

[Mpartial](/python/langchain-core/prompts/base/BasePromptTemplate/partial)

[Mformat](/python/langchain-core/prompts/base/BasePromptTemplate/format)

[Maformat](/python/langchain-core/prompts/base/BasePromptTemplate/aformat)

[Mdict](/python/langchain-core/prompts/base/BasePromptTemplate/dict)

[Msave](/python/langchain-core/prompts/base/BasePromptTemplate/save)

M

get\_config\_jsonschema

[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)

[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)

[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)

[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)

[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)

[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)

[Mstream](/python/langchain-core/runnables/base/Runnable/stream)

[Mastream](/python/langchain-core/runnables/base/Runnable/astream)

[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)

[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)

[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)

[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)

[Mbind](/python/langchain-core/runnables/base/Runnable/bind)

[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)

[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)

[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)

[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)

[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)

[Mmap](/python/langchain-core/runnables/base/Runnable/map)

[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)

[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)