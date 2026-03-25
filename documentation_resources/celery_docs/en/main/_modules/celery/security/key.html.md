<!-- Source: https://docs.celeryq.dev/en/main/_modules/celery/security/key.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/_modules/celery/security/key.html).

# Source code for celery.security.key

```
"""Private keys for the security serializer."""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from kombu.utils.encoding import ensure_bytes

from .utils import reraise_errors

__all__ = ('PrivateKey',)

[docs]
class PrivateKey:
    """Represents a private key."""

    def __init__(self, key, password=None):
        with reraise_errors(
            'Invalid private key: {0!r}', errors=(ValueError,)
        ):
            self._key = serialization.load_pem_private_key(
                ensure_bytes(key),
                password=ensure_bytes(password),
                backend=default_backend())

            if not isinstance(self._key, rsa.RSAPrivateKey):
                raise ValueError("Non-RSA keys are not supported.")

[docs]
    def sign(self, data, digest):
        """Sign string containing data."""
        with reraise_errors('Unable to sign data: {0!r}'):

            pad = padding.PSS(
                mgf=padding.MGF1(digest),
                salt_length=padding.PSS.MAX_LENGTH)

            return self._key.sign(ensure_bytes(data), pad, digest)
```