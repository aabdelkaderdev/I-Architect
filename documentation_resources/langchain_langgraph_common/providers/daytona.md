<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/daytona -->

[Daytona](https://daytona.io) provides fast-starting sandbox environments with multi-language support. See the [Daytona docs](https://www.daytona.io/docs) for signup, authentication, and platform details.

## [​](#installation) Installation

pip

uv

Copy

```
pip install langchain-daytona
```

## [​](#create-a-sandbox-backend) Create a sandbox backend

In Python, you create the sandbox using the provider SDK, then wrap it with the [deepagents backend](/oss/python/deepagents/backends).

Copy

```
from daytona import Daytona

from langchain_daytona import DaytonaSandbox

sandbox = Daytona().create()
backend = DaytonaSandbox(sandbox=sandbox)

result = backend.execute("echo hello")
print(result.output)
```

## [​](#use-with-deepagents) Use with deepagents

Copy

```
from daytona import Daytona
from langchain_anthropic import ChatAnthropic

from deepagents import create_deep_agent
from langchain_daytona import DaytonaSandbox

sandbox = Daytona().create()
backend = DaytonaSandbox(sandbox=sandbox)

agent = create_deep_agent(
    model=ChatAnthropic(model="claude-sonnet-4-20250514"),
    system_prompt="You are a coding assistant with sandbox access.",
    backend=backend,
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "Create a hello world Python script and run it"}
        ]
    }
)
```

## [​](#cleanup) Cleanup

You are responsible for managing the sandbox lifecycle via the Daytona SDK.
When you are done, stop or destroy the sandbox.
See also: [Sandboxes](/oss/python/deepagents/sandboxes).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/daytona.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.