<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/image -->

Modulev1.2.21 (latest)●Since v0.1

# image

Image prompt template for a multimodal model.

## Attributes

[attribute

DEFAULT\_FORMATTER\_MAPPING: dict[str, Callable[..., str]]](/python/langchain-core/prompts/string/DEFAULT_FORMATTER_MAPPING)[attribute

PromptTemplateFormat: Literal['f-string', 'mustache', 'jinja2']](/python/langchain-core/prompts/string/PromptTemplateFormat)

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

ImagePromptValue

Image prompt value.](/python/langchain-core/prompt_values/ImagePromptValue)[class

ImageURL

Image URL for multimodal model inputs (OpenAI format).

Represents the inner `image_url` object in OpenAI's Chat Completion API format. This
is used by `ImagePromptTemplate` and `ChatPromptTemplate`.](/python/langchain-core/prompt_values/ImageURL)[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)[class

ImagePromptTemplate

Image prompt template for a multimodal model.](/python/langchain-core/prompts/image/ImagePromptTemplate)


