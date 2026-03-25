<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values/ImagePromptValue -->

Classv1.2.21 (latest)●Since v0.1

# ImagePromptValue

Image prompt value.


```
ImagePromptValue(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`PromptValue`

## Attributes

[attribute

image\_url: ImageURL

Image URL.](/python/langchain-core/prompt_values/ImagePromptValue/image_url)[attribute

type: Literal['ImagePromptValue']](/python/langchain-core/prompt_values/ImagePromptValue/type)

## Methods

[method

to\_string

Return prompt (image URL) as string.](/python/langchain-core/prompt_values/ImagePromptValue/to_string)[method

to\_messages

Return prompt (image URL) as messages.](/python/langchain-core/prompt_values/ImagePromptValue/to_messages)

## Inherited from[PromptValue](/python/langchain-core/prompt_values/PromptValue)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/prompt_values/PromptValue/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/prompt_values/PromptValue/get_lc_namespace)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable

—

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


