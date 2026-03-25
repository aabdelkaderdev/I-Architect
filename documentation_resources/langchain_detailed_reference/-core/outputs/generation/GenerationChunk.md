<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/generation/GenerationChunk -->

Classv1.2.21 (latest)●Since v0.1

# GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.


```
GenerationChunk(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`Generation`

## Inherited from[Generation](/python/langchain-core/outputs/generation/Generation)

### Attributes

[Atext: str

—

Generated text output.](/python/langchain-core/outputs/generation/Generation/text)[Ageneration\_info: dict[str, Any] | None

—

Raw response from the provider.](/python/langchain-core/outputs/generation/Generation/generation_info)[Atype: Literal['Generation']

—

Type is used exclusively for serialization purposes.](/python/langchain-core/outputs/generation/Generation/type)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/outputs/generation/Generation/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/outputs/generation/Generation/get_lc_namespace)

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


