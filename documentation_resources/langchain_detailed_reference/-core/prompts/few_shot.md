<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/few_shot -->

Modulev1.2.21 (latest)●Since v0.1

# few\_shot

Prompt template that contains few shot examples.

## Attributes

[attribute

DEFAULT\_FORMATTER\_MAPPING: dict[str, Callable[..., str]]](/python/langchain-core/prompts/string/DEFAULT_FORMATTER_MAPPING)

## Functions

[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)[function

check\_valid\_template

Check that template string is valid.](/python/langchain-core/prompts/string/check_valid_template)[function

get\_template\_variables

Get the variables from the template.](/python/langchain-core/prompts/string/get_template_variables)

## Classes

[class

BaseExampleSelector

Interface for selecting examples to include in prompts.](/python/langchain-core/example_selectors/base/BaseExampleSelector)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseChatPromptTemplate

Base class for chat prompt templates.](/python/langchain-core/prompts/chat/BaseChatPromptTemplate)[class

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

FewShotPromptTemplate

Prompt template that contains few shot examples.](/python/langchain-core/prompts/few_shot/FewShotPromptTemplate)[class

FewShotChatMessagePromptTemplate

Chat prompt template that supports few-shot examples.

The high level structure of produced by this prompt template is a list of messages
consisting of prefix message(s), example message(s), and suffix message(s).

This structure enables creating a conversation with intermediate examples like:

```
System: You are a helpful AI Assistant

Human: What is 2+2?

AI: 4

Human: What is 2+3?

AI: 5

Human: What is 4+4?
```

This prompt template can be used to generate a fixed list of examples or else to
dynamically select examples based on the input.](/python/langchain-core/prompts/few_shot/FewShotChatMessagePromptTemplate)


