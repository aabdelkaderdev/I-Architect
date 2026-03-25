<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Evaluators for parsing strings.

## Classes

[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

JsonValidityEvaluator

Evaluate whether the prediction is valid JSON.

This evaluator checks if the prediction is a valid JSON string. It does not
require any input or reference.](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator)[class

JsonEqualityEvaluator

Json Equality Evaluator.

Evaluate whether the prediction is equal to the reference after
parsing both as JSON.

This evaluator checks if the prediction, after parsing as JSON, is equal
to the reference,
which is also parsed as JSON. It does not require an input string.](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator)


