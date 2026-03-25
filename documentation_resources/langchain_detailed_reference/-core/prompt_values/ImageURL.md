<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values/ImageURL -->

Classv1.2.21 (latest)●Since v0.1

# ImageURL

Image URL for multimodal model inputs (OpenAI format).

Represents the inner `image_url` object in OpenAI's Chat Completion API format. This
is used by `ImagePromptTemplate` and `ChatPromptTemplate`.


```
ImageURL()
```

## Bases

`TypedDict`

**See Also:**

`ImageContentBlock`: LangChain's provider-agnostic image format used in message
content blocks. Use `ImageContentBlock` when working with the standardized
message format across different providers.

**Note:**

The `detail` field values are not validated locally. Invalid values
will be rejected by the downstream API, allowing new valid values to
be used without requiring a LangChain update.

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| detail | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['auto', 'low', 'high'] |
| url | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

detail: Literal['auto', 'low', 'high']

Specifies the detail level of the image.

Defaults to `'auto'` if not specified. Higher detail levels consume
more tokens but provide better image understanding.](/python/langchain-core/prompt_values/ImageURL/detail)[attribute

url: str

URL of the image or base64-encoded image data.](/python/langchain-core/prompt_values/ImageURL/url)


