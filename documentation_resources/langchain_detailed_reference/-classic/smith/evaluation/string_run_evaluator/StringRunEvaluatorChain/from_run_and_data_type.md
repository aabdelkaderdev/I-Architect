<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunEvaluatorChain/from_run_and_data_type -->

Methodv1.2.13 (latest)●Since v1.0

# from\_run\_and\_data\_type

Create a StringRunEvaluatorChain.

Create a StringRunEvaluatorChain from an evaluator and the run and dataset
types.

This method provides an easy way to instantiate a StringRunEvaluatorChain, by
taking an evaluator and information about the type of run and the data.
The method supports LLM and chain runs.


```
from_run_and_data_type(
  cls,
  evaluator: StringEvaluator,
  run_type: str,
  data_type: DataType,
  input_key: str | None = None,
  prediction_key: str | None = None,
  reference_key: str | None = None,
  tags: list[str] | None = None
) -> StringRunEvaluatorChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `evaluator`\* | `StringEvaluator` | The string evaluator to use. |
| `run_type`\* | `str` | The type of run being evaluated. Supported types are LLM and Chain. |
| `data_type`\* | `DataType` | The type of dataset used in the run. |
| `input_key` | `str | None` | Default:`None`  The key used to map the input from the run. |
| `prediction_key` | `str | None` | Default:`None`  The key used to map the prediction from the run. |
| `reference_key` | `str | None` | Default:`None`  The key used to map the reference from the dataset. |
| `tags` | `list[str] | None` | Default:`None`  List of tags to attach to the evaluation chain. |


