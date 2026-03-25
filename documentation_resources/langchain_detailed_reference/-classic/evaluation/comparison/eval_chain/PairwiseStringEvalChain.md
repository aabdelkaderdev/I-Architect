<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# PairwiseStringEvalChain


```
PairwiseStringEvalChain()
```

## Bases

`PairwiseStringEvaluator``LLMEvalChain``LLMChain`

## Attributes

## Methods

## Inherited from[PairwiseStringEvaluator](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)

### Methods

[Mevaluate\_string\_pairs

—

Evaluate the output string pairs.](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator/evaluate_string_pairs)[Maevaluate\_string\_pairs

—

Asynchronously evaluate the output string pairs.](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator/aevaluate_string_pairs)

## Inherited from[LLMChain](/python/langchain-classic/chains/llm/LLMChain)

### Attributes

[A](/python/langchain-classic/chains/llm/LLMChain/prompt)



prompt

: BasePromptTemplate

—

Prompt object to use.

[Allm: Runnable[LanguageModelInput, str] | Runnable[LanguageModelInput, BaseMessage]

—

Language model to call.](/python/langchain-classic/chains/llm/LLMChain/llm)

[Areturn\_final\_only: bool

—

Whether to return only the final parsed result.](/python/langchain-classic/chains/llm/LLMChain/return_final_only)

[Allm\_kwargs: dict](/python/langchain-classic/chains/llm/LLMChain/llm_kwargs)

[Ainput\_keys: list[str]

—

Will be whatever keys the prompt expects.](/python/langchain-classic/chains/llm/LLMChain/input_keys)

[Aoutput\_keys: list[str]

—

Will always return text key.](/python/langchain-classic/chains/llm/LLMChain/output_keys)

### Methods

[Mgenerate

—

Generate LLM result from inputs.](/python/langchain-classic/chains/llm/LLMChain/generate)[Magenerate

—

Generate LLM result from inputs.](/python/langchain-classic/chains/llm/LLMChain/agenerate)[Mprep\_prompts

—

Prepare prompts from inputs.](/python/langchain-classic/chains/llm/LLMChain/prep_prompts)[Maprep\_prompts

—

Prepare prompts from inputs.](/python/langchain-classic/chains/llm/LLMChain/aprep_prompts)[Mapply

—

Utilize the LLM generate method for speed gains.](/python/langchain-classic/chains/llm/LLMChain/apply)[Maapply

—

Utilize the LLM generate method for speed gains.](/python/langchain-classic/chains/llm/LLMChain/aapply)[Mcreate\_outputs

—

Create outputs from response.](/python/langchain-classic/chains/llm/LLMChain/create_outputs)[Mpredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/predict)[Mapredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/apredict)[Mpredict\_and\_parse

—

Call predict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/predict_and_parse)[Mapredict\_and\_parse

—

Call apredict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apredict_and_parse)[Mapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apply_and_parse)[Maapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/aapply_and_parse)[Mfrom\_string

—

Create LLMChain from LLM and template.](/python/langchain-classic/chains/llm/LLMChain/from_string)

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

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)[Ainput\_keys: list[str]

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

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

output\_key: str](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/output_key)

[attribute

output\_parser: BaseOutputParser](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/output_parser)

[attribute

model\_config](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/model_config)

[attribute

requires\_reference: bool

Return whether the chain requires a reference.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/requires_reference)

[attribute

requires\_input: bool

Return whether the chain requires an input.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/requires_input)

[method

is\_lc\_serializable](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/is_lc_serializable)

[method

from\_llm

Initialize the PairwiseStringEvalChain from an LLM.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/from_llm)

Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs.

**Example:**

> > > from langchain\_openai import ChatOpenAI
> > > from langchain\_classic.evaluation.comparison import PairwiseStringEvalChain
> > > model = ChatOpenAI(
> > > ... temperature=0, model\_name="gpt-4", model\_kwargs={"random\_seed": 42}
> > > ... )
> > > chain = PairwiseStringEvalChain.from\_llm(llm=model)
> > > result = chain.evaluate\_string\_pairs(
> > > ... input = "What is the chemical formula for water?",
> > > ... prediction = "H2O",
> > > ... prediction\_b = (
> > > ... "The chemical formula for water is H2O, which means"
> > > ... " there are two hydrogen atoms and one oxygen atom."
> > > ... reference = "The chemical formula for water is H2O.",
> > > ... )
> > > print(result)

# {

# "value": "B",

# "comment": "Both responses accurately state"

# " that the chemical formula for water is H2O."

# " However, Response B provides additional information"

# . " by explaining what the formula means.\n[[B]]"

# }

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