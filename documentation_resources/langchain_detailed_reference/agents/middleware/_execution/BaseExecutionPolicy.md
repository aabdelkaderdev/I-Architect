<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_execution/BaseExecutionPolicy -->

Classv1.2.13 (latest)●Since v1.0

# BaseExecutionPolicy

Configuration contract for persistent shell sessions.

Concrete subclasses encapsulate how a shell process is launched and constrained.

Each policy documents its security guarantees and the operating environments in
which it is appropriate. Use `HostExecutionPolicy` for trusted, same-host execution;
`CodexSandboxExecutionPolicy` when the Codex CLI sandbox is available and you want
additional syscall restrictions; and `DockerExecutionPolicy` for container-level
isolation using Docker.


```
BaseExecutionPolicy(
  self,
  command_timeout: float = 30.0,
  startup_timeout: float = 30.0,
  termination_timeout: float = 10.0,
  max_output_lines: int = 100,
  max_output_bytes: int | None = None
)
```

## Bases

`abc.ABC`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| command\_timeout | [float](https://docs.python.org/3/library/functions.html#float) |
| startup\_timeout | [float](https://docs.python.org/3/library/functions.html#float) |
| termination\_timeout | [float](https://docs.python.org/3/library/functions.html#float) |
| max\_output\_lines | [int](https://docs.python.org/3/library/functions.html#int) |
| max\_output\_bytes | [int](https://docs.python.org/3/library/functions.html#int) | None |

## Attributes

[attribute

command\_timeout: float](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/command_timeout)[attribute

startup\_timeout: float](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/startup_timeout)[attribute

termination\_timeout: float](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/termination_timeout)[attribute

max\_output\_lines: int](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/max_output_lines)[attribute

max\_output\_bytes: int | None](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/max_output_bytes)

## Methods

[method

spawn

Launch the persistent shell process.](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy/spawn)


