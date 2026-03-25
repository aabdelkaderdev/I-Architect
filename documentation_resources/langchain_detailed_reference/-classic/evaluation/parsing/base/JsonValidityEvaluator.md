<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# JsonValidityEvaluator

Evaluate whether the prediction is valid JSON.

This evaluator checks if the prediction is a valid JSON string. It does not
require any input or reference.


```
JsonValidityEvaluator(
    self,
    **_: Any = {},
)
```

## Bases

`StringEvaluator`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator/__init__)

## Attributes

[attribute

requires\_input: bool](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator/requires_input)[attribute

requires\_reference: bool](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator/requires_reference)[attribute

evaluation\_name: str](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


