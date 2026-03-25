<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/telegram -->

> [Telegram Messenger](https://web.telegram.org/a/) is a globally accessible freemium, cross-platform, encrypted, cloud-based and centralized instant messaging service. The application also provides optional end-to-end encrypted chats and video calling, VoIP, file sharing and several other features.

This notebook covers how to load data from `Telegram` into a format that can be ingested into LangChain.

Copy

```
from langchain_community.document_loaders import (
    TelegramChatApiLoader,
    TelegramChatFileLoader,
)
```

Copy

```
loader = TelegramChatFileLoader("example_data/telegram.json")
```

Copy

```
loader.load()
```

Copy

```
[Document(page_content="Henry on 2020-01-01T00:00:02: It's 2020...\n\nHenry on 2020-01-01T00:00:04: Fireworks!\n\nGrace ðŸ§¤ ðŸ\x8d’ on 2020-01-01T00:00:05: You're a minute late!\n\n", metadata={'source': 'example_data/telegram.json'})]
```

`TelegramChatApiLoader` loads data directly from any specified chat from Telegram. In order to export the data, you will need to authenticate your Telegram account.
You can get the API\_HASH and API\_ID from [my.telegram.org/auth?to=apps](https://my.telegram.org/auth?to=apps)
chat\_entity—recommended to be the [entity](https://docs.telethon.dev/en/stable/concepts/entities.html?highlight=Entity#what-is-an-entity) of a channel.

Copy

```
loader = TelegramChatApiLoader(
    chat_entity="<CHAT_URL>",  # recommended to use Entity here
    api_hash="<API HASH >",
    api_id="<API_ID>",
    username="",  # needed only for caching the session.
)
```

Copy

```
loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/telegram.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.