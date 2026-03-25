<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain -->

Classv1.2.13 (latest)●Since v1.0

# Chain


```
Chain()
```

## Bases

`RunnableSerializable[dict[str, Any], dict[str, Any]]``ABC`

## Attributes

## Methods

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

##



Inherited from

[Serializable](/python/langchain-core/load/serializable/Serializable)

(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[attribute

memory: BaseMemory | None

Optional memory object.
Memory is a class that gets called at the start
and at the end of every chain. At the start, memory loads variables and passes
them along in the chain. At the end, it saves any returned variables.
There are many different types of memory - please see memory docs
for the full catalog.](/python/langchain-classic/chains/base/Chain/memory)

[attribute

callbacks: Callbacks

Optional list of callback handlers (or callback manager).
Callback handlers are called throughout the lifecycle of a call to a chain,
starting with on\_chain\_start, ending with on\_chain\_end or on\_chain\_error.
Each custom chain can optionally call additional callback methods, see Callback docs
for full details.](/python/langchain-classic/chains/base/Chain/callbacks)

[attribute

verbose: bool

Whether or not run in verbose mode. In verbose mode, some intermediate logs
will be printed to the console. Defaults to the global `verbose` value,
accessible via `langchain.globals.get_verbose()`.](/python/langchain-classic/chains/base/Chain/verbose)

[attribute

tags: list[str] | None

Optional list of tags associated with the chain.
These tags will be associated with each call to this chain,
and passed as arguments to the handlers defined in `callbacks`.
You can use these to eg identify a specific instance of a chain with its use case.](/python/langchain-classic/chains/base/Chain/tags)

[attribute

metadata: builtins.dict[str, Any] | None

Optional metadata associated with the chain.
This metadata will be associated with each call to this chain,
and passed as arguments to the handlers defined in `callbacks`.
You can use these to eg identify a specific instance of a chain with its use case.](/python/langchain-classic/chains/base/Chain/metadata)

[attribute

callback\_manager: BaseCallbackManager | None

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

[attribute

model\_config](/python/langchain-classic/chains/base/Chain/model_config)

[attribute

input\_keys: list[str]

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)

[attribute

output\_keys: list[str]

Keys expected to be in the chain output.](/python/langchain-classic/chains/base/Chain/output_keys)

[method

get\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)

[method

get\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)

[method

invoke](/python/langchain-classic/chains/base/Chain/invoke)

[method

ainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)

[method

raise\_callback\_manager\_deprecation

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)

[method

set\_verbose

Set the chain verbosity.

Defaults to the global setting if not specified by the user.](/python/langchain-classic/chains/base/Chain/set_verbose)

[method

prep\_outputs

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)

[method

aprep\_outputs

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)

[method

prep\_inputs

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)

[method

aprep\_inputs

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)

[method

dict

Dictionary representation of chain.

Expects `Chain._chain_type` property to be implemented and for memory to be
null.](/python/langchain-classic/chains/base/Chain/dict)

[method

save

Save the chain.

Expects `Chain._chain_type` property to be implemented and for memory to be
null.](/python/langchain-classic/chains/base/Chain/save)

[deprecatedmethod

acall

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)

[deprecatedmethod

run

Convenience method for executing chain.

The main difference between this method and `Chain.__call__` is that this
method expects inputs to be passed directly in as positional arguments or
keyword arguments, whereas `Chain.__call__` expects a single input dictionary
with all the inputs](/python/langchain-classic/chains/base/Chain/run)

[deprecatedmethod

arun

Convenience method for executing chain.

The main difference between this method and `Chain.__call__` is that this
method expects inputs to be passed directly in as positional arguments or
keyword arguments, whereas `Chain.__call__` expects a single input dictionary
with all the inputs](/python/langchain-classic/chains/base/Chain/arun)

[deprecatedmethod

apply

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.

**The Chain interface makes it easy to create apps that are:**

- Stateful: add Memory to any Chain to give it state,
- Observable: pass Callbacks to a Chain to execute additional functionality,
  like logging, outside the main sequence of component calls,
- Composable: the Chain API is flexible enough that it is easy to combine
  Chains with other components, including other Chains.

**The main methods exposed by chains are:**

- `__call__`: Chains are callable. The `__call__` method is the primary way to
  execute a Chain. This takes inputs as a dictionary and returns a
  dictionary output.
- `run`: A convenience method that takes inputs as args/kwargs and returns the
  output as a string or object. This method can only be used for a subset of
  chains and cannot return as rich of an output as `__call__`.

M

get\_prompts

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

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