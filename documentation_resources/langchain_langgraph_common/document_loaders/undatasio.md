<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/undatasio -->

This notebook provides a quick overview for getting started with the **UnDatasIO document loader**. UnDatasIO enables efficient loading and parsing of various document formats including PDF, PNG, JPG, JPEG, and JFIF, with features like document lazy loading and native async support, all through UnDatasIO’s secure cloud API. These capabilities make the processed data ready for generative AI workflows like RAG.
For detailed documentation on all features and configurations, refer to the official API reference.

## [​](#overview) Overview

### [​](#loader-features) Loader features

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| UnDatasIOLoader | ✅ | ✅ |

## [​](#setup) Setup

### [​](#credentials) Credentials

UnDatasIO requires an API token.
Generate a free token at [undatas.io](https://undatas.io) and set it in the cell below:

Copy

```
import getpass
import os

if "UNDATASIO_TOKEN" not in os.environ:
    os.environ["UNDATASIO_TOKEN"] = getpass.getpass(
        "Enter your UnDatasIO API token: "
    )
```

### [​](#installation) Installation

#### [​](#normal-installation) Normal installation

The following packages are required to run the rest of this notebook.

Copy

```
# Install package, compatible with API partitioning
pip install langchain-undatasio
```

### [​](#initialization) Initialization

The **UnDatasIOLoader** supports single-file upload & parsing via the UnDatasIO cloud API.

Copy

```
from langchain_undatasio import UnDatasIOLoader

loader = UnDatasIOLoader(
    token=os.environ["UNDATASIO_TOKEN"],
    file_path="demo.pdf"
)
```

### [​](#load) Load

Copy

```
docs = loader.load()
docs[0]
```

Copy

```
Document(
    metadata={'source': 'demo.pdf', 'task_id': 't1', 'file_id': 'f1'},
    page_content='Growing a Tail: Increasing Output Diversity in Large Language Models\n\nAuthors: Michal Shur-Ofry1, Bar Horowitz-Amsalem1†, Adir Rahamim2, Yonatan Belinkov2*\n\nAffiliations:\n\n1Law Faculty, Hebrew University of Jerusalem; Jerusalem, Israel.\n\n2Faculty of Computer Science, Technion – I'
)
```

Copy

```
print(docs[0].page_content[:300])
```

Copy

```
Growing a Tail: Increasing Output Diversity in Large Language Models

Authors: Michal Shur-Ofry1, Bar Horowitz-Amsalem1†, Adir Rahamim2, Yonatan Belinkov2*

Affiliations:

1Law Faculty, Hebrew University of Jerusalem; Jerusalem, Israel.

2Faculty of Computer Science, Technion – I
```

### [​](#lazy-load) Lazy load

**UnDatasIOLoader** supports lazy loading for memory-efficient iteration.

Copy

```
pages = []
for doc in loader.lazy_load():
    pages.append(doc)

pages[0]
```

Copy

```
Document(
    metadata={'source': 'demo.pdf', 'task_id': 't1', 'file_id': 'f1'},
    page_content='Growing a Tail: Increasing Output Diversity in Large Language Models\n\nAuthors: Michal Shur-Ofry1, Bar Horowitz-Amsalem1†, Adir Rahamim2, Yonatan Belinkov2*\n\nAffiliations:\n\n1Law Faculty, Hebrew University of Jerusalem; Jerusalem, Israel.\n\n2Faculty of Computer Science, Technion – I'
)
```

## [​](#see-also) See also

- [UnDatasIO](https://undatas.io)
- [langchain-undatasio](https://pypi.org/project/langchain-undatasio/)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/undatasio.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.