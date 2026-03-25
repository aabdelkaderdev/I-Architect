<!-- Source: https://docs.langchain.com/oss/python/langchain/streaming/frontend -->

Build rich, interactive frontends for agents created with `createAgent`. These patterns cover everything from basic message rendering to advanced workflows like human-in-the-loop approval and time travel debugging.

## [​](#architecture) Architecture

Every pattern follows the same architecture: a `createAgent` backend streams state to a frontend via the `useStream` hook.

On the backend, `createAgent` produces a compiled LangGraph graph that exposes a streaming API. On the frontend, the `useStream` hook connects to that API and provides reactive state — messages, tool calls, interrupts, history, and more — that you render with any framework.

agent.py

types.ts

Chat.tsx

Copy

```
from langchain import create_agent
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather, search_web],
    checkpointer=MemorySaver(),
)
```

`useStream` is available for React, Vue, Svelte, and Angular:

Copy

```
import { useStream } from "@langchain/react";   // React
import { useStream } from "@langchain/vue";      // Vue
import { useStream } from "@langchain/svelte";   // Svelte
import { useStream } from "@langchain/angular";  // Angular
```

## [​](#patterns) Patterns

### [​](#render-messages-and-output) Render messages and output

## Markdown messages

Parse and render streamed markdown with proper formatting and code highlighting.

## Structured output

Render typed agent responses as custom UI components instead of plain text.

## Reasoning tokens

Display model thinking processes in collapsible blocks.

## Generative UI

Render AI-generated user interfaces from natural language prompts using json-render.

### [​](#display-agent-actions) Display agent actions

## Tool calling

Show tool calls as rich, type-safe UI cards with loading and error states.

## Human-in-the-loop

Pause the agent for human review with approve, reject, and edit workflows.

### [​](#manage-conversations) Manage conversations

## Branching chat

Edit messages, regenerate responses, and navigate conversation branches.

## Message queues

Queue multiple messages while the agent processes them sequentially.

### [​](#advanced-streaming) Advanced streaming

## Join & rejoin streams

Disconnect from and reconnect to running agent streams without losing progress.

## Time travel

Inspect, navigate, and resume from any checkpoint in the conversation history.

## [​](#integrations) Integrations

`useStream` is UI-agnostic. Use it to any component library or generative UI framework.

## AI Elements

Composable shadcn/ui components for AI chat: `Conversation`, `Message`, `Tool`, `Reasoning`.

## assistant-ui

Headless React framework with built-in thread management, branching, and attachment support.

## OpenUI

Generative UI library for data-rich reports and dashboards using the openui-lang component DSL.

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.