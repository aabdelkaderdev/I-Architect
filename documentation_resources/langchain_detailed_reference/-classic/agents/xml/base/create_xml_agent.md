<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/xml/base/create_xml_agent -->

Functionv1.2.13 (latest)●Since v1.0

# create\_xml\_agent

Create an agent that uses XML to format its logic.


```
create_xml_agent(
  llm: BaseLanguageModel,
  tools: Sequence[BaseTool],
  prompt: BasePromptTemplate,
  tools_renderer: ToolsRenderer = render_text_description,
  *,
  stop_sequence: bool | list[str] = True
) -> Runnable
```

**Example:**

```
from langchain_classic import hub
from langchain_anthropic import ChatAnthropic
from langchain_classic.agents import AgentExecutor, create_xml_agent

prompt = hub.pull("hwchase17/xml-agent-convo")
model = ChatAnthropic(model="claude-3-haiku-20240307")
tools = ...

agent = create_xml_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_executor.invoke({"input": "hi"})

# Use with chat history
from langchain_core.messages import AIMessage, HumanMessage

agent_executor.invoke(
    {
        "input": "what's my name?",
        # Notice that chat_history is a string
        # since this prompt is aimed at LLMs, not chat models
        "chat_history": "Human: My name is Bob\nAI: Hello Bob!",
    }
)
```

Prompt:

The prompt must have input keys:
\* `tools`: contains descriptions for each tool.
\* `agent_scratchpad`: contains previous agent actions and tool outputs as
an XML string.

Here's an example:

```
from langchain_core.prompts import PromptTemplate

template = '''You are a helpful assistant. Help the user answer any questions.

You have access to the following tools:

{tools}

In order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags. You will then get back a response in the form <observation></observation>
For example, if you have a tool called 'search' that could run a google search, in order to search for the weather in SF you would respond:

<tool>search</tool><tool_input>weather in SF</tool_input>
<observation>64 degrees</observation>

When you are done, respond with a final answer between <final_answer></final_answer>. For example:

<final_answer>The weather in SF is 64 degrees</final_answer>

Begin!

Previous Conversation:
{chat_history}

Question: {input}
{agent_scratchpad}'''
prompt = PromptTemplate.from_template(template)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | LLM to use as the agent. |
| `tools`\* | `Sequence[BaseTool]` | Tools this agent has access to. |
| `prompt`\* | `BasePromptTemplate` | The prompt to use, must have input keys `tools`: contains descriptions for each tool. `agent_scratchpad`: contains previous agent actions and tool outputs. |
| `tools_renderer` | `ToolsRenderer` | Default:`render_text_description`  This controls how the tools are converted into a string and then passed into the LLM. |
| `stop_sequence` | `bool | list[str]` | Default:`True`  bool or list of str. If `True`, adds a stop token of "</tool\_input>" to avoid hallucinates. If `False`, does not add a stop token. If a list of str, uses the provided list as the stop tokens.  You may to set this to False if the LLM you are using does not support stop sequences. |


