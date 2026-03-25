<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/EXAMPLE_INPUT -->

Attributev1.2.13 (latest)●Since v1.0

# EXAMPLE\_INPUT


```
EXAMPLE_INPUT = "An AI language model has been given access to the following set of tools to help answer a user's question.\n\nThe tools given to the AI model are:\n[TOOL_DESCRIPTIONS]\nTool 1:\nName: Search\nDescription: useful for when you need to ask with search\n\nTool 2:\nName: Lookup\nDescription: useful for when you need to ask with lookup\n\nTool 3:\nName: Calculator\nDescription: useful for doing calculations\n\nTool 4:\nName: Search the Web (
  SerpAPI)\nDescription: useful for when you need to answer questions about current events\n[END_TOOL_DESCRIPTIONS]\n\nThe question the human asked the AI model was: If laid the Statue of Liberty end to end, how many times would it stretch across the United States?\n\nThe AI language model decided to use the following set of tools to answer the question:\n[AGENT_TRAJECTORY]\nStep 1:\nTool used: Search the Web (SerpAPI)\nTool input: If laid the Statue of Liberty end to end, how many times would it stretch across the United States?\nTool output: The Statue of Liberty was given to the United States by France, as a symbol of the two countries' friendship. It was erected atop an American-designed ...\n[END_AGENT_TRAJECTORY]\n\n[RESPONSE]\nThe AI language model's final answer to the question was: There are different ways to measure the length of the United States, but if we use the distance between the Statue of Liberty and the westernmost point of the contiguous United States (Cape Alava,
  Washington), which is approximately 2,857 miles (4,
  596 km), and assume that the Statue of Liberty is 305 feet (93 meters
) tall, then the statue would stretch across the United States approximately 17.5 times if laid end to end.\n[END_RESPONSE]\n\nLet's to do a detailed evaluation of the AI language model's answer step by step.\n\nWe consider the following criteria before giving a score from 1 to 5:\n\ni. Is the final answer helpful?\nii. Does the AI language use a logical sequence of tools to answer the question?\niii. Does the AI language model use the tools in a helpful way?\niv. Does the AI language model use too many steps to answer the question?\nv. Are the appropriate tools used to answer the question?"
```


