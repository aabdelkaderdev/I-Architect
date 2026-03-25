<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/huggingfacehub -->

Let’s load the Hugging Face Embedding class.

Copy

```
pip install -qU  langchain langchain-huggingface sentence_transformers
```

Copy

```
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
```

Copy

```
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
```

Copy

```
text = "This is a test document."
```

Copy

```
query_result = embeddings.embed_query(text)
```

Copy

```
query_result[:3]
```

Copy

```
[-0.04895168915390968, -0.03986193612217903, -0.021562768146395683]
```

Copy

```
doc_result = embeddings.embed_documents([text])
```

## [​](#hugging-face-inference-providers) Hugging Face inference providers

We can also access embedding models via the [Inference Providers](https://huggingface.co/docs/inference-providers), which let’s us use open source models on scalable serverless infrastructure.
First, we need to get a read-only API key from [Hugging Face](https://huggingface.co/settings/tokens).

Copy

```
from getpass import getpass

huggingfacehub_api_token = getpass()
```

Now we can use the `HuggingFaceInferenceAPIEmbeddings` class to run open source embedding models via [Inference Providers](https://huggingface.co/docs/inference-providers).

Copy

```
from langchain_huggingface import HuggingFaceInferenceAPIEmbeddings

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=huggingfacehub_api_token,
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)

query_result = embeddings.embed_query(text)
query_result[:3]
```

Copy

```
[-0.038338541984558105, 0.1234646737575531, -0.028642963618040085]
```

## [​](#hugging-face-hub) Hugging Face hub

We can also generate embeddings locally via the Hugging Face Hub package, which requires us to install `huggingface_hub`

Copy

```
!pip install huggingface_hub
```

Copy

```
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
```

Copy

```
embeddings = HuggingFaceEndpointEmbeddings()
```

Copy

```
text = "This is a test document."
```

Copy

```
query_result = embeddings.embed_query(text)
```

Copy

```
query_result[:3]
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/huggingfacehub.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.