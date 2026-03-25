<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/json_distance -->

Modulev1.2.13 (latest)●Since v1.0

# json\_distance

## Classes

[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

JsonEditDistanceEvaluator

An evaluator that calculates the edit distance between JSON strings.

This evaluator computes a normalized Damerau-Levenshtein distance between two JSON strings
after parsing them and converting them to a canonical format (i.e., whitespace and key order are normalized).
It can be customized with alternative distance and canonicalization functions.](/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator)


