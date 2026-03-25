<!-- Source: https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector -->

Classv1.2.21 (latest)●Since v0.1

# MaxMarginalRelevanceExampleSelector

Select examples based on Max Marginal Relevance.

This was shown to improve performance in this paper:
<https://arxiv.org/pdf/2211.13892.pdf>


```
MaxMarginalRelevanceExampleSelector()
```

## Bases

`_VectorStoreExampleSelector`

## Attributes

[attribute

fetch\_k: int

Number of examples to fetch to rerank.](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/fetch_k)

## Methods

[method

select\_examples

Select examples based on Max Marginal Relevance.](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/select_examples)[method

aselect\_examples

Asynchronously select examples based on Max Marginal Relevance.](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/aselect_examples)[method

from\_examples

Create k-shot example selector using example list and embeddings.

Reshuffles examples dynamically based on Max Marginal Relevance.](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/from_examples)[method

afrom\_examples

Create k-shot example selector using example list and embeddings.

Reshuffles examples dynamically based on Max Marginal Relevance.](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/afrom_examples)


