<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.iso8601.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.iso8601.html).

# `celery.utils.iso8601`

Parse ISO8601 dates.

Originally taken from <https://pypi.org/project/pyiso8601/>
(<https://bitbucket.org/micktwomey/pyiso8601>)

Modified to match the behavior of `dateutil.parser`:

> - raise [`ValueError`](https://docs.python.org/dev/library/exceptions.html#ValueError "(in Python v3.15)") instead of `ParseError`
> - return naive [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") by default

This is the original License:

Copyright (c) 2007 Michael Twomey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sub-license, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

celery.utils.iso8601.parse\_iso8601(*datestring: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/iso8601.html#parse_iso8601)
:   Parse and convert ISO-8601 string to datetime.