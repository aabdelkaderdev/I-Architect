<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests -->

Classv1.1.4 (latest)●Since v1.1

# VectorStoreIntegrationTests


```
VectorStoreIntegrationTests()
```

## Bases

`BaseStandardTests`

## Attributes

[attribute

has\_sync: bool](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/has_sync)[attribute

has\_async: bool](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/has_async)[attribute

has\_get\_by\_ids: bool](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/has_get_by_ids)

## Methods

[method

vectorstore](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/vectorstore)[method

get\_embeddings](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/get_embeddings)[method

test\_vectorstore\_is\_empty](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_is_empty)[method

test\_add\_documents](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents)[method

test\_vectorstore\_still\_empty](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_still_empty)[method

test\_deleting\_documents](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_documents)[method

test\_deleting\_bulk\_documents](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_bulk_documents)[method

test\_delete\_missing\_content](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_delete_missing_content)[method

test\_add\_documents\_with\_ids\_is\_idempotent](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_ids_is_idempotent)[method

test\_add\_documents\_by\_id\_with\_mutation](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_by_id_with_mutation)[method

test\_get\_by\_ids](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_get_by_ids)[method

test\_get\_by\_ids\_missing](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_get_by_ids_missing)[method

test\_add\_documents\_documents](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_documents)[method

test\_add\_documents\_with\_existing\_ids](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_existing_ids)[method

test\_vectorstore\_is\_empty\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_is_empty_async)[method

test\_add\_documents\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_async)[method

test\_vectorstore\_still\_empty\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_vectorstore_still_empty_async)[method

test\_deleting\_documents\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_documents_async)[method

test\_deleting\_bulk\_documents\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_deleting_bulk_documents_async)[method

test\_delete\_missing\_content\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_delete_missing_content_async)[method

test\_add\_documents\_with\_ids\_is\_idempotent\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_ids_is_idempotent_async)[method

test\_add\_documents\_by\_id\_with\_mutation\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_by_id_with_mutation_async)[method

test\_get\_by\_ids\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_get_by_ids_async)[method

test\_get\_by\_ids\_missing\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_get_by_ids_missing_async)[method

test\_add\_documents\_documents\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_documents_async)[method

test\_add\_documents\_with\_existing\_ids\_async](/python/langchain-tests/integration_tests/vectorstores/VectorStoreIntegrationTests/test_add_documents_with_existing_ids_async)

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)



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

API references for individual test methods include troubleshooting tips.

Configurable property to enable or disable sync tests.

Configurable property to enable or disable async tests.

Whether the `VectorStore` supports `get_by_ids`.

Get the `VectorStore` class to test.

The returned `VectorStore` should be empty.

Get embeddings.

A pre-defined embeddings model that should be used for this test.

This currently uses `DeterministicFakeEmbedding` from `langchain-core`,
which uses numpy to generate random numbers based on a hash of the input text.

The resulting embeddings are not meaningful, but they are deterministic.

Test that the `VectorStore` is empty.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) initializes an empty vector store in the
`vectorestore` fixture.

Test adding documents into the `VectorStore`.

Troubleshooting

If this test fails, check that:

1. We correctly initialize an empty vector store in the `vectorestore`
   fixture.
2. Calling `similarity_search` for the top `k` similar documents does
   not threshold by score.
3. We do not mutate the original document object when adding it to the
   vector store (e.g., by adding an ID).

Test that the `VectorStore` is still empty.

This test should follow a test that adds documents.

This just verifies that the fixture is set up properly to be empty
after each test.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) correctly clears the vector store in the
`finally` block.

Test deleting documents from the `VectorStore`.

Troubleshooting

If this test fails, check that `add_documents` preserves identifiers
passed in through `ids`, and that `delete` correctly removes
documents.

Test that we can delete several documents at once.

Troubleshooting

If this test fails, check that `delete` correctly removes multiple
documents when given a list of IDs.

Deleting missing content should not raise an exception.

Troubleshooting

If this test fails, check that `delete` does not raise an exception
when deleting IDs that do not exist.

Adding by ID should be idempotent.

Troubleshooting

If this test fails, check that adding the same document twice with the
same IDs has the same effect as adding it once (i.e., it does not
duplicate the documents).

Test that we can overwrite by ID using `add_documents`.

Troubleshooting

If this test fails, check that when `add_documents` is called with an
ID that already exists in the vector store, the content is updated
rather than duplicated.

Test that the `VectorStore` is empty.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) initializes an empty vector store in the
`vectorestore` fixture.

Test adding documents into the `VectorStore`.

Troubleshooting

If this test fails, check that:

1. We correctly initialize an empty vector store in the `vectorestore`
   fixture.
2. Calling `.asimilarity_search` for the top `k` similar documents does
   not threshold by score.
3. We do not mutate the original document object when adding it to the
   vector store (e.g., by adding an ID).

Test that the `VectorStore` is still empty.

This test should follow a test that adds documents.

This just verifies that the fixture is set up properly to be empty
after each test.

Troubleshooting

If this test fails, check that the test class (i.e., sub class of
`VectorStoreIntegrationTests`) correctly clears the vector store in the
`finally` block.

Test deleting documents from the `VectorStore`.

Troubleshooting

If this test fails, check that `aadd_documents` preserves identifiers
passed in through `ids`, and that `delete` correctly removes
documents.

Test that we can delete several documents at once.

Troubleshooting

If this test fails, check that `adelete` correctly removes multiple
documents when given a list of IDs.

Deleting missing content should not raise an exception.

Troubleshooting

If this test fails, check that `adelete` does not raise an exception
when deleting IDs that do not exist.

Adding by ID should be idempotent.

Troubleshooting

If this test fails, check that adding the same document twice with the
same IDs has the same effect as adding it once (i.e., it does not
duplicate the documents).

Test that we can overwrite by ID using `add_documents`.

Troubleshooting

If this test fails, check that when `aadd_documents` is called with an
ID that already exists in the vector store, the content is updated
rather than duplicated.

Test get by IDs.

This test requires that `get_by_ids` be implemented on the vector store.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Test get by IDs with missing IDs.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and does not
raise an exception when given IDs that do not exist.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Run `add_documents` tests.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

Check also that `add_documents` will correctly generate string IDs if
none are provided.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Test that `add_documents` with existing IDs is idempotent.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

This test also verifies that:

1. IDs specified in the `Document.id` field are assigned when adding
   documents.
2. If some documents include IDs and others don't string IDs are generated
   for the latter.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Test get by IDs.

This test requires that `get_by_ids` be implemented on the vector store.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Test get by IDs with missing IDs.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and does not
raise an exception when given IDs that do not exist.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Run `add_documents` tests.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

Check also that `aadd_documents` will correctly generate string IDs if
none are provided.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```

Test that `add_documents` with existing IDs is idempotent.

Troubleshooting

If this test fails, check that `get_by_ids` is implemented and returns
documents in the same order as the IDs passed in.

This test also verifies that:

1. IDs specified in the `Document.id` field are assigned when adding
   documents.
2. If some documents include IDs and others don't string IDs are generated
   for the latter.

Note

`get_by_ids` was added to the `VectorStore` interface in
`langchain-core` version 0.2.11. If difficult to implement, this
test can be skipped by setting the `has_get_by_ids` property to
`False`.

```
@property
def has_get_by_ids(self) -> bool:
    return False
```