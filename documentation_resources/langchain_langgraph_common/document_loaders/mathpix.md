<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/mathpix -->

Inspired by Daniel Gross’s snippet here: <https://gist.github.com/danielgross/3ab4104e14faccc12b49200843adab21>

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| [MathPixPDFLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.MathpixPDFLoader.html) | [langchain-community](https://python.langchain.com/api_reference/community/index.html) | ✅ | ❌ | ❌ |

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| MathPixPDFLoader | ✅ | ❌ |

## [​](#setup) Setup

### [​](#credentials) Credentials

Sign up for Mathpix and [create an API key](https://mathpix.com/docs/ocr/creating-an-api-key) to set the `MATHPIX_API_KEY` variables in your environment

Copy

```
import getpass
import os

if "MATHPIX_API_KEY" not in os.environ:
    os.environ["MATHPIX_API_KEY"] = getpass.getpass("Enter your Mathpix API key: ")
```

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

## [​](#initialization) Initialization

Now we are ready to initialize our loader:

Copy

```
from langchain_community.document_loaders import MathpixPDFLoader

file_path = "./example_data/layout-parser-paper.pdf"
loader = MathpixPDFLoader(file_path)
```

## [​](#load) Load

Copy

```
docs = loader.load()
docs[0]
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

---

## [​](#api-reference) API reference

For detailed documentation of all MathpixPDFLoader features and configurations head to the API reference: [python.langchain.com/api\_reference/community/document\_loaders/langchain\_community.document\_loaders.pdf.MathpixPDFLoader.html](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.MathpixPDFLoader.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/mathpix.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.