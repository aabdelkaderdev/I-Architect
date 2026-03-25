<!-- Source: https://docs.celeryq.dev/projects/pytest-celery/en/latest/index.html -->

This document describes the current stable version of pytest\_celery (1.3).
For development docs,
[go here](https://pytest-celery.readthedocs.io/en/main/index.html).

# Official pytest plugin for Celery

Welcome to [pytest-celery](https://pypi.org/project/pytest-celery/), the official pytest plugin for Celery.

The pytest-celery plugin introduces significant enhancements with the introduction of
version >= 1.0.0, shifting towards a Docker-based approach for smoke and production-like testing.
While the celery.contrib.pytest API continues to support detailed integration
and unit testing, the new Docker-based methodology is tailored for testing in
environments that closely mirror production settings.

Adopting version >= 1.0.0 enriches your testing suite with these new capabilities
without affecting your existing tests, allowing for a smooth upgrade path.
The documentation here will navigate you through utilizing the Docker-based approach.
For information on the celery.contrib.pytest API for integration and unit testing,
please refer to the [official documentation](https://docs.celeryproject.org/en/latest/userguide/testing.html).

The pytest-celery plugin is Open Source and licensed under the [BSD License](https://www.opensource.org/license/BSD-3-Clause).

[Open Collective](https://opencollective.com/celery) is our community-powered funding platform that fuels Celery’s
ongoing development. Your sponsorship directly supports improvements, maintenance, and innovative features that keep
Celery robust and reliable.

## Getting Started

- If you’re new to pytest-celery you can get started by following the [Getting Started](getting-started/index.html#getting-started) tutorial.
- You can also check out the [FAQ](faq.html#faq).

## Contents

## Indices and tables

- [Index](genindex.html)
- [Module Index](py-modindex.html)
- [Search Page](search.html)