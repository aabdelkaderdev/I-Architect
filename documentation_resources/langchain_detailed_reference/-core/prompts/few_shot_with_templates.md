<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/few_shot_with_templates -->

Modulev1.2.21 (latest)●Since v0.1

# few\_shot\_with\_templates

Prompt template that contains few shot examples.

## Attributes

[attribute

DEFAULT\_FORMATTER\_MAPPING: dict[str, Callable[..., str]]](/python/langchain-core/prompts/string/DEFAULT_FORMATTER_MAPPING)[attribute

PromptTemplateFormat: Literal['f-string', 'mustache', 'jinja2']](/python/langchain-core/prompts/string/PromptTemplateFormat)

## Classes

[class

BaseExampleSelector

Interface for selecting examples to include in prompts.](/python/langchain-core/example_selectors/base/BaseExampleSelector)[class

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

FewShotPromptWithTemplates

Prompt template that contains few shot examples.](/python/langchain-core/prompts/few_shot_with_templates/FewShotPromptWithTemplates)


