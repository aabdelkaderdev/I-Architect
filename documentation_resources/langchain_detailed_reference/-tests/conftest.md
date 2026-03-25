<!-- Source: https://reference.langchain.com/python/langchain-tests/conftest -->

Modulev1.1.4 (latest)●Since v1.1

# conftest

Pytest conftest.

## Functions

[function

base\_vcr\_config](/python/langchain-tests/conftest/base_vcr_config)[function

vcr\_config](/python/langchain-tests/conftest/vcr_config)

## Classes

[class

CustomSerializer](/python/langchain-tests/conftest/CustomSerializer)[class

CustomPersister](/python/langchain-tests/conftest/CustomPersister)



Return VCR configuration that every cassette will receive.

(Anything permitted by `vcr.VCR(**kwargs)` can be put here.)

VCR config fixture.

Custom serializer for VCR cassettes using YAML and gzip.

We're using a custom serializer to avoid the default yaml serializer
used by VCR, which is not designed to be safe for untrusted input.

This step is an extra precaution necessary because the cassette files
are in compressed YAML format, which makes it more difficult to inspect
their contents during development or debugging.

A custom persister for VCR that uses the `CustomSerializer`.