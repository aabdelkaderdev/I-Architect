<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/encoder_backed -->

Modulev1.2.13 (latest)●Since v1.0

# encoder\_backed

## Attributes

[attribute

K](/python/langchain-classic/storage/encoder_backed/K)[attribute

V](/python/langchain-classic/storage/encoder_backed/V)

## Classes

[class

EncoderBackedStore

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
```](/python/langchain-classic/storage/encoder_backed/EncoderBackedStore)


