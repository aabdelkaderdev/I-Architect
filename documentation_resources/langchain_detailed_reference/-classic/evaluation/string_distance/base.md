<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/string_distance/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

String distance evaluators based on the RapidFuzz library.

## Attributes

[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

PairwiseStringEvaluator

Compare the output of two models (or two outputs of the same model).](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

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
> > > )](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain)[class

PairwiseStringDistanceEvalChain

Compute string edit distances between two predictions.](/python/langchain-classic/evaluation/string_distance/base/PairwiseStringDistanceEvalChain)


