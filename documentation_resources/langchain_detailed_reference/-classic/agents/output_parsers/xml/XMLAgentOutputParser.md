<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser -->

Classv1.2.13 (latest)●Since v1.0

# XMLAgentOutputParser


```
XMLAgentOutputParser()
```

## Bases

`AgentOutputParser`

## Attributes

## Methods

## Inherited from[BaseOutputParser](/python/langchain-core/output_parsers/base/BaseOutputParser)(langchain\_core)

### Attributes

[AInputType](/python/langchain-core/output_parsers/base/BaseOutputParser/InputType)[AOutputType](/python/langchain-core/output_parsers/base/BaseOutputParser/OutputType)

### Methods

[Minvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/invoke)[Mainvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/ainvoke)



M

parse\_result

[Maparse\_result](/python/langchain-core/output_parsers/base/BaseOutputParser/aparse_result)

[Maparse](/python/langchain-core/output_parsers/base/BaseOutputParser/aparse)

[Mparse\_with\_prompt](/python/langchain-core/output_parsers/base/BaseOutputParser/parse_with_prompt)

[Mdict](/python/langchain-core/output_parsers/base/BaseOutputParser/dict)

## Inherited from[BaseLLMOutputParser](/python/langchain-core/output_parsers/base/BaseLLMOutputParser)(langchain\_core)

### Methods

[Mparse\_result](/python/langchain-core/output_parsers/base/BaseLLMOutputParser/parse_result)[Maparse\_result](/python/langchain-core/output_parsers/base/BaseLLMOutputParser/aparse_result)

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
| `escape_format`\* | `unknown` | The escaping format to use when parsing XML content. Supports 'minimal' which uses custom delimiters like [[tool]] to replace XML tags within content, preventing parsing conflicts. Use 'minimal' if using a corresponding encoding format that uses the \_escape function when formatting the output (e.g., with format\_xml). |

[attribute

escape\_format: Literal['minimal'] | None

The format to use for escaping XML characters.

minimal - uses custom delimiters to replace XML tags within content,
preventing parsing conflicts. This is the only supported format currently.

None - no escaping is applied, which may lead to parsing conflicts.](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser/escape_format)

[method

parse](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser/parse)

[method

get\_format\_instructions](/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser/get_format_instructions)

Parses tool invocations and final answers from XML-formatted agent output.

This parser extracts structured information from XML tags to determine whether
an agent should perform a tool action or provide a final answer. It includes
built-in escaping support to safely handle tool names and inputs
containing XML special characters.

**Expected formats:**

Tool invocation (returns AgentAction):
search
<tool\_input>what is 2 + 2</tool\_input>

Final answer (returns AgentFinish):
<final\_answer>The answer is 4</final\_answer>

Minimal escaping allows tool names containing XML tags to be safely represented.
For example, a tool named `search<tool>nested</tool>` would be escaped as
`search[[tool]]nested[[/tool]]` in the XML and automatically unescaped during
parsing.

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