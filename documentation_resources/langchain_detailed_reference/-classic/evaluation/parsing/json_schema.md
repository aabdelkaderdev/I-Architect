<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/json_schema -->

Modulev1.2.13 (latest)●Since v1.0

# json\_schema

## Classes

[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

JsonSchemaEvaluator

An evaluator that validates a JSON prediction against a JSON schema reference.

This evaluator checks if a given JSON prediction conforms to the provided JSON schema.
If the prediction is valid, the score is True (no errors). Otherwise, the score is False (error occurred).](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator)


