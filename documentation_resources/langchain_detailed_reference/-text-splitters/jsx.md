<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/jsx -->

Modulev1.1.1 (latest)●Since v0.3

# jsx

JavaScript framework text splitter.

## Classes

[class

RecursiveCharacterTextSplitter](/python/langchain-text-splitters/jsx/RecursiveCharacterTextSplitter)[class

JSFrameworkTextSplitter](/python/langchain-text-splitters/jsx/JSFrameworkTextSplitter)



Splitting text by recursively look at characters.

Recursively tries to split by different characters to find one
that works.

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