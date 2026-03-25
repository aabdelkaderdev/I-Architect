<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/xml/XMLOutputParser -->

Classv1.2.21 (latest)●Since v0.1

# XMLOutputParser

Parse an output using xml format.

Returns a dictionary of tags.


```
XMLOutputParser(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`BaseTransformOutputParser`

## Attributes

[attribute

tags: list[str] | None

Tags to tell the LLM to expect in the XML output.

```
Note this may not be perfect depending on the LLM implementation.

For example, with `tags=["foo", "bar", "baz"]`:

1. A well-formatted XML instance:
    `'<foo>
```

'`

```
2. A badly-formatted XML instance (missing closing tag for 'bar'):
    `'<foo>
```

'`

```
3. A badly-formatted XML instance (unexpected 'tag' element):
    `'<foo>
```

'`](/python/langchain-core/output_parsers/xml/XMLOutputParser/tags)[attribute

encoding\_matcher: re.Pattern](/python/langchain-core/output_parsers/xml/XMLOutputParser/encoding_matcher)[attribute

parser: Literal['defusedxml', 'xml']

Parser to use for XML parsing.

Can be either `'defusedxml'` or `'xml'`.

- `'defusedxml'` is the default parser and is used to prevent XML vulnerabilities
  present in some distributions of Python's standard library xml. `defusedxml` is
  a wrapper around the standard library parser that sets up the parser with secure
  defaults.
- `'xml'` is the standard library parser.

Warning

Use `xml` only if you are sure that your distribution of the standard library is
not vulnerable to XML vulnerabilities.

Review the following resources for more information:

- <https://docs.python.org/3/library/xml.html#xml-vulnerabilities>
- <https://github.com/tiran/defusedxml>

The standard library relies on [`libexpat`](https://github.com/libexpat/libexpat)
for parsing XML.](/python/langchain-core/output_parsers/xml/XMLOutputParser/parser)

## Methods

[method

get\_format\_instructions

Return the format instructions for the XML output.](/python/langchain-core/output_parsers/xml/XMLOutputParser/get_format_instructions)[method

parse

Parse the output of an LLM call.](/python/langchain-core/output_parsers/xml/XMLOutputParser/parse)

## Inherited from[BaseTransformOutputParser](/python/langchain-core/output_parsers/transform/BaseTransformOutputParser)

### Methods

[Mtransform

—

Transform the input into the output format.](/python/langchain-core/output_parsers/transform/BaseTransformOutputParser/transform)[Matransform

—

Async transform the input into the output format.](/python/langchain-core/output_parsers/transform/BaseTransformOutputParser/atransform)

## Inherited from[BaseOutputParser](/python/langchain-core/output_parsers/base/BaseOutputParser)

### Attributes

[AInputType: Any

—

Return the input type for the parser.](/python/langchain-core/output_parsers/base/BaseOutputParser/InputType)[AOutputType: type[T]

—

Return the output type for the parser.](/python/langchain-core/output_parsers/base/BaseOutputParser/OutputType)

### Methods

[Minvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/invoke)[Mainvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/ainvoke)[Mparse\_result

—

Parse a list of candidate model `Generation` objects into a specific format.](/python/langchain-core/output_parsers/base/BaseOutputParser/parse_result)[Maparse\_result

—

Parse a list of candidate model `Generation` objects into a specific format.](/python/langchain-core/output_parsers/base/BaseOutputParser/aparse_result)[Maparse

—

Async parse a single string model output into some structure.](/python/langchain-core/output_parsers/base/BaseOutputParser/aparse)[Mparse\_with\_prompt

—

Parse the output of an LLM call with the input prompt for context.](/python/langchain-core/output_parsers/base/BaseOutputParser/parse_with_prompt)[Mdict

—

Return dictionary representation of output parser.](/python/langchain-core/output_parsers/base/BaseOutputParser/dict)

## Inherited from[BaseLLMOutputParser](/python/langchain-core/output_parsers/base/BaseLLMOutputParser)

### Methods

[Mparse\_result

—

Parse a list of candidate model `Generation` objects into a specific format.](/python/langchain-core/output_parsers/base/BaseLLMOutputParser/parse_result)[Maparse\_result

—

Parse a list of candidate model `Generation` objects into a specific format.](/python/langchain-core/output_parsers/base/BaseLLMOutputParser/aparse_result)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`.](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json

—

Serialize the `Runnable` to JSON.](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields

—

Configure particular `Runnable` fields at runtime.](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives

—

Configure alternatives for `Runnable` objects that can be set at runtime.](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable

—

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`. Used for debugging and tracing.](/python/langchain-core/runnables/base/Runnable/name)[AInputType: type[Input]

—

Input type.](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType: type[Output]

—

Output Type.](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema: type[BaseModel]

—

The type of input this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema: type[BaseModel]

—

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs: list[ConfigurableFieldSpec]

—

List configurable fields for this `Runnable`.](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name

—

Get the name of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema

—

Get a Pydantic model that can be used to validate input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema

—

Get a JSON schema that represents the input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema

—

Get a Pydantic model that can be used to validate output to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema

—

Get a JSON schema that represents the output of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema

—

The type of config this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema

—

Get a JSON schema that represents the config of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph

—

Return a graph representation of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_graph)[Mget\_prompts

—

Return a list of prompts used by this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_prompts)[Mpipe

—

Pipe `Runnable` objects.](/python/langchain-core/runnables/base/Runnable/pipe)[Mpick

—

Pick keys from the output `dict` of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/pick)[Massign

—

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Minvoke

—

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/invoke)[Mainvoke

—

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/ainvoke)[Mbatch

—

Default implementation runs invoke in parallel using a thread pool executor.](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed

—

Run `invoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch

—

Default implementation runs `ainvoke` in parallel using `asyncio.gather`.](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed

—

Run `ainvoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mstream

—

Default implementation of `stream`, which calls `invoke`.](/python/langchain-core/runnables/base/Runnable/stream)[Mastream

—

Default implementation of `astream`, which calls `ainvoke`.](/python/langchain-core/runnables/base/Runnable/astream)[Mastream\_log

—

Stream all output from a `Runnable`, as reported to the callback system.](/python/langchain-core/runnables/base/Runnable/astream_log)[Mastream\_events

—

Generate a stream of events.](/python/langchain-core/runnables/base/Runnable/astream_events)[Mtransform

—

Transform inputs to outputs.](/python/langchain-core/runnables/base/Runnable/transform)[Matransform

—

Transform inputs to outputs.](/python/langchain-core/runnables/base/Runnable/atransform)[Mbind

—

Bind arguments to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_config

—

Bind config to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_config)[Mwith\_listeners

—

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_listeners)[Mwith\_alisteners

—

Bind async lifecycle listeners to a `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mwith\_types

—

Bind input and output types to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_types)[Mwith\_retry

—

Create a new `Runnable` that retries the original `Runnable` on exceptions.](/python/langchain-core/runnables/base/Runnable/with_retry)[Mmap

—

Return a new `Runnable` that maps a list of inputs to a list of outputs.](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks

—

Add fallbacks to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool

—

Create a `BaseTool` from a `Runnable`.](/python/langchain-core/runnables/base/Runnable/as_tool)


