<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/jsx/JSFrameworkTextSplitter -->

Classv1.1.1 (latest)●Since v0.3

# JSFrameworkTextSplitter


```
JSFrameworkTextSplitter(
  self,
  separators: list[str] | None = None,
  chunk_size: int
```

## Bases

`RecursiveCharacterTextSplitter`

## Constructors

## Methods

## Inherited from[RecursiveCharacterTextSplitter](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter)

### Methods

[Mfrom\_language

—

Return an instance of this class based on a specific language.](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/from_language)[Mget\_separators\_for\_language

—

Retrieve a list of separators specific to the given language.](/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/get_separators_for_language)

## Inherited from[TextSplitter](/python/langchain-text-splitters/base/TextSplitter)

### Methods



=

2000

,

chunk\_overlap

:

[int](https://docs.python.org/3/library/functions.html#int)

=

0

,

\*\*

kwargs

:

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

=

{

}

)

M

create\_documents

—

Create a list of `Document` objects from a list of texts.

[Msplit\_documents

—

Split documents.](/python/langchain-text-splitters/base/TextSplitter/split_documents)

[Mfrom\_huggingface\_tokenizer

—

Text splitter that uses Hugging Face tokenizer to count length.](/python/langchain-text-splitters/base/TextSplitter/from_huggingface_tokenizer)

[Mfrom\_tiktoken\_encoder

—

Text splitter that uses `tiktoken` encoder to count length.](/python/langchain-text-splitters/base/TextSplitter/from_tiktoken_encoder)

[Mtransform\_documents

—

Transform sequence of documents by splitting them.](/python/langchain-text-splitters/base/TextSplitter/transform_documents)

## Inherited from[BaseDocumentTransformer](/python/langchain-core/documents/transformers/BaseDocumentTransformer)(langchain\_core)

### Methods

[Mtransform\_documents](/python/langchain-core/documents/transformers/BaseDocumentTransformer/transform_documents)[Matransform\_documents](/python/langchain-core/documents/transformers/BaseDocumentTransformer/atransform_documents)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `separators` | `list[str] | None` | Default:`None`  Optional list of custom separator strings to use |
| `chunk_size` | `int` | Default:`2000`  Maximum size of chunks to return |
| `chunk_overlap` | `int` | Default:`0` |
| `**kwargs` | `Any` | Default:`{}` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| separators | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| chunk\_size | [int](https://docs.python.org/3/library/functions.html#int) |
| chunk\_overlap | [int](https://docs.python.org/3/library/functions.html#int) |

[method

split\_text

Split text into chunks.

This method splits the text into chunks by:

- Extracting unique opening component tags using regex
- Creating separators list with extracted tags and JS separators
- Splitting the text using the separators by calling the parent class method](/python/langchain-text-splitters/jsx/JSFrameworkTextSplitter/split_text)

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

Overlap in characters between chunks

Additional arguments to pass to parent class