<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/together -->

This will help you get started with Together embedding models using LangChain. For detailed documentation on `TogetherEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/together/embeddings/langchain_together.embeddings.TogetherEmbeddings.html).

## [​](#overview) Overview

### [​](#integration-details) Integration details

## [​](#setup) Setup

To access Together embedding models you’ll need to create a/an Together account, get an API key, and install the `langchain-together` integration package.

### [​](#credentials) Credentials

Head to <https://api.together.xyz/> to sign up to Together and generate an API key. Once you’ve done this set the TOGETHER\_API\_KEY environment variable:

Copy

```
import getpass
import os

if not os.getenv("TOGETHER_API_KEY"):
    os.environ["TOGETHER_API_KEY"] = getpass.getpass("Enter your Together API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### [​](#installation) Installation

The LangChain Together integration lives in the `langchain-together` package:

Copy

```
pip install -qU langchain-together
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_together import TogetherEmbeddings

embeddings = TogetherEmbeddings(
    model="togethercomputer/m2-bert-80M-8k-retrieval",
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
[0.3812227, -0.052848946, -0.10564975, 0.03480297, 0.2878488, 0.0084609175, 0.11605915, 0.05303011,
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
[0.3812227, -0.052848946, -0.10564975, 0.03480297, 0.2878488, 0.0084609175, 0.11605915, 0.05303011,
[0.066308185, -0.032866564, 0.115751594, 0.19082588, 0.14017, -0.26976448, -0.056340694, -0.26923394
```

---

## [​](#api-reference) API reference

For detailed documentation on `TogetherEmbeddings` features and configuration options, please refer to the [API reference](https://python.langchain.com/api_reference/together/embeddings/langchain_together.embeddings.TogetherEmbeddings.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/together.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.