<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/model_profile/ModelProfile -->

Classv1.2.21 (latest)●Since v1.1

# ModelProfile

Model profile.

Beta feature

This is a beta feature. The format of model profiles is subject to change.

Provides information about chat model capabilities, such as context window sizes
and supported features.


```
ModelProfile()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| status | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| release\_date | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| last\_updated | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| open\_weights | [bool](https://docs.python.org/3/library/functions.html#bool) |
| max\_input\_tokens | [int](https://docs.python.org/3/library/functions.html#int) |
| text\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| image\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| image\_url\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| pdf\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| audio\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| video\_inputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| image\_tool\_message | [bool](https://docs.python.org/3/library/functions.html#bool) |
| pdf\_tool\_message | [bool](https://docs.python.org/3/library/functions.html#bool) |
| max\_output\_tokens | [int](https://docs.python.org/3/library/functions.html#int) |
| reasoning\_output | [bool](https://docs.python.org/3/library/functions.html#bool) |
| text\_outputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| image\_outputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| audio\_outputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| video\_outputs | [bool](https://docs.python.org/3/library/functions.html#bool) |
| tool\_calling | [bool](https://docs.python.org/3/library/functions.html#bool) |
| tool\_choice | [bool](https://docs.python.org/3/library/functions.html#bool) |
| structured\_output | [bool](https://docs.python.org/3/library/functions.html#bool) |
| attachment | [bool](https://docs.python.org/3/library/functions.html#bool) |
| temperature | [bool](https://docs.python.org/3/library/functions.html#bool) |

## Attributes

[attribute

name: str

Human-readable model name.](/python/langchain-core/language_models/model_profile/ModelProfile/name)[attribute

status: str

Model status (e.g., `'active'`, `'deprecated'`).](/python/langchain-core/language_models/model_profile/ModelProfile/status)[attribute

release\_date: str

Model release date (ISO 8601 format, e.g., `'2025-06-01'`).](/python/langchain-core/language_models/model_profile/ModelProfile/release_date)[attribute

last\_updated: str

Date the model was last updated (ISO 8601 format).](/python/langchain-core/language_models/model_profile/ModelProfile/last_updated)[attribute

open\_weights: bool

Whether the model weights are openly available.](/python/langchain-core/language_models/model_profile/ModelProfile/open_weights)[attribute

max\_input\_tokens: int

Maximum context window (tokens)](/python/langchain-core/language_models/model_profile/ModelProfile/max_input_tokens)[attribute

text\_inputs: bool

Whether text inputs are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/text_inputs)[attribute

image\_inputs: bool

Whether image inputs are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/image_inputs)[attribute

image\_url\_inputs: bool

Whether [image URL inputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/image_url_inputs)[attribute

pdf\_inputs: bool

Whether [PDF inputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/pdf_inputs)[attribute

audio\_inputs: bool

Whether [audio inputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/audio_inputs)[attribute

video\_inputs: bool

Whether [video inputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/video_inputs)[attribute

image\_tool\_message: bool

Whether images can be included in tool messages.](/python/langchain-core/language_models/model_profile/ModelProfile/image_tool_message)[attribute

pdf\_tool\_message: bool

Whether PDFs can be included in tool messages.](/python/langchain-core/language_models/model_profile/ModelProfile/pdf_tool_message)[attribute

max\_output\_tokens: int

Maximum output tokens](/python/langchain-core/language_models/model_profile/ModelProfile/max_output_tokens)[attribute

reasoning\_output: bool

Whether the model supports [reasoning / chain-of-thought](https://docs.langchain.com/oss/python/langchain/models#reasoning)](/python/langchain-core/language_models/model_profile/ModelProfile/reasoning_output)[attribute

text\_outputs: bool

Whether text outputs are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/text_outputs)[attribute

image\_outputs: bool

Whether [image outputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/image_outputs)[attribute

audio\_outputs: bool

Whether [audio outputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/audio_outputs)[attribute

video\_outputs: bool

Whether [video outputs](https://docs.langchain.com/oss/python/langchain/models#multimodal)
are supported.](/python/langchain-core/language_models/model_profile/ModelProfile/video_outputs)[attribute

tool\_calling: bool

Whether the model supports [tool calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling)](/python/langchain-core/language_models/model_profile/ModelProfile/tool_calling)[attribute

tool\_choice: bool

Whether the model supports [tool choice](https://docs.langchain.com/oss/python/langchain/models#forcing-tool-calls)](/python/langchain-core/language_models/model_profile/ModelProfile/tool_choice)[attribute

structured\_output: bool

Whether the model supports a native [structured output](https://docs.langchain.com/oss/python/langchain/models#structured-outputs)
feature](/python/langchain-core/language_models/model_profile/ModelProfile/structured_output)[attribute

attachment: bool

Whether the model supports file attachments.](/python/langchain-core/language_models/model_profile/ModelProfile/attachment)[attribute

temperature: bool

Whether the model supports a temperature parameter.](/python/langchain-core/language_models/model_profile/ModelProfile/temperature)


