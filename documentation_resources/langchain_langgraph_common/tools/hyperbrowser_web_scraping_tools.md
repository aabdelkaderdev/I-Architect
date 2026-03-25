<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/hyperbrowser_web_scraping_tools -->

[Hyperbrowser](https://hyperbrowser.ai) is a platform for running and scaling headless browsers. It lets you launch and manage browser sessions at scale and provides easy to use solutions for any webscraping needs, such as scraping a single page or crawling an entire site.
Key Features:

- Instant Scalability - Spin up hundreds of browser sessions in seconds without infrastructure headaches
- Simple Integration - Works seamlessly with popular tools like Puppeteer and Playwright
- Powerful APIs - Easy to use APIs for scraping/crawling any site, and much more
- Bypass Anti-Bot Measures - Built-in stealth mode, ad blocking, automatic CAPTCHA solving, and rotating proxies

This guide provides a quick overview for getting started with Hyperbrowser web tools.
For more information about Hyperbrowser, please visit the [Hyperbrowser website](https://hyperbrowser.ai) or if you want to check out the docs, you can visit the [Hyperbrowser docs](https://docs.hyperbrowser.ai).

## [​](#key-capabilities) Key capabilities

### [​](#scrape) Scrape

Hyperbrowser provides powerful scraping capabilities that allow you to extract data from any webpage. The scraping tool can convert web content into structured formats like markdown or HTML, making it easy to process and analyze the data.

### [​](#crawl) Crawl

The crawling functionality enables you to navigate through multiple pages of a website automatically. You can set parameters like page limits to control how extensively the crawler explores the site, collecting data from each page it visits.

### [​](#extract) Extract

Hyperbrowser’s extraction capabilities use AI to pull specific information from webpages according to your defined schema. This allows you to transform unstructured web content into structured data that matches your exact requirements.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Tool | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| Crawl Tool | langchain-hyperbrowser | ❌ | ❌ | ❌ |
| Scrape Tool | langchain-hyperbrowser | ❌ | ❌ | ❌ |
| Extract Tool | langchain-hyperbrowser | ❌ | ❌ | ❌ |

## [​](#setup) Setup

To access the Hyperbrowser web tools you’ll need to install the `langchain-hyperbrowser` integration package, and create a Hyperbrowser account and get an API key.

### [​](#credentials) Credentials

Head to [Hyperbrowser](https://app.hyperbrowser.ai/) to sign up and generate an API key. Once you’ve done this set the HYPERBROWSER\_API\_KEY environment variable:

Copy

```
export HYPERBROWSER_API_KEY=<your-api-key>
```

### [​](#installation) Installation

Install **langchain-hyperbrowser**.

Copy

```
pip install -qU langchain-hyperbrowser
```

## [​](#instantiation) Instantiation

### [​](#crawl-tool) Crawl tool

The `HyperbrowserCrawlTool` is a powerful tool that can crawl entire websites, starting from a given URL. It supports configurable page limits and scraping options.

Copy

```
from langchain_hyperbrowser import HyperbrowserCrawlTool
tool = HyperbrowserCrawlTool()
```

### [​](#scrape-tool) Scrape tool

The `HyperbrowserScrapeTool` is a tool that can scrape content from web pages. It supports both markdown and HTML output formats, along with metadata extraction.

Copy

```
from langchain_hyperbrowser import HyperbrowserScrapeTool
tool = HyperbrowserScrapeTool()
```

### [​](#extract-tool) Extract tool

The `HyperbrowserExtractTool` is a powerful tool that uses AI to extract structured data from web pages. It can extract information based predefined schemas.

Copy

```
from langchain_hyperbrowser import HyperbrowserExtractTool
tool = HyperbrowserExtractTool()
```

## [​](#invocation) Invocation

### [​](#basic-usage) Basic usage

#### [​](#crawl-tool-2) Crawl tool

Copy

```
from langchain_hyperbrowser import HyperbrowserCrawlTool

result = HyperbrowserCrawlTool().invoke(
    {
        "url": "https://example.com",
        "max_pages": 2,
        "scrape_options": {"formats": ["markdown"]},
    }
)
print(result)
```

Copy

```
{'data': [CrawledPage(metadata={'url': 'https://www.example.com/', 'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, html=None, markdown='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)', links=None, screenshot=None, url='https://example.com', status='completed', error=None)], 'error': None}
```

#### [​](#scrape-tool-2) Scrape tool

Copy

```
from langchain_hyperbrowser import HyperbrowserScrapeTool

result = HyperbrowserScrapeTool().invoke(
    {"url": "https://example.com", "scrape_options": {"formats": ["markdown"]}}
)
print(result)
```

Copy

```
{'data': ScrapeJobData(metadata={'url': 'https://www.example.com/', 'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, html=None, markdown='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)', links=None, screenshot=None), 'error': None}
```

#### [​](#extract-tool-2) Extract tool

Copy

```
from langchain_hyperbrowser import HyperbrowserExtractTool
from pydantic import BaseModel

class SimpleExtractionModel(BaseModel):
    title: str

result = HyperbrowserExtractTool().invoke(
    {
        "url": "https://example.com",
        "schema": SimpleExtractionModel,
    }
)
print(result)
```

Copy

```
{'data': {'title': 'Example Domain'}, 'error': None}
```

### [​](#with-custom-options) With custom options

#### [​](#crawl-tool-with-custom-options) Crawl tool with custom options

Copy

```
result = HyperbrowserCrawlTool().run(
    {
        "url": "https://example.com",
        "max_pages": 2,
        "scrape_options": {
            "formats": ["markdown", "html"],
        },
        "session_options": {"use_proxy": True, "solve_captchas": True},
    }
)
print(result)
```

Copy

```
{'data': [CrawledPage(metadata={'url': 'https://www.example.com/', 'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, html=None, markdown='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)', links=None, screenshot=None, url='https://example.com', status='completed', error=None)], 'error': None}
```

#### [​](#scrape-tool-with-custom-options) Scrape tool with custom options

Copy

```
result = HyperbrowserScrapeTool().run(
    {
        "url": "https://example.com",
        "scrape_options": {
            "formats": ["markdown", "html"],
        },
        "session_options": {"use_proxy": True, "solve_captchas": True},
    }
)
print(result)
```

Copy

```
{'data': ScrapeJobData(metadata={'url': 'https://www.example.com/', 'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, html='<html><head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8">\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n        \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href="https://www.iana.org/domains/example">More information...</a></p>\n</div>\n\n\n</body></html>', markdown='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)', links=None, screenshot=None), 'error': None}
```

#### [​](#extract-tool-with-custom-schema) Extract tool with custom schema

Copy

```
from typing import List

from pydantic import BaseModel

class ProductSchema(BaseModel):
    title: str
    price: float

class ProductsSchema(BaseModel):
    products: List[ProductSchema]

result = HyperbrowserExtractTool().run(
    {
        "url": "https://dummyjson.com/products?limit=10",
        "schema": ProductsSchema,
        "session_options": {"session_options": {"use_proxy": True}},
    }
)
print(result)
```

Copy

```
{'data': {'products': [{'price': 9.99, 'title': 'Essence Mascara Lash Princess'}, {'price': 19.99, 'title': 'Eyeshadow Palette with Mirror'}, {'price': 14.99, 'title': 'Powder Canister'}, {'price': 12.99, 'title': 'Red Lipstick'}, {'price': 8.99, 'title': 'Red Nail Polish'}, {'price': 49.99, 'title': 'Calvin Klein CK One'}, {'price': 129.99, 'title': 'Chanel Coco Noir Eau De'}, {'price': 89.99, 'title': "Dior J'adore"}, {'price': 69.99, 'title': 'Dolce Shine Eau de'}, {'price': 79.99, 'title': 'Gucci Bloom Eau de'}]}, 'error': None}
```

### [​](#async-usage) Async usage

All tools support async usage:

Copy

```
from typing import List

from langchain_hyperbrowser import (
    HyperbrowserCrawlTool,
    HyperbrowserExtractTool,
    HyperbrowserScrapeTool,
)
from pydantic import BaseModel

class ExtractionSchema(BaseModel):
    popular_library_name: List[str]

async def web_operations():
    # Crawl
    crawl_tool = HyperbrowserCrawlTool()
    crawl_result = await crawl_tool.arun(
        {
            "url": "https://example.com",
            "max_pages": 5,
            "scrape_options": {"formats": ["markdown"]},
        }
    )

    # Scrape
    scrape_tool = HyperbrowserScrapeTool()
    scrape_result = await scrape_tool.arun(
        {"url": "https://example.com", "scrape_options": {"formats": ["markdown"]}}
    )

    # Extract
    extract_tool = HyperbrowserExtractTool()
    extract_result = await extract_tool.arun(
        {
            "url": "https://npmjs.com",
            "schema": ExtractionSchema,
        }
    )

    return crawl_result, scrape_result, extract_result

results = await web_operations()
print(results)
```

Copy

```
---------------------------------------------------------------------------
```

Copy

```
NameError                                 Traceback (most recent call last)
```

Copy

```
Cell In[6], line 10
      1 from langchain_hyperbrowser import (
      2     HyperbrowserCrawlTool,
      3     HyperbrowserExtractTool,
      4     HyperbrowserScrapeTool,
      5 )
      7 from pydantic import BaseModel
---> 10 class ExtractionSchema(BaseModel):
     11     popular_library_name: List[str]
     14 async def web_operations():
     15     # Crawl
```

Copy

```
Cell In[6], line 11, in ExtractionSchema()
     10 class ExtractionSchema(BaseModel):
---> 11     popular_library_name: List[str]
```

Copy

```
NameError: name 'List' is not defined
```

## [​](#use-within-an-agent) Use within an agent

Here’s how to use any of the web tools within an agent:

Copy

```
from langchain_hyperbrowser import HyperbrowserCrawlTool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# Initialize the crawl tool
crawl_tool = HyperbrowserCrawlTool()

# Create the agent with the crawl tool
model = ChatOpenAI(temperature=0)

agent = create_agent(model, [crawl_tool])
user_input = "Crawl https://example.com and get content from up to 5 pages"
for step in agent.stream(
    {"messages": user_input},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```

Copy

```
================================ Human Message =================================

Crawl https://example.com and get content from up to 5 pages
================================== Ai Message ==================================
Tool Calls:
  hyperbrowser_crawl_data (call_G2ofdHOqjdnJUZu4hhbuga58)
 Call ID: call_G2ofdHOqjdnJUZu4hhbuga58
  Args:
    url: https://example.com
    max_pages: 5
    scrape_options: {'formats': ['markdown']}
================================= Tool Message =================================
Name: hyperbrowser_crawl_data

{'data': [CrawledPage(metadata={'url': 'https://www.example.com/', 'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}, html=None, markdown='Example Domain\n\n# Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission.\n\n[More information...](https://www.iana.org/domains/example)', links=None, screenshot=None, url='https://example.com', status='completed', error=None)], 'error': None}
================================== Ai Message ==================================

I have crawled the website [https://example.com](https://example.com) and retrieved content from the first page. Here is the content in markdown format:

\`\`\`
Example Domain

# Example Domain

This domain is for use in illustrative examples in documents. You may use this
domain in literature without prior coordination or asking for permission.

[More information...](https://www.iana.org/domains/example)
\`\`\`

If you would like to crawl more pages or need additional information, please let me know!
```

## [​](#configuration-options) Configuration options

### [​](#common-options) Common options

All tools support these basic configuration options:

- `url`: The URL to process
- `session_options`: Browser session configuration
  - `use_proxy`: Whether to use a proxy
  - `solve_captchas`: Whether to automatically solve CAPTCHAs
  - `accept_cookies`: Whether to accept cookies

### [​](#tool-specific-options) Tool-Specific options

#### [​](#crawl-tool-3) Crawl tool

- `max_pages`: Maximum number of pages to crawl
- `scrape_options`: Options for scraping each page
  - `formats`: List of output formats (markdown, html)

#### [​](#scrape-tool-3) Scrape tool

- `scrape_options`: Options for scraping the page
  - `formats`: List of output formats (markdown, html)

#### [​](#extract-tool-3) Extract tool

- `schema`: Pydantic model defining the structure to extract
- `extraction_prompt`: Natural language prompt for extraction

For more details, see the respective API references:

- [Crawl API Reference](https://docs.hyperbrowser.ai/reference/api-reference/crawl)
- [Scrape API Reference](https://docs.hyperbrowser.ai/reference/api-reference/scrape)
- [Extract API Reference](https://docs.hyperbrowser.ai/reference/api-reference/extract)

---

## [​](#api-reference) API reference

- [GitHub](https://github.com/hyperbrowserai/langchain-hyperbrowser/)
- [PyPi](https://pypi.org/project/langchain-hyperbrowser/)
- [Hyperbrowser Docs](https://docs.hyperbrowser.ai/)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/hyperbrowser_web_scraping_tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.