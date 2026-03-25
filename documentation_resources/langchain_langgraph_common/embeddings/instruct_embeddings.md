<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/instruct_embeddings -->

> [Hugging Face sentence-transformers](https://huggingface.co/sentence-transformers) is a Python framework for state-of-the-art sentence, text and image embeddings.
> One of the instruct embedding models is used in the `HuggingFaceInstructEmbeddings` class.

Copy

```
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
```

Copy

```
embeddings = HuggingFaceInstructEmbeddings(
    query_instruction="Represent the query for retrieval: "
)
```

Copy

```
load INSTRUCTOR_Transformer
max_seq_length  512
```

Copy

```
text = "This is a test document."
```

Copy

```
query_result = embeddings.embed_query(text)
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/instruct_embeddings.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.