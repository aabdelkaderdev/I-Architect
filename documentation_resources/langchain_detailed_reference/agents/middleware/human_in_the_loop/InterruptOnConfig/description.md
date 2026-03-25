<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig/description -->

Attributev1.2.13 (latest)●Since v1.0

# description

The description attached to the request for human input.

Can be either:

- A static string describing the approval request
- A callable that dynamically generates the description based on agent state,
  runtime, and tool call information


```
description: NotRequired[str | _DescriptionFactory]
```

**Example:**

```
# Static string description
config = ToolConfig(
    allowed_decisions=["approve", "reject"],
    description="Please review this tool execution"
)

# Dynamic callable description
def format_tool_description(
    tool_call: ToolCall,
    state: AgentState,
    runtime: Runtime[ContextT]
) -> str:
    import json
    return (
        f"Tool: {tool_call['name']}\n"
        f"Arguments:\n{json.dumps(tool_call['args'], indent=2)}"
    )

config = InterruptOnConfig(
    allowed_decisions=["approve", "edit", "reject"],
    description=format_tool_description
)
```


