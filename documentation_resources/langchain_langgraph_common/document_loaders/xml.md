<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/xml -->

This guide provides a quick overview for getting started with UnstructuredXMLLoader [document loader](https://python.langchain.com/docs/concepts/document_loaders). The `UnstructuredXMLLoader` is used to load `XML` files. The loader works with `.xml` files. The page content will be the text extracted from the XML tags.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | [JS support](https://js.langchain.com/docs/integrations/document_loaders/file_loaders/unstructured/) |
| --- | --- | --- | --- | --- |
| [UnstructuredXMLLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.xml.UnstructuredXMLLoader.html) | [langchain\_community](https://python.langchain.com/api_reference/community/index.html) | ✅ | ❌ | ✅ |

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| UnstructuredXMLLoader | ✅ | ❌ |

## [​](#setup) Setup

To access UnstructuredXMLLoader document loader you’ll need to install the `langchain-community` integration package.

### [​](#credentials) Credentials

No credentials are needed to use the UnstructuredXMLLoader
To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

Install **langchain\_community**.

Copy

```
pip install -qU langchain_community
```

## [​](#initialization) Initialization

Now we can instantiate our model object and load documents:

Copy

```
from langchain_community.document_loaders import UnstructuredXMLLoader

loader = UnstructuredXMLLoader(
    "./example_data/factbook.xml",
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
Document(metadata={'source': './example_data/factbook.xml'}, page_content='United States\n\nWashington, DC\n\nJoe Biden\n\nBaseball\n\nCanada\n\nOttawa\n\nJustin Trudeau\n\nHockey\n\nFrance\n\nParis\n\nEmmanuel Macron\n\nSoccer\n\nTrinidad & Tobado\n\nPort of Spain\n\nKeith Rowley\n\nTrack & Field')
```

Copy

```
print(docs[0].metadata)
```

Copy

```
{'source': './example_data/factbook.xml'}
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

---

## [​](#api-reference) API reference

For detailed documentation of all \_\_ModuleName\_\_Loader features and configurations head to the API reference: [python.langchain.com/api\_reference/community/document\_loaders/langchain\_community.document\_loaders.xml.UnstructuredXMLLoader.html](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.xml.UnstructuredXMLLoader.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/xml.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.