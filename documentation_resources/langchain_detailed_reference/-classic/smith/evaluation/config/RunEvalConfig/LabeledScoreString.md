<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/config/RunEvalConfig/LabeledScoreString -->

Classv1.2.13 (latest)●Since v1.0

# LabeledScoreString

Configuration for a labeled score string evaluator.


```
LabeledScoreString()
```

## Bases

`ScoreString`

## Attributes

[attribute

evaluator\_type: EvaluatorType](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/LabeledScoreString/evaluator_type)

## Inherited from[ScoreString](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString)

### Attributes

[Acriteria: CRITERIA\_TYPE | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/criteria)[Allm: BaseLanguageModel | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/llm)[Anormalize\_by: float | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/normalize_by)[Aprompt: BasePromptTemplate | None](/python/langchain-classic/smith/evaluation/config/RunEvalConfig/ScoreString/prompt)

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


