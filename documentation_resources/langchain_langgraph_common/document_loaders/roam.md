<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/roam -->

> [ROAM](https://roamresearch.com/) is a note-taking tool for networked thought, designed to create a personal knowledge base.

This notebook covers how to load documents from a Roam database. This takes a lot of inspiration from the [Roam QA example repository](https://github.com/JimmyLv/roam-qa).

## [​](#-instructions-for-ingesting-your-own-dataset) 🧑 Instructions for ingesting your own dataset

Export your dataset from Roam Research. You can do this by clicking on the three dots in the upper right hand corner and then clicking `Export`.
When exporting, make sure to select the `Markdown & CSV` format option.
This will produce a `.zip` file in your Downloads folder. Move the `.zip` file into this repository.
Run the following command to unzip the zip file (replace the `Export...` with your own file name as needed).

Copy

```
unzip Roam-Export-1675782732639.zip -d Roam_DB
```

Copy

```
from langchain_community.document_loaders import RoamLoader
```

Copy

```
loader = RoamLoader("Roam_DB")
```

Copy

```
docs = loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/roam.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.