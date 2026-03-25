<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite -->

Classv1.1.4 (latest)●Since v1.1

# DocumentIndexerTestSuite

Test suite for checking the read-write of a document index.

Implementers should subclass this test suite and provide a fixture that returns an
empty index for each test.


```
DocumentIndexerTestSuite()
```

## Bases

`ABC`

## Methods

[method

index

Get the index.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/index)[method

test\_upsert\_documents\_has\_no\_ids

Verify that there is no parameter called IDs in upsert.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_upsert_documents_has_no_ids)[method

test\_upsert\_no\_ids

Upsert works with documents that do not have IDs.

At the moment, the ID field in documents is optional.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_upsert_no_ids)[method

test\_upsert\_some\_ids

Test an upsert where some docs have IDs and some don't.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_upsert_some_ids)[method

test\_upsert\_overwrites

Test that upsert overwrites existing content.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_upsert_overwrites)[method

test\_delete\_missing\_docs

Verify that we can delete docs that aren't there.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_delete_missing_docs)[method

test\_delete\_semantics

Test deletion of content has appropriate semantics.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_delete_semantics)[method

test\_bulk\_delete

Test that we can delete several documents at once.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_bulk_delete)[method

test\_delete\_no\_args

Test delete with no args raises `ValueError`.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_delete_no_args)[method

test\_delete\_missing\_content

Deleting missing content should not raise an exception.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_delete_missing_content)[method

test\_get\_with\_missing\_ids

Test get with missing IDs.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_get_with_missing_ids)[method

test\_get\_missing

Test get by IDs with missing IDs.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite/test_get_missing)


