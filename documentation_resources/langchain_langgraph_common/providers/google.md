<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/google -->

This page covers all LangChain integrations with [Google Gemini](https://ai.google.dev/gemini-api/docs), [Google Cloud](https://cloud.google.com/), and other Google products (such as Google Maps, YouTube, and [more](#other-google-products)).

**Unified SDK & package consolidation**As of `langchain-google-genai` 4.0.0, this package uses the consolidated [`google-genai`](https://googleapis.github.io/python-genai/) SDK and now supports **both the Gemini Developer API and Vertex AI** backends.The `langchain-google-vertexai` package remains supported for Vertex AI platform-specific features (Model Garden, Vector Search, evaluation services, etc.).Read the [full announcement and migration guide](https://github.com/langchain-ai/langchain-google/discussions/1422).

Not sure which package to use?

Google Generative AI (Gemini API & Vertex AI)

Access Google Gemini models via the **[Gemini Developer API](https://ai.google.dev/)** or **[Vertex AI](https://cloud.google.com/vertex-ai)**. The backend is selected automatically based on your configuration.

- **Gemini Developer API**: Quick setup with API key, ideal for individual developers and rapid prototyping
- **Vertex AI**: Enterprise features with Google Cloud integration (requires GCP project)

Use the `langchain-google-genai` package for chat models, LLMs, and embeddings.[See integrations.](#google-generative-ai)

Google Cloud (Vertex AI Platform Services)

Access Vertex AI platform-specific services beyond Gemini models: Model Garden (Llama, Mistral, Anthropic), evaluation services, and specialized vision models.Use the `langchain-google-vertexai` package for platform services and specific packages (e.g., `langchain-google-community`, `langchain-google-cloud-sql-pg`) for other cloud services like databases and storage.[See integrations.](#google-cloud)

See Google’s guide on [migrating from the Gemini API to Vertex AI](https://ai.google.dev/gemini-api/docs/migrate-to-cloud) for more details on the differences.

---

## [​](#google-generative-ai) Google Generative AI

Access Google Gemini models via the [Gemini Developer API](https://ai.google.dev/gemini-api/docs) or [Vertex AI](https://cloud.google.com/vertex-ai) using the unified `langchain-google-genai` package.

### [​](#chat-models) Chat models

## ChatGoogleGenerativeAI

Google Gemini chat models via **Gemini Developer API** or **Vertex AI**.

Get started

### [​](#llms) LLMs

## GoogleGenerativeAI

Gemini models using the (legacy) LLM text completion interface.

Get started

### [​](#embedding-models) Embedding models

## GoogleGenerativeAIEmbeddings

Gemini embedding models via **Gemini Developer API** or **Vertex AI**.

Get started

---

## [​](#google-cloud) Google Cloud

Access Vertex AI platform-specific services including Model Garden (Llama, Mistral, Anthropic), Vector Search, evaluation services, and specialized vision models.

**For Gemini models**, use [`ChatGoogleGenerativeAI`](/oss/python/integrations/chat/google_generative_ai) from `langchain-google-genai`. The classes below focus on **Vertex AI platform services** not available in the consolidated SDK.

### [​](#chat-models-2) Chat models

## ChatAnthropicVertex

Anthropic on Vertex AI Model Garden

Get started

ChatVertexAI (deprecated)

**Deprecated**—Use [`ChatGoogleGenerativeAI`](/oss/python/integrations/chat/google_generative_ai) for Gemini models instead.

Copy

```
from langchain_google_vertexai import ChatVertexAI
```

VertexModelGardenLlama

Llama on Vertex AI Model Garden

Copy

```
from langchain_google_vertexai.model_garden_maas.llama import VertexModelGardenLlama
```

VertexModelGardenMistral

Mistral on Vertex AI Model Garden

Copy

```
from langchain_google_vertexai.model_garden_maas.mistral import VertexModelGardenMistral
```

GemmaChatLocalHF

Local Gemma model loaded from HuggingFace.

Copy

```
from langchain_google_vertexai.gemma import GemmaChatLocalHF
```

GemmaChatLocalKaggle

Local Gemma model loaded from Kaggle.

Copy

```
from langchain_google_vertexai.gemma import GemmaChatLocalKaggle
```

GemmaChatVertexAIModelGarden

Gemma on Vertex AI Model Garden

Copy

```
from langchain_google_vertexai.gemma import GemmaChatVertexAIModelGarden
```

VertexAIImageCaptioningChat

Image captioning model as a chat interface.

Copy

```
from langchain_google_vertexai.vision_models import VertexAIImageCaptioningChat
```

VertexAIImageEditorChat

Edit images given a prompt. Currently supports mask-free editing only.

Copy

```
from langchain_google_vertexai.vision_models import VertexAIImageEditorChat
```

VertexAIImageGeneratorChat

Generate images from a prompt.

Copy

```
from langchain_google_vertexai.vision_models import VertexAIImageGeneratorChat
```

VertexAIVisualQnAChat

Visual question answering model as a chat interface.

Copy

```
from langchain_google_vertexai.vision_models import VertexAIVisualQnAChat
```

### [​](#llms-2) LLMs

(Legacy) string-in, string-out LLM interface.

## VertexAIModelGarden

Hundreds of OSS models via Vertex AI Model Garden.

Get started

VertexAI (deprecated)

**Deprecated**—Use [`GoogleGenerativeAI`](/oss/python/integrations/llms/google_generative_ai) for Gemini models instead.

Copy

```
from langchain_google_vertexai import VertexAI
```

Gemma local from Hugging Face

Local Gemma model loaded from HuggingFace.

Copy

```
from langchain_google_vertexai.gemma import GemmaLocalHF
```

Gemma local from Kaggle

Local Gemma model loaded from Kaggle.

Copy

```
from langchain_google_vertexai.gemma import GemmaLocalKaggle
```

Gemma on Vertex AI Model Garden

Copy

```
from langchain_google_vertexai.gemma import GemmaVertexAIModelGarden
```

Vertex AI image captioning

Image captioning model as an LLM interface.

Copy

```
from langchain_google_vertexai.vision_models import VertexAIImageCaptioning
```

### [​](#embedding-models-2) Embedding models

VertexAIEmbeddings (deprecated)

**Deprecated**—Use [`GoogleGenerativeAIEmbeddings`](/oss/python/integrations/embeddings/google_generative_ai) instead.

Copy

```
from langchain_google_vertexai import VertexAIEmbeddings
```

### [​](#document-loaders) Document loaders

## AlloyDB for PostgreSQL

PostgreSQL-compatible database on Google Cloud.

Get started

## BigQuery

Serverless data warehouse.

Get started

## Bigtable

Key-value and wide-column store for structured and semi-structured data.

Get started

## Cloud SQL for MySQL

Managed MySQL database.

Get started

## Cloud SQL for SQL Server

Managed SQL Server database.

Get started

## Cloud SQL for PostgreSQL

Managed PostgreSQL database.

Get started

## Cloud Storage (directory)

Load documents from a GCS bucket directory.

Get started

## Cloud Storage (file)

Load a single document from GCS.

Get started

## El Carro for Oracle Workloads

Oracle databases on Kubernetes via El Carro.

Get started

## Firestore (Native Mode)

NoSQL document database.

Get started

## Firestore (Datastore Mode)

Firestore in Datastore mode.

Get started

## Memorystore for Redis

Managed Redis service.

Get started

## Spanner

Globally distributed relational database.

Get started

## Speech-to-Text

Transcribe audio files.

Get started

Cloud Vision loader

Load data using Google Cloud Vision API.

Copy

```
from langchain_google_community.vision import CloudVisionLoader
```

### [​](#document-transformers) Document transformers

## Document AI

Extract structured data from unstructured documents.

Get started

## Google Translate

Translate text and HTML via Cloud Translation API.

Get started

### [​](#vector-stores) Vector stores

Store and search vectors using Google Cloud databases and Vertex AI Vector Search.

## AlloyDB for PostgreSQL

PostgreSQL-compatible vector store on AlloyDB.

Get started

## BigQuery Vector Search

Semantic search using GoogleSQL with vector indexes.

Get started

## Memorystore for Redis

Vector store on Memorystore for Redis.

Get started

## Spanner

Vector store on Cloud Spanner.

Get started

## Bigtable

Vector store on Cloud Bigtable.

Get started

## Firestore (Native Mode)

Vector store on Firestore.

Get started

## Cloud SQL for MySQL

Vector store on Cloud SQL for MySQL.

Get started

## Cloud SQL for PostgreSQL

Vector store on Cloud SQL for PostgreSQL.

Get started

## Vertex AI Vector Search

Formerly known as Vertex AI Matching Engine, provides a low latency vector database. These vector databases are commonly referred to as vector similarity-matching or an approximate nearest neighbor (ANN) service.

Get started

## Vertex AI Vector Search + Datastore

Vector search with Datastore for document storage.

Get started

### [​](#retrievers) Retrievers

## Vertex AI Search

Generative AI powered search via Vertex AI Search.

Get started

## Document AI Warehouse

Search, store, and manage documents using Document AI Warehouse.

Get started

Other retrievers

Copy

```
from langchain_google_community import VertexAIMultiTurnSearchRetriever
from langchain_google_community import VertexAISearchRetriever
from langchain_google_community import VertexAISearchSummaryTool
```

### [​](#tools) Tools

Integrate agents with various Google Cloud services.

## Text-to-Speech

Synthesize natural-sounding speech with 100+ voices.

Get started

### [​](#callbacks) Callbacks

Track LLM/Chat model usage.

Vertex AI callback handler

Track `VertexAI` usage info.

Copy

```
from langchain_google_vertexai.callbacks import VertexAICallbackHandler
```

Google BigQuery

See the [documentation](/oss/python/integrations/callbacks/google_bigquery) for more details.

Copy

```
from langchain_google_community.callbacks.bigquery_callback import BigQueryCallbackHandler
```

### [​](#evaluators) Evaluators

Evaluate model outputs using Vertex AI.

VertexPairWiseStringEvaluator

Pair-wise evaluation using Vertex AI models.

Copy

```
from langchain_google_vertexai.evaluators.evaluation import VertexPairWiseStringEvaluator
```

VertexStringEvaluator

Single prediction evaluation using Vertex AI models.

Copy

```
from langchain_google_vertexai.evaluators.evaluation import VertexStringEvaluator
```

---

## [​](#other-google-products) Other Google products

Integrations with various Google services beyond the core Cloud Platform.

### [​](#document-loaders-2) Document loaders

## Google Drive

Load files from Google Drive. Currently supports Google Docs.

Get started

### [​](#vector-stores-2) Vector stores

## ScaNN (Local Index)

Efficient local vector similarity search at scale.

Get started

### [​](#retrievers-2) Retrievers

## Google Drive

Retrieve documents from Google Drive.

Get started

### [​](#tools-2) Tools

## Google Search

Web search via Google Custom Search Engine (CSE).

Get started

## Google Drive

Interact with Google Drive.

Get started

## Google Finance

Query financial data.

Get started

## Google Jobs

Query job listings.

Get started

## Google Lens

Visual searches.

Get started

## Google Places

Search for places.

Get started

## Google Scholar

Search academic papers.

Get started

## Google Trends

Query Google Trends data.

Get started

### [​](#mcp) MCP

## MCP Toolbox

Connect to databases including Cloud SQL and AlloyDB.

Get started

### [​](#toolkits) Toolkits

## Gmail

Create, search, and send emails via the Gmail API.

Get started

### [​](#chat-loaders) Chat loaders

## Gmail

Load chat history from Gmail threads.

Get started

---

## [​](#3rd-party-integrations) 3rd party integrations

Access Google services via unofficial third-party APIs.

### [​](#search) Search

## SearchApi

API access to Google search results, YouTube, and more.

Get started

## SerpApi

API access to Google search results.

Get started

## Serper.dev

API access to Google search results.

Get started

## cloro

Google Search results with AI Overview support.

Get started

### [​](#youtube) YouTube

## Search tool

Search YouTube videos without the official API.

Get started

## Audio loader

Download audio from YouTube videos.

Get started

## Transcripts loader

Load video transcripts.

Get started

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/google.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.