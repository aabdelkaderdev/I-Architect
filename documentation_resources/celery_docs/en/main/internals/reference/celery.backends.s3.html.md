<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.backends.s3.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.s3.html).

# `celery.backends.s3`

s3 result store backend.

class celery.backends.s3.S3Backend(*\*\*kwargs*)[[source]](../../_modules/celery/backends/s3.html#S3Backend)
:   An S3 task result store.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/boto3/> is not available,
        if the `aws_access_key_id` or
        setting:aws\_secret\_access\_key are not set,
        or it the `bucket` is not set.

    delete(*key*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.delete)

    get(*key*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.get)

    set(*key*, *value*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.set)