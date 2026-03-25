<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter -->

Classv1.1.1 (latest)●Since v0.2

# ExperimentalMarkdownSyntaxTextSplitter

An experimental text splitter for handling Markdown syntax.

This splitter aims to retain the exact whitespace of the original text while
extracting structured metadata, such as headers. It is a re-implementation of the
`MarkdownHeaderTextSplitter` with notable changes to the approach and additional
features.

Key Features:

- Retains the original whitespace and formatting of the Markdown text.
- Extracts headers, code blocks, and horizontal rules as metadata.
- Splits out code blocks and includes the language in the "Code" metadata key.
- Splits text on horizontal rules (`---`) as well.
- Defaults to sensible splitting behavior, which can be overridden using the
  `headers_to_split_on` parameter.


```
ExperimentalMarkdownSyntaxTextSplitter(
  self,
  headers_to_split_on: list[tuple[str, str]] | None = None,
  return_each_line: bool = False,
  strip_headers: bool = True
)
```

**Example:**

```
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]
splitter = ExperimentalMarkdownSyntaxTextSplitter(
    headers_to_split_on=headers_to_split_on
)
chunks = splitter.split(text)
for chunk in chunks:
    print(chunk)
```

This class is currently experimental and subject to change based on feedback and
further development.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `headers_to_split_on` | `list[tuple[str, str]] | None` | Default:`None`  A list of tuples, where each tuple contains a header tag (e.g., "h1") and its corresponding metadata key.  If `None`, default headers are used. |
| `return_each_line` | `bool` | Default:`False`  Whether to return each line as an individual chunk.  Defaults to `False`, which aggregates lines into larger chunks. |
| `strip_headers` | `bool` | Default:`True`  Whether to exclude headers from the resulting chunks. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| headers\_to\_split\_on | [list](https://docs.python.org/3/library/stdtypes.html#list)[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]] | None |
| return\_each\_line | [bool](https://docs.python.org/3/library/functions.html#bool) |
| strip\_headers | [bool](https://docs.python.org/3/library/functions.html#bool) |

## Attributes

[attribute

chunks: list[Document]](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/chunks)[attribute

current\_chunk](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/current_chunk)[attribute

current\_header\_stack: list[tuple[int, str]]](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/current_header_stack)[attribute

strip\_headers: strip\_headers](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/strip_headers)[attribute

splittable\_headers](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/splittable_headers)[attribute

return\_each\_line: return\_each\_line](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/return_each_line)

## Methods

[method

split\_text

Split the input text into structured chunks.

This method processes the input text line by line, identifying and handling
specific patterns such as headers, code blocks, and horizontal rules to split it
into structured chunks based on headers, code blocks, and horizontal rules.](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/split_text)


