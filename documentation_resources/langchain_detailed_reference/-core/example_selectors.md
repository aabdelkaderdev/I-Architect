<!-- Source: https://reference.langchain.com/python/langchain-core/example_selectors -->

Modulev1.2.21 (latest)●Since v0.1

# example\_selectors

Example selectors.

**Example selector** implements logic for selecting examples to include them in prompts.
This allows us to select examples that are most relevant to the input.

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)[function

sorted\_values

Return a list of values in dict sorted by key.](/python/langchain-core/example_selectors/semantic_similarity/sorted_values)

## Classes

[class

BaseExampleSelector

Interface for selecting examples to include in prompts.](/python/langchain-core/example_selectors/base/BaseExampleSelector)[class

LengthBasedExampleSelector

Select examples based on length.](/python/langchain-core/example_selectors/length_based/LengthBasedExampleSelector)[class

MaxMarginalRelevanceExampleSelector

Select examples based on Max Marginal Relevance.

This was shown to improve performance in this paper:
<https://arxiv.org/pdf/2211.13892.pdf>](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector)[class

SemanticSimilarityExampleSelector

Select examples based on semantic similarity.](/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)

## Modules

[module

length\_based

Select examples based on length.](/python/langchain-core/example_selectors/length_based)[module

base

Interface for selecting examples to include in prompts.](/python/langchain-core/example_selectors/base)[module

semantic\_similarity

Example selector that selects examples based on SemanticSimilarity.](/python/langchain-core/example_selectors/semantic_similarity)


