<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils -->

Modulev1.2.21 (latest)●Since v0.1

# utils

Utility code for `Runnable` objects.

## Attributes

[attribute

Input](/python/langchain-core/runnables/utils/Input)[attribute

Output](/python/langchain-core/runnables/utils/Output)[attribute

Addable](/python/langchain-core/runnables/utils/Addable)

## Functions

[function

create\_model

Create a Pydantic model with the given field definitions.

Please use `create_model_v2` instead of this function.](/python/langchain-core/utils/pydantic/create_model)[function

gated\_coro

Run a coroutine with a semaphore.](/python/langchain-core/runnables/utils/gated_coro)[function

gather\_with\_concurrency

Gather coroutines with a limit on the number of concurrent coroutines.](/python/langchain-core/runnables/utils/gather_with_concurrency)[function

accepts\_run\_manager

Check if a callable accepts a run\_manager argument.](/python/langchain-core/runnables/utils/accepts_run_manager)[function

accepts\_config

Check if a callable accepts a config argument.](/python/langchain-core/runnables/utils/accepts_config)[function

accepts\_context

Check if a callable accepts a context argument.](/python/langchain-core/runnables/utils/accepts_context)[function

asyncio\_accepts\_context

Check if asyncio.create\_task accepts a `context` arg.](/python/langchain-core/runnables/utils/asyncio_accepts_context)[function

coro\_with\_context

Await a coroutine with a context.](/python/langchain-core/runnables/utils/coro_with_context)[function

get\_function\_first\_arg\_dict\_keys

Get the keys of the first argument of a function if it is a dict.](/python/langchain-core/runnables/utils/get_function_first_arg_dict_keys)[function

get\_lambda\_source

Get the source code of a lambda function.](/python/langchain-core/runnables/utils/get_lambda_source)[function

get\_function\_nonlocals

Get the nonlocal variables accessed by a function.](/python/langchain-core/runnables/utils/get_function_nonlocals)[function

indent\_lines\_after\_first

Indent all lines of text after the first line.](/python/langchain-core/runnables/utils/indent_lines_after_first)[function

add

Add a sequence of addable objects together.](/python/langchain-core/runnables/utils/add)[function

aadd

Asynchronously add a sequence of addable objects together.](/python/langchain-core/runnables/utils/aadd)[function

get\_unique\_config\_specs

Get the unique config specs from a sequence of config specs.](/python/langchain-core/runnables/utils/get_unique_config_specs)[function

is\_async\_generator

Check if a function is an async generator.](/python/langchain-core/runnables/utils/is_async_generator)[function

is\_async\_callable

Check if a function is async.](/python/langchain-core/runnables/utils/is_async_callable)

## Classes

[class

IsLocalDict

Check if a name is a local dict.](/python/langchain-core/runnables/utils/IsLocalDict)[class

IsFunctionArgDict

Check if the first argument of a function is a dict.](/python/langchain-core/runnables/utils/IsFunctionArgDict)[class

NonLocals

Get nonlocal variables accessed.](/python/langchain-core/runnables/utils/NonLocals)[class

FunctionNonLocals

Get the nonlocal variables accessed of a function.](/python/langchain-core/runnables/utils/FunctionNonLocals)[class

GetLambdaSource

Get the source code of a lambda function.](/python/langchain-core/runnables/utils/GetLambdaSource)[class

AddableDict

Dictionary that can be added to another dictionary.](/python/langchain-core/runnables/utils/AddableDict)[class

SupportsAdd

Protocol for objects that support addition.](/python/langchain-core/runnables/utils/SupportsAdd)[class

ConfigurableField

Field that can be configured by the user.](/python/langchain-core/runnables/utils/ConfigurableField)[class

ConfigurableFieldSingleOption

Field that can be configured by the user with a default value.](/python/langchain-core/runnables/utils/ConfigurableFieldSingleOption)[class

ConfigurableFieldMultiOption

Field that can be configured by the user with multiple default values.](/python/langchain-core/runnables/utils/ConfigurableFieldMultiOption)[class

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)

## Type Aliases

[typeAlias

StreamEvent](/python/langchain-core/runnables/schema/StreamEvent)[typeAlias

AnyConfigurableField](/python/langchain-core/runnables/utils/AnyConfigurableField)


