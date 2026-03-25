<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# EmbeddingDistanceEvalChain

Embedding distance evaluation chain.

Use embedding distances to score semantic difference between
a prediction and reference.


```
EmbeddingDistanceEvalChain()
```

## Bases

`_EmbeddingDistanceChainMixin``StringEvaluator`

## Attributes

[attribute

requires\_reference: bool

Return whether the chain requires a reference.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain/requires_reference)[attribute

evaluation\_name: str](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain/evaluation_name)[attribute

input\_keys: list[str]

Return the input keys of the chain.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain/input_keys)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


