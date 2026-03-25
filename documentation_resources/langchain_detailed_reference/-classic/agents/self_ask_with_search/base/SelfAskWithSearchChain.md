<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/self_ask_with_search/base/SelfAskWithSearchChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# SelfAskWithSearchChain


```
SelfAskWithSearchChain(
  self,
  llm: BaseLanguageModel,
  search_chain: GoogleSerperAPIWrapper | SearchApiAPIWrapper | SerpAPIWrapper
```

## Bases

`AgentExecutor`

## Constructors

## Inherited from[AgentExecutor](/python/langchain-classic/agents/agent/AgentExecutor)

### Attributes

[Aagent: BaseSingleActionAgent | BaseMultiActionAgent | Runnable

—

The agent to run for creating a plan and determining actions](/python/langchain-classic/agents/agent/AgentExecutor/agent)[Atools: Sequence[BaseTool]

—

The valid tools the agent can call.](/python/langchain-classic/agents/agent/AgentExecutor/tools)[Areturn\_intermediate\_steps: bool

—

Whether to return the agent's trajectory of intermediate steps](/python/langchain-classic/agents/agent/AgentExecutor/return_intermediate_steps)



,

\*\*

kwargs

:

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

=

{

}

)

A

max\_iterations

: int | None

—

The maximum number of steps to take before ending the execution

[Amax\_execution\_time: float | None

—

The maximum amount of wall clock time to spend in the execution](/python/langchain-classic/agents/agent/AgentExecutor/max_execution_time)

[Aearly\_stopping\_method: str

—

The method to use for early stopping if the agent never](/python/langchain-classic/agents/agent/AgentExecutor/early_stopping_method)

[Ahandle\_parsing\_errors: bool | str | Callable[[OutputParserException], str]

—

How to handle errors raised by the agent's output parser.](/python/langchain-classic/agents/agent/AgentExecutor/handle_parsing_errors)

[Atrim\_intermediate\_steps: int | Callable[[list[tuple[AgentAction, str]]], list[tuple[AgentAction, str]]]

—

How to trim the intermediate steps before returning them.](/python/langchain-classic/agents/agent/AgentExecutor/trim_intermediate_steps)

[Ainput\_keys: list[str]

—

Return the input keys.](/python/langchain-classic/agents/agent/AgentExecutor/input_keys)

[Aoutput\_keys: list[str]

—

Return the singular output key.](/python/langchain-classic/agents/agent/AgentExecutor/output_keys)

### Methods

[Mfrom\_agent\_and\_tools

—

Create from agent and tools.](/python/langchain-classic/agents/agent/AgentExecutor/from_agent_and_tools)[Mvalidate\_tools

—

Validate that tools are compatible with agent.](/python/langchain-classic/agents/agent/AgentExecutor/validate_tools)[Mvalidate\_runnable\_agent

—

Convert runnable to agent if passed in.](/python/langchain-classic/agents/agent/AgentExecutor/validate_runnable_agent)[Msave

—

Raise error - saving not supported for Agent Executors.](/python/langchain-classic/agents/agent/AgentExecutor/save)[Msave\_agent

—

Save the underlying agent.](/python/langchain-classic/agents/agent/AgentExecutor/save_agent)[Miter

—

Enables iteration over steps taken to reach final output.](/python/langchain-classic/agents/agent/AgentExecutor/iter)[Mlookup\_tool

—

Lookup tool by name.](/python/langchain-classic/agents/agent/AgentExecutor/lookup_tool)[Mstream

—

Enables streaming over steps taken to reach final output.](/python/langchain-classic/agents/agent/AgentExecutor/stream)[Mastream

—

Async enables streaming over steps taken to reach final output.](/python/langchain-classic/agents/agent/AgentExecutor/astream)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[Atags: list[str] | None

—

Optional list of tags associated with the chain.](/python/langchain-classic/chains/base/Chain/tags)[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)[Amodel\_config](/python/langchain-classic/chains/base/Chain/model_config)[Ainput\_keys: list[str]

—

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)[Aoutput\_keys: list[str]

—

Keys expected to be in the chain output.](/python/langchain-classic/chains/base/Chain/output_keys)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[M](/python/langchain-classic/chains/base/Chain/set_verbose)

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

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| llm | [BaseLanguageModel](/python/langchain-core/language_models/base/BaseLanguageModel) |
| search\_chain | [GoogleSerperAPIWrapper](/python/langchain-community/utilities/google_serper/GoogleSerperAPIWrapper) | [SearchApiAPIWrapper](/python/langchain-community/utilities/searchapi/SearchApiAPIWrapper) | [SerpAPIWrapper](/python/langchain-community/utilities/serpapi/SerpAPIWrapper) |

[Deprecated] Chain that does self-ask with search.

set\_verbose

—

Set the chain verbosity.

[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)

[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)

[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)

[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)

[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)

[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)

[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)

[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)

[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)

[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

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