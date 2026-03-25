<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/StringDistance -->

Classv1.2.13 (latest)●Since v1.0

# StringDistance

Configuration for a string distance evaluator.


```
StringDistance()
```

## Bases

`SingleKeyEvalConfig`

## Attributes

[attribute

evaluator\_type: EvaluatorType](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/StringDistance/evaluator_type)[attribute

distance: StringDistanceEnum | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/StringDistance/distance)[attribute

normalize\_score: bool](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/StringDistance/normalize_score)

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


