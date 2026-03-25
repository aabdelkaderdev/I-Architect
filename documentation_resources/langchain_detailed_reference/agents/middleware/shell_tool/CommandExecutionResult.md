<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/CommandExecutionResult -->

Classv1.2.13 (latest)●Since v1.0

# CommandExecutionResult

Structured result from command execution.


```
CommandExecutionResult(
  self,
  output: str,
  exit_code: int | None,
  timed_out: bool,
  truncated_by_lines: bool,
  truncated_by_bytes: bool,
  total_lines: int,
  total_bytes: int
)
```

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| output | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| exit\_code | [int](https://docs.python.org/3/library/functions.html#int) | None |
| timed\_out | [bool](https://docs.python.org/3/library/functions.html#bool) |
| truncated\_by\_lines | [bool](https://docs.python.org/3/library/functions.html#bool) |
| truncated\_by\_bytes | [bool](https://docs.python.org/3/library/functions.html#bool) |
| total\_lines | [int](https://docs.python.org/3/library/functions.html#int) |
| total\_bytes | [int](https://docs.python.org/3/library/functions.html#int) |

## Attributes

[attribute

output: str](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/output)[attribute

exit\_code: int | None](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/exit_code)[attribute

timed\_out: bool](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/timed_out)[attribute

truncated\_by\_lines: bool](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/truncated_by_lines)[attribute

truncated\_by\_bytes: bool](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/truncated_by_bytes)[attribute

total\_lines: int](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/total_lines)[attribute

total\_bytes: int](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult/total_bytes)


