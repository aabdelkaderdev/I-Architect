<!-- Source: https://docs.celeryq.dev/en/main/internals/reference/celery.utils.term.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.term.html).

# `celery.utils.term`

Terminals and colors.

class celery.utils.term.colored(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/term.html#colored)
:   Terminal colored text.

    Example

    ```
    >>> c = colored(enabled=True)
    >>> print(str(c.red('the quick '), c.blue('brown ', c.bold('fox ')),
    ...       c.magenta(c.underline('jumps over')),
    ...       c.yellow(' the lazy '),
    ...       c.green('dog ')))
    ```

    black(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.black)

    blink(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.blink)

    blue(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.blue)

    bold(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.bold)

    bright(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.bright)

    cyan(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.cyan)

    embed() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/term.html#colored.embed)

    green(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.green)

    iblue(*\*s: [colored](#celery.utils.term.colored "celery.utils.term.colored")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iblue)

    icyan(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.icyan)

    igreen(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.igreen)

    imagenta(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.imagenta)

    ired(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.ired)

    iwhite(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iwhite)

    iyellow(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iyellow)

    magenta(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.magenta)

    no\_color() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/term.html#colored.no_color)

    node(*s: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)"), ...]*, *op: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.node)

    red(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.red)

    reset(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.reset)

    reverse(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.reverse)

    underline(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.underline)

    white(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.white)

    yellow(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.yellow)