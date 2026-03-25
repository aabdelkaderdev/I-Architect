<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/qdrant -->

> [Qdrant](https://qdrant.tech/documentation/) (read: quadrant) is a vector similarity search engine.
> It provides a production-ready service with a convenient API to store, search, and manage
> points - vectors with an additional payload. `Qdrant` is tailored to extended filtering support.

## [​](#installation-and-setup) Installation and setup

Install the Python partner package:

pip

uv

Copy

```
pip install langchain-qdrant
```

## [​](#embedding-models) Embedding models

### [​](#fastembedsparse) FastEmbedSparse

Copy

```
from langchain_qdrant import FastEmbedSparse
```

### [​](#sparseembeddings) SparseEmbeddings

Copy

```
from langchain_qdrant import SparseEmbeddings
```

## [​](#vector-store) Vector store

There exists a wrapper around `Qdrant` indexes, allowing you to use it as a vectorstore,
whether for semantic search or example selection.
To import this vectorstore:

Copy

```
from langchain_qdrant import QdrantVectorStore
```

For a more detailed walkthrough of the Qdrant wrapper, see [this notebook](/oss/python/integrations/vectorstores/qdrant)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/qdrant.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.