<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema/StringEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.


```
StringEvaluator()
```

## Bases

`_EvalArgsMixin``ABC`

## Attributes

[attribute

evaluation\_name: str

The name of the evaluation.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluation_name)[attribute

requires\_reference: bool

Whether this evaluator requires a reference label.](/python/langchain-classic/evaluation/schema/StringEvaluator/requires_reference)

## Methods

[method

evaluate\_strings

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[method

aevaluate\_strings

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


