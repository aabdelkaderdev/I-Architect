<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper -->

Classv1.2.13 (latest)●Since v1.0

# StringExampleMapper


```
StringExampleMapper()
```

## Bases

`Serializable`

## Attributes

## Methods

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)



M

get\_lc\_namespace

[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)

[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

reference\_key: str | None](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper/reference_key)

[attribute

output\_keys: list[str]](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper/output_keys)

[method

serialize\_chat\_messages](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper/serialize_chat_messages)

[method

map](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper/map)

Map an example, or row in the dataset, to the inputs of an evaluation.

The keys to extract from the run.

Extract the input messages from the run.

Maps the Example, or dataset row to a dictionary.