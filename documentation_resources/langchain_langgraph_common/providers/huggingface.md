<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/huggingface -->

This page covers all LangChain integrations with [Hugging Face Hub](https://huggingface.co/) and libraries like [transformers](https://huggingface.co/docs/transformers/index), [sentence transformers](https://sbert.net/), and [datasets](https://huggingface.co/docs/datasets/index).

## [​](#chat-models) Chat models

### [​](#chathuggingface) ChatHuggingFace

We can use the `Hugging Face` LLM classes or directly use the `ChatHuggingFace` class.
See a [usage example](/oss/python/integrations/chat/huggingface).

Copy

```
from langchain_huggingface import ChatHuggingFace
```

## [​](#llms) LLMs

### [​](#huggingfaceendpoint) HuggingFaceEndpoint

We can use the `HuggingFaceEndpoint` class to run open source models via serverless [Inference Providers](https://huggingface.co/docs/inference-providers) or via dedicated [Inference Endpoints](https://huggingface.co/inference-endpoints/dedicated).
See a [usage example](/oss/python/integrations/llms/huggingface_endpoint).

Copy

```
from langchain_huggingface import HuggingFaceEndpoint
```

### [​](#huggingfacepipeline) HuggingFacePipeline

We can use the `HuggingFacePipeline` class to run open source models locally.
See a [usage example](/oss/python/integrations/llms/huggingface_pipelines).

Copy

```
from langchain_huggingface import HuggingFacePipeline
```

## [​](#embedding-models) Embedding models

### [​](#huggingfaceembeddings) HuggingFaceEmbeddings

We can use the `HuggingFaceEmbeddings` class to run open source embedding models locally.
See a [usage example](/oss/python/integrations/embeddings/huggingfacehub).

Copy

```
from langchain_huggingface import HuggingFaceEmbeddings
```

### [​](#huggingfaceendpointembeddings) HuggingFaceEndpointEmbeddings

We can use the `HuggingFaceEndpointEmbeddings` class to run open source embedding models via a dedicated [Inference Endpoint](https://huggingface.co/inference-endpoints/dedicated).
See a [usage example](/oss/python/integrations/embeddings/huggingfacehub).

Copy

```
from langchain_huggingface import HuggingFaceEndpointEmbeddings
```

### [​](#huggingfaceinferenceapiembeddings) HuggingFaceInferenceAPIEmbeddings

We can use the `HuggingFaceInferenceAPIEmbeddings` class to run open source embedding models via [Inference Providers](https://huggingface.co/docs/inference-providers).
See a [usage example](/oss/python/integrations/embeddings/huggingfacehub).

Copy

```
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
```

### [​](#huggingfaceinstructembeddings) HuggingFaceInstructEmbeddings

We can use the `HuggingFaceInstructEmbeddings` class to run open source embedding models locally.
See a [usage example](/oss/python/integrations/embeddings/instruct_embeddings).

Copy

```
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
```

### [​](#huggingfacebgeembeddings) HuggingFaceBgeEmbeddings

> [BGE models on the HuggingFace](https://huggingface.co/BAAI/bge-large-en-v1.5) are one of [the best open-source embedding models](https://huggingface.co/spaces/mteb/leaderboard).
> BGE model is created by the [Beijing Academy of Artificial Intelligence (BAAI)](https://en.wikipedia.org/wiki/Beijing_Academy_of_Artificial_Intelligence). `BAAI` is a private non-profit organization engaged in AI research and development.

See a [usage example](/oss/python/integrations/embeddings/bge_huggingface).

Copy

```
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
```

## [​](#document-loaders) Document loaders

### [​](#hugging-face-dataset) Hugging Face dataset

> [Hugging Face Hub](https://huggingface.co/docs/hub/index) is home to over 75,000
> [datasets](https://huggingface.co/docs/hub/index#datasets) in more than 100 languages
> that can be used for a broad range of tasks across NLP, Computer Vision, and Audio.
> They used for a diverse range of tasks such as translation, automatic speech
> recognition, and image classification.

We need to install `datasets` python package.

pip

uv

Copy

```
pip install datasets
```

See a [usage example](/oss/python/integrations/document_loaders/hugging_face_dataset).

Copy

```
from langchain_community.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader
```

### [​](#hugging-face-model-loader) Hugging Face model loader

> Load model information from `Hugging Face Hub`, including README content.
> This loader interfaces with the `Hugging Face Models API` to fetch
> and load model metadata and README files.
> The API allows you to search and filter models based on
> specific criteria such as model tags, authors, and more.

Copy

```
from langchain_community.document_loaders import HuggingFaceModelLoader
```

### [​](#image-captions) Image captions

It uses the Hugging Face models to generate image captions.
We need to install several python packages.

pip

uv

Copy

```
pip install transformers pillow
```

See a [usage example](/oss/python/integrations/document_loaders/image_captions).

Copy

```
from langchain_community.document_loaders import ImageCaptionLoader
```

## [​](#tools) Tools

### [​](#hugging-face-hub-tools) Hugging Face hub tools

> [Hugging Face Tools](https://huggingface.co/docs/transformers/v4.29.0/en/custom_tools)
> support text I/O and are loaded using the `load_huggingface_tool` function.

We need to install several python packages.

pip

uv

Copy

```
pip install transformers huggingface_hub
```

See a [usage example](/oss/python/integrations/tools/huggingface_tools).

Copy

```
from langchain_community.agent_toolkits.load_tools import load_huggingface_tool
```

### [​](#hugging-face-text-to-speech-model-inference) Hugging Face Text-to-Speech model inference.

> It is a wrapper around `OpenAI Text-to-Speech API`.

Copy

```
from langchain_community.tools.audio import HuggingFaceTextToSpeechModelInference
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/huggingface.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.