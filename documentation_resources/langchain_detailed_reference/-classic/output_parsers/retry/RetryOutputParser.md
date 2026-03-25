<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/retry/RetryOutputParser -->

Classv1.2.13 (latest)●Since v1.0

# RetryOutputParser


```
RetryOutputParser()
```

## Bases

`BaseOutputParser[T]`

## Attributes

## Methods

## Inherited from[BaseOutputParser](/python/langchain-core/output_parsers/base/BaseOutputParser)(langchain\_core)

### Attributes

[AInputType](/python/langchain-core/output_parsers/base/BaseOutputParser/InputType)

### Methods

[Minvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/invoke)[Mainvoke](/python/langchain-core/output_parsers/base/BaseOutputParser/ainvoke)[Mparse\_result](/python/langchain-core/output_parsers/base/BaseOutputParser/parse_result)



M

aparse\_result

[Maparse](/python/langchain-core/output_parsers/base/BaseOutputParser/aparse)

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

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

parser: Annotated[BaseOutputParser[T], SkipValidation()]

The parser to use to parse the output.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/parser)

[attribute

retry\_chain: Annotated[RunnableSerializable[RetryOutputParserRetryChainInput, str] | Any, SkipValidation()]

The RunnableSerializable to use to retry the completion (Legacy: LLMChain).](/python/langchain-classic/output_parsers/retry/RetryOutputParser/retry_chain)

[attribute

max\_retries: int

The maximum number of times to retry the parse.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/max_retries)

[attribute

legacy: bool

Whether to use the run or arun method of the retry\_chain.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/legacy)

[attribute

OutputType: type[T]](/python/langchain-classic/output_parsers/retry/RetryOutputParser/OutputType)

[method

from\_llm

Create an RetryOutputParser from a language model and a parser.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/from_llm)

[method

parse\_with\_prompt

Parse the output of an LLM call using a wrapped parser.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/parse_with_prompt)

[method

aparse\_with\_prompt

Parse the output of an LLM call using a wrapped parser.](/python/langchain-classic/output_parsers/retry/RetryOutputParser/aparse_with_prompt)

[method

parse](/python/langchain-classic/output_parsers/retry/RetryOutputParser/parse)

[method

get\_format\_instructions](/python/langchain-classic/output_parsers/retry/RetryOutputParser/get_format_instructions)

Wrap a parser and try to fix parsing errors.

Does this by passing the original prompt and the completion to another
LLM, and telling it the completion did not satisfy criteria in the prompt.

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