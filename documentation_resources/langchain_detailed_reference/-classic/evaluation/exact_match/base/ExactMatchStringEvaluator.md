<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# ExactMatchStringEvaluator

Compute an exact match between the prediction and the reference.

## Examples:

> > > evaluator = ExactMatchChain()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CTO",
> > > ) # This will return {'score': 1.0}

> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CEO",
> > > ) # This will return {'score': 0.0}


```
ExactMatchStringEvaluator(
  self,
  *,
  ignore_case: bool = False,
  ignore_punctuation: bool = False,
  ignore_numbers: bool = False,
  **_: Any = {}
)
```

## Bases

`StringEvaluator`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ignore_case` | `bool` | Default:`False`  Whether to ignore case when comparing strings. |
| `ignore_punctuation` | `bool` | Default:`False`  Whether to ignore punctuation when comparing strings. |
| `ignore_numbers` | `bool` | Default:`False`  Whether to ignore numbers when comparing strings. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| ignore\_case | [bool](https://docs.python.org/3/library/functions.html#bool) |
| ignore\_punctuation | [bool](https://docs.python.org/3/library/functions.html#bool) |
| ignore\_numbers | [bool](https://docs.python.org/3/library/functions.html#bool) |

## Attributes

[attribute

ignore\_case: ignore\_case](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/ignore_case)[attribute

ignore\_punctuation: ignore\_punctuation](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/ignore_punctuation)[attribute

ignore\_numbers: ignore\_numbers](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/ignore_numbers)[attribute

requires\_input: bool

This evaluator does not require input.](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/requires_input)[attribute

requires\_reference: bool

This evaluator requires a reference.](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/requires_reference)[attribute

input\_keys: list[str]

Get the input keys.](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/input_keys)[attribute

evaluation\_name: str

Get the evaluation name.](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


