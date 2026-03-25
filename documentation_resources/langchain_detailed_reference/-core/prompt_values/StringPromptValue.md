<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values/StringPromptValue -->

Classv1.2.21 (latest)●Since v0.1

# StringPromptValue

String prompt value.


```
StringPromptValue(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`PromptValue`

## Attributes

[attribute

text: str

Prompt text.](/python/langchain-core/prompt_values/StringPromptValue/text)[attribute

type: Literal['StringPromptValue']](/python/langchain-core/prompt_values/StringPromptValue/type)

## Methods

[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/prompt_values/StringPromptValue/get_lc_namespace)[method

to\_string

Return prompt as string.](/python/langchain-core/prompt_values/StringPromptValue/to_string)[method

to\_messages

Return prompt as messages.](/python/langchain-core/prompt_values/StringPromptValue/to_messages)

## Inherited from[PromptValue](/python/langchain-core/prompt_values/PromptValue)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/prompt_values/PromptValue/is_lc_serializable)

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

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


