<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base/format_document -->

Functionv1.2.21 (latest)●Since v0.1

# format\_document

Format a document into a string based on a prompt template.

First, this pulls information from the document from two sources:

1. `page_content`: This takes the information from the `document.page_content` and
   assigns it to a variable named `page_content`.
2. `metadata`: This takes information from `document.metadata` and assigns it to
   variables of the same name.

Those variables are then passed into the `prompt` to produce a formatted string.


```
format_document(
    doc: Document,
    prompt: BasePromptTemplate[str],
) -> str
```

**Example:**

```
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

doc = Document(page_content="This is a joke", metadata={"page": "1"})
prompt = PromptTemplate.from_template("Page {page}: {page_content}")
format_document(doc, prompt)
# -> "Page 1: This is a joke"
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `doc`\* | `Document` | `Document`, the `page_content` and `metadata` will be used to create the final string. |
| `prompt`\* | `BasePromptTemplate[str]` | `BasePromptTemplate`, will be used to format the `page_content` and `metadata` into the final string. |


