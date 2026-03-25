<!-- Source: https://docs.trychroma.com/integrations/embedding-models/voyageai -->

Chroma also provides a convenient wrapper around VoyageAI’s embedding API. This embedding function runs remotely on VoyageAI’s servers, and requires an API key. You can get an API key by signing up for an account at [VoyageAI](https://dash.voyageai.com/).

- Python
- TypeScript

This embedding function relies on the `voyageai` python package, which you can install with `pip install voyageai`.

Report incorrect code

Copy

Ask AI

```
import chromadb.utils.embedding_functions as embedding_functions
voyageai_ef  = embedding_functions.VoyageAIEmbeddingFunction(api_key="YOUR_API_KEY",  model_name="voyage-3-large")
voyageai_ef(input=["document1","document2"])
```

Report incorrect code

Copy

Ask AI

```
// npm install @chroma-core/voyageai

import { VoyageAIEmbeddingFunction } from "@chroma-core/voyageai";

const embedder = new VoyageAIEmbeddingFunction({
    apiKey: "apiKey",
    modelName: "model_name",
});

// use directly
const embeddings = embedder.generate(["document1", "document2"]);

// pass documents to query for .add and .query
const collection = await client.createCollection({
    name: "name",
    embeddingFunction: embedder,
});
const collectionGet = await client.getCollection({
    name: "name",
    embeddingFunction: embedder,
});
```

### [​](#multilingual-model-example) Multilingual model example

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
voyageai_ef  = embedding_functions.VoyageAIEmbeddingFunction(
    api_key="YOUR_API_KEY",
    model_name="voyage-3-large"
)

multilingual_texts  = [
    'Hello from VoyageAI!', 'مرحباً من VoyageAI!!',
    'Hallo von VoyageAI!', 'Bonjour de VoyageAI!',
    '¡Hola desde VoyageAI!', 'Olá do VoyageAI!',
    'Ciao da VoyageAI!', '您好，来自 VoyageAI！',
    'कोहिअर से VoyageAI!'
]

voyageai_ef(input=multilingual_texts)
```

For further details on VoyageAI’s models check the [documentation](https://docs.voyageai.com/docs/introduction) and the [blogs](https://blog.voyageai.com/).