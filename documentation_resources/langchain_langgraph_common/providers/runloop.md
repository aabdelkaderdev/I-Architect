<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/runloop -->

[Runloop](https://www.runloop.ai/) provides disposable devboxes for running code in isolated environments. See the [Runloop docs](https://docs.runloop.ai/) for signup, authentication, and platform details.

## [​](#installation) Installation

pip

uv

Copy

```
pip install langchain-runloop
```

## [​](#create-a-sandbox-backend) Create a sandbox backend

In Python, you create the devbox using the provider SDK, then wrap it with the [deepagents backend](/oss/python/deepagents/backends).

Copy

```
from runloop_api_client import RunloopSDK

from langchain_runloop import RunloopSandbox

api_key = "..."
client = RunloopSDK(bearer_token=api_key)

devbox = client.devbox.create()
backend = RunloopSandbox(devbox=devbox)

try:
    result = backend.execute("echo hello")
    print(result.output)
finally:
    devbox.shutdown()
```

## [​](#use-with-deepagents) Use with deepagents

Copy

```
from runloop_api_client import RunloopSDK
from langchain_anthropic import ChatAnthropic

from deepagents import create_deep_agent
from langchain_runloop import RunloopSandbox

api_key = "..."
client = RunloopSDK(bearer_token=api_key)

devbox = client.devbox.create()
backend = RunloopSandbox(devbox=devbox)

agent = create_deep_agent(
    model=ChatAnthropic(model="claude-sonnet-4-20250514"),
    system_prompt="You are a coding assistant with sandbox access.",
    backend=backend,
)

try:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Create a small Python project and run tests"}]}
    )
finally:
    devbox.shutdown()
```

## [​](#cleanup) Cleanup

Always shut down devboxes when you are done to avoid ongoing resource usage.
See also: [Sandboxes](/oss/python/deepagents/sandboxes).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/runloop.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.