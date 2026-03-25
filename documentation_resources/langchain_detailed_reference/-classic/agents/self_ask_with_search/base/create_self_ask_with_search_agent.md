<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/self_ask_with_search/base/create_self_ask_with_search_agent -->

Functionv1.2.13 (latest)●Since v1.0

# create\_self\_ask\_with\_search\_agent

Create an agent that uses self-ask with search prompting.


```
create_self_ask_with_search_agent(
  llm: BaseLanguageModel,
  tools: Sequence[BaseTool],
  prompt: BasePromptTemplate
) -> Runnable
```

Prompt:

The prompt must have input key `agent_scratchpad` which will
contain agent actions and tool outputs as a string.

Here's an example:

```
from langchain_core.prompts import PromptTemplate

template = '''Question: Who lived longer, Muhammad Ali or Alan Turing?
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali

Question: When was the founder of craigslist born?
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952

Question: Who was the maternal grandfather of George Washington?
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball

Question: Are both the directors of Jaws and Casino Royale from the same country?
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate answer: New Zealand.
So the final answer is: No

Question: {input}
Are followup questions needed here:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | LLM to use as the agent. |
| `tools`\* | `Sequence[BaseTool]` | List of tools. Should just be of length 1, with that tool having name `Intermediate Answer` |
| `prompt`\* | `BasePromptTemplate` | The prompt to use, must have input key `agent_scratchpad` which will contain agent actions and tool outputs. |


