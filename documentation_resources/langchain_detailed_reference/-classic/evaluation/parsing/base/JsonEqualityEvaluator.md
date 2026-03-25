<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# JsonEqualityEvaluator

Json Equality Evaluator.

Evaluate whether the prediction is equal to the reference after
parsing both as JSON.

This evaluator checks if the prediction, after parsing as JSON, is equal
to the reference,
which is also parsed as JSON. It does not require an input string.


```
JsonEqualityEvaluator(
  self,
  operator: Callable | None = None,
  **_: Any = {}
)
```

## Bases

`StringEvaluator`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `operator` | `Callable | None` | Default:`None`  A custom operator to compare the parsed JSON objects. Defaults to equality (`eq`). |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| operator | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable) | None |

## Attributes

[attribute

operator](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator/operator)[attribute

requires\_input: bool](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator/requires_input)[attribute

requires\_reference: bool](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator/requires_reference)[attribute

evaluation\_name: str](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


