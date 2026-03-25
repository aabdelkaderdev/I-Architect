<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/langchain_text_splitters -->

Modulev1.1.1 (latest)●Since v0.0

# langchain\_text\_splitters

Text Splitters are classes for splitting text.

Note

`MarkdownHeaderTextSplitter` and `HTMLHeaderTextSplitter` do not derive from
`TextSplitter`.

## Functions

## Classes

## Modules



[function

split\_text\_on\_tokens](/python/langchain-text-splitters/split_text_on_tokens)

[class

Language](/python/langchain-text-splitters/Language)

[class

TextSplitter](/python/langchain-text-splitters/TextSplitter)

[class

Tokenizer](/python/langchain-text-splitters/Tokenizer)

[class

TokenTextSplitter](/python/langchain-text-splitters/TokenTextSplitter)

[class

CharacterTextSplitter](/python/langchain-text-splitters/CharacterTextSplitter)

[class

RecursiveCharacterTextSplitter](/python/langchain-text-splitters/RecursiveCharacterTextSplitter)

[class

ElementType](/python/langchain-text-splitters/ElementType)

[class

HTMLHeaderTextSplitter](/python/langchain-text-splitters/HTMLHeaderTextSplitter)

[class

HTMLSectionSplitter](/python/langchain-text-splitters/HTMLSectionSplitter)

[class

HTMLSemanticPreservingSplitter](/python/langchain-text-splitters/HTMLSemanticPreservingSplitter)

[class

RecursiveJsonSplitter](/python/langchain-text-splitters/RecursiveJsonSplitter)

[class

JSFrameworkTextSplitter](/python/langchain-text-splitters/JSFrameworkTextSplitter)

[class

KonlpyTextSplitter](/python/langchain-text-splitters/KonlpyTextSplitter)

[class

LatexTextSplitter](/python/langchain-text-splitters/LatexTextSplitter)

[class

ExperimentalMarkdownSyntaxTextSplitter](/python/langchain-text-splitters/ExperimentalMarkdownSyntaxTextSplitter)

[class

HeaderType](/python/langchain-text-splitters/HeaderType)

[class

LineType](/python/langchain-text-splitters/LineType)

[class

MarkdownHeaderTextSplitter](/python/langchain-text-splitters/MarkdownHeaderTextSplitter)

[class

MarkdownTextSplitter](/python/langchain-text-splitters/MarkdownTextSplitter)

[class

NLTKTextSplitter](/python/langchain-text-splitters/NLTKTextSplitter)

[class

PythonCodeTextSplitter](/python/langchain-text-splitters/PythonCodeTextSplitter)

[class

SentenceTransformersTokenTextSplitter](/python/langchain-text-splitters/SentenceTransformersTokenTextSplitter)

[class

SpacyTextSplitter](/python/langchain-text-splitters/SpacyTextSplitter)

[module

base](/python/langchain-text-splitters/base)

[module

markdown](/python/langchain-text-splitters/markdown)

[module

html](/python/langchain-text-splitters/html)

[module

jsx](/python/langchain-text-splitters/jsx)

[module

python](/python/langchain-text-splitters/python)

[module

konlpy](/python/langchain-text-splitters/konlpy)

[module

character](/python/langchain-text-splitters/character)

[module

sentence\_transformers](/python/langchain-text-splitters/sentence_transformers)

[module

json](/python/langchain-text-splitters/json)

[module

latex](/python/langchain-text-splitters/latex)

[module

nltk](/python/langchain-text-splitters/nltk)

[module

spacy](/python/langchain-text-splitters/spacy)

Split incoming text and return chunks using tokenizer.

Enum of the programming languages.

Interface for splitting text into chunks.

Tokenizer data class.

Splitting text to tokens using model tokenizer.

Splitting text that looks at characters.

Splitting text by recursively look at characters.

Recursively tries to split by different characters to find one
that works.

Element type as typed dict.

Split HTML content into structured Documents based on specified headers.

Splits HTML content by detecting specified header tags and creating hierarchical
`Document` objects that reflect the semantic structure of the original content. For
each identified section, the splitter associates the extracted text with metadata
corresponding to the encountered headers.

If no specified headers are found, the entire content is returned as a single
`Document`. This allows for flexible handling of HTML input, ensuring that
information is organized according to its semantic headers.

The splitter provides the option to return each HTML element as a separate
`Document` or aggregate them into semantically meaningful chunks. It also
gracefully handles multiple levels of nested headers, creating a rich,
hierarchical representation of the content.

Splitting HTML files based on specified tag and font sizes.

Requires lxml package.

Split HTML content preserving semantic structure.

Splits HTML content by headers into generalized chunks, preserving semantic
structure. If chunks exceed the maximum chunk size, it uses
`RecursiveCharacterTextSplitter` for further splitting.

The splitter preserves full HTML elements and converts links to Markdown-like links.
It can also preserve images, videos, and audio elements by converting them into
Markdown format. Note that some chunks may exceed the maximum size to maintain
semantic integrity.

Splits JSON data into smaller, structured chunks while preserving hierarchy.

This class provides methods to split JSON data into smaller dictionaries or
JSON-formatted strings based on configurable maximum and minimum chunk sizes.
It supports nested JSON structures, optionally converts lists into dictionaries
for better chunking, and allows the creation of document objects for further use.

Text splitter that handles React (JSX), Vue, and Svelte code.

This splitter extends `RecursiveCharacterTextSplitter` to handle React (JSX), Vue,
and Svelte code by:

1. Detecting and extracting custom component tags from the text
2. Using those tags as additional separators along with standard JS syntax

The splitter combines:

- Custom component tags as separators (e.g. `<Component`, `<div`)
- JavaScript syntax elements (function, const, if, etc)
- Standard text splitting on newlines

This allows chunks to break at natural boundaries in React, Vue, and Svelte
component code.

Splitting text using Konlpy package.

It is good for splitting Korean text.

Attempts to split the text along Latex-formatted layout elements.

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

Header type as `TypedDict`.

Line type as `TypedDict`.

Splitting markdown files based on specified headers.

Attempts to split the text along Markdown-formatted headings.

Splitting text using NLTK package.

Attempts to split the text along Python syntax.

Splitting text to tokens using sentence model tokenizer.

Splitting text using Spacy package.

Per default, Spacy's `en_core_web_sm` model is used and
its default max\_length is 1000000 (it is the length of maximum character
this model takes which can be increased for large files). For a faster, but
potentially less accurate splitting, you can use `pipeline='sentencizer'`.

Text splitter base interface.

Markdown text splitters.

HTML text splitters.

JavaScript framework text splitter.

Python code text splitter.

Konlpy text splitter.

Character text splitters.

Sentence transformers text splitter.

JSON text splitter.

Latex text splitter.

NLTK text splitter.

Spacy text splitter.