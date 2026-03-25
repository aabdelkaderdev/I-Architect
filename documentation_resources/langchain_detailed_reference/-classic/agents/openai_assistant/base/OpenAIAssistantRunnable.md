<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable -->

Classv1.2.13 (latest)●Since v1.0

# OpenAIAssistantRunnable


```
OpenAIAssistantRunnable()
```

## Bases

`RunnableSerializable[dict, OutputType]`

## Attributes

## Methods

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)[Amodel\_config](/python/langchain-core/runnables/base/RunnableSerializable/model_config)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)



M

configurable\_alternatives

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

client: Any

`OpenAI` or `AzureOpenAI` client.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/client)

[attribute

async\_client: Any

`OpenAI` or `AzureOpenAI` async client.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/async_client)

[attribute

assistant\_id: str

OpenAI assistant id.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/assistant_id)

[attribute

check\_every\_ms: float

Frequency with which to check run progress in ms.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/check_every_ms)

[attribute

as\_agent: bool

Use as a LangChain agent, compatible with the `AgentExecutor`.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/as_agent)

[method

create\_assistant

Create an OpenAI Assistant and instantiate the Runnable.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/create_assistant)

[method

invoke

Invoke assistant.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/invoke)

[method

acreate\_assistant

Async create an AsyncOpenAI Assistant and instantiate the Runnable.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/acreate_assistant)

[method

ainvoke

Async invoke assistant.](/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/ainvoke)

Run an OpenAI Assistant.

**Example using OpenAI tools:**

```
from langchain_experimental.openai_assistant import OpenAIAssistantRunnable

interpreter_assistant = OpenAIAssistantRunnable.create_assistant(
    name="langchain assistant",
    instructions="You are a personal math tutor. "
    "Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)
output = interpreter_assistant.invoke(
    {"content": "What's 10 - 4 raised to the 2.7"}
)
```

**Example using custom tools and AgentExecutor:**

```
from langchain_experimental.openai_assistant import OpenAIAssistantRunnable
from langchain_classic.agents import AgentExecutor
from langchain_classic.tools import E2BDataAnalysisTool

tools = [E2BDataAnalysisTool(api_key="...")]
agent = OpenAIAssistantRunnable.create_assistant(
    name="langchain assistant e2b tool",
    instructions="You are a personal math tutor. "
    "Write and run code to answer math questions.",
    tools=tools,
    model="gpt-4-1106-preview",
    as_agent=True,
)

agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_executor.invoke({"content": "What's 10 - 4 raised to the 2.7"})
```

**Example using custom tools and custom execution:**

```
from langchain_experimental.openai_assistant import OpenAIAssistantRunnable
from langchain_classic.agents import AgentExecutor
from langchain_core.agents import AgentFinish
from langchain_classic.tools import E2BDataAnalysisTool

tools = [E2BDataAnalysisTool(api_key="...")]
agent = OpenAIAssistantRunnable.create_assistant(
    name="langchain assistant e2b tool",
    instructions="You are a personal math tutor. "
    "Write and run code to answer math questions.",
    tools=tools,
    model="gpt-4-1106-preview",
    as_agent=True,
)

def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            tool_outputs.append(
                {
                    "output": tool_output,
                    "tool_call_id": action.tool_call_id,
                }
            )
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id,
            }
        )

    return response

response = execute_agent(
    agent, tools, {"content": "What's 10 - 4 raised to the 2.7"}
)
next_response = execute_agent(
    agent,
    tools,
    {"content": "now add 17.241", "thread_id": response.thread_id},
)
```

M

get\_config\_jsonschema

[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)

[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)

[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)

[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)

[Mstream](/python/langchain-core/runnables/base/Runnable/stream)

[Mastream](/python/langchain-core/runnables/base/Runnable/astream)

[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)

[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)

[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)

[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)

[Mbind](/python/langchain-core/runnables/base/Runnable/bind)

[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)

[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)

[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)

[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)

[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)

[Mmap](/python/langchain-core/runnables/base/Runnable/map)

[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)

[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)