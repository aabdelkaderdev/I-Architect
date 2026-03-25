<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/mistralai -->

This will help you get started with MistralAI embedding models using LangChain. For detailed documentation on `MistralAIEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/mistralai/embeddings/langchain_mistralai.embeddings.MistralAIEmbeddings.html).

## [​](#overview) Overview

### [​](#integration-details) Integration details

## [​](#setup) Setup

To access MistralAI embedding models you’ll need to create a/an MistralAI account, get an API key, and install the `langchain-mistralai` integration package.

### [​](#credentials) Credentials

Head to <https://console.mistral.ai/> to sign up to MistralAI and generate an API key. Once you’ve done this set the MISTRAL\_API\_KEY environment variable:

Copy

```
import getpass
import os

if not os.getenv("MISTRAL_API_KEY"):
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your MistralAI API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### [​](#installation) Installation

The LangChain MistralAI integration lives in the `langchain-mistralai` package:

Copy

```
pip install -qU langchain-mistralai
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_mistralai import MistralAIEmbeddings

embeddings = MistralAIEmbeddings(
    model="mistral-embed",
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
[-0.04443359375, 0.01885986328125, 0.018035888671875, -0.00864410400390625, 0.049652099609375, -0.00
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
[-0.04443359375, 0.01885986328125, 0.0180511474609375, -0.0086517333984375, 0.049652099609375, -0.00
[-0.02032470703125, 0.02606201171875, 0.051605224609375, -0.0281982421875, 0.055755615234375, 0.0019
```

---

## [​](#api-reference) API reference

For detailed documentation on `MistralAIEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/mistralai/embeddings/langchain_mistralai.embeddings.MistralAIEmbeddings.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/mistralai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.