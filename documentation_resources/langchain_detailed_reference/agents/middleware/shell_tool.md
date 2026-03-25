<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool -->

Modulev1.2.13 (latest)●Since v1.0

# shell\_tool

Middleware that exposes a persistent shell tool to agents.

## Attributes

[attribute

SHELL\_TEMP\_PREFIX: str](/python/langchain/agents/middleware/shell_tool/SHELL_TEMP_PREFIX)[attribute

PrivateStateAttr

Annotation used to mark state attributes as purely internal for a given middleware.](/python/langchain/agents/middleware/shell_tool/PrivateStateAttr)[attribute

ResponseT](/python/langchain/agents/middleware/shell_tool/ResponseT)[attribute

LOGGER](/python/langchain/agents/middleware/shell_tool/LOGGER)[attribute

DEFAULT\_TOOL\_DESCRIPTION: str](/python/langchain/agents/middleware/shell_tool/DEFAULT_TOOL_DESCRIPTION)[attribute

SHELL\_TOOL\_NAME: str](/python/langchain/agents/middleware/shell_tool/SHELL_TOOL_NAME)

## Classes

[class

BaseExecutionPolicy

Configuration contract for persistent shell sessions.

Concrete subclasses encapsulate how a shell process is launched and constrained.

Each policy documents its security guarantees and the operating environments in
which it is appropriate. Use `HostExecutionPolicy` for trusted, same-host execution;
`CodexSandboxExecutionPolicy` when the Codex CLI sandbox is available and you want
additional syscall restrictions; and `DockerExecutionPolicy` for container-level
isolation using Docker.](/python/langchain/agents/middleware/shell_tool/BaseExecutionPolicy)[class

CodexSandboxExecutionPolicy

Launch the shell through the Codex CLI sandbox.

Ideal when you have the Codex CLI installed and want the additional syscall and
filesystem restrictions provided by Anthropic's Seatbelt (macOS) or Landlock/seccomp
(Linux) profiles. Commands still run on the host, but within the sandbox requested by
the CLI. If the Codex binary is unavailable or the runtime lacks the required
kernel features (e.g., Landlock inside some containers), process startup fails with a
`RuntimeError`.

Configure sandbox behavior via `config_overrides` to align with your Codex CLI
profile. This policy does not add its own resource limits; combine it with
host-level guards (cgroups, container resource limits) as needed.](/python/langchain/agents/middleware/shell_tool/CodexSandboxExecutionPolicy)[class

DockerExecutionPolicy

Run the shell inside a dedicated Docker container.

Choose this policy when commands originate from untrusted users or you require
strong isolation between sessions. By default the workspace is bind-mounted only
when it refers to an existing non-temporary directory; ephemeral sessions run
without a mount to minimise host exposure. The container's network namespace is
disabled by default (`--network none`) and you can enable further hardening via
`read_only_rootfs` and `user`.

The security guarantees depend on your Docker daemon configuration. Run the agent on
a host where Docker is locked down (rootless mode, AppArmor/SELinux, etc.) and
review any additional volumes or capabilities passed through `extra_run_args`. The
default image is `python:3.12-alpine3.19`; supply a custom image if you need
preinstalled tooling.](/python/langchain/agents/middleware/shell_tool/DockerExecutionPolicy)[class

HostExecutionPolicy

Run the shell directly on the host process.

This policy is best suited for trusted or single-tenant environments (CI jobs,
developer workstations, pre-sandboxed containers) where the agent must access the
host filesystem and tooling without additional isolation. Enforces optional CPU and
memory limits to prevent runaway commands but offers **no** filesystem or network
sandboxing; commands can modify anything the process user can reach.

On Linux platforms resource limits are applied with `resource.prlimit` after the
shell starts. On macOS, where `prlimit` is unavailable, limits are set in a
`preexec_fn` before `exec`. In both cases the shell runs in its own process group
so timeouts can terminate the full subtree.](/python/langchain/agents/middleware/shell_tool/HostExecutionPolicy)[class

PIIDetectionError

Raised when configured to block on detected sensitive values.](/python/langchain/agents/middleware/shell_tool/PIIDetectionError)[class

PIIMatch

Represents an individual match of sensitive data.](/python/langchain/agents/middleware/shell_tool/PIIMatch)[class

RedactionRule

Configuration for handling a single PII type.](/python/langchain/agents/middleware/shell_tool/RedactionRule)[class

ResolvedRedactionRule

Resolved redaction rule ready for execution.](/python/langchain/agents/middleware/shell_tool/ResolvedRedactionRule)[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/shell_tool/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/shell_tool/AgentState)[class

ShellToolState

Agent state extension for tracking shell session resources.](/python/langchain/agents/middleware/shell_tool/ShellToolState)[class

CommandExecutionResult

Structured result from command execution.](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult)[class

ShellSession

Persistent shell session that supports sequential command execution.](/python/langchain/agents/middleware/shell_tool/ShellSession)[class

ShellToolMiddleware

Middleware that registers a persistent shell tool for agents.

The middleware exposes a single long-lived shell session. Use the execution policy
to match your deployment's security posture:

- `HostExecutionPolicy` – full host access; best for trusted environments where the
  agent already runs inside a container or VM that provides isolation.
- `CodexSandboxExecutionPolicy` – reuses the Codex CLI sandbox for additional
  syscall/filesystem restrictions when the CLI is available.
- `DockerExecutionPolicy` – launches a separate Docker container for each agent run,
  providing harder isolation, optional read-only root filesystems, and user
  remapping.

When no policy is provided the middleware defaults to `HostExecutionPolicy`.](/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware)


