<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# LLMCheckerChain


```
LLMCheckerChain()
```

## Bases

`Chain`

## Attributes

## Methods

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)



A

tags

: list[str] | None

—

Optional list of tags associated with the chain.

[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)

[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[Mset\_verbose

—

Set the chain verbosity.](/python/langchain-classic/chains/base/Chain/set_verbose)[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)[Mprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/prep_inputs)[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

question\_to\_checked\_assertions\_chain: SequentialChain](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/question_to_checked_assertions_chain)

[attribute

llm: BaseLanguageModel | None

[Deprecated] LLM wrapper to use.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/llm)

[attribute

create\_draft\_answer\_prompt: PromptTemplate

[Deprecated]](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/create_draft_answer_prompt)

[attribute

list\_assertions\_prompt: PromptTemplate

[Deprecated]](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/list_assertions_prompt)

[attribute

check\_assertions\_prompt: PromptTemplate

[Deprecated]](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/check_assertions_prompt)

[attribute

revised\_answer\_prompt: PromptTemplate

[Deprecated] Prompt to use when questioning the documents.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/revised_answer_prompt)

[attribute

input\_key: str](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/input_key)

[attribute

output\_key: str](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/output_key)

[attribute

model\_config](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/model_config)

[attribute

input\_keys: list[str]

Return the singular input key.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/input_keys)

[attribute

output\_keys: list[str]

Return the singular output key.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/output_keys)

[method

from\_llm

Create an LLMCheckerChain from a language model.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/from_llm)

Chain for question-answering with self-verification.

**Example:**

```
from langchain_openai import OpenAI
from langchain_classic.chains import LLMCheckerChain

model = OpenAI(temperature=0.7)
checker_chain = LLMCheckerChain.from_llm(model)
```

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