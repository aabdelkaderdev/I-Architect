<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/embeddings/EmbeddingsUnitTests -->

Classv1.1.4 (latest)●Since v1.1

# EmbeddingsUnitTests

Base class for embeddings unit tests.

Test subclasses must implement the `embeddings_class` property to specify the
embeddings model to be tested. You can also override the
`embedding_model_params` property to specify initialization parameters.

```
from typing import Type

from langchain_tests.unit_tests import EmbeddingsUnitTests
from my_package.embeddings import MyEmbeddingsModel

class TestMyEmbeddingsModelUnit(EmbeddingsUnitTests):
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

Testing initialization from environment variables
Overriding the `init_from_env_params` property will enable additional tests
for initialization from environment variables. See below for details.

`init_from_env_params`

This property is used in unit tests to test initialization from
environment variables. It should return a tuple of three dictionaries
that specify the environment variables, additional initialization args,
and expected instance attributes to check.

Defaults to empty dicts. If not overridden, the test is skipped.

```
@property
def init_from_env_params(self) -> Tuple[dict, dict, dict]:
    return (
        {
            "MY_API_KEY": "api_key",
        },
        {
            "model": "model-001",
        },
        {
            "my_api_key": "api_key",
        },
    )
```


```
EmbeddingsUnitTests()
```

## Bases

`EmbeddingsTests`

## Attributes

[attribute

init\_from\_env\_params: tuple[dict[str, str], dict[str, Any], dict[str, Any]]

Init from env params.

This property is used in unit tests to test initialization from environment
variables. It should return a tuple of three dictionaries that specify the
environment variables, additional initialization args, and expected instance
attributes to check.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsUnitTests/init_from_env_params)

## Methods

[method

test\_init

Test model initialization.

Troubleshooting

If this test fails, ensure that `embedding_model_params` is specified
and the model can be initialized from those params.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsUnitTests/test_init)[method

test\_init\_from\_env

Test initialization from environment variables.

Relies on the `init_from_env_params` property.
Test is skipped if that property is not set.

Troubleshooting

If this test fails, ensure that `init_from_env_params` is specified
correctly and that model parameters are properly set from environment
variables during initialization.](/python/langchain-tests/unit_tests/embeddings/EmbeddingsUnitTests/test_init_from_env)

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


