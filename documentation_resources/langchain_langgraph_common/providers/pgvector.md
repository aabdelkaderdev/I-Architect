<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/pgvector -->

This page covers how to use the Postgres [PGVector](https://github.com/pgvector/pgvector) ecosystem within LangChain
It is broken into two parts: installation and setup, and then references to specific PGVector wrappers.

## [​](#installation) Installation

- Install the Python package with `pip install pgvector`

## [​](#setup) Setup

1. The first step is to create a database with the `pgvector` extension installed.
   Follow the steps at [PGVector Installation Steps](https://github.com/pgvector/pgvector#installation) to install the database and the extension. The docker image is the easiest way to get started.

## [​](#wrappers) Wrappers

### [​](#vectorstore) VectorStore

There exists a wrapper around Postgres vector databases, allowing you to use it as a vectorstore,
whether for semantic search or example selection.
To import this vectorstore:

Copy

```
from langchain_community.vectorstores.pgvector import PGVector
```

### [​](#usage) Usage

For a more detailed walkthrough of the PGVector Wrapper, see [this notebook](/oss/python/integrations/vectorstores/pgvector)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/pgvector.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.