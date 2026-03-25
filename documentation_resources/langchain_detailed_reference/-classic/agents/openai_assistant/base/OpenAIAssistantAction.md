<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantAction -->

Classv1.2.13 (latest)●Since v1.0

# OpenAIAssistantAction


```
OpenAIAssistantAction()
```

## Bases

`AgentAction`

## Attributes

## Methods

## Inherited from[AgentAction](/python/langchain-core/agents/AgentAction)(langchain\_core)

### Attributes

[Atool](/python/langchain-core/agents/AgentAction/tool)[Atool\_input](/python/langchain-core/agents/AgentAction/tool_input)[Alog](/python/langchain-core/agents/AgentAction/log)[Atype](/python/langchain-core/agents/AgentAction/type)[Amessages](/python/langchain-core/agents/AgentAction/messages)

### Methods



[Mget\_lc\_namespace](/python/langchain-core/agents/AgentAction/get_lc_namespace)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tool_call_id`\* | `unknown` | Tool call id. |
| `run_id`\* | `unknown` | Run id. |
| `thread_id`\* | `unknown` | Thread id |

[attribute

tool\_call\_id: str](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantAction/tool_call_id)

[attribute

run\_id: str](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantAction/run_id)

[attribute

thread\_id: str](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantAction/thread_id)

[method

is\_lc\_serializable

Check if the class is serializable by LangChain.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantAction/is_lc_serializable)

AgentAction with info needed to submit custom tool output to existing run.