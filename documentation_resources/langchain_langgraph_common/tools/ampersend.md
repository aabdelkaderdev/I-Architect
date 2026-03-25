<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/ampersend -->

[Ampersend](https://ampersend.ai) enables LangChain agents to pay for and use remote AI agent services. Payments are handled transparently via the [x402](https://www.x402.org/) protocol, with [A2A](https://google.github.io/A2A/) as the communication layer.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | JS support | Version |
| --- | --- | --- | --- | --- |
| A2AToolkit | `langchain-ampersend` | ❌ | ❌ |  |

### [​](#tool-features) Tool features

1. **a2a\_get\_agent\_details** - Get capabilities of the remote agent
2. **a2a\_send\_message** - Send messages to the remote agent (payments handled automatically)

### [​](#key-features) Key features

- **Spend controls**: Pluggable payment authorization with limits and policies
- **Transparent payments**: x402 protocol handles payment negotiation automatically

---

## [​](#setup) Setup

### [​](#installation) Installation

Install the `langchain-ampersend` package:

pip

uv

Copy

```
pip install -U langchain-ampersend
```

### [​](#credentials) Credentials

The toolkit requires a session key and smart account address, which you can obtain from the [Ampersend dashboard](https://app.ampersend.ai).

Set up credentials

Copy

```
import os

SESSION_KEY = os.environ.get("AMPERSEND_SESSION_KEY")  # 0x...
SMART_ACCOUNT_ADDRESS = os.environ.get("AMPERSEND_SMART_ACCOUNT_ADDRESS")  # 0x...
```

---

## [​](#instantiation) Instantiation

Initialize toolkit

Copy

```
from langchain_ampersend import (
    A2AToolkit,
    AmpersendTreasurer,
    ApiClient,
    ApiClientOptions,
    SmartAccountConfig,
    SmartAccountWallet,
)

# Setup wallet
wallet = SmartAccountWallet(
    config=SmartAccountConfig(
        session_key=SESSION_KEY,
        smart_account_address=SMART_ACCOUNT_ADDRESS,
    )
)

# Setup treasurer
treasurer = AmpersendTreasurer(
    api_client=ApiClient(
        options=ApiClientOptions(
            base_url="https://api.ampersend.ai",
            session_key_private_key=SESSION_KEY,
        )
    ),
    wallet=wallet,
)

# Create toolkit
toolkit = A2AToolkit(
    remote_agent_url="https://agent.example.com",
    treasurer=treasurer,
)

await toolkit.initialize()
```

---

## [​](#invocation) Invocation

Send a message to the remote agent:

Send message

Copy

```
tools = toolkit.get_tools()
send_tool = tools[1]  # a2a_send_message
response = await send_tool.ainvoke({"message": "Analyze the sales trends in Q4"})
print(response)
```

---

## [​](#use-within-an-agent) Use within an agent

Create agent

Copy

```
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

# Initialize the LLM
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

# Get tools from the toolkit
tools = toolkit.get_tools()

# Create the agent
agent = create_agent(llm, tools)
```

Example usage:

Run agent

Copy

```
result = await agent.ainvoke({
    "messages": [("user", "What can this agent do, and then ask it to analyze recent trends")]
})

# The agent will call the remote agent and handle payments automatically
```

---

## [​](#how-payments-work) How payments work

When the remote agent requires payment (HTTP 402), the toolkit:

1. Receives the payment requirement
2. Calls the treasurer to authorize the payment
3. Signs the payment with the configured wallet
4. Retries the request with the payment attached

This is transparent to your LangChain agent.
The `AmpersendTreasurer` provides managed payment sessions with spend limits and analytics. Alternative treasurer implementations are available in `ampersend_sdk`.

---

## [​](#api-reference) API reference

- [Ampersend Documentation](https://docs.ampersend.ai)
- [x402 Protocol Specification](https://www.x402.org/)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/ampersend.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.