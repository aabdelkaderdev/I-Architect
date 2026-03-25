<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests -->

Classv1.1.4 (latest)●Since v1.1

# EmbeddingsIntegrationTests

Base class for embeddings integration tests.

Test subclasses must implement the `embeddings_class` property to specify the
embeddings model to be tested. You can also override the
`embedding_model_params` property to specify initialization parameters.

```
from typing import Type

from langchain_tests.integration_tests import EmbeddingsIntegrationTests
from my_package.embeddings import MyEmbeddingsModel

class TestMyEmbeddingsModelIntegration(EmbeddingsIntegrationTests):
    @property
    def embeddings_class(self) -> Type[MyEmbeddingsModel]:
        # Return the embeddings model class to test here
        return MyEmbeddingsModel

    @property
    def embedding_model_params(self) -> dict:
        # Return initialization parameters for the model.
        return {"model": "model-001"}
```

Note

API references for individual test methods include troubleshooting tips.


```
EmbeddingsIntegrationTests()
```

## Bases

`EmbeddingsTests`

## Methods

[method

test\_embed\_query

Test embedding a string query.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of floats when calling `.embed_query`
   on a string.
2. The length of the list is consistent across different inputs.](/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_embed_query)[method

test\_embed\_documents

Test embedding a list of strings.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of lists of floats when calling
   `embed_documents` on a list of strings.
2. The length of each list is the same.](/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_embed_documents)[method

test\_aembed\_query

Test embedding a string query async.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of floats when calling `aembed_query`
   on a string.
2. The length of the list is consistent across different inputs.](/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_aembed_query)[method

test\_aembed\_documents

Test embedding a list of strings async.

Troubleshooting

If this test fails, check that:

1. The model will generate a list of lists of floats when calling
   `aembed_documents` on a list of strings.
2. The length of each list is the same.](/python/langchain-tests/integration_tests/embeddings/EmbeddingsIntegrationTests/test_aembed_documents)

## Inherited from[EmbeddingsTests](/python/langchain-tests/unit_tests/embeddings/EmbeddingsTests)

### Attributes

[Aembeddings\_class: type[Embeddings]

—

Embeddings class.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsTests/embeddings_class)[Aembedding\_model\_params: dict[str, Any]

—

Embeddings model parameters.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsTests/embedding_model_params)

### Methods

[Mmodel

—

Embeddings model fixture.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsTests/model)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)


