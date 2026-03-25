<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# StringDistanceEvalChain

Compute string distances between the prediction and the reference.

## Examples:

> > > from langchain\_classic.evaluation import StringDistanceEvalChain
> > > evaluator = StringDistanceEvalChain()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CEO",
> > > )

Using the `load_evaluator` function:

> > > from langchain\_classic.evaluation import load\_evaluator
> > > evaluator = load\_evaluator("string\_distance")
> > > evaluator.evaluate\_strings(
> > > prediction="The answer is three",
> > > reference="three",
> > > )


```
StringDistanceEvalChain()
```

## Bases

`StringEvaluator``_RapidFuzzChainMixin`

## Attributes

[attribute

requires\_input: bool

This evaluator does not require input.](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain/requires_input)[attribute

requires\_reference: bool

This evaluator does not require a reference.](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain/requires_reference)[attribute

input\_keys: list[str]

Get the input keys.](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain/input_keys)[attribute

evaluation\_name: str

Get the evaluation name.](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


