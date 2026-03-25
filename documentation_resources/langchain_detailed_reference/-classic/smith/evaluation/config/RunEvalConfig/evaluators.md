<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/evaluators -->

Attributev1.2.13 (latest)●Since v1.0

# evaluators

Configurations for which evaluators to apply to the dataset run.
Each can be the string of an
`EvaluatorType <langchain.evaluation.schema.EvaluatorType>`, such
as `EvaluatorType.QA`, the evaluator type string ("qa"), or a configuration for a
given evaluator
(e.g.,
`RunEvalConfig.QA <langchain.smith.evaluation.config.RunEvalConfig.QA>`).


```
evaluators: list[SINGLE_EVAL_CONFIG_TYPE | CUSTOM_EVALUATOR_TYPE] = Field(default_factory=list)
```


