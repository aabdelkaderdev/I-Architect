<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.security.serialization.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.serialization.html).

# `celery.security.serialization`

Secure serializer.

class celery.security.serialization.SecureSerializer(*key=None*, *cert=None*, *cert\_store=None*, *digest='sha256'*, *serializer='json'*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer)
:   Signed serializer.

    deserialize(*data*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer.deserialize)
    :   Deserialize data structure from string.

    serialize(*data*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer.serialize)
    :   Serialize data structure into string.

celery.security.serialization.register\_auth(*key=None*, *key\_password=None*, *cert=None*, *store=None*, *digest='sha256'*, *serializer='json'*)[[source]](../../_modules/celery/security/serialization.html#register_auth)
:   Register security serializer.