<!-- Source: https://reference.langchain.com/python/langchain-tests/conftest/CustomSerializer -->

Classv1.1.4 (latest)●Since v1.1

# CustomSerializer

Custom serializer for VCR cassettes using YAML and gzip.

We're using a custom serializer to avoid the default yaml serializer
used by VCR, which is not designed to be safe for untrusted input.

This step is an extra precaution necessary because the cassette files
are in compressed YAML format, which makes it more difficult to inspect
their contents during development or debugging.


```
CustomSerializer()
```

## Methods

[method

serialize

Convert cassette to YAML and compress it.](/python/langchain-tests/conftest/CustomSerializer/serialize)[method

deserialize

Decompress data and convert it from YAML.](/python/langchain-tests/conftest/CustomSerializer/deserialize)


