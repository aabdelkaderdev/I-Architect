<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/mojeek_search -->

The following notebook will explain how to get results using Mojeek Search. Please visit [Mojeek Website](https://www.mojeek.com/services/search/web-search-api/) to obtain an API key.

Copy

```
from langchain_community.tools import MojeekSearch
```

Copy

```
api_key = "KEY"  # obtained from Mojeek Website
```

Copy

```
search = MojeekSearch.config(api_key=api_key, search_kwargs={"t": 10})
```

In `search_kwargs` you can add any search parameter that you can find on [Mojeek Documentation](https://www.mojeek.com/support/api/search/request_parameters.html)

Copy

```
search.run("mojeek")
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/mojeek_search.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.