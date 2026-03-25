<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter -->

Classv1.1.1 (latest)●Since v0.0

# TextSplitter


```
TextSplitter(
  self,
  chunk_size: int = 4000,
  chunk_overlap: int = 200,
  length_function:
```

## Bases

`BaseDocumentTransformer``ABC`

## Constructors

## Methods

## Inherited from[BaseDocumentTransformer](/python/langchain-core/documents/transformers/BaseDocumentTransformer)(langchain\_core)

### Methods

[Matransform\_documents](/python/langchain-core/documents/transformers/BaseDocumentTransformer/atransform_documents)



[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[

[

[str](https://docs.python.org/3/library/stdtypes.html#str)

]

,

int

]

=

len

,

keep\_separator

:

[bool](https://docs.python.org/3/library/functions.html#bool)

|

[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)

[

'start'

,

'end'

]

=

False

,

add\_start\_index

:

[bool](https://docs.python.org/3/library/functions.html#bool)

=

False

,

strip\_whitespace

:

[bool](https://docs.python.org/3/library/functions.html#bool)

=

True

)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `chunk_size` | `int` | Default:`4000`  Maximum size of chunks to return |
| `chunk_overlap` | `int` | Default:`200`  Overlap in characters between chunks |
| `length_function` | `Callable[[str], int]` | Default:`len` |
| `keep_separator` | `bool | Literal['start', 'end']` | Default:`False` |
| `add_start_index` | `bool` | Default:`False` |
| `strip_whitespace` | `bool` | Default:`True` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| chunk\_size | [int](https://docs.python.org/3/library/functions.html#int) |
| chunk\_overlap | [int](https://docs.python.org/3/library/functions.html#int) |
| length\_function | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[str](https://docs.python.org/3/library/stdtypes.html#str)], [int](https://docs.python.org/3/library/functions.html#int)] |
| keep\_separator | [bool](https://docs.python.org/3/library/functions.html#bool) | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['start', 'end'] |
| add\_start\_index | [bool](https://docs.python.org/3/library/functions.html#bool) |
| strip\_whitespace | [bool](https://docs.python.org/3/library/functions.html#bool) |

[method

split\_text

Split text into multiple components.](/python/langchain-text-splitters/base/TextSplitter/split_text)

[method

create\_documents

Create a list of `Document` objects from a list of texts.](/python/langchain-text-splitters/base/TextSplitter/create_documents)

[method

split\_documents

Split documents.](/python/langchain-text-splitters/base/TextSplitter/split_documents)

[method

from\_huggingface\_tokenizer

Text splitter that uses Hugging Face tokenizer to count length.](/python/langchain-text-splitters/base/TextSplitter/from_huggingface_tokenizer)

[method

from\_tiktoken\_encoder

Text splitter that uses `tiktoken` encoder to count length.](/python/langchain-text-splitters/base/TextSplitter/from_tiktoken_encoder)

[method

transform\_documents

Transform sequence of documents by splitting them.](/python/langchain-text-splitters/base/TextSplitter/transform_documents)

Interface for splitting text into chunks.

Function that measures the length of given chunks

Whether to keep the separator and where to place it
in each corresponding chunk `(True='start')`

If `True`, includes chunk's start index in metadata

If `True`, strips whitespace from the start and end of
every document