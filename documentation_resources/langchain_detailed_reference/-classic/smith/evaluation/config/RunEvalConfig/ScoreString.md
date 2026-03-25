<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString -->

Classv1.2.13 (latest)●Since v1.0

# ScoreString

Configuration for a score string evaluator.

This is like the criteria evaluator but it is configured by
default to return a score on the scale from 1-10.

It is recommended to normalize these scores
by setting `normalize_by` to 10.


```
ScoreString()
```

## Bases

`SingleKeyEvalConfig`

## Attributes

[attribute

evaluator\_type: EvaluatorType](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/evaluator_type)[attribute

criteria: CRITERIA\_TYPE | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/criteria)[attribute

llm: BaseLanguageModel | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/llm)[attribute

normalize\_by: float | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/normalize_by)[attribute

prompt: BasePromptTemplate | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/prompt)

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


