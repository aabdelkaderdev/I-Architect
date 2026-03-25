<!-- Source: https://docs.trychroma.com/integrations/embedding-models/ollama -->

Chroma provides a convenient wrapper around [Ollama](https://github.com/ollama/ollama)’s [embeddings API](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings). You can use the `OllamaEmbeddingFunction` embedding function to generate embeddings for your documents with a [model](https://github.com/ollama/ollama?tab=readme-ov-file#model-library) of your choice.

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

ollama_ef = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="llama2",
)

embeddings = ollama_ef(["This is my first text to embed",
                        "This is my second document"])
```