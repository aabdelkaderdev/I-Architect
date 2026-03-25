<!-- Source: https://reference.langchain.com/python/langchain-core/messages/utils/trim_messages -->

Functionv1.2.21 (latest)●Since v0.2

# trim\_messages

Trim messages to be below a token count.

`trim_messages` can be used to reduce the size of a chat history to a specified
token or message count.

In either case, if passing the trimmed chat history back into a chat model
directly, the resulting chat history should usually satisfy the following
properties:

1. The resulting chat history should be valid. Most chat models expect that chat
   history starts with either (1) a `HumanMessage` or (2) a `SystemMessage`
   followed by a `HumanMessage`. To achieve this, set `start_on='human'`.
   In addition, generally a `ToolMessage` can only appear after an `AIMessage`
   that involved a tool call.
2. It includes recent messages and drops old messages in the chat history.
   To achieve this set the `strategy='last'`.
3. Usually, the new chat history should include the `SystemMessage` if it
   was present in the original chat history since the `SystemMessage` includes
   special instructions to the chat model. The `SystemMessage` is almost always
   the first message in the history if present. To achieve this set the
   `include_system=True`.

Note

The examples below show how to configure `trim_messages` to achieve a behavior
consistent with the above properties.


```
trim_messages(
  messages: Iterable[MessageLikeRepresentation] | PromptValue,
  *,
  max_tokens: int,
  token_counter: Callable[[list[BaseMessage]], int] | Callable[[BaseMessage], int] | BaseLanguageModel | Literal['approximate'],
  strategy: Literal['first', 'last'] = 'last',
  allow_partial: bool = False,
  end_on: str | type[BaseMessage] | Sequence[str | type[BaseMessage]] | None = None,
  start_on: str | type[BaseMessage] | Sequence[str | type[BaseMessage]] | None = None,
  include_system: bool = False,
  text_splitter: Callable[[str], list[str]] | TextSplitter | None = None
) -> list[BaseMessage]
```

**Example:**

Trim chat history based on token count, keeping the `SystemMessage` if
present, and ensuring that the chat history starts with a `HumanMessage` (or a
`SystemMessage` followed by a `HumanMessage`).

```
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage,
    SystemMessage,
    trim_messages,
)

messages = [
    SystemMessage("you're a good assistant, you always respond with a joke."),
    HumanMessage("i wonder why it's called langchain"),
    AIMessage(
        'Well, I guess they thought "WordRope" and "SentenceString" just '
        "didn't have the same ring to it!"
    ),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        "Hmmm let me think.\n\nWhy, he's probably chasing after the last "
        "cup of coffee in the office!"
    ),
    HumanMessage("what do you call a speechless parrot"),
]

trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o"),
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    allow_partial=False,
)
```

```
[
    SystemMessage(
        content="you're a good assistant, you always respond with a joke."
    ),
    HumanMessage(content="what do you call a speechless parrot"),
]
```

Trim chat history using approximate token counting with `'approximate'`:

```
trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    # Using the "approximate" shortcut for fast token counting
    token_counter="approximate",
    start_on="human",
    include_system=True,
)

# This is equivalent to using `count_tokens_approximately` directly
from langchain_core.messages.utils import count_tokens_approximately

trim_messages(
    messages,
    max_tokens=45,
    strategy="last",
    token_counter=count_tokens_approximately,
    start_on="human",
    include_system=True,
)
```

Trim chat history based on the message count, keeping the `SystemMessage` if
present, and ensuring that the chat history starts with a HumanMessage (
or a `SystemMessage` followed by a `HumanMessage`).

```
trim_messages(
    messages,
    # When `len` is passed in as the token counter function,
    # max_tokens will count the number of messages in the chat history.
    max_tokens=4,
    strategy="last",
    # Passing in `len` as a token counter function will
    # count the number of messages in the chat history.
    token_counter=len,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    allow_partial=False,
)
```

```
[
    SystemMessage(
        content="you're a good assistant, you always respond with a joke."
    ),
    HumanMessage(content="and who is harrison chasing anyways"),
    AIMessage(
        content="Hmmm let me think.\n\nWhy, he's probably chasing after "
        "the last cup of coffee in the office!"
    ),
    HumanMessage(content="what do you call a speechless parrot"),
]
```

Trim chat history using a custom token counter function that counts the
number of tokens in each message.

```
messages = [
    SystemMessage("This is a 4 token text. The full message is 10 tokens."),
    HumanMessage(
        "This is a 4 token text. The full message is 10 tokens.", id="first"
    ),
    AIMessage(
        [
            {"type": "text", "text": "This is the FIRST 4 token block."},
            {"type": "text", "text": "This is the SECOND 4 token block."},
        ],
        id="second",
    ),
    HumanMessage(
        "This is a 4 token text. The full message is 10 tokens.", id="third"
    ),
    AIMessage(
        "This is a 4 token text. The full message is 10 tokens.",
        id="fourth",
    ),
]

def dummy_token_counter(messages: list[BaseMessage]) -> int:
    # treat each message like it adds 3 default tokens at the beginning
    # of the message and at the end of the message. 3 + 4 + 3 = 10 tokens
    # per message.

    default_content_len = 4
    default_msg_prefix_len = 3
    default_msg_suffix_len = 3

    count = 0
    for msg in messages:
        if isinstance(msg.content, str):
            count += (
                default_msg_prefix_len
                + default_content_len
                + default_msg_suffix_len
            )
        if isinstance(msg.content, list):
            count += (
                default_msg_prefix_len
                + len(msg.content) * default_content_len
                + default_msg_suffix_len
            )
    return count
```

First 30 tokens, allowing partial messages:

```
trim_messages(
    messages,
    max_tokens=30,
    token_counter=dummy_token_counter,
    strategy="first",
    allow_partial=True,
)
```

```
[
    SystemMessage("This is a 4 token text. The full message is 10 tokens."),
    HumanMessage(
        "This is a 4 token text. The full message is 10 tokens.",
        id="first",
    ),
    AIMessage(
        [{"type": "text", "text": "This is the FIRST 4 token block."}],
        id="second",
    ),
]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `Iterable[MessageLikeRepresentation] | PromptValue` | Sequence of Message-like objects to trim. |
| `max_tokens`\* | `int` | Max token count of trimmed messages. |
| `token_counter`\* | `Callable[[list[BaseMessage]], int] | Callable[[BaseMessage], int] | BaseLanguageModel | Literal['approximate']` | Function or llm for counting tokens in a `BaseMessage` or a list of `BaseMessage`.  If a `BaseLanguageModel` is passed in then `BaseLanguageModel.get_num_tokens_from_messages()` will be used. Set to `len` to count the number of **messages** in the chat history.  You can also use string shortcuts for convenience:   - `'approximate'`: Uses `count_tokens_approximately` for fast, approximate   token counts.   Note  `count_tokens_approximately` (or the shortcut `'approximate'`) is recommended for using `trim_messages` on the hot path, where exact token counting is not necessary. |
| `strategy` | `Literal['first', 'last']` | Default:`'last'`  Strategy for trimming.   - `'first'`: Keep the first `<= n_count` tokens of the messages. - `'last'`: Keep the last `<= n_count` tokens of the messages. |
| `allow_partial` | `bool` | Default:`False`  Whether to split a message if only part of the message can be included.  If `strategy='last'` then the last partial contents of a message are included. If `strategy='first'` then the first partial contents of a message are included. |
| `end_on` | `str | type[BaseMessage] | Sequence[str | type[BaseMessage]] | None` | Default:`None`  The message type to end on.  If specified then every message after the last occurrence of this type is ignored. If `strategy='last'` then this is done before we attempt to get the last `max_tokens`. If `strategy='first'` then this is done after we get the first `max_tokens`. Can be specified as string names (e.g. `'system'`, `'human'`, `'ai'`, ...) or as `BaseMessage` classes (e.g. `SystemMessage`, `HumanMessage`, `AIMessage`, ...). Can be a single type or a list of types. |
| `start_on` | `str | type[BaseMessage] | Sequence[str | type[BaseMessage]] | None` | Default:`None`  The message type to start on.  Should only be specified if `strategy='last'`. If specified then every message before the first occurrence of this type is ignored. This is done after we trim the initial messages to the last `max_tokens`. Does not apply to a `SystemMessage` at index 0 if `include_system=True`. Can be specified as string names (e.g. `'system'`, `'human'`, `'ai'`, ...) or as `BaseMessage` classes (e.g. `SystemMessage`, `HumanMessage`, `AIMessage`, ...). Can be a single type or a list of types. |
| `include_system` | `bool` | Default:`False`  Whether to keep the `SystemMessage` if there is one at index `0`.  Should only be specified if `strategy="last"`. |
| `text_splitter` | `Callable[[str], list[str]] | TextSplitter | None` | Default:`None`  Function or `langchain_text_splitters.TextSplitter` for splitting the string contents of a message.  Only used if `allow_partial=True`. If `strategy='last'` then the last split tokens from a partial message will be included. if `strategy='first'` then the first split tokens from a partial message will be included. Token splitter assumes that separators are kept, so that split contents can be directly concatenated to recreate the original text. Defaults to splitting on newlines. |


