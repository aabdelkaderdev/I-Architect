<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/hyperbrowser -->

[Hyperbrowser](https://hyperbrowser.ai) is a platform for running and scaling headless browsers. It lets you launch and manage browser sessions at scale and provides easy to use solutions for any webscraping needs, such as scraping a single page or crawling an entire site.
Key Features:

- Instant Scalability - Spin up hundreds of browser sessions in seconds without infrastructure headaches
- Simple Integration - Works seamlessly with popular tools like Puppeteer and Playwright
- Powerful APIs - Easy to use APIs for scraping/crawling any site, and much more
- Bypass Anti-Bot Measures - Built-in stealth mode, ad blocking, automatic CAPTCHA solving, and rotating proxies

This guide provides a quick overview for getting started with Hyperbrowser [document loader](https://python.langchain.com/docs/concepts/#document-loaders).
For more information about Hyperbrowser, please visit the [Hyperbrowser website](https://hyperbrowser.ai) or if you want to check out the docs, you can visit the [Hyperbrowser docs](https://docs.hyperbrowser.ai).

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| HyperbrowserLoader | langchain-hyperbrowser | ❌ | ❌ | ❌ |

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| HyperbrowserLoader | ✅ | ✅ |

## [​](#setup) Setup

To access Hyperbrowser document loader you’ll need to install the `langchain-hyperbrowser` integration package, and create a Hyperbrowser account and get an API key.

### [​](#credentials) Credentials

Head to [Hyperbrowser](https://app.hyperbrowser.ai/) to sign up and generate an API key. Once you’ve done this set the HYPERBROWSER\_API\_KEY environment variable:

### [​](#installation) Installation

Install **langchain-hyperbrowser**.

Copy

```
pip install -qU langchain-hyperbrowser
```

## [​](#initialization) Initialization

Now we can instantiate our model object and load documents:

Copy

```
from langchain_hyperbrowser import HyperbrowserLoader

loader = HyperbrowserLoader(
    urls="https://example.com",
    api_key="YOUR_API_KEY",
)
```

## [​](#load) Load

Copy

```
docs = loader.load()
docs[0]
```

Copy

```
Document(metadata={'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, page_content='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)')
```

Copy

```
print(docs[0].metadata)
```

## [​](#lazy-load) Lazy load

Copy

```
page = []
for doc in loader.lazy_load():
    page.append(doc)
    if len(page) >= 10:
        # do some paged operation, e.g.
        # index.upsert(page)

        page = []
```

## [​](#advanced-usage) Advanced usage

You can specify the operation to be performed by the loader. The default operation is `scrape`. For `scrape`, you can provide a single URL or a list of URLs to be scraped. For `crawl`, you can only provide a single URL. The `crawl` operation will crawl the provided page and subpages and return a document for each page.

Copy

```
loader = HyperbrowserLoader(
    urls="https://hyperbrowser.ai", api_key="YOUR_API_KEY", operation="crawl"
)
```

Optional params for the loader can also be provided in the `params` argument. For more information on the supported params, visit [docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait](https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait) or [docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait](https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait).

Copy

```
loader = HyperbrowserLoader(
    urls="https://example.com",
    api_key="YOUR_API_KEY",
    operation="scrape",
    params={"scrape_options": {"include_tags": ["h1", "h2", "p"]}},
)
```

---

## [​](#api-reference) API reference

- [GitHub](https://github.com/hyperbrowserai/langchain-hyperbrowser/)
- [PyPi](https://pypi.org/project/langchain-hyperbrowser/)
- [Hyperbrowser Docs](https://docs.hyperbrowser.ai/)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/hyperbrowser.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.