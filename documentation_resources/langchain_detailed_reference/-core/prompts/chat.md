<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat -->

Modulev1.2.21 (latest)●Since v0.1

# chat

Chat prompt template.

## Attributes

[attribute

AnyMessage

A type representing any defined `Message` or `MessageChunk` type.](/python/langchain-core/messages/utils/AnyMessage)[attribute

PromptTemplateFormat: Literal['f-string', 'mustache', 'jinja2']](/python/langchain-core/prompts/string/PromptTemplateFormat)[attribute

MessagePromptTemplateT

Type variable for message prompt templates.](/python/langchain-core/prompts/chat/MessagePromptTemplateT)

## Functions

[function

convert\_to\_messages

Convert a sequence of messages to a list of messages.](/python/langchain-core/messages/utils/convert_to_messages)[function

get\_msg\_title\_repr

Get a title representation for a message.](/python/langchain-core/messages/base/get_msg_title_repr)[function

get\_template\_variables

Get the variables from the template.](/python/langchain-core/prompts/string/get_template_variables)[function

get\_colored\_text

Get colored text.](/python/langchain-core/utils/input/get_colored_text)[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-core/utils/interactive_env/is_interactive_env)

## Classes

[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

ChatMessage

Message that can be assigned an arbitrary speaker (i.e. role).](/python/langchain-core/messages/chat/ChatMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

SystemMessage

Message for priming AI behavior.

The system message is usually passed in as the first of a sequence
of input messages.](/python/langchain-core/messages/system/SystemMessage)[class

ChatPromptValue

Chat prompt value.

A type of a prompt value that is built from messages.](/python/langchain-core/prompt_values/ChatPromptValue)[class

ImageURL

Image URL for multimodal model inputs (OpenAI format).

Represents the inner `image_url` object in OpenAI's Chat Completion API format. This
is used by `ImagePromptTemplate` and `ChatPromptTemplate`.](/python/langchain-core/prompt_values/ImageURL)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)[class

DictPromptTemplate

Template represented by a dictionary.

Recognizes variables in f-string or mustache formatted string dict values.

Does NOT recognize variables in dict keys. Applies recursively.](/python/langchain-core/prompts/dict/DictPromptTemplate)[class

ImagePromptTemplate

Image prompt template for a multimodal model.](/python/langchain-core/prompts/image/ImagePromptTemplate)[class

BaseMessagePromptTemplate

Base class for message prompt templates.](/python/langchain-core/prompts/message/BaseMessagePromptTemplate)[class

PromptTemplate

Prompt template for a language model.

A prompt template consists of a string template. It accepts a set of parameters
from the user that can be used to generate a prompt for a language model.

The template can be formatted using either f-strings (default), jinja2, or mustache
syntax.

Security

Prefer using `template_format='f-string'` instead of `template_format='jinja2'`,
or make sure to NEVER accept jinja2 templates from untrusted sources as they may
lead to arbitrary Python code execution.

As of LangChain 0.0.329, Jinja2 templates will be rendered using Jinja2's
SandboxedEnvironment by default. This sand-boxing should be treated as a
best-effort approach rather than a guarantee of security, as it is an opt-out
rather than opt-in approach.

Despite the sandboxing, we recommend to never use jinja2 templates from
untrusted sources.](/python/langchain-core/prompts/prompt/PromptTemplate)[class

StringPromptTemplate

String prompt that exposes the format method, returning a prompt.](/python/langchain-core/prompts/string/StringPromptTemplate)[class

MessagesPlaceholder

Prompt template that assumes variable is already list of messages.

A placeholder which can be used to pass in a list of messages.

Direct usage

```
from langchain_core.prompts import MessagesPlaceholder

prompt = MessagesPlaceholder("history")
prompt.format_messages()  # raises KeyError

prompt = MessagesPlaceholder("history", optional=True)
prompt.format_messages()  # returns empty list []

prompt.format_messages(
    history=[
        ("system", "You are an AI assistant."),
        ("human", "Hello!"),
    ]
)
# -> [
#     SystemMessage(content="You are an AI assistant."),
#     HumanMessage(content="Hello!"),
# ]
```

Building a prompt with chat history

```
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)
prompt.invoke(
    {
        "history": [("human", "what's 5 + 2"), ("ai", "5 + 2 is 7")],
        "question": "now multiply that by 4",
    }
)
# -> ChatPromptValue(messages=[
#     SystemMessage(content="You are a helpful assistant."),
#     HumanMessage(content="what's 5 + 2"),
#     AIMessage(content="5 + 2 is 7"),
#     HumanMessage(content="now multiply that by 4"),
# ])
```

Limiting the number of messages

```
from langchain_core.prompts import MessagesPlaceholder

prompt = MessagesPlaceholder("history", n_messages=1)

prompt.format_messages(
    history=[
        ("system", "You are an AI assistant."),
        ("human", "Hello!"),
    ]
)
# -> [
#     HumanMessage(content="Hello!"),
# ]
```](/python/langchain-core/prompts/chat/MessagesPlaceholder)[class

BaseStringMessagePromptTemplate

Base class for message prompt templates that use a string prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate)[class

ChatMessagePromptTemplate

Chat message prompt template.](/python/langchain-core/prompts/chat/ChatMessagePromptTemplate)[class

HumanMessagePromptTemplate

Human message prompt template.

This is a message sent from the user.](/python/langchain-core/prompts/chat/HumanMessagePromptTemplate)[class

AIMessagePromptTemplate

AI message prompt template.

This is a message sent from the AI.](/python/langchain-core/prompts/chat/AIMessagePromptTemplate)[class

SystemMessagePromptTemplate

System message prompt template.

This is a message that is not sent to the user.](/python/langchain-core/prompts/chat/SystemMessagePromptTemplate)[class

BaseChatPromptTemplate

Base class for chat prompt templates.](/python/langchain-core/prompts/chat/BaseChatPromptTemplate)[class

ChatPromptTemplate

Prompt template for chat models.

Use to create flexible templated prompts for chat models.

Example

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?",
    }
)
# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot. Your name is Bob.'),
#        HumanMessage(content='Hello, how are you doing?'),
#        AIMessage(content="I'm doing well, thanks!"),
#        HumanMessage(content='What is your name?')
#    ]
# )
```

Messages Placeholder

```
# In addition to Human/AI/Tool/Function messages,
# you can initialize the template with a MessagesPlaceholder
# either using the class directly or with the shorthand tuple syntax:

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot."),
        # Means the template will receive an optional list of messages under
        # the "conversation" key
        ("placeholder", "{conversation}"),
        # Equivalently:
        # MessagesPlaceholder(variable_name="conversation", optional=True)
    ]
)

prompt_value = template.invoke(
    {
        "conversation": [
            ("human", "Hi!"),
            ("ai", "How can I assist you today?"),
            ("human", "Can you make me an ice cream sundae?"),
            ("ai", "No."),
        ]
    }
)

# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot.'),
#        HumanMessage(content='Hi!'),
#        AIMessage(content='How can I assist you today?'),
#        HumanMessage(content='Can you make me an ice cream sundae?'),
#        AIMessage(content='No.'),
#    ]
# )
```

Single-variable template

If your prompt has only a single input variable (i.e., one instance of
`'{variable_nams}'`), and you invoke the template with a non-dict object, the
prompt template will inject the provided argument into that variable location.

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is Carl."),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke("Hello, there!")
# Equivalent to
# prompt_value = template.invoke({"user_input": "Hello, there!"})

# Output:
#  ChatPromptValue(
#     messages=[
#         SystemMessage(content='You are a helpful AI bot. Your name is Carl.'),
#         HumanMessage(content='Hello, there!'),
#     ]
# )
```](/python/langchain-core/prompts/chat/ChatPromptTemplate)

## Type Aliases

[typeAlias

MessageLike](/python/langchain-core/prompts/chat/MessageLike)[typeAlias

MessageLikeRepresentation](/python/langchain-core/prompts/chat/MessageLikeRepresentation)


