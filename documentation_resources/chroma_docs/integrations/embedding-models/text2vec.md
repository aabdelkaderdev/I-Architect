<!-- Source: https://docs.trychroma.com/integrations/embedding-models/text2vec -->

Chroma provides a convenient wrapper around the Text2Vec library. This embedding function runs locally and is particularly useful for Chinese text embeddings.

- Python

This embedding function relies on the `text2vec` python package, which you can install with `pip install text2vec`.

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions import Text2VecEmbeddingFunction

text2vec_ef = Text2VecEmbeddingFunction(
    model_name="shibing624/text2vec-base-chinese"
)

texts = ["你好，世界！", "你好吗？"]
embeddings = text2vec_ef(texts)
```

You can pass in an optional `model_name` argument. By default, Chroma uses `shibing624/text2vec-base-chinese`.

Text2Vec is optimized for Chinese text embeddings. For English text, consider using Sentence Transformer or other embedding functions.