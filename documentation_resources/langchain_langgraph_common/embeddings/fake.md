<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/fake -->

LangChain also provides a fake embedding class. You can use this to test your pipelines.

Copy

```
from langchain_community.embeddings import FakeEmbeddings
```

Copy

```
embeddings = FakeEmbeddings(size=1352)
```

Copy

```
query_result = embeddings.embed_query("foo")
```

Copy

```
doc_results = embeddings.embed_documents(["foo"])
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/fake.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.