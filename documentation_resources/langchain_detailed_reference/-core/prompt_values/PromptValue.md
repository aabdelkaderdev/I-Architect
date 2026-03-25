<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values/PromptValue -->

Classv1.2.21 (latest)●Since v0.1

# PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.


```
PromptValue(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`Serializable``ABC`

## Methods

[method

is\_lc\_serializable

Return `True` as this class is serializable.](/python/langchain-core/prompt_values/PromptValue/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/prompt_values/PromptValue/get_lc_namespace)[method

to\_string

Return prompt value as string.](/python/langchain-core/prompt_values/PromptValue/to_string)[method

to\_messages

Return prompt as a list of messages.](/python/langchain-core/prompt_values/PromptValue/to_messages)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


