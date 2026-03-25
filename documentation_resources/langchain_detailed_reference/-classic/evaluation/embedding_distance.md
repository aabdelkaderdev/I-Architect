<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/embedding_distance -->

Modulev1.2.13 (latest)●Since v1.0

# embedding\_distance

Evaluators that measure embedding distances.

## Classes

[class

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

## Modules

[module

base

A chain for comparing the output of two models using embeddings.](/python/langchain-classic/evaluation/embedding_distance/base)


