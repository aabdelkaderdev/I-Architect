<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/indexer -->

Modulev1.1.4 (latest)●Since v1.1

# indexer

Test suite to check index implementations.

Standard tests for the `DocumentIndex` abstraction

We don't recommend implementing externally managed `DocumentIndex` abstractions at this
time.

## Classes

[class

DocumentIndexerTestSuite

Test suite for checking the read-write of a document index.

Implementers should subclass this test suite and provide a fixture that returns an
empty index for each test.](/python/langchain-tests/integration_tests/indexer/DocumentIndexerTestSuite)[class

AsyncDocumentIndexTestSuite

Test suite for checking the read-write of a document index.

Implementers should subclass this test suite and provide a fixture
that returns an empty index for each test.](/python/langchain-tests/integration_tests/indexer/AsyncDocumentIndexTestSuite)


