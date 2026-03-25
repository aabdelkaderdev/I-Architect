<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/json -->

Modulev1.1.1 (latest)●Since v0.0

# json

JSON text splitter.

## Classes

[class

RecursiveJsonSplitter](/python/langchain-text-splitters/json/RecursiveJsonSplitter)



Splits JSON data into smaller, structured chunks while preserving hierarchy.

This class provides methods to split JSON data into smaller dictionaries or
JSON-formatted strings based on configurable maximum and minimum chunk sizes.
It supports nested JSON structures, optionally converts lists into dictionaries
for better chunking, and allows the creation of document objects for further use.