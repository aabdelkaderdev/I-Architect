<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/nomic -->

This will help you get started with Nomic embedding models using LangChain. For detailed documentation on `NomicEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/nomic/embeddings/langchain_nomic.embeddings.NomicEmbeddings.html).

## [​](#overview) Overview

### [​](#integration-details) Integration details

## [​](#setup) Setup

To access Nomic embedding models you’ll need to create a/an Nomic account, get an API key, and install the `langchain-nomic` integration package.

### [​](#credentials) Credentials

Head to <https://atlas.nomic.ai/> to sign up to Nomic and generate an API key. Once you’ve done this set the `NOMIC_API_KEY` environment variable:

Copy

```
import getpass
import os

if not os.getenv("NOMIC_API_KEY"):
    os.environ["NOMIC_API_KEY"] = getpass.getpass("Enter your Nomic API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### [​](#installation) Installation

The LangChain Nomic integration lives in the `langchain-nomic` package:

Copy

```
pip install -qU langchain-nomic
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_nomic import NomicEmbeddings

embeddings = NomicEmbeddings(
    model="nomic-embed-text-v1.5",
    # dimensionality=256,
    # Nomic's `nomic-embed-text-v1.5` model was [trained with Matryoshka learning](https://blog.nomic.ai/posts/nomic-embed-matryoshka)
    # to enable variable-length embeddings with a single model.
    # This means that you can specify the dimensionality of the embeddings at inference time.
    # The model supports dimensionality from 64 to 768.
    # inference_mode="remote",
    # One of `remote`, `local` (Embed4All), or `dynamic` (automatic). Defaults to `remote`.
    # api_key=... , # if using remote inference,
    # device="cpu",
    # The device to use for local embeddings. Choices include
    # `cpu`, `gpu`, `nvidia`, `amd`, or a specific device name. See
    # the docstring for `GPT4All.__init__` for more info. Typically
    # defaults to CPU. Do not use on macOS.
)
```

## [​](#indexing-and-retrieval) Indexing and retrieval

Embedding models are often used in retrieval-augmented generation (RAG) flows, both as part of indexing data as well as later retrieving it. For more detailed instructions, please see our [RAG tutorials](/oss/python/langchain/rag).
Below, see how to index and retrieve data using the `embeddings` object we initialized above. In this example, we will index and retrieve a sample document in the `InMemoryVectorStore`.

Copy

```
# Create a vector store with a sample text
from langchain_core.vectorstores import InMemoryVectorStore

text = "LangChain is the framework for building context-aware reasoning applications"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke("What is LangChain?")

# show the retrieved document's content
retrieved_documents[0].page_content
```

Copy

```
'LangChain is the framework for building context-aware reasoning applications'
```

## [​](#direct-usage) Direct usage

Under the hood, the vectorstore and retriever implementations are calling `embeddings.embed_documents(...)` and `embeddings.embed_query(...)` to create embeddings for the text(s) used in `from_texts` and retrieval `invoke` operations, respectively.
You can directly call these methods to get embeddings for your own use cases.

### [​](#embed-single-texts) Embed single texts

You can embed single texts or documents with `embed_query`:

Copy

```
single_vector = embeddings.embed_query(text)
print(str(single_vector)[:100])  # Show the first 100 characters of the vector
```

Copy

```
[0.024642944, 0.029083252, -0.14013672, -0.09082031, 0.058898926, -0.07489014, -0.0138168335, 0.0037
```

### [​](#embed-multiple-texts) Embed multiple texts

You can embed multiple texts with `embed_documents`:

Copy

```
text2 = (
    "LangGraph is a library for building stateful, multi-actor applications with LLMs"
)
two_vectors = embeddings.embed_documents([text, text2])
for vector in two_vectors:
    print(str(vector)[:100])  # Show the first 100 characters of the vector
```

Copy

```
[0.012771606, 0.023727417, -0.12365723, -0.083740234, 0.06530762, -0.07110596, -0.021896362, -0.0068
[-0.019058228, 0.04058838, -0.15222168, -0.06842041, -0.012130737, -0.07128906, -0.04534912, 0.00522
```

---

## [​](#api-reference) API reference

For detailed documentation on `NomicEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/nomic/embeddings/langchain_nomic.embeddings.NomicEmbeddings.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/nomic.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.