<!-- Source: https://reference.langchain.com/python/langchain/agents/factory/DYNAMIC_TOOL_ERROR_TEMPLATE -->

Attributev1.2.13 (latest)●Since v1.2

# DYNAMIC\_TOOL\_ERROR\_TEMPLATE


```
DYNAMIC_TOOL_ERROR_TEMPLATE = '\nMiddleware added tools that the agent doesn\'t know how to execute.\n\nUnknown tools: {unknown_tool_names}\nRegistered tools: {available_tool_names}\n\nThis happens when middleware modifies `request.tools` in `wrap_model_call` to include\ntools that weren\'t passed to `create_agent(
  )`.\n\nHow to fix this:\n\nOption 1: Register tools at agent creation (recommended for most cases)\n    Pass the tools to `create_agent(tools=[...])` or set them on `middleware.tools`.\n    This makes tools available for every agent invocation.\n\nOption 2: Handle dynamic tools in middleware (for tools created at runtime)\n    Implement `wrap_tool_call` to execute tools that are added dynamically:\n\n    class MyMiddleware(AgentMiddleware):\n        def wrap_tool_call(self,
  request,
  handler):\n            if request.tool_call["name"] == "dynamic_tool":\n                # Execute the dynamic tool yourself or override with tool instance\n                return handler(request.override(tool=my_dynamic_tool))\n            return handler(request)\n'.strip(
)
```


