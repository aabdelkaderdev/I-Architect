<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/retry/RunnableRetry -->

Classv1.2.21 (latest)●Since v0.1

# RunnableRetry

Retry a Runnable if it fails.

RunnableRetry can be used to add retry logic to any object
that subclasses the base Runnable.

Such retries are especially useful for network calls that may fail
due to transient errors.

The RunnableRetry is implemented as a RunnableBinding. The easiest
way to use it is through the `.with_retry()` method on all Runnables.

Example:
Here's an example that uses a RunnableLambda to raise an exception

```
import time

def foo(input) -> None:
    '''Fake function that raises an exception.'''
    raise ValueError(f"Invoking foo failed. At time {time.time()}")

runnable = RunnableLambda(foo)

runnable_with_retries = runnable.with_retry(
    retry_if_exception_type=(ValueError,),  # Retry only on ValueError
    wait_exponential_jitter=True,  # Add jitter to the exponential backoff
    stop_after_attempt=2,  # Try twice
    exponential_jitter_params={"initial": 2},  # if desired, customize backoff
)

# The method invocation above is equivalent to the longer form below:

runnable_with_retries = RunnableRetry(
    bound=runnable,
    retry_exception_types=(ValueError,),
    max_attempt_number=2,
    wait_exponential_jitter=True,
    exponential_jitter_params={"initial": 2},
)
```

This logic can be used to retry any Runnable, including a chain of Runnables,
but in general it's best practice to keep the scope of the retry as small as
possible. For example, if you have a chain of Runnables, you should only retry
the Runnable that is likely to fail, not the entire chain.


```
RunnableRetry(
  self,
  *,
  bound: Runnable[Input, Output],
  kwargs: Mapping[str, Any] | None = None,
  config: RunnableConfig | None = None,
  config_factories: list[Callable[[RunnableConfig], RunnableConfig]] | None = None,
  custom_input_type: type[Input] | BaseModel | None = None,
  custom_output_type: type[Output] | BaseModel | None = None,
  **other_kwargs: Any = {}
)
```

## Bases

`RunnableBindingBase[Input, Output]`

**Example:**

```
from langchain_core.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("tell me a joke about {topic}.")
model = ChatOpenAI(temperature=0.5)

# Good
chain = template | model.with_retry()

# Bad
chain = template | model
retryable_chain = chain.with_retry()
```

## Attributes

[attribute

retry\_exception\_types: tuple[type[BaseException], ...]

The exception types to retry on. By default all exceptions are retried.

In general you should only retry on exceptions that are likely to be
transient, such as network errors.

Good exceptions to retry are all server errors (5xx) and selected client
errors (4xx) such as 429 Too Many Requests.](/python/langchain-core/runnables/retry/RunnableRetry/retry_exception_types)[attribute

wait\_exponential\_jitter: bool

Whether to add jitter to the exponential backoff.](/python/langchain-core/runnables/retry/RunnableRetry/wait_exponential_jitter)[attribute

exponential\_jitter\_params: ExponentialJitterParams | None

Parameters for `tenacity.wait_exponential_jitter`. Namely: `initial`,
`max`, `exp_base`, and `jitter` (all `float` values).](/python/langchain-core/runnables/retry/RunnableRetry/exponential_jitter_params)[attribute

max\_attempt\_number: int

The maximum number of attempts to retry the Runnable.](/python/langchain-core/runnables/retry/RunnableRetry/max_attempt_number)

## Methods

[method

invoke](/python/langchain-core/runnables/retry/RunnableRetry/invoke)[method

ainvoke](/python/langchain-core/runnables/retry/RunnableRetry/ainvoke)[method

batch](/python/langchain-core/runnables/retry/RunnableRetry/batch)[method

abatch](/python/langchain-core/runnables/retry/RunnableRetry/abatch)

## Inherited from[RunnableBindingBase](/python/langchain-core/runnables/base/RunnableBindingBase)

### Attributes

[Abound: Runnable[Input, Output]

—

The underlying `Runnable` that this `Runnable` delegates to.](/python/langchain-core/runnables/base/RunnableBindingBase/bound)[Akwargs: Mapping[str, Any]

—

kwargs to pass to the underlying `Runnable` when running.](/python/langchain-core/runnables/base/RunnableBindingBase/kwargs)[Aconfig: RunnableConfig

—

The config to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config)[Aconfig\_factories: list[Callable[[RunnableConfig], RunnableConfig]]

—

The config factories to bind to the underlying `Runnable`.](/python/langchain-core/runnables/base/RunnableBindingBase/config_factories)[Acustom\_input\_type: Any | None

—

Override the input type of the underlying `Runnable` with a custom type.](/python/langchain-core/runnables/base/RunnableBindingBase/custom_input_type)[Acustom\_output\_type: Any | None

—

Override the output type of the underlying `Runnable` with a custom type.](/python/langchain-core/runnables/base/RunnableBindingBase/custom_output_type)[Amodel\_config](/python/langchain-core/runnables/base/RunnableBindingBase/model_config)[AInputType: type[Input]](/python/langchain-core/runnables/base/RunnableBindingBase/InputType)[AOutputType: type[Output]](/python/langchain-core/runnables/base/RunnableBindingBase/OutputType)[Aconfig\_specs: list[ConfigurableFieldSpec]](/python/langchain-core/runnables/base/RunnableBindingBase/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/RunnableBindingBase/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_input_schema)[Mget\_output\_schema](/python/langchain-core/runnables/base/RunnableBindingBase/get_output_schema)[Mget\_graph](/python/langchain-core/runnables/base/RunnableBindingBase/get_graph)[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/runnables/base/RunnableBindingBase/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/runnables/base/RunnableBindingBase/get_lc_namespace)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/batch_as_completed)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/RunnableBindingBase/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/RunnableBindingBase/stream)[Mastream](/python/langchain-core/runnables/base/RunnableBindingBase/astream)[Mastream\_events](/python/langchain-core/runnables/base/RunnableBindingBase/astream_events)[Mtransform](/python/langchain-core/runnables/base/RunnableBindingBase/transform)[Matransform](/python/langchain-core/runnables/base/RunnableBindingBase/atransform)

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

Assigns new fields to the `dict` output of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/assign)[Mbatch\_as\_completed

—

Run `invoke` in parallel on a list of inputs.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch\_as\_completed

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


