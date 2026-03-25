<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/slack -->

This will help you get started with the Slack [toolkit](/oss/python/integrations/tools/slack). For detailed documentation of all SlackToolkit features and configurations head to the [API reference](https://python.langchain.com/api_reference/community/agent_toolkits/langchain_community.agent_toolkits.slack.toolkit.SlackToolkit.html).

## [​](#setup) Setup

To use this toolkit, you will need to get a token as explained in the [Slack API docs](https://api.slack.com/tutorials/tracks/getting-a-token). Once you’ve received a SLACK\_USER\_TOKEN, you can input it as an environment variable below.

Copy

```
import getpass
import os

if not os.getenv("SLACK_USER_TOKEN"):
    os.environ["SLACK_USER_TOKEN"] = getpass.getpass("Enter your Slack user token: ")
```

To enable automated tracing of individual tools, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

This toolkit lives in the `langchain-community` package. We will also need the Slack SDK:

Copy

```
pip install -qU langchain-community slack_sdk
```

Optionally, we can install beautifulsoup4 to assist in parsing HTML messages:

Copy

```
pip install -qU beautifulsoup4 # This is optional but is useful for parsing HTML messages
```

## [​](#instantiation) Instantiation

Now we can instantiate our toolkit:

Copy

```
from langchain_community.agent_toolkits import SlackToolkit

toolkit = SlackToolkit()
```

## [​](#tools) Tools

View available tools:

Copy

```
tools = toolkit.get_tools()

tools
```

Copy

```
[SlackGetChannel(client=<slack_sdk.web.client.WebClient object at 0x113caa8c0>),
 SlackGetMessage(client=<slack_sdk.web.client.WebClient object at 0x113caa4d0>),
 SlackScheduleMessage(client=<slack_sdk.web.client.WebClient object at 0x113caa440>),
 SlackSendMessage(client=<slack_sdk.web.client.WebClient object at 0x113caa410>)]
```

This toolkit loads:

- [SlackGetChannel](https://python.langchain.com/api_reference/community/tools/langchain_community.tools.slack.get_channel.SlackGetChannel.html)
- [SlackGetMessage](https://python.langchain.com/api_reference/community/tools/langchain_community.tools.slack.get_message.SlackGetMessage.html)
- [SlackScheduleMessage](https://python.langchain.com/api_reference/community/tools/langchain_community.tools.slack.schedule_message.SlackScheduleMessage.html)
- [SlackSendMessage](https://python.langchain.com/api_reference/community/tools/langchain_community.tools.slack.send_message.SlackSendMessage.html)

## [​](#use-within-an-agent) Use within an agent

Let’s equip an agent with the Slack toolkit and query for information about a channel.

Copy

```
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-4.1-mini")

agent_executor = create_agent(model, tools)
```

Copy

```
example_query = "When was the #general channel created?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    message = event["messages"][-1]
    if message.type != "tool":  # mask sensitive information
        event["messages"][-1].pretty_print()
```

Copy

```
================================ Human Message =================================

When was the #general channel created?
================================== Ai Message ==================================
Tool Calls:
  get_channelid_name_dict (call_NXDkALjoOx97uF1v0CoZTqtJ)
 Call ID: call_NXDkALjoOx97uF1v0CoZTqtJ
  Args:
================================== Ai Message ==================================

The #general channel was created on timestamp 1671043305.
```

Copy

```
example_query = "Send a friendly greeting to channel C072Q1LP4QM."

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    message = event["messages"][-1]
    if message.type != "tool":  # mask sensitive information
        event["messages"][-1].pretty_print()
```

Copy

```
================================ Human Message =================================

Send a friendly greeting to channel C072Q1LP4QM.
================================== Ai Message ==================================
Tool Calls:
  send_message (call_xQxpv4wFeAZNZgSBJRIuaizi)
 Call ID: call_xQxpv4wFeAZNZgSBJRIuaizi
  Args:
    message: Hello! Have a great day!
    channel: C072Q1LP4QM
================================== Ai Message ==================================

I have sent a friendly greeting to the channel C072Q1LP4QM.
```

---

## [​](#api-reference) API reference

For detailed documentation of all `SlackToolkit` features and configurations head to the [API reference](https://python.langchain.com/api_reference/community/agent_toolkits/langchain_community.agent_toolkits.slack.toolkit.SlackToolkit.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/slack.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.