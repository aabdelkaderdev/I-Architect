<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/history -->

Modulev1.2.21 (latest)●Since v0.1

# history

`Runnable` that manages chat message history for another `Runnable`.

## Attributes

[attribute

Output](/python/langchain-core/runnables/utils/Output)[attribute

LanguageModelLike: Runnable[LanguageModelInput, LanguageModelOutput]

Input/output interface for a language model.](/python/langchain-core/language_models/base/LanguageModelLike)[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

GetSessionHistoryCallable: Callable[..., BaseChatMessageHistory]](/python/langchain-core/runnables/history/GetSessionHistoryCallable)

## Functions

[function

load

Revive a LangChain class from a JSON object.

Use this if you already have a parsed JSON object, eg. from `json.load` or
`orjson.loads`.

Only classes in the allowlist can be instantiated. The default allowlist includes
core LangChain types (messages, prompts, documents, etc.). See
`langchain_core.load.mapping` for the full list.

Do not use with untrusted input

This function instantiates Python objects and can trigger side effects
during deserialization. **Never call `load()` on data from an untrusted
or unauthenticated source.** See the module-level security model
documentation for details and best practices.](/python/langchain-core/load/load/load)[function

get\_unique\_config\_specs

Get the unique config specs from a sequence of config specs.](/python/langchain-core/runnables/utils/get_unique_config_specs)[function

create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.](/python/langchain-core/utils/pydantic/create_model_v2)

## Classes

[class

BaseChatMessageHistory

Abstract base class for storing chat message history.

Implementations guidelines:

Implementations are expected to over-ride all or some of the following methods:

- `add_messages`: sync variant for bulk addition of messages
- `aadd_messages`: async variant for bulk addition of messages
- `messages`: sync variant for getting messages
- `aget_messages`: async variant for getting messages
- `clear`: sync variant for clearing messages
- `aclear`: async variant for clearing messages

`add_messages` contains a default implementation that calls `add_message`
for each message in the sequence. This is provided for backwards compatibility
with existing implementations which only had `add_message`.

Async variants all have default implementations that call the sync variants.
Implementers can choose to override the async implementations to provide
truly async implementations.

Usage guidelines:

When used for updating history, users should favor usage of `add_messages`
over `add_message` or other variants like `add_user_message` and `add_ai_message`
to avoid unnecessary round-trips to the underlying persistence layer.](/python/langchain-core/chat_history/BaseChatMessageHistory)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

Runnable

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

For a UI (and much more) checkout [LangSmith](https://docs.langchain.com/langsmith/home).](/python/langchain-core/runnables/base/Runnable)[class

RunnableBindingBase

`Runnable` that delegates calls to another `Runnable` with a set of `**kwargs`.

Use only if creating a new `RunnableBinding` subclass with different `__init__`
args.

See documentation for `RunnableBinding` for more details.](/python/langchain-core/runnables/base/RunnableBindingBase)[class

RunnableLambda

`RunnableLambda` converts a python callable into a `Runnable`.

Wrapping a callable in a `RunnableLambda` makes the callable usable
within either a sync or async context.

`RunnableLambda` can be composed as any other `Runnable` and provides
seamless integration with LangChain tracing.

`RunnableLambda` is best suited for code that does not need to support
streaming. If you need to support streaming (i.e., be able to operate
on chunks of inputs and yield chunks of outputs), use `RunnableGenerator`
instead.

Note that if a `RunnableLambda` returns an instance of `Runnable`, that
instance is invoked (or streamed) during execution.](/python/langchain-core/runnables/base/RunnableLambda)[class

RunnablePassthrough

Runnable to passthrough inputs unchanged or with additional keys.

This `Runnable` behaves almost like the identity function, except that it
can be configured to add additional keys to the output, if the input is a
dict.

The examples below demonstrate this `Runnable` works using a few simple
chains. The chains rely on simple lambdas to make the examples easy to execute
and experiment with.](/python/langchain-core/runnables/passthrough/RunnablePassthrough)[class

ConfigurableFieldSpec

Field that can be configured by the user. It is a specification of a field.](/python/langchain-core/runnables/utils/ConfigurableFieldSpec)[class

RunnableConfig

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
```](/python/langchain-core/runnables/config/RunnableConfig)[class

RunnableWithMessageHistory

`Runnable` that manages chat message history for another `Runnable`.

A chat message history is a sequence of messages that represent a conversation.

`RunnableWithMessageHistory` wraps another `Runnable` and manages the chat message
history for it; it is responsible for reading and updating the chat message
history.

The formats supported for the inputs and outputs of the wrapped `Runnable`
are described below.

`RunnableWithMessageHistory` must always be called with a config that contains
the appropriate parameters for the chat message history factory.

By default, the `Runnable` is expected to take a single configuration parameter
called `session_id` which is a string. This parameter is used to create a new
or look up an existing chat message history that matches the given `session_id`.

In this case, the invocation would look like this:

`with_history.invoke(..., config={"configurable": {"session_id": "bar"}})`
; e.g., `{"configurable": {"session_id": "<SESSION_ID>"}}`.

The configuration can be customized by passing in a list of
`ConfigurableFieldSpec` objects to the `history_factory_config` parameter (see
example below).

In the examples, we will use a chat message history with an in-memory
implementation to make it easy to experiment and see the results.

For production use cases, you will want to use a persistent implementation
of chat message history, such as `RedisChatMessageHistory`.

Example: Chat message history with an in-memory implementation for testing.

```
from operator import itemgetter

from langchain_openai.chat_models import ChatOpenAI

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: list[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

# Here we use a global variable to store the chat message history.
# This will make it easier to inspect it to see the underlying results.
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

history = get_by_session_id("1")
history.add_message(AIMessage(content="hello"))
print(store)  # noqa: T201
```

Example where the wrapped `Runnable` takes a dictionary input:

```
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who's good at {ability}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatAnthropic(model="claude-2")

chain_with_history = RunnableWithMessageHistory(
    chain,
    # Uses the get_by_session_id function defined in the example
    # above.
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

print(
    chain_with_history.invoke(  # noqa: T201
        {"ability": "math", "question": "What does cosine mean?"},
        config={"configurable": {"session_id": "foo"}},
    )
)

# Uses the store defined in the example above.
print(store)  # noqa: T201

print(
    chain_with_history.invoke(  # noqa: T201
        {"ability": "math", "question": "What's its inverse"},
        config={"configurable": {"session_id": "foo"}},
    )
)

print(store)  # noqa: T201
```

Example where the session factory takes two keys (`user_id` and `conversation_id`):

```
store = {}

def get_session_history(
    user_id: str, conversation_id: str
) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant who's good at {ability}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatAnthropic(model="claude-2")

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
)

with_message_history.invoke(
    {"ability": "math", "question": "What does cosine mean?"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
```](/python/langchain-core/runnables/history/RunnableWithMessageHistory)

## Type Aliases

[typeAlias

MessagesOrDictWithMessages: Sequence['BaseMessage'] | dict[str, Any]](/python/langchain-core/runnables/history/MessagesOrDictWithMessages)


