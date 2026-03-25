<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/ShellSession -->

Classv1.2.13 (latest)●Since v1.0

# ShellSession

Persistent shell session that supports sequential command execution.


```
ShellSession(
  self,
  workspace: Path,
  policy: BaseExecutionPolicy,
  command: tuple[str, ...],
  environment: Mapping[str, str]
)
```

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| workspace | [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) |
| policy | [BaseExecutionPolicy](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy) |
| command | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] |
| environment | [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)] |

## Methods

[method

start

Start the shell subprocess and reader threads.](/python/langchain/agents/middleware/shell_tool/ShellSession/start)[method

restart

Restart the shell process.](/python/langchain/agents/middleware/shell_tool/ShellSession/restart)[method

stop

Stop the shell subprocess.](/python/langchain/agents/middleware/shell_tool/ShellSession/stop)[method

execute

Execute a command in the persistent shell.](/python/langchain/agents/middleware/shell_tool/ShellSession/execute)


