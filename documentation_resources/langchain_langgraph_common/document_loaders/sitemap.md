<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/sitemap -->

Extends from the `WebBaseLoader`, `SitemapLoader` loads a sitemap from a given URL, and then scrapes and loads all pages in the sitemap, returning each page as a Document.
The scraping is done concurrently. There are reasonable limits to concurrent requests, defaulting to 2 per second. If you aren’t concerned about being a good citizen, or you control the scrapped server, or don’t care about load you can increase this limit. Note, while this will speed up the scraping process, it may cause the server to block you. Be careful!

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | [JS support](https://js.langchain.com/docs/integrations/document_loaders/web_loaders/sitemap/) |
| --- | --- | --- | --- | --- |
| [SiteMapLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.sitemap.SitemapLoader.html#langchain_community.document_loaders.sitemap.SitemapLoader) | [langchain-community](https://python.langchain.com/api_reference/community/index.html) | ✅ | ❌ | ✅ |

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| SiteMapLoader | ✅ | ❌ |

## [​](#setup) Setup

To access SiteMap document loader you’ll need to install the `langchain-community` integration package.

### [​](#credentials) Credentials

No credentials are needed to run this.
To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

Install **langchain-community**.

Copy

```
pip install -qU langchain-community
```

### [​](#fix-notebook-asyncio-bug) Fix notebook asyncio bug

Copy

```
import nest_asyncio

nest_asyncio.apply()
```

## [​](#initialization) Initialization

Now we can instantiate our model object and load documents:

Copy

```
from langchain_community.document_loaders.sitemap import SitemapLoader
```

Copy

```
sitemap_loader = SitemapLoader(web_path="https://api.python.langchain.com/sitemap.xml")
```

## [​](#load) Load

Copy

```
docs = sitemap_loader.load()
docs[0]
```

Copy

```
Fetching pages: 100%|##########| 28/28 [00:04<00:00,  6.83it/s]
```

Copy

```
Document(metadata={'source': 'https://api.python.langchain.com/en/stable/', 'loc': 'https://api.python.langchain.com/en/stable/', 'lastmod': '2024-05-15T00:29:42.163001+00:00', 'changefreq': 'weekly', 'priority': '1'}, page_content='\n\n\n\n\n\n\n\n\n\nLangChain Python API Reference Documentation.\n\n\nYou will be automatically redirected to the new location of this page.\n\n')
```

Copy

```
print(docs[0].metadata)
```

Copy

```
{'source': 'https://api.python.langchain.com/en/stable/', 'loc': 'https://api.python.langchain.com/en/stable/', 'lastmod': '2024-05-15T00:29:42.163001+00:00', 'changefreq': 'weekly', 'priority': '1'}
```

You can change the `requests_per_second` parameter to increase the max concurrent requests. and use `requests_kwargs` to pass kwargs when send requests.

Copy

```
sitemap_loader.requests_per_second = 2
# Optional: avoid `[SSL: CERTIFICATE_VERIFY_FAILED]` issue
sitemap_loader.requests_kwargs = {"verify": False}
```

## [​](#lazy-load) Lazy load

You can also load the pages lazily in order to minimize the memory load.

Copy

```
page = []
for doc in sitemap_loader.lazy_load():
    page.append(doc)
    if len(page) >= 10:
        # do some paged operation, e.g.
        # index.upsert(page)

        page = []
```

Copy

```
Fetching pages: 100%|##########| 28/28 [00:01<00:00, 19.06it/s]
```

## [​](#filtering-sitemap-urls) Filtering sitemap URLs

Sitemaps can be massive files, with thousands of URLs. Often you don’t need every single one of them. You can filter the URLs by passing a list of strings or regex patterns to the `filter_urls` parameter. Only URLs that match one of the patterns will be loaded.

Copy

```
loader = SitemapLoader(
    web_path="https://api.python.langchain.com/sitemap.xml",
    filter_urls=["https://api.python.langchain.com/en/latest"],
)
documents = loader.load()
```

Copy

```
documents[0]
```

Copy

```
Document(page_content='\n\n\n\n\n\n\n\n\n\nLangChain Python API Reference Documentation.\n\n\nYou will be automatically redirected to the new location of this page.\n\n', metadata={'source': 'https://api.python.langchain.com/en/latest/', 'loc': 'https://api.python.langchain.com/en/latest/', 'lastmod': '2024-02-12T05:26:10.971077+00:00', 'changefreq': 'daily', 'priority': '0.9'})
```

## [​](#add-custom-scraping-rules) Add custom scraping rules

The `SitemapLoader` uses `beautifulsoup4` for the scraping process, and it scrapes every element on the page by default. The `SitemapLoader` constructor accepts a custom scraping function. This feature can be helpful to tailor the scraping process to your specific needs; for example, you might want to avoid scraping headers or navigation elements.
The following example shows how to develop and use a custom function to avoid navigation and header elements.
Import the `beautifulsoup4` library and define the custom function.

Copy

```
pip install beautifulsoup4
```

Copy

```
from bs4 import BeautifulSoup

def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Find all 'nav' and 'header' elements in the BeautifulSoup object
    nav_elements = content.find_all("nav")
    header_elements = content.find_all("header")

    # Remove each 'nav' and 'header' element from the BeautifulSoup object
    for element in nav_elements + header_elements:
        element.decompose()

    return str(content.get_text())
```

Add your custom function to the `SitemapLoader` object.

Copy

```
loader = SitemapLoader(
    "https://api.python.langchain.com/sitemap.xml",
    filter_urls=["https://api.python.langchain.com/en/latest/"],
    parsing_function=remove_nav_and_header_elements,
)
```

## [​](#local-sitemap) Local sitemap

The sitemap loader can also be used to load local files.

Copy

```
sitemap_loader = SitemapLoader(web_path="example_data/sitemap.xml", is_local=True)

docs = sitemap_loader.load()
```

---

## [​](#api-reference) API reference

For detailed documentation of all SiteMapLoader features and configurations head to the API reference: [python.langchain.com/api\_reference/community/document\_loaders/langchain\_community.document\_loaders.sitemap.SitemapLoader.html#langchain\_community.document\_loaders.sitemap.SitemapLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.sitemap.SitemapLoader.html#langchain_community.document_loaders.sitemap.SitemapLoader)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/sitemap.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.