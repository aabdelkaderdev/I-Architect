<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/self_query/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Retriever that generates and executes structured queries over its own data source.

## Attributes

[attribute

logger](/python/langchain-classic/retrievers/self_query/base/logger)[attribute

QUERY\_CONSTRUCTOR\_RUN\_NAME: str](/python/langchain-classic/retrievers/self_query/base/QUERY_CONSTRUCTOR_RUN_NAME)

## Functions

[function

load\_query\_constructor\_runnable

Load a query constructor runnable chain.](/python/langchain-classic/chains/query_constructor/base/load_query_constructor_runnable)

## Classes

[class

AttributeInfo

Information about a data source attribute.](/python/langchain-classic/chains/query_constructor/schema/AttributeInfo)[class

SelfQueryRetriever

Self Query Retriever.

Retriever that uses a vector store and an LLM to generate the vector store queries.](/python/langchain-classic/retrievers/self_query/base/SelfQueryRetriever)


