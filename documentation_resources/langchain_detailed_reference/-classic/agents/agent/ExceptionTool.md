<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/ExceptionTool -->

Classv1.2.13 (latest)●Since v1.0

# ExceptionTool


```
ExceptionTool()
```

## Bases

`BaseTool`

## Attributes

## Inherited from[BaseTool](/python/langchain-core/tools/base/BaseTool)(langchain\_core)

### Attributes

[Aargs\_schema](/python/langchain-core/tools/base/BaseTool/args_schema)[Areturn\_direct](/python/langchain-core/tools/base/BaseTool/return_direct)[Averbose](/python/langchain-core/tools/base/BaseTool/verbose)[Acallbacks](/python/langchain-core/tools/base/BaseTool/callbacks)[Atags](/python/langchain-core/tools/base/BaseTool/tags)



A

metadata

[Ahandle\_tool\_error](/python/langchain-core/tools/base/BaseTool/handle_tool_error)

[Ahandle\_validation\_error](/python/langchain-core/tools/base/BaseTool/handle_validation_error)

[Aresponse\_format](/python/langchain-core/tools/base/BaseTool/response_format)

[Aextras](/python/langchain-core/tools/base/BaseTool/extras)

[Amodel\_config](/python/langchain-core/tools/base/BaseTool/model_config)

[Ais\_single\_input](/python/langchain-core/tools/base/BaseTool/is_single_input)

[Aargs](/python/langchain-core/tools/base/BaseTool/args)

[Atool\_call\_schema](/python/langchain-core/tools/base/BaseTool/tool_call_schema)

### Methods

[Mget\_input\_schema](/python/langchain-core/tools/base/BaseTool/get_input_schema)[Minvoke](/python/langchain-core/tools/base/BaseTool/invoke)[Mainvoke](/python/langchain-core/tools/base/BaseTool/ainvoke)[Mrun](/python/langchain-core/tools/base/BaseTool/run)[Marun](/python/langchain-core/tools/base/BaseTool/arun)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

name: str

Name of the tool.](/python/langchain-classic/agents/agent/ExceptionTool/name)

[attribute

description: str

Description of the tool.](/python/langchain-classic/agents/agent/ExceptionTool/description)

Tool that just returns the query.

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