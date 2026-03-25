<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.text.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.text.html).

# `celery.utils.text`

Text formatting utilities.

celery.utils.text.abbr(*S: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *max: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *ellipsis: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = '...'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#abbr)
:   Abbreviate word.

celery.utils.text.abbrtask(*S: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *max: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#abbrtask)
:   Abbreviate task name.

celery.utils.text.dedent(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\n'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#dedent)
:   Remove indentation.

celery.utils.text.dedent\_initial(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *n: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 4*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#dedent_initial)
:   Remove indentation from first line of text.

celery.utils.text.ensure\_newlines(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *n: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 2*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")
:   Ensure text s ends in separator sep’.

celery.utils.text.ensure\_sep(*sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *n: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 2*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#ensure_sep)
:   Ensure text s ends in separator sep’.

celery.utils.text.fill\_paragraphs(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *width: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\n'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#fill_paragraphs)
:   Fill paragraphs with newlines (or custom separator).

celery.utils.text.indent(*t: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *indent: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 0*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\n'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#indent)
:   Indent text.

celery.utils.text.join(*l: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\n'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#join)
:   Concatenate list of strings.

celery.utils.text.pluralize(*n: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")*, *text: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *suffix: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 's'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#pluralize)
:   Pluralize term when n is greater than one.

celery.utils.text.pretty(*value: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *width: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 80*, *nl\_width: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 80*, *sep: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\n'*, *\*\*kw: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#pretty)
:   Format value for printing to console.

celery.utils.text.simple\_format(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *keys: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")]*, *pattern: [Pattern](https://docs.python.org/dev/library/typing.html#typing.Pattern "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] = re.compile('%(\\w)')*, *expand: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '\\1'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#simple_format)
:   Format string, expanding abbreviations in keys’.

celery.utils.text.str\_to\_list(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../../_modules/celery/utils/text.html#str_to_list)
:   Convert string to list.

celery.utils.text.truncate(*s: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *maxlen: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 128*, *suffix: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = '...'*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/text.html#truncate)
:   Truncate text to a maximum number of characters.