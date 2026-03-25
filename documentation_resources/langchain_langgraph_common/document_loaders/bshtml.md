<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/bshtml -->

This guide provides a quick overview for getting started with BeautifulSoup4 [document loader](https://python.langchain.com/docs/concepts/document_loaders). For detailed documentation of all \_\_ModuleName\_\_Loader features and configurations head to the [API reference](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.html_bs.BSHTMLLoader.html).

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| [BSHTMLLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.html_bs.BSHTMLLoader.html) | [langchain-community](https://python.langchain.com/api_reference/community/index.html) | ✅ | ❌ | ❌ |

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| BSHTMLLoader | ✅ | ❌ |

## [​](#setup) Setup

To access BSHTMLLoader document loader you’ll need to install the `langchain-community` integration package and the `bs4` python package.

### [​](#credentials) Credentials

No credentials are needed to use the `BSHTMLLoader` class.
To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

Install **langchain-community** and **bs4**.

Copy

```
pip install -qU langchain-community bs4
```

## [​](#initialization) Initialization

Now we can instantiate our model object and load documents:

- TODO: Update model instantiation with relevant params.

Copy

```
from langchain_community.document_loaders import BSHTMLLoader

loader = BSHTMLLoader(
    file_path="./example_data/fake-content.html",
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
Document(metadata={'source': './example_data/fake-content.html', 'title': 'Test Title'}, page_content='\nTest Title\n\n\nMy First Heading\nMy first paragraph.\n\n\n')
```

Copy

```
print(docs[0].metadata)
```

Copy

```
{'source': './example_data/fake-content.html', 'title': 'Test Title'}
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
page[0]
```

Copy

```
Document(metadata={'source': './example_data/fake-content.html', 'title': 'Test Title'}, page_content='\nTest Title\n\n\nMy First Heading\nMy first paragraph.\n\n\n')
```

## [​](#adding-separator-to-bs4) Adding separator to BS4

We can also pass a separator to use when calling get\_text on the soup

Copy

```
loader = BSHTMLLoader(
    file_path="./example_data/fake-content.html", get_text_separator=", "
)

docs = loader.load()
print(docs[0])
```

Copy

```
page_content='
, Test Title,
,
,
, My First Heading,
, My first paragraph.,
,
,
' metadata={'source': './example_data/fake-content.html', 'title': 'Test Title'}
```

---

## [​](#api-reference) API reference

For detailed documentation of all BSHTMLLoader features and configurations head to the API reference: [python.langchain.com/api\_reference/community/document\_loaders/langchain\_community.document\_loaders.html\_bs.BSHTMLLoader.html](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.html_bs.BSHTMLLoader.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/bshtml.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.