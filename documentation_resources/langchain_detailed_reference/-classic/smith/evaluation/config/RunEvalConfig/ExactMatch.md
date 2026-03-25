<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch -->

Classv1.2.13 (latest)●Since v1.0

# ExactMatch

Configuration for an exact match string evaluator.


```
ExactMatch()
```

## Bases

`SingleKeyEvalConfig`

## Attributes

[attribute

evaluator\_type: EvaluatorType](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch/evaluator_type)[attribute

ignore\_case: bool](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch/ignore_case)[attribute

ignore\_punctuation: bool](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch/ignore_punctuation)[attribute

ignore\_numbers: bool](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ExactMatch/ignore_numbers)

## Inherited from[SingleKeyEvalConfig](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig)

### Attributes

[Areference\_key: str | None

—

The key in the dataset run to use as the reference string.](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/reference_key)[Aprediction\_key: str | None

—

The key from the traced run's outputs dictionary to use to](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/prediction_key)[Ainput\_key: str | None

—

The key from the traced run's inputs dictionary to use to represent the](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/input_key)

### Methods

[Mget\_kwargs](/python/langchain-classic/smith/evaluation/config/SingleKeyEvalConfig/get_kwargs)

## Inherited from[EvalConfig](/python/langchain-classic/smith/evaluation/config/EvalConfig)

### Methods

[Mget\_kwargs

—

Get the keyword arguments for the `load_evaluator` call.](/python/langchain-classic/smith/evaluation/config/EvalConfig/get_kwargs)


