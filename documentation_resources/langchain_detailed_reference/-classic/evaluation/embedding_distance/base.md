<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/embedding_distance/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

A chain for comparing the output of two models using embeddings.

## Attributes

[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)[attribute

logger](/python/langchain-classic/evaluation/embedding_distance/base/logger)

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

EmbeddingDistance

Embedding Distance Metric.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistance)[class

EmbeddingDistanceEvalChain

Embedding distance evaluation chain.

Use embedding distances to score semantic difference between
a prediction and reference.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain)[class

PairwiseEmbeddingDistanceEvalChain

Use embedding distances to score semantic difference between two predictions.

Examples:

> > > chain = PairwiseEmbeddingDistanceEvalChain()
> > > result = chain.evaluate\_string\_pairs(prediction="Hello", prediction\_b="Hi")
> > > print(result)
> > > {'score': 0.5}](/python/langchain-classic/evaluation/embedding_distance/base/PairwiseEmbeddingDistanceEvalChain)


