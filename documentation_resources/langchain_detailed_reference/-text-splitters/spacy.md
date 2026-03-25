<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/spacy -->

Modulev1.1.1 (latest)●Since v0.0

# spacy

Spacy text splitter.

## Classes

[class

TextSplitter

Interface for splitting text into chunks.](/python/langchain-text-splitters/spacy/TextSplitter)[class

SpacyTextSplitter

Splitting text using Spacy package.

Per default, Spacy's `en_core_web_sm` model is used and
its default max\_length is 1000000 (it is the length of maximum character
this model takes which can be increased for large files). For a faster, but
potentially less accurate splitting, you can use `pipeline='sentencizer'`.](/python/langchain-text-splitters/spacy/SpacyTextSplitter)


