<!-- Source: https://reference.langchain.com/python/langchain-classic/runnables/openai_functions/OpenAIFunctionsRouter -->

Classv1.2.13 (latest)●Since v1.0

# OpenAIFunctionsRouter


```
OpenAIFunctionsRouter(
  self,
  runnables: Mapping[str, Runnable[dict, Any] | Callable[[dict],
```

## Bases

`RunnableBindingBase[BaseMessage, Any]`

## Constructors

## Attributes

## Inherited from[RunnableBindingBase](/python/langchain-core/runnables/base/RunnableBindingBase)(langchain\_core)

### Attributes

[Abound](/python/langchain-core/runnables/base/RunnableBindingBase/bound)[Akwargs](/python/langchain-core/runnables/base/RunnableBindingBase/kwargs)[Aconfig](/python/langchain-core/runnables/base/RunnableBindingBase/config)[Aconfig\_factories](/python/langchain-core/runnables/base/RunnableBindingBase/config_factories)[A](/python/langchain-core/runnables/base/RunnableBindingBase/custom_input_type)



Any

]

]

,

functions

:

[list](https://docs.python.org/3/library/stdtypes.html#list)

[

[OpenAIFunction](/python/langchain-classic/runnables/openai_functions/OpenAIFunction)

]

|

None

=

None

)

custom\_input\_type

[Acustom\_output\_type](/python/langchain-core/runnables/base/RunnableBindingBase/custom_output_type)

[Amodel\_config](/python/langchain-core/runnables/base/RunnableBindingBase/model_config)

[AInputType](/python/langchain-core/runnables/base/RunnableBindingBase/InputType)

[AOutputType](/python/langchain-core/runnables/base/RunnableBindingBase/OutputType)

[Aconfig\_specs](/python/langchain-core/runnables/base/RunnableBindingBase/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/RunnableBindingBase/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_input_schema)[Mget\_output\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_output_schema)[Mget\_graph](/python/langchain-core/runnables/base/RunnableBindingBase/get_graph)[Mis\_lc\_serializable](/python/langchain-core/runnables/base/RunnableBindingBase/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/runnables/base/RunnableBindingBase/get_lc_namespace)[Minvoke](/python/langchain-core/runnables/base/RunnableBindingBase/invoke)[Mainvoke](/python/langchain-core/runnables/base/RunnableBindingBase/ainvoke)[Mbatch](/python/langchain-core/runnables/base/RunnableBindingBase/batch)[Mabatch](/python/langchain-core/runnables/base/RunnableBindingBase/abatch)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/batch_as_completed)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/RunnableBindingBase/stream)[Mastream](/python/langchain-core/runnables/base/RunnableBindingBase/astream)[Mastream\_events](/python/langchain-core/runnables/base/RunnableBindingBase/astream_events)[Mtransform](/python/langchain-core/runnables/base/RunnableBindingBase/transform)[Matransform](/python/langchain-core/runnables/base/RunnableBindingBase/atransform)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `runnables`\* | `Mapping[str, Runnable[dict, Any] | Callable[[dict], Any]]` | A mapping of function names to runnables. |
| `functions` | `list[OpenAIFunction] | None` | Default:`None` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| runnables | [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Runnable](/python/langchain-core/runnables/base/Runnable)[[dict](https://docs.python.org/3/library/stdtypes.html#dict), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[dict](https://docs.python.org/3/library/stdtypes.html#dict)], [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |
| functions | [list](https://docs.python.org/3/library/stdtypes.html#list)[[OpenAIFunction](/python/langchain-classic/runnables/openai_functions/OpenAIFunction)] | None |

[attribute

functions: list[OpenAIFunction] | None](/python/langchain-classic/runnables/openai_functions/OpenAIFunctionsRouter/functions)

A runnable that routes to the selected function.

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

Optional list of functions to check against the runnables.