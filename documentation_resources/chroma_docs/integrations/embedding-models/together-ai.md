<!-- Source: https://docs.trychroma.com/integrations/embedding-models/together-ai -->

Chroma provides a wrapper around [Together AI](https://www.together.ai/) embedding models. This embedding function runs remotely against the Together AI servers, and will require an API key and a Together AI account. You can find more information in the [Together AI Embeddings Docs](https://docs.together.ai/docs/embeddings-overview), and [supported models](https://docs.together.ai/docs/serverless-models#embedding-models).

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions import TogetherAIEmbeddingFunction

os.environ["CHROMA_TOGETHER_AI_API_KEY"] = "<INSERT API KEY HERE>"

ef = TogetherAIEmbeddingFunction(
    model_name="togethercomputer/m2-bert-80M-32k-retrieval",
)
ef(input=["This is my first text to embed", "This is my second document"])
```

You must pass in a `model_name` to the embedding function. It is recommended to set the `CHROMA_TOGETHER_AI_API_KEY` environment variable for the API key, but the embedding function also optionally takes in an `api_key` parameter directly.