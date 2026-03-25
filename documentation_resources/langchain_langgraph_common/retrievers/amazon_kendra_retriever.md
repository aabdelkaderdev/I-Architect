<!-- Source: https://docs.langchain.com/oss/python/integrations/retrievers/amazon_kendra_retriever -->

> [Amazon Kendra](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html) is an intelligent search service provided by `Amazon Web Services` (`AWS`). It utilizes advanced natural language processing (NLP) and machine learning algorithms to enable powerful search capabilities across various data sources within an organization. `Kendra` is designed to help users find the information they need quickly and accurately, improving productivity and decision-making.

> With `Kendra`, users can search across a wide range of content types, including documents, FAQs, knowledge bases, manuals, and websites. It supports multiple languages and can understand complex queries, synonyms, and contextual meanings to provide highly relevant search results.

## [​](#using-the-amazon-kendra-index-retriever) Using the Amazon kendra index retriever

Copy

```
pip install -qU  boto3
```

Copy

```
from langchain_community.retrievers import AmazonKendraRetriever
```

Create New Retriever

Copy

```
retriever = AmazonKendraRetriever(index_id="c0806df7-e76b-4bce-9b5c-d5582f6b1a03")
```

Now you can use retrieved documents from Kendra index

Copy

```
retriever.invoke("what is langchain")
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/retrievers/amazon_kendra_retriever.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.