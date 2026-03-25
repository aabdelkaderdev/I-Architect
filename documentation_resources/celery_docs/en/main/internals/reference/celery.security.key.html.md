<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.security.key.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.key.html).

# `celery.security.key`

Private keys for the security serializer.

class celery.security.key.PrivateKey(*key*, *password=None*)[[source]](../../_modules/celery/security/key.html#PrivateKey)
:   Represents a private key.

    sign(*data*, *digest*)[[source]](../../_modules/celery/security/key.html#PrivateKey.sign)
    :   Sign string containing data.