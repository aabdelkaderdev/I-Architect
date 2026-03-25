<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# CriteriaEvalChain


```
CriteriaEvalChain(
```

)

## Bases

`StringEvaluator``LLMEvalChain``LLMChain`

## Attributes

[attribute

output\_parser: BaseOutputParser](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/output_parser)[attribute

criterion\_name: str](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/criterion_name)[attribute

output\_key: str](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/output_key)[attribute

model\_config](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/model_config)[attribute

requires\_reference: bool](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/requires_reference)[attribute

requires\_input: bool](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/requires_input)[attribute

evaluation\_name: str](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/evaluation_name)

## Methods

[method

is\_lc\_serializable](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/is_lc_serializable)[method

resolve\_criteria](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/resolve_criteria)[method

from\_llm](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/from_llm)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)

## Inherited from[LLMChain](/python/langchain-classic/chains/llm/LLMChain)

### Attributes

[Aprompt: BasePromptTemplate

—

Prompt object to use.](/python/langchain-classic/chains/llm/LLMChain/prompt)[Allm: Runnable[LanguageModelInput, str] | Runnable[LanguageModelInput, BaseMessage]

—

Language model to call.](/python/langchain-classic/chains/llm/LLMChain/llm)[Areturn\_final\_only: bool

—

Whether to return only the final parsed result.](/python/langchain-classic/chains/llm/LLMChain/return_final_only)[Allm\_kwargs: dict](/python/langchain-classic/chains/llm/LLMChain/llm_kwargs)[Ainput\_keys: list[str]

—

Will be whatever keys the prompt expects.](/python/langchain-classic/chains/llm/LLMChain/input_keys)[Aoutput\_keys: list[str]

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

Prepare prompts from inputs.](/python/langchain-classic/chains/llm/LLMChain/aprep_prompts)[M](/python/langchain-classic/chains/llm/LLMChain/apply)

## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[A](/python/langchain-classic/chains/base/Chain/tags)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[M](/python/langchain-core/load/serializable/Serializable/to_json)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)



LLM Chain for evaluating runs against criteria.

## Parameters

llm : BaseLanguageModel
The language model to use for evaluation.
criteria : Union[Mapping[str, str]]
The criteria or rubric to evaluate the runs against. It can be a mapping of
criterion name to its description, or a single criterion name.
prompt : Optional[BasePromptTemplate], default=None
The prompt template to use for generating prompts. If not provided, a
default prompt template will be used based on the value of
`requires_reference`.
requires\_reference : bool, default=False
Whether the evaluation requires a reference text. If `True`, the
`PROMPT_WITH_REFERENCES` template will be used, which includes the
reference labels in the prompt. Otherwise, the `PROMPT` template will be
used, which is a reference-free prompt.
\*\*kwargs : Any
Additional keyword arguments to pass to the `LLMChain` constructor.

## Returns:

CriteriaEvalChain
An instance of the `CriteriaEvalChain` class.

## Examples:

> > > from langchain\_anthropic import ChatAnthropic
> > > from langchain\_classic.evaluation.criteria import CriteriaEvalChain
> > > model = ChatAnthropic(temperature=0)
> > > criteria = {"my-custom-criterion": "Is the submission the most amazing ever?"}
> > > evaluator = CriteriaEvalChain.from\_llm(llm=model, criteria=criteria)
> > > evaluator.evaluate\_strings(
> > > ... prediction="Imagine an ice cream flavor for the color aquamarine",
> > > ... input="Tell me an idea",
> > > ... )
> > > {
> > > 'reasoning': 'Here is my step-by-step reasoning for the given criteria:\n\nThe criterion is: "Is the submission the most amazing ever?" This is a subjective criterion and open to interpretation. The submission suggests an aquamarine-colored ice cream flavor which is creative but may or may not be considered the most amazing idea ever conceived. There are many possible amazing ideas and this one ice cream flavor suggestion may or may not rise to that level for every person. \n\nN',
> > > 'value': 'N',
> > > 'score': 0,
> > > }

> > > from langchain\_openai import ChatOpenAI
> > > from langchain\_classic.evaluation.criteria import LabeledCriteriaEvalChain
> > > model = ChatOpenAI(model="gpt-4", temperature=0)
> > > criteria = "correctness"
> > > evaluator = LabeledCriteriaEvalChain.from\_llm(
> > > ... llm=model,
> > > ... criteria=criteria,
> > > ... )
> > > evaluator.evaluate\_strings(
> > > ... prediction="The answer is 4",
> > > ... input="How many apples are there?",
> > > ... reference="There are 3 apples",
> > > ... )
> > > {
> > > 'score': 0,
> > > 'reasoning': 'The criterion for this task is the correctness of the submission. The submission states that there are 4 apples, but the reference indicates that there are actually 3 apples. Therefore, the submission is not correct, accurate, or factual according to the given criterion.\n\nN',
> > > 'value': 'N',
> > > }

apply

—

Utilize the LLM generate method for speed gains.

[Maapply

—

Utilize the LLM generate method for speed gains.](/python/langchain-classic/chains/llm/LLMChain/aapply)

[Mcreate\_outputs

—

Create outputs from response.](/python/langchain-classic/chains/llm/LLMChain/create_outputs)

[Mpredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/predict)

[Mapredict

—

Format prompt with kwargs and pass to LLM.](/python/langchain-classic/chains/llm/LLMChain/apredict)

[Mpredict\_and\_parse

—

Call predict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/predict_and_parse)

[Mapredict\_and\_parse

—

Call apredict and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apredict_and_parse)

[Mapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/apply_and_parse)

[Maapply\_and\_parse

—

Call apply and then parse the results.](/python/langchain-classic/chains/llm/LLMChain/aapply_and_parse)

[Mfrom\_string

—

Create LLMChain from LLM and template.](/python/langchain-classic/chains/llm/LLMChain/from_string)

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

[Ainput\_keys: list[str]

—

Keys expected to be in the chain input.](/python/langchain-classic/chains/base/Chain/input_keys)

[Aoutput\_keys: list[str]

—

Keys expected to be in the chain output.](/python/langchain-classic/chains/base/Chain/output_keys)

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

to\_json

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)[Mget\_config\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)[Mpick](/python/langchain-core/runnables/base/Runnable/pick)[Massign](/python/langchain-core/runnables/base/Runnable/assign)[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[Mstream](/python/langchain-core/runnables/base/Runnable/stream)[Mastream](/python/langchain-core/runnables/base/Runnable/astream)[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)[Mbind](/python/langchain-core/runnables/base/Runnable/bind)[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)[Mmap](/python/langchain-core/runnables/base/Runnable/map)[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)

The parser to use to map the output to a structured result.

The name of the criterion being evaluated.

Whether the evaluation requires a reference text.

Get the name of the evaluation.

## Returns:

str
The name of the evaluation.

Resolve the criteria to evaluate.

## Parameters

criteria : CRITERIA\_TYPE
The criteria to evaluate the runs against. It can be:
- a mapping of a criterion name to its description
- a single criterion name present in one of the default criteria
- a single `ConstitutionalPrinciple` instance

## Returns:

Dict[str, str]
A dictionary mapping criterion names to descriptions.

## Examples:

> > > criterion = "relevance"
> > > CriteriaEvalChain.resolve\_criteria(criteria)
> > > {'relevance': 'Is the submission referring to a real quote from the text?'}

Create a `CriteriaEvalChain` instance from an llm and criteria.

## Parameters

llm : BaseLanguageModel
The language model to use for evaluation.
criteria : CRITERIA\_TYPE - default=None for "helpfulness"
The criteria to evaluate the runs against. It can be:
- a mapping of a criterion name to its description
- a single criterion name present in one of the default criteria
- a single `ConstitutionalPrinciple` instance
prompt : Optional[BasePromptTemplate], default=None
The prompt template to use for generating prompts. If not provided,
a default prompt template will be used.
\*\*kwargs : Any
Additional keyword arguments to pass to the `LLMChain`
constructor.

## Returns:

CriteriaEvalChain
An instance of the `CriteriaEvalChain` class.

## Examples:

> > > from langchain\_openai import OpenAI
> > > from langchain\_classic.evaluation.criteria import LabeledCriteriaEvalChain
> > > model = OpenAI()
> > > criteria = {
> > > "hallucination": (
> > > "Does this submission contain information"
> > > " not present in the input or reference?"
> > > ),
> > > }
> > > chain = LabeledCriteriaEvalChain.from\_llm(
> > > llm=model,
> > > criteria=criteria,
> > > )