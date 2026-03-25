<!-- Source: https://reference.langchain.com/python/langchain-classic/callbacks/tracers -->

Modulev1.2.13 (latest)●Since v1.0

# tracers

Tracers that record execution of LangChain runs.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/callbacks/tracers/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Classes

[class

LoggingCallbackHandler

Tracer that logs via the input Logger.](/python/langchain-classic/callbacks/tracers/logging/LoggingCallbackHandler)

## Modules

[module

evaluation

A tracer that runs evaluators over completed runs.](/python/langchain-classic/callbacks/tracers/evaluation)[module

wandb](/python/langchain-classic/callbacks/tracers/wandb)[module

run\_collector](/python/langchain-classic/callbacks/tracers/run_collector)[module

base

Base interfaces for tracing runs.](/python/langchain-classic/callbacks/tracers/base)[module

comet](/python/langchain-classic/callbacks/tracers/comet)[module

logging](/python/langchain-classic/callbacks/tracers/logging)[module

log\_stream](/python/langchain-classic/callbacks/tracers/log_stream)[module

root\_listeners](/python/langchain-classic/callbacks/tracers/root_listeners)[module

stdout](/python/langchain-classic/callbacks/tracers/stdout)[module

schemas](/python/langchain-classic/callbacks/tracers/schemas)[module

langchain

A Tracer implementation that records to LangChain endpoint.](/python/langchain-classic/callbacks/tracers/langchain)


