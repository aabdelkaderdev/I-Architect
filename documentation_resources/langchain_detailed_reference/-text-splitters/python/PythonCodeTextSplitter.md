<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/python/PythonCodeTextSplitter -->

Classv1.1.1 (latest)●Since v0.0

# PythonCodeTextSplitter


```
PythonCodeTextSplitter(
    self,
    **kwargs: Any = {},
)
```

## Bases

`RecursiveCharacterTextSplitter`

## Constructors

## Inherited from[RecursiveCharacterTextSplitter](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter)

### Methods

[Msplit\_text

—

Split the input text into smaller chunks based on predefined separators.](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/split_text)[Mfrom\_language

—

Return an instance of this class based on a specific language.](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/from_language)[Mget\_separators\_for\_language

—

Retrieve a list of separators specific to the given language.](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/get_separators_for_language)



## Inherited from[TextSplitter](/python/langchain-text-splitters/base/TextSplitter)

### Methods

[Msplit\_text

—

Split text into multiple components.](/python/langchain-text-splitters/base/TextSplitter/split_text)[Mcreate\_documents

—

Create a list of `Document` objects from a list of texts.](/python/langchain-text-splitters/base/TextSplitter/create_documents)[Msplit\_documents

—

Split documents.](/python/langchain-text-splitters/base/TextSplitter/split_documents)[Mfrom\_huggingface\_tokenizer

—

Text splitter that uses Hugging Face tokenizer to count length.](/python/langchain-text-splitters/base/TextSplitter/from_huggingface_tokenizer)[Mfrom\_tiktoken\_encoder

—

Text splitter that uses `tiktoken` encoder to count length.](/python/langchain-text-splitters/base/TextSplitter/from_tiktoken_encoder)[Mtransform\_documents

—

Transform sequence of documents by splitting them.](/python/langchain-text-splitters/base/TextSplitter/transform_documents)

## Inherited from[BaseDocumentTransformer](/python/langchain-core/documents/transformers/BaseDocumentTransformer)(langchain\_core)

### Methods

[Mtransform\_documents](/python/langchain-core/documents/transformers/BaseDocumentTransformer/transform_documents)[Matransform\_documents](/python/langchain-core/documents/transformers/BaseDocumentTransformer/atransform_documents)

[constructor

\_\_init\_\_](/python/langchain-text-splitters/python/PythonCodeTextSplitter/__init__)

Attempts to split the text along Python syntax.