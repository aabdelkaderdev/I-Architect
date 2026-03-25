<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores -->

Modulev1.1.4 (latest)●Since v1.1

# vectorstores

## Attributes

## Classes



[attribute

EMBEDDING\_SIZE: int](/python/langchain-tests/integration_tests/vectorstores/EMBEDDING_SIZE)

[class

BaseStandardTests

Base class for standard tests.](/python/langchain-tests/base/BaseStandardTests)

[class

VectorStoreIntegrationTests

Base class for vector store integration tests.

Implementers should subclass this test suite and provide a fixture
that returns an empty vector store for each test.

The fixture should use the `get_embeddings` method to get a pre-defined
embeddings model that should be used for this test suite.

Here is a template:

```
from typing import Generator

import pytest
from langchain_core.vectorstores import VectorStore
from langchain_parrot_link.vectorstores import ParrotVectorStore
from langchain_tests.integration_tests.vectorstores import VectorStoreIntegrationTests

class TestParrotVectorStore(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty vectorstore."""
        store = ParrotVectorStore(self.get_embeddings())
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass
```

In the fixture, before the `yield` we instantiate an empty vector store. In the
`finally` block, we call whatever logic is necessary to bring the vector store
to a clean state.

```
from typing import Generator

import pytest
from langchain_core.vectorstores import VectorStore
from langchain_tests.integration_tests.vectorstores import VectorStoreIntegrationTests

from langchain_chroma import Chroma

class TestChromaStandard(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty VectorStore for unit tests."""
        store = Chroma(embedding_function=self.get_embeddings())
        try:
            yield store
        finally:
            store.delete_collection()
            pass
```

Note that by default we enable both sync and async tests. To disable either,
override the `has_sync` or `has_async` properties to `False` in the
subclass. For example:

```
class TestParrotVectorStore(VectorStoreIntegrationTests):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        ...

    @property
    def has_async(self) -> bool:
        return False
```

Note

API references for individual test methods include troubleshooting tips.](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests)

Test suite to test `VectorStore` integrations.