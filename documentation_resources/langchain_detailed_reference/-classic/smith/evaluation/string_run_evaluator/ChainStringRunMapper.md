<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/string_run_evaluator/ChainStringRunMapper -->

Classv1.2.13 (latest)●Since v1.0

# ChainStringRunMapper


```
ChainStringRunMapper()
```

## Bases

`StringRunMapper`

## Attributes

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

[attribute

input\_key: str | None](/python/langchain-classic/smith/evaluation/string_run_evaluator/ChainStringRunMapper/input_key)

[attribute

prediction\_key: str | None](/python/langchain-classic/smith/evaluation/string_run_evaluator/ChainStringRunMapper/prediction_key)

[method

map](/python/langchain-classic/smith/evaluation/string_run_evaluator/ChainStringRunMapper/map)

Extract items to evaluate from the run object from a chain.

The key from the model Run's inputs to use as the eval input.
If not provided, will use the only input key or raise an
error if there are multiple.

The key from the model Run's outputs to use as the eval prediction.
If not provided, will use the only output key or raise an error
if there are multiple.

Maps the Run to a dictionary.