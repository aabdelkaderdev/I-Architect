<!-- Source: https://reference.langchain.com/python/langchain-core/tracers -->

Modulev1.2.21 (latest)●Since v0.1

# tracers

Tracers are classes for tracing runs.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)

## Classes

[class

BaseTracer

Base interface for tracers.](/python/langchain-core/tracers/base/BaseTracer)[class

EvaluatorCallbackHandler

Tracer that runs a run evaluator whenever a run is persisted.](/python/langchain-core/tracers/evaluation/EvaluatorCallbackHandler)[class

LangChainTracer

Implementation of the `SharedTracer` that `POSTS` to the LangChain endpoint.](/python/langchain-core/tracers/langchain/LangChainTracer)[class

LogStreamCallbackHandler

Tracer that streams run logs to a stream.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler)[class

RunLog

Run log.](/python/langchain-core/tracers/log_stream/RunLog)[class

RunLogPatch

Patch to the run log.](/python/langchain-core/tracers/log_stream/RunLogPatch)[class

ConsoleCallbackHandler

Tracer that prints to the console.](/python/langchain-core/tracers/stdout/ConsoleCallbackHandler)

## Modules

[module

evaluation

A tracer that runs evaluators over completed runs.](/python/langchain-core/tracers/evaluation)[module

run\_collector

A tracer that collects all nested runs in a list.](/python/langchain-core/tracers/run_collector)[module

core

Utilities for the root listener.](/python/langchain-core/tracers/core)[module

base

Base interfaces for tracing runs.](/python/langchain-core/tracers/base)[module

memory\_stream

Module implements a memory stream for communication between two co-routines.

This module provides a way to communicate between two co-routines using a memory
channel. The writer and reader can be in the same event loop or in different event
loops. When they're in different event loops, they will also be in different threads.

Useful in situations when there's a mix of synchronous and asynchronous used in the
code.](/python/langchain-core/tracers/memory_stream)[module

event\_stream

Internal tracer to power the event stream API.](/python/langchain-core/tracers/event_stream)[module

log\_stream

Tracer that streams run logs to a stream.](/python/langchain-core/tracers/log_stream)[module

root\_listeners

Tracers that call listeners.](/python/langchain-core/tracers/root_listeners)[module

stdout

Tracers that print to the console.](/python/langchain-core/tracers/stdout)[module

context

Context management for tracers.](/python/langchain-core/tracers/context)[module

schemas

Schemas for tracers.](/python/langchain-core/tracers/schemas)[module

langchain

A tracer implementation that records to LangChain endpoint.](/python/langchain-core/tracers/langchain)


