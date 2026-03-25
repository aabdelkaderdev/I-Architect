<!-- Source: https://docs.langchain.com/oss/python/integrations/embeddings/azure_openai -->

This will help you get started with AzureOpenAI embedding models using LangChain. For detailed documentation on `AzureOpenAIEmbeddings` features and configuration options, please refer to the [API reference](https://reference.langchain.com/python/langchain-openai/embeddings/azure/AzureOpenAIEmbeddings).

## [​](#overview) Overview

### [​](#integration-details) Integration details

## [​](#setup) Setup

To access AzureOpenAI embedding models you’ll need to create an Azure account, get an API key, and install the `langchain-openai` integration package.

### [​](#credentials) Credentials

You’ll need to have an Azure OpenAI instance deployed. You can deploy a version on Azure Portal following this [guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).
Once you have your instance running, make sure you have the name of your instance and key. You can find the key in the Azure Portal, under the “Keys and Endpoint” section of your instance.

Copy

```
AZURE_OPENAI_ENDPOINT=<YOUR API ENDPOINT>
AZURE_OPENAI_API_KEY=<YOUR_KEY>
AZURE_OPENAI_API_VERSION="2024-02-01"
```

Copy

```
import getpass
import os

if not os.getenv("AZURE_OPENAI_API_KEY"):
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
        "Enter your AzureOpenAI API key: "
    )
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
```

### [​](#installation) Installation

The LangChain AzureOpenAI integration lives in the `langchain-openai` package:

Copy

```
pip install -qU langchain-openai
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

```
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    # dimensions: Optional[int] = None, # Can specify dimensions with new text-embedding-3 models
    # azure_endpoint="https://<your-endpoint>.openai.azure.com/", If not provided, will read env variable AZURE_OPENAI_ENDPOINT
    # api_key=... # Can provide an API key directly. If missing read env variable AZURE_OPENAI_API_KEY
    # openai_api_version=..., # If not provided, will read env variable AZURE_OPENAI_API_VERSION
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
[-0.0011676070280373096, 0.007125577889382839, -0.014674457721412182, -0.034061674028635025, 0.01128
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
[-0.0011966148158535361, 0.007160289213061333, -0.014659193344414234, -0.03403077274560928, 0.011280
[-0.005595256108790636, 0.016757294535636902, -0.011055258102715015, -0.031094247475266457, -0.00363
```

---

## [​](#api-reference) API reference

For detailed documentation on `AzureOpenAIEmbeddings` features and configuration options, please refer to the [API reference](https://reference.langchain.com/python/langchain-openai/embeddings/azure/AzureOpenAIEmbeddings).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/embeddings/azure_openai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.