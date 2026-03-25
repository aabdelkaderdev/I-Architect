<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config -->

Modulev1.2.13 (latest)●Since v1.0

# config

Configuration for run evaluators.

## Attributes

[attribute

RUN\_EVALUATOR\_LIKE: Callable[[Run, Example | None], EvaluationResult | EvaluationResults | dict]](/python/langchain-classic/smith/evaluation/config/RUN_EVALUATOR_LIKE)[attribute

BATCH\_EVALUATOR\_LIKE: Callable[[Sequence[Run], Sequence[Example] | None], EvaluationResult | EvaluationResults | dict]](/python/langchain-classic/smith/evaluation/config/BATCH_EVALUATOR_LIKE)

## Classes

[class

EmbeddingDistanceEnum

Embedding Distance Metric.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistance)[class

EvaluatorType

The types of the evaluators.](/python/langchain-classic/evaluation/schema/EvaluatorType)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

StringDistanceEnum

Distance metric to use.](/python/langchain-classic/evaluation/string_distance/base/StringDistance)[class

EvalConfig

Configuration for a given run evaluator.](/python/langchain-classic/smith/evaluation/config/EvalConfig)[class

SingleKeyEvalConfig

Configuration for a run evaluator that only requires a single key.](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig)[class

RunEvalConfig

Configuration for a run evaluation.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig)

## Type Aliases

[typeAlias

CRITERIA\_TYPE: Mapping[str, str] | Criteria | ConstitutionalPrinciple](/python/langchain-classic/evaluation/criteria/eval_chain/CRITERIA_TYPE)[typeAlias

CUSTOM\_EVALUATOR\_TYPE](/python/langchain-classic/smith/evaluation/config/CUSTOM_EVALUATOR_TYPE)[typeAlias

SINGLE\_EVAL\_CONFIG\_TYPE](/python/langchain-classic/smith/evaluation/config/SINGLE_EVAL_CONFIG_TYPE)


