<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/dict -->

Modulev1.2.21 (latest)●Since v0.3

# dict

Dictionary prompt template.

## Attributes

## Functions

## Classes



[attribute

DEFAULT\_FORMATTER\_MAPPING: dict[str, Callable[..., str]]](/python/langchain-core/prompts/string/DEFAULT_FORMATTER_MAPPING)

[function

dumpd](/python/langchain-core/load/dump/dumpd)

[function

get\_template\_variables](/python/langchain-core/prompts/string/get_template_variables)

[function

ensure\_config](/python/langchain-core/runnables/config/ensure_config)

[class

RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig)

[class

RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

[class

DictPromptTemplate](/python/langchain-core/prompts/dict/DictPromptTemplate)

Return a dict representation of an object.

Get the variables from the template.

Ensure that a config is a dict with all keys present.

Runnable that can be serialized to JSON.

Template represented by a dictionary.

Recognizes variables in f-string or mustache formatted string dict values.

Does NOT recognize variables in dict keys. Applies recursively.

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
```