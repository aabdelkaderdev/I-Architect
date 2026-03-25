<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/base/BaseLoader/load_and_split -->

Methodv1.2.21 (latest)●Since v0.1

# load\_and\_split

Load `Document` and split into chunks. Chunks are returned as `Document`.

Danger

Do not override this method. It should be considered to be deprecated!


```
load_and_split(
    self,
    text_splitter: TextSplitter | None = None,
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text_splitter` | `TextSplitter | None` | Default:`None`  `TextSplitter` instance to use for splitting documents.  Defaults to `RecursiveCharacterTextSplitter`. |


