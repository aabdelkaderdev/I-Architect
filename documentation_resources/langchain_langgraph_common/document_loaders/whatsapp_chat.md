<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/whatsapp_chat -->

> [WhatsApp](https://www.whatsapp.com/) (also called `WhatsApp Messenger`) is a freeware, cross-platform, centralized instant messaging (IM) and voice-over-IP (VoIP) service. It allows users to send text and voice messages, make voice and video calls, and share images, documents, user locations, and other content.

This notebook covers how to load data from the `WhatsApp Chats` into a format that can be ingested into LangChain.

Copy

```
from langchain_community.document_loaders import WhatsAppChatLoader
```

Copy

```
loader = WhatsAppChatLoader("example_data/whatsapp_chat.txt")
```

Copy

```
loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/whatsapp_chat.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.