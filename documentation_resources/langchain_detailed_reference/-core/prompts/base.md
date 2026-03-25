<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base class for prompt templates.

## Attributes

[attribute

FormatOutputType](/python/langchain-core/prompts/base/FormatOutputType)

## Functions

[function

create\_message

Create a message with a link to the LangChain troubleshooting guide.](/python/langchain-core/exceptions/create_message)[function

dumpd

Return a dict representation of an object.](/python/langchain-core/load/dump/dumpd)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.](/python/langchain-core/utils/pydantic/create_model_v2)[function

format\_document

Format a document into a string based on a prompt template.

First, this pulls information from the document from two sources:

1. `page_content`: This takes the information from the `document.page_content` and
   assigns it to a variable named `page_content`.
2. `metadata`: This takes information from `document.metadata` and assigns it to
   variables of the same name.

Those variables are then passed into the `prompt` to produce a formatted string.](/python/langchain-core/prompts/base/format_document)[function

aformat\_document

Async format a document into a string based on a prompt template.

First, this pulls information from the document from two sources:

1. `page_content`: This takes the information from the `document.page_content` and
   assigns it to a variable named `page_content`.
2. `metadata`: This takes information from `document.metadata` and assigns it to
   variables of the same name.

Those variables are then passed into the `prompt` to produce a formatted string.](/python/langchain-core/prompts/base/aformat_document)

## Classes

[class

ErrorCode

Error codes.](/python/langchain-core/exceptions/ErrorCode)[class

BaseOutputParser

Base class to parse the output of an LLM call.

Output parsers help structure language model responses.](/python/langchain-core/output_parsers/base/BaseOutputParser)[class

ChatPromptValueConcrete

Chat prompt value which explicitly lists out the message types it accepts.

For use in external schemas.](/python/langchain-core/prompt_values/ChatPromptValueConcrete)[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

StringPromptValue

String prompt value.](/python/langchain-core/prompt_values/StringPromptValue)[class

RunnableConfig

Configuration for a `Runnable`.

Note

Custom values

The `TypedDict` has `total=False` set intentionally to:

- Allow partial configs to be created and merged together via `merge_configs`
- Support config propagation from parent to child runnables via
  `var_child_runnable_config` (a `ContextVar` that automatically passes
  config down the call stack without explicit parameter passing), where
  configs are merged rather than replaced

Example

```
# Parent sets tags
chain.invoke(input, config={"tags": ["parent"]})
# Child automatically inherits and can add:
# ensure_config({"tags": ["child"]}) -> {"tags": ["parent", "child"]}
```](/python/langchain-core/runnables/config/RunnableConfig)[class

RunnableSerializable

Runnable that can be serialized to JSON.](/python/langchain-core/runnables/base/RunnableSerializable)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)


