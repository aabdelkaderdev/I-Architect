<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig -->

Classv1.2.13 (latest)●Since v1.0

# RunEvalConfig

Configuration for a run evaluation.


```
RunEvalConfig()
```

## Bases

`BaseModel`

## Attributes

[attribute

evaluators: list[SINGLE\_EVAL\_CONFIG\_TYPE | CUSTOM\_EVALUATOR\_TYPE]

Configurations for which evaluators to apply to the dataset run.
Each can be the string of an
`EvaluatorType <langchain.evaluation.schema.EvaluatorType>`, such
as `EvaluatorType.QA`, the evaluator type string ("qa"), or a configuration for a
given evaluator
(e.g.,
`RunEvalConfig.QA <langchain.smith.evaluation.config.RunEvalConfig.QA>`).](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/evaluators)[attribute

custom\_evaluators: list[CUSTOM\_EVALUATOR\_TYPE] | None

Custom evaluators to apply to the dataset run.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/custom_evaluators)[attribute

batch\_evaluators: list[BATCH\_EVALUATOR\_LIKE] | None

Evaluators that run on an aggregate/batch level.

These generate one or more metrics that are assigned to the full test run.
As a result, they are not associated with individual traces.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/batch_evaluators)[attribute

reference\_key: str | None

The key in the dataset run to use as the reference string.
If not provided, we will attempt to infer automatically.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/reference_key)[attribute

prediction\_key: str | None

The key from the traced run's outputs dictionary to use to
represent the prediction. If not provided, it will be inferred
automatically.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/prediction_key)[attribute

input\_key: str | None

The key from the traced run's inputs dictionary to use to represent the
input. If not provided, it will be inferred automatically.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/input_key)[attribute

eval\_llm: BaseLanguageModel | None

The language model to pass to any evaluators that require one.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/eval_llm)[attribute

model\_config](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/model_config)

## Classes

[class

Criteria

Configuration for a reference-free criteria evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/Criteria)[class

LabeledCriteria

Configuration for a labeled (with references) criteria evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/LabeledCriteria)[class

EmbeddingDistance

Configuration for an embedding distance evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/EmbeddingDistance)[class

StringDistance

Configuration for a string distance evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/StringDistance)[class

QA

Configuration for a QA evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/QA)[class

ContextQA

Configuration for a context-based QA evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ContextQA)[class

CoTQA

Configuration for a context-based QA evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/CoTQA)[class

JsonValidity

Configuration for a json validity evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/JsonValidity)[class

JsonEqualityEvaluator

Configuration for a json equality evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/JsonEqualityEvaluator)[class

ExactMatch

Configuration for an exact match string evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch)[class

RegexMatch

Configuration for a regex match string evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/RegexMatch)[class

ScoreString

Configuration for a score string evaluator.

This is like the criteria evaluator but it is configured by
default to return a score on the scale from 1-10.

It is recommended to normalize these scores
by setting `normalize_by` to 10.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString)[class

LabeledScoreString

Configuration for a labeled score string evaluator.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/LabeledScoreString)


