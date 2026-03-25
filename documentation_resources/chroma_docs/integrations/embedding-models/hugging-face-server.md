<!-- Source: https://docs.trychroma.com/integrations/embedding-models/hugging-face-server -->

Chroma provides a convenient wrapper for HuggingFace Text Embedding Server, a standalone server that provides text embeddings via a REST API. You can read more about it [**here**](https://github.com/huggingface/text-embeddings-inference).

## [​](#setting-up-the-server) Setting Up The Server

To run the embedding server locally you can run the following command from the root of the Chroma repository. The docker compose command will run Chroma and the embedding server together.

Report incorrect code

Copy

Ask AI

```
docker compose -f examples/server_side_embeddings/huggingface/docker-compose.yml up -d
```

or

Report incorrect code

Copy

Ask AI

```
docker run -p 8001:80 -d -rm --name huggingface-embedding-server ghcr.io/huggingface/text-embeddings-inference:cpu-0.3.0 --model-id BAAI/bge-small-en-v1.5 --revision -main
```

The above docker command will run the server with the `BAAI/bge-small-en-v1.5` model. You can find more information about running the server in docker [**here**](https://github.com/huggingface/text-embeddings-inference#docker).

## [​](#usage) Usage

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingServer
huggingface_ef = HuggingFaceEmbeddingServer(url="http://localhost:8001/embed")
```

The embedding model is configured on the server side. Check the docker-compose file in `examples/server_side_embeddings/huggingface/docker-compose.yml` for an example of how to configure the server.

## [​](#authentication) Authentication

The embedding server can be configured to only allow usage with API keys.
You can use authentication in the chroma clients:

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingServer
huggingface_ef = HuggingFaceEmbeddingServer(url="http://localhost:8001/embed", api_key="your secret key")
```