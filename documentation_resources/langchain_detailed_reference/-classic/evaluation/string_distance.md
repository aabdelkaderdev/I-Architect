<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/string_distance -->

Modulev1.2.13 (latest)●Since v1.0

# string\_distance

String distance evaluators.

## Classes

[class

PairwiseStringDistanceEvalChain

Compute string edit distances between two predictions.](/python/langchain-classic/evaluation/string_distance/base/PairwiseStringDistanceEvalChain)[class

StringDistance

Distance metric to use.](/python/langchain-classic/evaluation/string_distance/base/StringDistance)[class

StringDistanceEvalChain

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
> > > )](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain)

## Modules

[module

base

String distance evaluators based on the RapidFuzz library.](/python/langchain-classic/evaluation/string_distance/base)


