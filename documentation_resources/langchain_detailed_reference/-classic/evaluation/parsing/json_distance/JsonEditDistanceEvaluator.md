<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator -->

Classv1.2.13 (latest)●Since v1.0

# JsonEditDistanceEvaluator

An evaluator that calculates the edit distance between JSON strings.

This evaluator computes a normalized Damerau-Levenshtein distance between two JSON strings
after parsing them and converting them to a canonical format (i.e., whitespace and key order are normalized).
It can be customized with alternative distance and canonicalization functions.


```
JsonEditDistanceEvaluator(
  self,
  string_distance: Callable[[str, str], float] | None = None,
  canonicalize: Callable[[Any], Any] | None = None,
  **_: Any = {}
)
```

## Bases

`StringEvaluator`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `string_distance` | `Callable[[str, str], float] | None` | Default:`None`  A callable that computes the distance between two strings. If not provided, a Damerau-Levenshtein distance from the `rapidfuzz` package will be used. |
| `canonicalize` | `Callable[[Any], Any] | None` | Default:`None`  A callable that converts a parsed JSON object into its canonical string form. If not provided, the default behavior is to serialize the JSON with sorted keys and no extra whitespace. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| string\_distance | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)], [float](https://docs.python.org/3/library/functions.html#float)] | None |
| canonicalize | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[Any](https://docs.python.org/3/library/typing.html#typing.Any)], [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |

## Attributes

[attribute

requires\_input: bool](/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator/requires_input)[attribute

requires\_reference: bool](/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator/requires_reference)[attribute

evaluation\_name: str](/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator/evaluation_name)

## Inherited from[StringEvaluator](/python/langchain-classic/evaluation/schema/StringEvaluator)

### Methods

[Mevaluate\_strings

—

Evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/evaluate_strings)[Maevaluate\_strings

—

Asynchronously evaluate Chain or LLM output, based on optional input and label.](/python/langchain-classic/evaluation/schema/StringEvaluator/aevaluate_strings)


