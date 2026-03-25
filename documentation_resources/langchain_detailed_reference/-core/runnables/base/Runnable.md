<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable -->

Classv1.2.21 (latest)●Since v0.1

# Runnable

A unit of work that can be invoked, batched, streamed, transformed and composed.

# Key Methods

- `invoke`/`ainvoke`: Transforms a single input into an output.
- `batch`/`abatch`: Efficiently transforms multiple inputs into outputs.
- `stream`/`astream`: Streams output from a single input as it's produced.
- `astream_log`: Streams output and selected intermediate results from an
  input.

Built-in optimizations:

- **Batch**: By default, batch runs invoke() in parallel using a thread pool
  executor. Override to optimize batching.
- **Async**: Methods with `'a'` prefix are asynchronous. By default, they execute
  the sync counterpart using asyncio's thread pool.
  Override for native async.

All methods accept an optional config argument, which can be used to configure
execution, add tags and metadata for tracing and debugging etc.

Runnables expose schematic information about their input, output and config via
the `input_schema` property, the `output_schema` property and `config_schema`
method.

# Composition

Runnable objects can be composed together to create chains in a declarative way.

Any chain constructed this way will automatically have sync, async, batch, and
streaming support.

The main composition primitives are `RunnableSequence` and `RunnableParallel`.

**`RunnableSequence`** invokes a series of runnables sequentially, with
one Runnable's output serving as the next's input. Construct using
the `|` operator or by passing a list of runnables to `RunnableSequence`.

**`RunnableParallel`** invokes runnables concurrently, providing the same input
to each. Construct it using a dict literal within a sequence or by passing a
dict to `RunnableParallel`.

For example,

```
from langchain_core.runnables import RunnableLambda

# A RunnableSequence constructed using the `|` operator
sequence = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
sequence.invoke(1)  # 4
sequence.batch([1, 2, 3])  # [4, 6, 8]

# A sequence that contains a RunnableParallel constructed using a dict literal
sequence = RunnableLambda(lambda x: x + 1) | {
    "mul_2": RunnableLambda(lambda x: x * 2),
    "mul_5": RunnableLambda(lambda x: x * 5),
}
sequence.invoke(1)  # {'mul_2': 4, 'mul_5': 10}
```

# Standard Methods

All `Runnable`s expose additional methods that can be used to modify their
behavior (e.g., add a retry policy, add lifecycle listeners, make them
configurable, etc.).

These methods will work on any `Runnable`, including `Runnable` chains
constructed by composing other `Runnable`s.
See the individual methods for details.

For example,

```
from langchain_core.runnables import RunnableLambda

import random

def add_one(x: int) -> int:
    return x + 1

def buggy_double(y: int) -> int:
    """Buggy code that will fail 70% of the time"""
    if random.random() > 0.3:
        print('This code failed, and will probably be retried!')  # noqa: T201
        raise ValueError('Triggered buggy code')
    return y * 2

sequence = (
    RunnableLambda(add_one) |
    RunnableLambda(buggy_double).with_retry( # Retry on failure
        stop_after_attempt=10,
        wait_exponential_jitter=False
    )
)

print(sequence.input_schema.model_json_schema()) # Show inferred input schema
print(sequence.output_schema.model_json_schema()) # Show inferred output schema
print(sequence.invoke(2)) # invoke the sequence (note the retry above!!)
```

# Debugging and tracing

As the chains get longer, it can be useful to be able to see intermediate results
to debug and trace the chain.

You can set the global debug flag to True to enable debug output for all chains:

```
from langchain_core.globals import set_debug

set_debug(True)
```

Alternatively, you can pass existing or custom callbacks to any given chain:

```
from langchain_core.tracers import ConsoleCallbackHandler

chain.invoke(..., config={"callbacks": [ConsoleCallbackHandler()]})
```

For a UI (and much more) checkout [LangSmith](https://docs.langchain.com/langsmith/home).


```
Runnable()
```

## Bases

`ABC``Generic[Input, Output]`

## Attributes

[attribute

name: str | None

The name of the `Runnable`. Used for debugging and tracing.](/python/langchain-core/runnables/base/Runnable/name)[attribute

InputType: type[Input]

Input type.

The type of input this `Runnable` accepts specified as a type annotation.](/python/langchain-core/runnables/base/Runnable/InputType)[attribute

OutputType: type[Output]

Output Type.

The type of output this `Runnable` produces specified as a type annotation.](/python/langchain-core/runnables/base/Runnable/OutputType)[attribute

input\_schema: type[BaseModel]

The type of input this `Runnable` accepts specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/input_schema)[attribute

output\_schema: type[BaseModel]

Output schema.

The type of output this `Runnable` produces specified as a Pydantic model.](/python/langchain-core/runnables/base/Runnable/output_schema)[attribute

config\_specs: list[ConfigurableFieldSpec]

List configurable fields for this `Runnable`.](/python/langchain-core/runnables/base/Runnable/config_specs)

## Methods

[method

get\_name

Get the name of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_name)[method

get\_input\_schema

Get a Pydantic model that can be used to validate input to the `Runnable`.

`Runnable` objects that leverage the `configurable_fields` and
`configurable_alternatives` methods will have a dynamic input schema that
depends on which configuration the `Runnable` is invoked with.

This method allows to get an input schema for a specific configuration.](/python/langchain-core/runnables/base/Runnable/get_input_schema)[method

get\_input\_jsonschema

Get a JSON schema that represents the input to the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[method

get\_output\_schema

Get a Pydantic model that can be used to validate output to the `Runnable`.

`Runnable` objects that leverage the `configurable_fields` and
`configurable_alternatives` methods will have a dynamic output schema that
depends on which configuration the `Runnable` is invoked with.

This method allows to get an output schema for a specific configuration.](/python/langchain-core/runnables/base/Runnable/get_output_schema)[method

get\_output\_jsonschema

Get a JSON schema that represents the output of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[method

config\_schema

The type of config this `Runnable` accepts specified as a Pydantic model.

To mark a field as configurable, see the `configurable_fields`
and `configurable_alternatives` methods.](/python/langchain-core/runnables/base/Runnable/config_schema)[method

get\_config\_jsonschema

Get a JSON schema that represents the config of the `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_config_jsonschema)[method

get\_graph

Return a graph representation of this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_graph)[method

get\_prompts

Return a list of prompts used by this `Runnable`.](/python/langchain-core/runnables/base/Runnable/get_prompts)[method

pipe

Pipe `Runnable` objects.

Compose this `Runnable` with `Runnable`-like objects to make a
`RunnableSequence`.

Equivalent to `RunnableSequence(self, *others)` or `self | others[0] | ...`](/python/langchain-core/runnables/base/Runnable/pipe)[method

pick

Pick keys from the output `dict` of this `Runnable`.

Pick a single key

```
import json

from langchain_core.runnables import RunnableLambda, RunnableMap

as_str = RunnableLambda(str)
as_json = RunnableLambda(json.loads)
chain = RunnableMap(str=as_str, json=as_json)

chain.invoke("[1, 2, 3]")
# -> {"str": "[1, 2, 3]", "json": [1, 2, 3]}

json_only_chain = chain.pick("json")
json_only_chain.invoke("[1, 2, 3]")
# -> [1, 2, 3]
```

Pick a list of keys

```
from typing import Any

import json

from langchain_core.runnables import RunnableLambda, RunnableMap

as_str = RunnableLambda(str)
as_json = RunnableLambda(json.loads)

def as_bytes(x: Any) -> bytes:
    return bytes(x, "utf-8")

chain = RunnableMap(
    str=as_str, json=as_json, bytes=RunnableLambda(as_bytes)
)

chain.invoke("[1, 2, 3]")
# -> {"str": "[1, 2, 3]", "json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

json_and_bytes_chain = chain.pick(["json", "bytes"])
json_and_bytes_chain.invoke("[1, 2, 3]")
# -> {"json": [1, 2, 3], "bytes": b"[1, 2, 3]"}
```](/python/langchain-core/runnables/base/Runnable/pick)[method

assign

Assigns new fields to the `dict` output of this `Runnable`.

```
from langchain_core.language_models.fake import FakeStreamingListLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.runnables import Runnable
from operator import itemgetter

prompt = (
    SystemMessagePromptTemplate.from_template("You are a nice assistant.")
    + "{question}"
)
model = FakeStreamingListLLM(responses=["foo-lish"])

chain: Runnable = prompt | model | {"str": StrOutputParser()}

chain_with_assign = chain.assign(hello=itemgetter("str") | model)

print(chain_with_assign.input_schema.model_json_schema())
# {'title': 'PromptInput', 'type': 'object', 'properties':
{'question': {'title': 'Question', 'type': 'string'}}}
print(chain_with_assign.output_schema.model_json_schema())
# {'title': 'RunnableSequenceOutput', 'type': 'object', 'properties':
{'str': {'title': 'Str',
'type': 'string'}, 'hello': {'title': 'Hello', 'type': 'string'}}}
```](/python/langchain-core/runnables/base/Runnable/assign)[method

invoke

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/invoke)[method

ainvoke

Transform a single input into an output.](/python/langchain-core/runnables/base/Runnable/ainvoke)[method

batch

Default implementation runs invoke in parallel using a thread pool executor.

The default implementation of batch works well for IO bound runnables.

Subclasses must override this method if they can batch more efficiently;
e.g., if the underlying `Runnable` uses an API which supports a batch mode.](/python/langchain-core/runnables/base/Runnable/batch)[method

batch\_as\_completed

Run `invoke` in parallel on a list of inputs.

Yields results as they complete.](/python/langchain-core/runnables/base/Runnable/batch_as_completed)[method

abatch

Default implementation runs `ainvoke` in parallel using `asyncio.gather`.

The default implementation of `batch` works well for IO bound runnables.

Subclasses must override this method if they can batch more efficiently;
e.g., if the underlying `Runnable` uses an API which supports a batch mode.](/python/langchain-core/runnables/base/Runnable/abatch)[method

abatch\_as\_completed

Run `ainvoke` in parallel on a list of inputs.

Yields results as they complete.](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)[method

stream

Default implementation of `stream`, which calls `invoke`.

Subclasses must override this method if they support streaming output.](/python/langchain-core/runnables/base/Runnable/stream)[method

astream

Default implementation of `astream`, which calls `ainvoke`.

Subclasses must override this method if they support streaming output.](/python/langchain-core/runnables/base/Runnable/astream)[method

astream\_log

Stream all output from a `Runnable`, as reported to the callback system.

This includes all inner runs of LLMs, Retrievers, Tools, etc.

Output is streamed as Log objects, which include a list of
Jsonpatch ops that describe how the state of the run has changed in each
step, and the final state of the run.

The Jsonpatch ops can be applied in order to construct state.](/python/langchain-core/runnables/base/Runnable/astream_log)[method

astream\_events

Generate a stream of events.

Use to create an iterator over `StreamEvent` that provide real-time information
about the progress of the `Runnable`, including `StreamEvent` from intermediate
results.

A `StreamEvent` is a dictionary with the following schema:

- `event`: Event names are of the format:
  `on_[runnable_type]_(start|stream|end)`.
- `name`: The name of the `Runnable` that generated the event.
- `run_id`: Randomly generated ID associated with the given execution of the
  `Runnable` that emitted the event. A child `Runnable` that gets invoked as
  part of the execution of a parent `Runnable` is assigned its own unique ID.
- `parent_ids`: The IDs of the parent runnables that generated the event. The
  root `Runnable` will have an empty list. The order of the parent IDs is from
  the root to the immediate parent. Only available for v2 version of the API.
  The v1 version of the API will return an empty list.
- `tags`: The tags of the `Runnable` that generated the event.
- `metadata`: The metadata of the `Runnable` that generated the event.
- `data`: The data associated with the event. The contents of this field
  depend on the type of event. See the table below for more details.

Below is a table that illustrates some events that might be emitted by various
chains. Metadata fields have been omitted from the table for brevity.
Chain definitions have been included after the table.

Note

This reference table is for the v2 version of the schema.

| event | name | chunk | input | output |
| --- | --- | --- | --- | --- |
| `on_chat_model_start` | `'[model name]'` |  | `{"messages": [[SystemMessage, HumanMessage]]}` |  |
| `on_chat_model_stream` | `'[model name]'` | `AIMessageChunk(content="hello")` |  |  |
| `on_chat_model_end` | `'[model name]'` |  | `{"messages": [[SystemMessage, HumanMessage]]}` | `AIMessageChunk(content="hello world")` |
| `on_llm_start` | `'[model name]'` |  | `{'input': 'hello'}` |  |
| `on_llm_stream` | `'[model name]'` | `'Hello'` |  |  |
| `on_llm_end` | `'[model name]'` |  | `'Hello human!'` |  |
| `on_chain_start` | `'format_docs'` |  |  |  |
| `on_chain_stream` | `'format_docs'` | `'hello world!, goodbye world!'` |  |  |
| `on_chain_end` | `'format_docs'` |  | `[Document(...)]` | `'hello world!, goodbye world!'` |
| `on_tool_start` | `'some_tool'` |  | `{"x": 1, "y": "2"}` |  |
| `on_tool_end` | `'some_tool'` |  |  | `{"x": 1, "y": "2"}` |
| `on_retriever_start` | `'[retriever name]'` |  | `{"query": "hello"}` |  |
| `on_retriever_end` | `'[retriever name]'` |  | `{"query": "hello"}` | `[Document(...), ..]` |
| `on_prompt_start` | `'[template_name]'` |  | `{"question": "hello"}` |  |
| `on_prompt_end` | `'[template_name]'` |  | `{"question": "hello"}` | `ChatPromptValue(messages: [SystemMessage, ...])` |

In addition to the standard events, users can also dispatch custom events (see example below).

Custom events will be only be surfaced with in the v2 version of the API!

A custom event has following format:

| Attribute | Type | Description |
| --- | --- | --- |
| `name` | `str` | A user defined name for the event. |
| `data` | `Any` | The data associated with the event. This can be anything, though we suggest making it JSON serializable. |

Here are declarations associated with the standard events shown above:

`format_docs`:

```
def format_docs(docs: list[Document]) -> str:
    '''Format the docs.'''
    return ", ".join([doc.page_content for doc in docs])

format_docs = RunnableLambda(format_docs)
```

`some_tool`:

```
@tool
def some_tool(x: int, y: str) -> dict:
    '''Some_tool.'''
    return {"x": x, "y": y}
```

`prompt`:

```
template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are Cat Agent 007"),
        ("human", "{question}"),
    ]
).with_config({"run_name": "my_template", "tags": ["my_template"]})
```

Example

```
from langchain_core.runnables import RunnableLambda

async def reverse(s: str) -> str:
    return s[::-1]

chain = RunnableLambda(func=reverse)

events = [
    event async for event in chain.astream_events("hello", version="v2")
]

# Will produce the following events
# (run_id, and parent_ids has been omitted for brevity):
[
    {
        "data": {"input": "hello"},
        "event": "on_chain_start",
        "metadata": {},
        "name": "reverse",
        "tags": [],
    },
    {
        "data": {"chunk": "olleh"},
        "event": "on_chain_stream",
        "metadata": {},
        "name": "reverse",
        "tags": [],
    },
    {
        "data": {"output": "olleh"},
        "event": "on_chain_end",
        "metadata": {},
        "name": "reverse",
        "tags": [],
    },
]
```

```
from langchain_core.callbacks.manager import (
    adispatch_custom_event,
)
from langchain_core.runnables import RunnableLambda, RunnableConfig
import asyncio

async def slow_thing(some_input: str, config: RunnableConfig) -> str:
    """Do something that takes a long time."""
    await asyncio.sleep(1) # Placeholder for some slow operation
    await adispatch_custom_event(
        "progress_event",
        {"message": "Finished step 1 of 3"},
        config=config # Must be included for python < 3.10
    )
    await asyncio.sleep(1) # Placeholder for some slow operation
    await adispatch_custom_event(
        "progress_event",
        {"message": "Finished step 2 of 3"},
        config=config # Must be included for python < 3.10
    )
    await asyncio.sleep(1) # Placeholder for some slow operation
    return "Done"

slow_thing = RunnableLambda(slow_thing)

async for event in slow_thing.astream_events("some_input", version="v2"):
    print(event)
```](/python/langchain-core/runnables/base/Runnable/astream_events)[method

transform

Transform inputs to outputs.

Default implementation of transform, which buffers input and calls `astream`.

Subclasses must override this method if they can start producing output while
input is still being generated.](/python/langchain-core/runnables/base/Runnable/transform)[method

atransform

Transform inputs to outputs.

Default implementation of atransform, which buffers input and calls `astream`.

Subclasses must override this method if they can start producing output while
input is still being generated.](/python/langchain-core/runnables/base/Runnable/atransform)[method

bind

Bind arguments to a `Runnable`, returning a new `Runnable`.

Useful when a `Runnable` in a chain requires an argument that is not
in the output of the previous `Runnable` or included in the user input.](/python/langchain-core/runnables/base/Runnable/bind)[method

with\_config

Bind config to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_config)[method

with\_listeners

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.

The Run object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.](/python/langchain-core/runnables/base/Runnable/with_listeners)[method

with\_alisteners

Bind async lifecycle listeners to a `Runnable`.

Returns a new `Runnable`.

The Run object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.](/python/langchain-core/runnables/base/Runnable/with_alisteners)[method

with\_types

Bind input and output types to a `Runnable`, returning a new `Runnable`.](/python/langchain-core/runnables/base/Runnable/with_types)[method

with\_retry

Create a new `Runnable` that retries the original `Runnable` on exceptions.](/python/langchain-core/runnables/base/Runnable/with_retry)[method

map

Return a new `Runnable` that maps a list of inputs to a list of outputs.

Calls `invoke` with each input.](/python/langchain-core/runnables/base/Runnable/map)[method

with\_fallbacks

Add fallbacks to a `Runnable`, returning a new `Runnable`.

The new `Runnable` will try the original `Runnable`, and then each fallback
in order, upon failures.](/python/langchain-core/runnables/base/Runnable/with_fallbacks)[method

as\_tool

Create a `BaseTool` from a `Runnable`.

`as_tool` will instantiate a `BaseTool` with a name, description, and
`args_schema` from a `Runnable`. Where possible, schemas are inferred
from `runnable.get_input_schema`.

Alternatively (e.g., if the `Runnable` takes a dict as input and the specific
`dict` keys are not typed), the schema can be specified directly with
`args_schema`.

You can also pass `arg_types` to just specify the required arguments and their
types.](/python/langchain-core/runnables/base/Runnable/as_tool)


