<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/string -->

Modulev1.2.21 (latest)●Since v0.1

# string

`BasePrompt` schema definition.

## Attributes

[attribute

formatter](/python/langchain-core/utils/formatting/formatter)[attribute

PromptTemplateFormat: Literal['f-string', 'mustache', 'jinja2']](/python/langchain-core/prompts/string/PromptTemplateFormat)[attribute

Defs: dict[str, 'Defs']](/python/langchain-core/prompts/string/Defs)[attribute

DEFAULT\_FORMATTER\_MAPPING: dict[str, Callable[..., str]]](/python/langchain-core/prompts/string/DEFAULT_FORMATTER_MAPPING)[attribute

DEFAULT\_VALIDATOR\_MAPPING: dict[str, Callable]](/python/langchain-core/prompts/string/DEFAULT_VALIDATOR_MAPPING)

## Functions

[function

get\_colored\_text

Get colored text.](/python/langchain-core/utils/input/get_colored_text)[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-core/utils/interactive_env/is_interactive_env)[function

jinja2\_formatter

Format a template using jinja2.

Security

As of LangChain 0.0.329, this method uses Jinja2's `SandboxedEnvironment` by
default. However, this sandboxing should be treated as a best-effort approach
rather than a guarantee of security.

Do not accept jinja2 templates from untrusted sources as they may lead
to arbitrary Python code execution.

[More information.](https://jinja.palletsprojects.com/en/3.1.x/sandbox/)](/python/langchain-core/prompts/string/jinja2_formatter)[function

validate\_jinja2

Validate that the input variables are valid for the template.

Issues a warning if missing or extra variables are found.](/python/langchain-core/prompts/string/validate_jinja2)[function

mustache\_formatter

Format a template using mustache.](/python/langchain-core/prompts/string/mustache_formatter)[function

mustache\_template\_vars

Get the top-level variables from a mustache template.

For nested variables like `{{person.name}}`, only the top-level key (`person`) is
returned.](/python/langchain-core/prompts/string/mustache_template_vars)[function

mustache\_schema

Get the variables from a mustache template.](/python/langchain-core/prompts/string/mustache_schema)[function

check\_valid\_template

Check that template string is valid.](/python/langchain-core/prompts/string/check_valid_template)[function

get\_template\_variables

Get the variables from the template.](/python/langchain-core/prompts/string/get_template_variables)[function

is\_subsequence

Return `True` if child is subsequence of parent.](/python/langchain-core/prompts/string/is_subsequence)

## Classes

[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

StringPromptValue

String prompt value.](/python/langchain-core/prompt_values/StringPromptValue)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)[class

StringPromptTemplate

String prompt that exposes the format method, returning a prompt.](/python/langchain-core/prompts/string/StringPromptTemplate)

## Modules

[module

mustache

Adapted from <https://github.com/noahmorrison/chevron>.

MIT License.](/python/langchain-core/utils/mustache)


