<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/message -->

Modulev1.2.21 (latest)●Since v0.3

# message

Message prompt templates.

## Functions

[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-core/utils/interactive_env/is_interactive_env)

## Classes

[class

Serializable

Serializable base class.

This class is used to serialize objects to JSON.

It relies on the following methods and properties:

- [`is_lc_serializable`](/python/langchain-core/load/serializable/Serializable/is_lc_serializable): Is this class serializable?

  By design, even if a class inherits from `Serializable`, it is not serializable
  by default. This is to prevent accidental serialization of objects that should
  not be serialized.
- [`get_lc_namespace`](/python/langchain-core/load/serializable/Serializable/get_lc_namespace): Get the namespace of the LangChain object.

  During deserialization, this namespace is used to identify
  the correct class to instantiate.

  Please see the `Reviver` class in `langchain_core.load.load` for more details.

  During deserialization an additional mapping is handle classes that have moved
  or been renamed across package versions.
- [`lc_secrets`](/python/langchain-core/load/serializable/Serializable/lc_secrets): A map of constructor argument names to secret ids.
- [`lc_attributes`](/python/langchain-core/load/serializable/Serializable/lc_attributes): List of additional attribute names that should be included
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

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
```](/python/langchain-core/prompts/chat/ChatPromptTemplate)[class

BaseMessagePromptTemplate

Base class for message prompt templates.](/python/langchain-core/prompts/message/BaseMessagePromptTemplate)


