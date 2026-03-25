<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/structured -->

Modulev1.2.21 (latest)●Since v0.1

# structured

Structured prompt template for a language model.

## Attributes

[attribute

PromptTemplateFormat: Literal['f-string', 'mustache', 'jinja2']](/python/langchain-core/prompts/string/PromptTemplateFormat)[attribute

Other](/python/langchain-core/runnables/base/Other)

## Functions

[function

beta

Decorator to mark a function, a class, or a property as beta.

When marking a classmethod, a staticmethod, or a property, the `@beta` decorator
should go *under* `@classmethod` and `@staticmethod` (i.e., `beta` should directly
decorate the underlying callable), but *over* `@property`.

When marking a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@beta` would mess up
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).](/python/langchain-core/_api/beta_decorator/beta)[function

get\_pydantic\_field\_names

Get field names, including aliases, for a pydantic class.](/python/langchain-core/utils/utils/get_pydantic_field_names)

## Classes

[class

BaseLanguageModel

Abstract base class for interfacing with language models.

All language model wrappers inherited from `BaseLanguageModel`.](/python/langchain-core/language_models/base/BaseLanguageModel)[class

ChatPromptTemplate

Prompt template for chat models.

Use to create flexible templated prompts for chat models.

Example

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?",
    }
)
# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot. Your name is Bob.'),
#        HumanMessage(content='Hello, how are you doing?'),
#        AIMessage(content="I'm doing well, thanks!"),
#        HumanMessage(content='What is your name?')
#    ]
# )
```

Messages Placeholder

```
# In addition to Human/AI/Tool/Function messages,
# you can initialize the template with a MessagesPlaceholder
# either using the class directly or with the shorthand tuple syntax:

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot."),
        # Means the template will receive an optional list of messages under
        # the "conversation" key
        ("placeholder", "{conversation}"),
        # Equivalently:
        # MessagesPlaceholder(variable_name="conversation", optional=True)
    ]
)

prompt_value = template.invoke(
    {
        "conversation": [
            ("human", "Hi!"),
            ("ai", "How can I assist you today?"),
            ("human", "Can you make me an ice cream sundae?"),
            ("ai", "No."),
        ]
    }
)

# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot.'),
#        HumanMessage(content='Hi!'),
#        AIMessage(content='How can I assist you today?'),
#        HumanMessage(content='Can you make me an ice cream sundae?'),
#        AIMessage(content='No.'),
#    ]
# )
```

Single-variable template

If your prompt has only a single input variable (i.e., one instance of
`'{variable_nams}'`), and you invoke the template with a non-dict object, the
prompt template will inject the provided argument into that variable location.

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is Carl."),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke("Hello, there!")
# Equivalent to
# prompt_value = template.invoke({"user_input": "Hello, there!"})

# Output:
#  ChatPromptValue(
#     messages=[
#         SystemMessage(content='You are a helpful AI bot. Your name is Carl.'),
#         HumanMessage(content='Hello, there!'),
#     ]
# )
```](/python/langchain-core/prompts/chat/ChatPromptTemplate)[class

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

RunnableSequence

Sequence of `Runnable` objects, where the output of one is the input of the next.

**`RunnableSequence`** is the most important composition operator in LangChain
as it is used in virtually every chain.

A `RunnableSequence` can be instantiated directly or more commonly by using the
`|` operator where either the left or right operands (or both) must be a
`Runnable`.

Any `RunnableSequence` automatically supports sync, async, batch.

The default implementations of `batch` and `abatch` utilize threadpools and
asyncio gather and will be faster than naive invocation of `invoke` or `ainvoke`
for IO bound `Runnable`s.

Batching is implemented by invoking the batch method on each component of the
`RunnableSequence` in order.

A `RunnableSequence` preserves the streaming properties of its components, so if
all components of the sequence implement a `transform` method -- which
is the method that implements the logic to map a streaming input to a streaming
output -- then the sequence will be able to stream input to output!

If any component of the sequence does not implement transform then the
streaming will only begin after this component is run. If there are
multiple blocking components, streaming begins after the last one.

Note

`RunnableLambdas` do not support `transform` by default! So if you need to
use a `RunnableLambdas` be careful about where you place them in a
`RunnableSequence` (if you need to use the `stream`/`astream` methods).

If you need arbitrary logic and need streaming, you can subclass
Runnable, and implement `transform` for whatever logic you need.

Here is a simple example that uses simple functions to illustrate the use of
`RunnableSequence`:

```
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
sequence = runnable_1 | runnable_2
# Or equivalently:
# sequence = RunnableSequence(first=runnable_1, last=runnable_2)
sequence.invoke(1)
await sequence.ainvoke(1)

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
```

Here's an example that uses streams JSON output generated by an LLM:

```
from langchain_core.output_parsers.json import SimpleJsonOutputParser
from langchain_openai import ChatOpenAI

prompt = PromptTemplate.from_template(
    "In JSON format, give me a list of {topic} and their "
    "corresponding names in French, Spanish and in a "
    "Cat Language."
)

model = ChatOpenAI()
chain = prompt | model | SimpleJsonOutputParser()

async for chunk in chain.astream({"topic": "colors"}):
    print("-")  # noqa: T201
    print(chunk, sep="", flush=True)  # noqa: T201
```](/python/langchain-core/runnables/base/RunnableSequence)[class

RunnableSerializable

Runnable that can be serialized to JSON.](/python/langchain-core/runnables/base/RunnableSerializable)[class

StructuredPrompt

Structured prompt template for a language model.](/python/langchain-core/prompts/structured/StructuredPrompt)

## Type Aliases

[typeAlias

MessageLikeRepresentation](/python/langchain-core/prompts/chat/MessageLikeRepresentation)


