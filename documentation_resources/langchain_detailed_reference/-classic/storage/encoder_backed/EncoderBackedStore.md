<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/encoder_backed/EncoderBackedStore -->

Classv1.2.13 (latest)●Since v1.0

# EncoderBackedStore


```
EncoderBackedStore(
  self,
  store: BaseStore[str, Any],
  key_encoder: Callable[[K
```

## Bases

`BaseStore[K, V]`

## Constructors

## Attributes

## Methods



]

,

str

]

,

value\_serializer

:

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[

[

[V](/python/langchain-classic/storage/encoder_backed/V)

]

,

bytes

]

,

value\_deserializer

:

[Callable](https://docs.python.org/3/library/typing.html#typing.Callable)

[

[

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

]

,

V

]

)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `store`\* | `BaseStore[str, Any]` | The underlying byte store to wrap. |
| `key_encoder`\* | `Callable[[K], str]` | Function to encode keys from type `K` to strings. |
| `value_serializer`\* | `Callable[[V], bytes]` |  |
| `value_deserializer`\* | `Callable[[Any], V]` |  |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| store | [BaseStore](/python/langchain-core/stores/BaseStore)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| key\_encoder | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[K](/python/langchain-classic/storage/encoder_backed/K)], [str](https://docs.python.org/3/library/stdtypes.html#str)] |
| value\_serializer | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[V](/python/langchain-classic/storage/encoder_backed/V)], [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)] |
| value\_deserializer | [Callable](https://docs.python.org/3/library/typing.html#typing.Callable)[[[Any](https://docs.python.org/3/library/typing.html#typing.Any)], [V](/python/langchain-classic/storage/encoder_backed/V)] |

[attribute

store: store](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/store)

[attribute

key\_encoder: key\_encoder](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/key_encoder)

[attribute

value\_serializer: value\_serializer](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/value_serializer)

[attribute

value\_deserializer: value\_deserializer](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/value_deserializer)

[method

mget

Get the values associated with the given keys.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/mget)

[method

amget

Async get the values associated with the given keys.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/amget)

[method

mset

Set the values for the given keys.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/mset)

[method

amset

Async set the values for the given keys.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/amset)

[method

mdelete

Delete the given keys and their associated values.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/mdelete)

[method

amdelete

Async delete the given keys and their associated values.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/amdelete)

[method

yield\_keys

Get an iterator over keys that match the given prefix.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/yield_keys)

[method

ayield\_keys

Async get an iterator over keys that match the given prefix.](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/ayield_keys)

Wraps a store with key and value encoders/decoders.

Examples that uses JSON for encoding/decoding:

```
import json

def key_encoder(key: int) -> str:
    return json.dumps(key)

def value_serializer(value: float) -> str:
    return json.dumps(value)

def value_deserializer(serialized_value: str) -> float:
    return json.loads(serialized_value)

# Create an instance of the abstract store
abstract_store = MyCustomStore()

# Create an instance of the encoder-backed store
store = EncoderBackedStore(
    store=abstract_store,
    key_encoder=key_encoder,
    value_serializer=value_serializer,
    value_deserializer=value_deserializer,
)

# Use the encoder-backed store methods
store.mset([(1, 3.14), (2, 2.718)])
values = store.mget([1, 2])  # Retrieves [3.14, 2.718]
store.mdelete([1, 2])  # Deletes the keys 1 and 2
```

Function to serialize values from type `V` to bytes.

Function to deserialize bytes back to type V.