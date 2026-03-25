<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/embedding_distance/base/PairwiseEmbeddingDistanceEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# PairwiseEmbeddingDistanceEvalChain

Use embedding distances to score semantic difference between two predictions.

Examples:

> > > chain = PairwiseEmbeddingDistanceEvalChain()
> > > result = chain.evaluate\_string\_pairs(prediction="Hello", prediction\_b="Hi")
> > > print(result)
> > > {'score': 0.5}


```
PairwiseEmbeddingDistanceEvalChain()
```

## Bases

`_EmbeddingDistanceChainMixin``PairwiseStringEvaluator`

## Attributes

[attribute

input\_keys: list[str]

Return the input keys of the chain.](/python/langchain-classic/evaluation/embedding_distance/base/PairwiseEmbeddingDistanceEvalChain/input_keys)[attribute

evaluation\_name: str

Return the evaluation name.](/python/langchain-classic/evaluation/embedding_distance/base/PairwiseEmbeddingDistanceEvalChain/evaluation_name)

## Inherited from[PairwiseStringEvaluator](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)

### Methods

[Mevaluate\_string\_pairs

—

Evaluate the output string pairs.](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator/evaluate_string_pairs)[Maevaluate\_string\_pairs

—

Asynchronously evaluate the output string pairs.](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator/aevaluate_string_pairs)


