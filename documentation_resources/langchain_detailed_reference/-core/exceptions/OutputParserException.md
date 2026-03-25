<!-- Source: https://reference.langchain.com/python/langchain-core/exceptions/OutputParserException -->

Classv1.2.21 (latest)●Since v0.1

# OutputParserException

Exception that output parsers should raise to signify a parsing error.

This exists to differentiate parsing errors from other code or execution errors
that also may arise inside the output parser.

`OutputParserException` will be available to catch and handle in ways to fix the
parsing error, while other errors will be raised.


```
OutputParserException(
  self,
  error: Any,
  observation: str | None = None,
  llm_output: str | None = None,
  send_to_llm: bool = False
)
```

## Bases

`ValueError``LangChainException`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error`\* | `Any` | The error that's being re-raised or an error message. |
| `observation` | `str | None` | Default:`None`  String explanation of error which can be passed to a model to try and remediate the issue. |
| `llm_output` | `str | None` | Default:`None`  String model output which is error-ing. |
| `send_to_llm` | `bool` | Default:`False`  Whether to send the observation and llm\_output back to an Agent after an `OutputParserException` has been raised.  This gives the underlying model driving the agent the context that the previous output was improperly structured, in the hopes that it will update the output to the correct format. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| error | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |
| observation | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| llm\_output | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| send\_to\_llm | [bool](https://docs.python.org/3/library/functions.html#bool) |

## Attributes

[attribute

observation: observation](/python/langchain-core/exceptions/OutputParserException/observation)[attribute

llm\_output: llm\_output](/python/langchain-core/exceptions/OutputParserException/llm_output)[attribute

send\_to\_llm: send\_to\_llm](/python/langchain-core/exceptions/OutputParserException/send_to_llm)


