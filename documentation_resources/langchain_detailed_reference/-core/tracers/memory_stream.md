<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/memory_stream -->

Modulev1.2.21 (latest)●Since v0.1

# memory\_stream

Module implements a memory stream for communication between two co-routines.

This module provides a way to communicate between two co-routines using a memory
channel. The writer and reader can be in the same event loop or in different event
loops. When they're in different event loops, they will also be in different threads.

Useful in situations when there's a mix of synchronous and asynchronous used in the
code.

## Attributes

[attribute

T](/python/langchain-core/tracers/memory_stream/T)


