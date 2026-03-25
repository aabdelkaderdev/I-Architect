<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/configurable/RunnableConfigurableFields -->

Classv1.2.21 (latest)●Since v0.1

# RunnableConfigurableFields

`Runnable` that can be dynamically configured.

A `RunnableConfigurableFields` should be initiated using the
`configurable_fields` method of a `Runnable`.

Here is an example of using a `RunnableConfigurableFields` with LLMs:

```
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)
# This creates a RunnableConfigurableFields for a chat model.

# When invoking the created RunnableSequence, you can pass in the
# value for your ConfigurableField's id which in this case
# will be change in temperature

prompt = PromptTemplate.from_template("Pick a random number above {x}")
chain = prompt | model

chain.invoke({"x": 0})
chain.invoke({"x": 0}, config={"configurable": {"temperature": 0.9}})
```

Here is an example of using a `RunnableConfigurableFields` with `HubRunnables`:

```
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from langchain.runnables.hub import HubRunnable

prompt = HubRunnable("rlm/rag-prompt").configurable_fields(
    owner_repo_commit=ConfigurableField(
        id="hub_commit",
        name="Hub Commit",
        description="The Hub commit to pull from",
    )
)

prompt.invoke({"question": "foo", "context": "bar"})

# Invoking prompt with `with_config` method

prompt.invoke(
    {"question": "foo", "context": "bar"},
    config={"configurable": {"hub_commit": "rlm/rag-prompt-llama"}},
)
```


```
RunnableConfigurableFields(
  self,
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`DynamicRunnable[Input, Output]`

## Attributes

[attribute

fields: dict[str, AnyConfigurableField]

The configurable fields to use.](/python/langchain-core/runnables/configurable/RunnableConfigurableFields/fields)[attribute

config\_specs: list[ConfigurableFieldSpec]

Get the configuration specs for the `RunnableConfigurableFields`.](/python/langchain-core/runnables/configurable/RunnableConfigurableFields/config_specs)

## Methods

[method

configurable\_fields](/python/langchain-core/runnables/configurable/RunnableConfigurableFields/configurable_fields)

## Inherited from[DynamicRunnable](/python/langchain-core/runnables/configurable/DynamicRunnable)

### Attributes

[Adefault: RunnableSerializable[Input, Output]

—

The default `Runnable` to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/default)[Aconfig: RunnableConfig | None

—

The configuration to use.](/python/langchain-core/runnables/configurable/DynamicRunnable/config)[Amodel\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/model_config)[AInputType: type[Input]](/python/langchain-core/runnables/configurable/DynamicRunnable/InputType)[AOutputType: type[Output]](/python/langchain-core/runnables/configurable/DynamicRunnable/OutputType)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/runnables/configurable/DynamicRunnable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/runnables/configurable/DynamicRunnable/get_lc_namespace)[Mget\_input\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_input_schema)[Mget\_output\_schema](/python/langchain-core/runnables/configurable/DynamicRunnable/get_output_schema)[Mget\_graph](/python/langchain-core/runnables/configurable/DynamicRunnable/get_graph)[Mwith\_config](/python/langchain-core/runnables/configurable/DynamicRunnable/with_config)[Mprepare

—

Prepare the `Runnable` for invocation.](/python/langchain-core/runnables/configurable/DynamicRunnable/prepare)[Minvoke](/python/langchain-core/runnables/configurable/DynamicRunnable/invoke)[Mainvoke](/python/langchain-core/runnables/configurable/DynamicRunnable/ainvoke)[Mbatch](/python/langchain-core/runnables/configurable/DynamicRunnable/batch)[Mabatch](/python/langchain-core/runnables/configurable/DynamicRunnable/abatch)[Mstream](/python/langchain-core/runnables/configurable/DynamicRunnable/stream)[Mastream](/python/langchain-core/runnables/configurable/DynamicRunnable/astream)[Mtransform](/python/langchain-core/runnables/configurable/DynamicRunnable/transform)[Matransform](/python/langchain-core/runnables/configurable/DynamicRunnable/atransform)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

### Attributes

[Aname: str | None

—

The name of the `Runnable`.](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json

—

Serialize the `Runnable` to JSON.](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_alternatives

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

Output schema.](/python/langchain-core/runnables/base/Runnable/output_schema)

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


