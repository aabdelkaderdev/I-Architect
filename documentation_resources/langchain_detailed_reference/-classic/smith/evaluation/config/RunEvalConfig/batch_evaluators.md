<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/batch_evaluators -->

Attributev1.2.13 (latest)●Since v1.0

# batch\_evaluators

Evaluators that run on an aggregate/batch level.

These generate one or more metrics that are assigned to the full test run.
As a result, they are not associated with individual traces.


```
batch_evaluators: list[BATCH_EVALUATOR_LIKE] | None = None
```


