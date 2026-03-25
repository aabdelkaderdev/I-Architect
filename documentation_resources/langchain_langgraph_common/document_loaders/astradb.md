<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/astradb -->

> [DataStax Astra DB](https://docs.datastax.com/en/astra-db-serverless/index.html) is a serverless
> AI-ready database built on `Apache Cassandra®` and made conveniently available
> through an easy-to-use JSON API.

## [​](#overview) Overview

The Astra DB Document Loader returns a list of LangChain [`Document`](https://reference.langchain.com/python/langchain-core/documents/base/Document) objects read from an Astra DB collection.
The loader takes the following parameters:

- `api_endpoint`: Astra DB API endpoint. Looks like `https://01234567-89ab-cdef-0123-456789abcdef-us-east1.apps.astra.datastax.com`
- `token`: Astra DB token. Looks like `AstraCS:aBcD0123...`
- `collection_name` : AstraDB collection name
- `namespace`: (Optional) AstraDB namespace (called *keyspace* in Astra DB)
- `filter_criteria`: (Optional) Filter used in the find query
- `projection`: (Optional) Projection used in the find query
- `limit`: (Optional) Maximum number of documents to retrieve
- `extraction_function`: (Optional) A function to convert the AstraDB document to the LangChain `page_content` string. Defaults to `json.dumps`

The loader sets the following metadata for the documents it reads:

Copy

```
metadata={
    "namespace": "...",
    "api_endpoint": "...",
    "collection": "..."
}
```

## [​](#setup) Setup

Copy

```
!pip install "langchain-astradb>=0.6,<0.7"
```

## [​](#load-documents-with-the-document-loader) Load documents with the document loader

Copy

```
from langchain_astradb import AstraDBLoader
```

[**API Reference:** `AstraDBLoader`](https://python.langchain.com/api_reference/astradb/document_loaders/langchain_astradb.document_loaders.AstraDBLoader.html#langchain_astradb.document_loaders.AstraDBLoader)

Copy

```
from getpass import getpass

ASTRA_DB_API_ENDPOINT = input("ASTRA_DB_API_ENDPOINT = ")
ASTRA_DB_APPLICATION_TOKEN = getpass("ASTRA_DB_APPLICATION_TOKEN = ")
```

Copy

```
ASTRA_DB_API_ENDPOINT =  https://01234567-89ab-cdef-0123-456789abcdef-us-east1.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN =  ········
```

Copy

```
loader = AstraDBLoader(
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    collection_name="movie_reviews",
    projection={"title": 1, "reviewtext": 1},
    limit=10,
)
```

Copy

```
docs = loader.load()
```

Copy

```
docs[0]
```

Copy

```
Document(metadata={'namespace': 'default_keyspace', 'api_endpoint': 'https://01234567-89ab-cdef-0123-456789abcdef-us-east1.apps.astra.datastax.com', 'collection': 'movie_reviews'}, page_content='{"_id": "659bdffa16cbc4586b11a423", "title": "Dangerous Men", "reviewtext": "\\"Dangerous Men,\\" the picture\'s production notes inform, took 26 years to reach the big screen. After having seen it, I wonder: What was the rush?"}')
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/astradb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.