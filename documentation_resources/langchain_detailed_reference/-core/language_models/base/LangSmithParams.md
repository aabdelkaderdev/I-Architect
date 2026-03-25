<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/base/LangSmithParams -->

Classv1.2.21 (latest)●Since v0.2

# LangSmithParams

LangSmith parameters for tracing.


```
LangSmithParams()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| ls\_provider | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| ls\_model\_name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| ls\_model\_type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['chat', 'llm'] |
| ls\_temperature | [float](https://docs.python.org/3/library/functions.html#float) | None |
| ls\_max\_tokens | [int](https://docs.python.org/3/library/functions.html#int) | None |
| ls\_stop | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| ls\_integration | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

ls\_provider: str

Provider of the model.](/python/langchain-core/language_models/base/LangSmithParams/ls_provider)[attribute

ls\_model\_name: str

Name of the model.](/python/langchain-core/language_models/base/LangSmithParams/ls_model_name)[attribute

ls\_model\_type: Literal['chat', 'llm']

Type of the model.

Should be `'chat'` or `'llm'`.](/python/langchain-core/language_models/base/LangSmithParams/ls_model_type)[attribute

ls\_temperature: float | None

Temperature for generation.](/python/langchain-core/language_models/base/LangSmithParams/ls_temperature)[attribute

ls\_max\_tokens: int | None

Max tokens for generation.](/python/langchain-core/language_models/base/LangSmithParams/ls_max_tokens)[attribute

ls\_stop: list[str] | None

Stop words for generation.](/python/langchain-core/language_models/base/LangSmithParams/ls_stop)[attribute

ls\_integration: str

Integration that created the trace.](/python/langchain-core/language_models/base/LangSmithParams/ls_integration)


