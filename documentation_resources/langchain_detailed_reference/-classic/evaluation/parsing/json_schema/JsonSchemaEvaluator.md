<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# JsonSchemaEvaluator

An evaluator that validates a JSON prediction against a JSON schema reference.

This evaluator checks if a given JSON prediction conforms to the provided JSON schema.
If the prediction is valid, the score is True (no errors). Otherwise, the score is False (error occurred).


```
JsonSchemaEvaluator(
    self,
    **_: Any = {},
)
```

## Bases

`StringEvaluator`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator/__init__)

## Attributes

[attribute

requires\_input: bool

Returns whether the evaluator requires input.](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator/requires_input)[attribute

requires\_reference: bool

Returns whether the evaluator requires reference.](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator/requires_reference)[attribute

evaluation\_name: str

Returns the name of the evaluation.](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


