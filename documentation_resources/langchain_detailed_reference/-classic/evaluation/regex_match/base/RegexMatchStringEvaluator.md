<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# RegexMatchStringEvaluator

Compute a regex match between the prediction and the reference.

## Examples:

> > > evaluator = RegexMatchStringEvaluator(flags=re.IGNORECASE)
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^mindy.\*cto$",
> > > ) # This will return {'score': 1.0} due to the IGNORECASE flag

> > > evaluator = RegexMatchStringEvaluator()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$",
> > > ) # This will return {'score': 0.0}

> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$|^Mindy.\*CTO$",
> > > ) # This will return {'score': 1.0} as the prediction matches the second pattern in the union


```
RegexMatchStringEvaluator(
  self,
  *,
  flags: int = 0,
  **_: Any = {}
)
```

## Bases

`StringEvaluator`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `flags` | `int` | Default:`0`  Flags to use for the regex match. Defaults to no flags. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| flags | [int](https://docs.python.org/3/library/functions.html#int) |

## Attributes

[attribute

flags: flags](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator/flags)[attribute

requires\_input: bool

This evaluator does not require input.](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator/requires_input)[attribute

requires\_reference: bool

This evaluator requires a reference.](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator/requires_reference)[attribute

input\_keys: list[str]

Get the input keys.](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator/input_keys)[attribute

evaluation\_name: str

Get the evaluation name.](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


