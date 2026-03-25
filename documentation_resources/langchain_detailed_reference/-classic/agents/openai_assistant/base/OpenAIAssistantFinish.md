<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantFinish -->

Classv1.2.13 (latest)●Since v1.0

# OpenAIAssistantFinish


```
OpenAIAssistantFinish()
```

## Bases

`AgentFinish`

## Attributes

## Methods

## Inherited from[AgentFinish](/python/langchain-core/agents/AgentFinish)(langchain\_core)

### Attributes

[Areturn\_values](/python/langchain-core/agents/AgentFinish/return_values)[Alog](/python/langchain-core/agents/AgentFinish/log)[Atype](/python/langchain-core/agents/AgentFinish/type)[Amessages](/python/langchain-core/agents/AgentFinish/messages)

### Methods

[M](/python/langchain-core/agents/AgentFinish/get_lc_namespace)



get\_lc\_namespace

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `run_id`\* | `unknown` | Run id. |
| `thread_id`\* | `unknown` | Thread id. |

[attribute

run\_id: str](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantFinish/run_id)

[attribute

thread\_id: str](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantFinish/thread_id)

[method

is\_lc\_serializable

Check if the class is serializable by LangChain.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantFinish/is_lc_serializable)

AgentFinish with run and thread metadata.