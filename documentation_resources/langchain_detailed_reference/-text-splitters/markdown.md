<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/markdown -->

Modulev1.1.1 (latest)●Since v0.0

# markdown

Markdown text splitters.

## Classes

[class

Language

Enum of the programming languages.](/python/langchain-text-splitters/markdown/Language)[class

RecursiveCharacterTextSplitter

Splitting text by recursively look at characters.

Recursively tries to split by different characters to find one
that works.](/python/langchain-text-splitters/markdown/RecursiveCharacterTextSplitter)[class

MarkdownTextSplitter

Attempts to split the text along Markdown-formatted headings.](/python/langchain-text-splitters/markdown/MarkdownTextSplitter)[class

MarkdownHeaderTextSplitter

Splitting markdown files based on specified headers.](/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter)[class

LineType

Line type as `TypedDict`.](/python/langchain-text-splitters/markdown/LineType)[class

HeaderType

Header type as `TypedDict`.](/python/langchain-text-splitters/markdown/HeaderType)[class

ExperimentalMarkdownSyntaxTextSplitter

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
  `headers_to_split_on` parameter.](/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter)


