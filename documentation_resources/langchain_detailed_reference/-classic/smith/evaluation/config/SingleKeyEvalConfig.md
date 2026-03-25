<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig -->

Classv1.2.13 (latest)●Since v1.0

# SingleKeyEvalConfig

Configuration for a run evaluator that only requires a single key.


```
SingleKeyEvalConfig()
```

## Bases

`EvalConfig`

## Attributes

[attribute

reference\_key: str | None

The key in the dataset run to use as the reference string.
If not provided, we will attempt to infer automatically.](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/reference_key)[attribute

prediction\_key: str | None

The key from the traced run's outputs dictionary to use to
represent the prediction. If not provided, it will be inferred
automatically.](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/prediction_key)[attribute

input\_key: str | None

The key from the traced run's inputs dictionary to use to represent the
input. If not provided, it will be inferred automatically.](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/input_key)

## Methods

[method

get\_kwargs](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/get_kwargs)

## Inherited from[EvalConfig](/python/langchain-classic/smith/evaluation/config/EvalConfig)

### Attributes

[Aevaluator\_type: EvaluatorType](/python/langchain-classic/smith/evaluation/config/EvalConfig/evaluator_type)


