<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/tools/ToolAgentAction -->

Classv1.2.13 (latest)●Since v1.0

# ToolAgentAction


```
ToolAgentAction()
```

## Bases

`AgentActionMessageLog`

## Attributes

## Inherited from[AgentActionMessageLog](/python/langchain-core/agents/AgentActionMessageLog)(langchain\_core)

### Attributes

[Amessage\_log](/python/langchain-core/agents/AgentActionMessageLog/message_log)[Atype](/python/langchain-core/agents/AgentActionMessageLog/type)

## Inherited from[AgentAction](/python/langchain-core/agents/AgentAction)(langchain\_core)

### Attributes

[Atool](/python/langchain-core/agents/AgentAction/tool)



A

tool\_input

[Alog](/python/langchain-core/agents/AgentAction/log)

[Atype](/python/langchain-core/agents/AgentAction/type)

[Amessages](/python/langchain-core/agents/AgentAction/messages)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/agents/AgentAction/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/agents/AgentAction/get_lc_namespace)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

tool\_call\_id: str | None

Tool call that this message is responding to.](/python/langchain-classic/agents/output_parsers/tools/ToolAgentAction/tool_call_id)

Tool agent action.