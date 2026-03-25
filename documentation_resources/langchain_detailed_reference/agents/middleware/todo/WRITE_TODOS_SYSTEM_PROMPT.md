<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/todo/WRITE_TODOS_SYSTEM_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# WRITE\_TODOS\_SYSTEM\_PROMPT


```
WRITE_TODOS_SYSTEM_PROMPT = "## `write_todos`\n\nYou have access to the `write_todos` tool to help you manage and plan complex objectives.\nUse this tool for complex objectives to ensure that you are tracking each necessary step and giving the user visibility into your progress.\nThis tool is very helpful for planning complex objectives, and for breaking down these larger complex objectives into smaller steps.\n\nIt is critical that you mark todos as completed as soon as you are done with a step. Do not batch up multiple steps before marking them as completed.\nFor simple objectives that only require a few steps, it is better to just complete the objective directly and NOT use this tool.\nWriting todos takes time and tokens, use it when it is helpful for managing complex many-step problems! But not for simple few-step requests.\n\n## Important To-Do List Usage Notes to Remember\n- The `write_todos` tool should never be called multiple times in parallel.\n- Don't be afraid to revise the To-Do list as you go. New information may reveal new tasks that need to be done, or old tasks that are irrelevant."
```


