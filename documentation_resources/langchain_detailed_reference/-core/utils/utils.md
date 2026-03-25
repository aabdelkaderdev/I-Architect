<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils -->

Modulev1.2.21 (latest)●Since v0.1

# utils

Generic utility functions.

## Attributes

[attribute

LC\_AUTO\_PREFIX: str

LangChain auto-generated ID prefix for messages and content blocks.](/python/langchain-core/utils/utils/LC_AUTO_PREFIX)[attribute

LC\_ID\_PREFIX: str

Internal tracing/callback system identifier.

Used for:

- Tracing. Every LangChain operation (LLM call, chain execution, tool use, etc.)
  gets a unique run\_id (UUID)
- Enables tracking parent-child relationships between operations](/python/langchain-core/utils/utils/LC_ID_PREFIX)

## Functions

[function

is\_pydantic\_v1\_subclass

Check if the given class is Pydantic v1-like.](/python/langchain-core/utils/pydantic/is_pydantic_v1_subclass)[function

xor\_args

Validate specified keyword args are mutually exclusive.](/python/langchain-core/utils/utils/xor_args)[function

raise\_for\_status\_with\_text

Raise an error with the response text.](/python/langchain-core/utils/utils/raise_for_status_with_text)[function

mock\_now

Context manager for mocking out datetime.now() in unit tests.](/python/langchain-core/utils/utils/mock_now)[function

guard\_import

Dynamically import a module.

Raise an exception if the module is not installed.](/python/langchain-core/utils/utils/guard_import)[function

check\_package\_version

Check the version of a package.](/python/langchain-core/utils/utils/check_package_version)[function

get\_pydantic\_field\_names

Get field names, including aliases, for a pydantic class.](/python/langchain-core/utils/utils/get_pydantic_field_names)[function

build\_extra\_kwargs

Build extra kwargs from values and extra\_kwargs.

DON'T USE

Kept for backwards-compatibility but should never have been public. Use the
internal `_build_model_kwargs` function instead.](/python/langchain-core/utils/utils/build_extra_kwargs)[function

convert\_to\_secret\_str

Convert a string to a `SecretStr` if needed.](/python/langchain-core/utils/utils/convert_to_secret_str)[function

from\_env

Create a factory method that gets a value from an environment variable.](/python/langchain-core/utils/utils/from_env)[function

secret\_from\_env

Secret from env.](/python/langchain-core/utils/utils/secret_from_env)[function

ensure\_id

Ensure the ID is a valid string, generating a new UUID if not provided.

Auto-generated UUIDs are prefixed by `'lc_'` to indicate they are
LangChain-generated IDs.](/python/langchain-core/utils/utils/ensure_id)


