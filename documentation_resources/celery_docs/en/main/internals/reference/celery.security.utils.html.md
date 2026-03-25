<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.security.utils.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.utils.html).

# `celery.security.utils`

Utilities used by the message signing serializer.

celery.security.utils.get\_digest\_algorithm(*digest='sha256'*)[[source]](../../_modules/celery/security/utils.html#get_digest_algorithm)
:   Convert string to hash object of cryptography library.

celery.security.utils.reraise\_errors(*msg='{0!r}'*, *errors=None*)[[source]](../../_modules/celery/security/utils.html#reraise_errors)
:   Context reraising crypto errors as `SecurityError`.