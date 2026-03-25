<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper -->

Classv1.2.13 (latest)●Since v1.0

# LLMStringRunMapper


```
LLMStringRunMapper()
```

## Bases

`StringRunMapper`

## Methods

## Inherited from[StringRunMapper](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunMapper)

### Attributes

[Aoutput\_keys: list[str]

—

The keys to extract from the run.](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunMapper/output_keys)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[A](/python/langchain-core/load/serializable/Serializable/lc_attributes)



lc\_attributes

[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[method

serialize\_chat\_messages](/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper/serialize_chat_messages)

[method

serialize\_inputs](/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper/serialize_inputs)

[method

serialize\_outputs](/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper/serialize_outputs)

[method

map](/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper/map)

Extract items to evaluate from the run object.

Extract the input messages from the run.

Serialize inputs.

Serialize outputs.

Maps the Run to a dictionary.