<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/serpapi -->

This notebook goes over how to use the [SerpApi](https://serpapi.com/) component to search the web.
Sign up for a SerpApi account [on the sign-up page](https://serpapi.com/users/sign_up) to get 250 free searches per month. After signing up, you can find your API key on the [dashboard](https://serpapi.com/manage-api-key).
Then set the environment variable `.env` file `SERPAPI_API_KEY` to your API key.

Copy

```
import os
os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY
```

Copy

```
from langchain_community.utilities import SerpAPIWrapper
```

Copy

```
search = SerpAPIWrapper()
```

Copy

```
search.run("Obama's first name?")
```

Copy

```
'Barack Hussein Obama II'
```

## [​](#custom-parameters) Custom parameters

You can also customize the SerpAPI wrapper with arbitrary parameters. For example, in the below example we will use `bing` instead of `google`.

Copy

```
params = {
    "engine": "bing",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
```

Copy

```
search.run("Obama's first name?")
```

Copy

```
'Barack Hussein Obama II is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Obama was the first African-American presi…New content will be added above the current area of focus upon selectionBarack Hussein Obama II is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Obama was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and as an Illinois state senator from 1997 to 2004, and previously worked as a civil rights lawyer before entering politics.Wikipediabarackobama.com'
```

Copy

```
from langchain.tools import tool

# You can create the tool to pass to an agent
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return search.run(query)
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/serpapi.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.