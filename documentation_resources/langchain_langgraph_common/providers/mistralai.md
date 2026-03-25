<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/mistralai -->

> [Mistral AI](https://docs.mistral.ai/api/) is a platform that offers hosting for their powerful open source models.

## [​](#installation-and-setup) Installation and setup

A valid [API key](https://console.mistral.ai/users/api-keys/) is needed to communicate with the API.
You will also need the `langchain-mistralai` package:

pip

uv

Copy

```
pip install langchain-mistralai
```

## [​](#chat-models) Chat models

### [​](#chatmistralai) ChatMistralAI

See a [usage example](/oss/python/integrations/chat/mistralai).

Copy

```
from langchain_mistralai.chat_models import ChatMistralAI
```

## [​](#embedding-models) Embedding models

### [​](#mistralaiembeddings) MistralAIEmbeddings

See a [usage example](/oss/python/integrations/embeddings/mistralai).

Copy

```
from langchain_mistralai import MistralAIEmbeddings
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/mistralai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.