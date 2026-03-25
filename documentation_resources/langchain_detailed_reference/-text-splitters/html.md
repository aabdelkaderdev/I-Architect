<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/html -->

Modulev1.1.1 (latest)●Since v0.0

# html

HTML text splitters.

## Classes

[class

RecursiveCharacterTextSplitter](/python/langchain-text-splitters/html/RecursiveCharacterTextSplitter)[class

ElementType](/python/langchain-text-splitters/html/ElementType)[class

HTMLHeaderTextSplitter](/python/langchain-text-splitters/html/HTMLHeaderTextSplitter)[class

HTMLSectionSplitter](/python/langchain-text-splitters/html/HTMLSectionSplitter)[class

HTMLSemanticPreservingSplitter](/python/langchain-text-splitters/html/HTMLSemanticPreservingSplitter)



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