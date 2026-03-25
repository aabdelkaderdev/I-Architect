<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/chroma -->

> [Chroma](https://docs.trychroma.com/getting-started) is a database for building AI applications with embeddings.

## [​](#installation-and-setup) Installation and setup

pip

uv

Copy

```
pip install langchain-chroma
```

## [​](#vectorstore) VectorStore

There exists a wrapper around Chroma vector databases, allowing you to use it as a vectorstore,
whether for semantic search or example selection.

Copy

```
from langchain_chroma import Chroma
```

For a more detailed walkthrough of the Chroma wrapper, see [this notebook](/oss/python/integrations/vectorstores/chroma)

## [​](#retriever) Retriever

Copy

```
from langchain_classic.retrievers import SelfQueryRetriever
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/chroma.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.