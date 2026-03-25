<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/exact_match/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Classes

[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

ExactMatchStringEvaluator

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
> > > ) # This will return {'score': 0.0}](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator)


