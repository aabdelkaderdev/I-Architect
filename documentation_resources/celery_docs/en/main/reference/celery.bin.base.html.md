<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.bin.base.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.bin.base.html).

# `celery.bin.base`

Click customizations for Celery.

class celery.bin.base.CLIContext(*app*, *no\_color*, *workdir*, *quiet=False*)[[source]](../_modules/celery/bin/base.html#CLIContext)
:   Context Object for the CLI.

    property ERROR

    property OK

    echo(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.echo)

    error(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.error)

    pretty(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty)

    pretty\_dict\_ok\_error(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty_dict_ok_error)

    pretty\_list(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty_list)

    say\_chat(*direction*, *title*, *body=''*, *show\_body=False*)[[source]](../_modules/celery/bin/base.html#CLIContext.say_chat)

    secho(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.secho)

    style(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.style)

class celery.bin.base.CeleryCommand(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")*, *context\_settings: [MutableMapping](https://docs.python.org/dev/library/collections.abc.html#collections.abc.MutableMapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callback: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[...], [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *params: [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[Parameter](https://click.palletsprojects.com/en/stable/api/#click.Parameter "(in Click v8.3.x)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *help: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *epilog: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *short\_help: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *options\_metavar: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = '[OPTIONS]'*, *add\_help\_option: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *no\_args\_is\_help: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *hidden: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *deprecated: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") | [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = False*)[[source]](../_modules/celery/bin/base.html#CeleryCommand)
:   Customized command for Celery.

    format\_options(*ctx*, *formatter*)[[source]](../_modules/celery/bin/base.html#CeleryCommand.format_options)
    :   Write all the options into the formatter if they exist.

class celery.bin.base.CeleryDaemonCommand(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryDaemonCommand)
:   Daemon commands.

class celery.bin.base.CeleryOption(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryOption)
:   Customized option for Celery.

    get\_default(*ctx*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryOption.get_default)
    :   Get the default for the parameter. Tries
        `Context.lookup_default()` first, then the local default.

        Parameters:
        :   - **ctx** – Current context.
            - **call** – If the default is a callable, call it. Disable to
              return the callable instead.

        Changed in version 8.0.2: Type casting is no longer performed when getting a default.

        Changed in version 8.0.1: Type casting can fail in resilient parsing mode. Invalid
        defaults will not prevent showing help text.

        Changed in version 8.0: Looks at `ctx.default_map` first.

        Changed in version 8.0: Added the `call` parameter.

class celery.bin.base.CommaSeparatedList[[source]](../_modules/celery/bin/base.html#CommaSeparatedList)
:   Comma separated list argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#CommaSeparatedList.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'comma separated list'
    :   the descriptive name of this type

class celery.bin.base.DaemonOption(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#DaemonOption)
:   Common daemonization option

    daemon\_setting(*ctx: [Context](https://click.palletsprojects.com/en/stable/api/#click.Context "(in Click v8.3.x)")*, *opt: [CeleryOption](#celery.bin.base.CeleryOption "celery.bin.base.CeleryOption")*, *value: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/bin/base.html#DaemonOption.daemon_setting)
    :   Try to fetch daemonization option from applications settings.
        Use the daemon command name as prefix (eg. worker -> worker\_pidfile)

class celery.bin.base.ISO8601DateTime[[source]](../_modules/celery/bin/base.html#ISO8601DateTime)
:   ISO 8601 Date Time argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#ISO8601DateTime.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'iso-86091'
    :   the descriptive name of this type

class celery.bin.base.ISO8601DateTimeOrFloat[[source]](../_modules/celery/bin/base.html#ISO8601DateTimeOrFloat)
:   ISO 8601 Date Time or float argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#ISO8601DateTimeOrFloat.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'iso-86091 or float'
    :   the descriptive name of this type

class celery.bin.base.JsonArray[[source]](../_modules/celery/bin/base.html#JsonArray)
:   JSON formatted array argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#JsonArray.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'json array'
    :   the descriptive name of this type

class celery.bin.base.JsonObject[[source]](../_modules/celery/bin/base.html#JsonObject)
:   JSON formatted object argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#JsonObject.convert)
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   - **value** – The value to convert.
            - **param** – The parameter that is using this type to convert
              its value. May be `None`.
            - **ctx** – The current context that arrived at this value. May
              be `None`.

    name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'json object'
    :   the descriptive name of this type

class celery.bin.base.LogLevel[[source]](../_modules/celery/bin/base.html#LogLevel)
:   Log level option.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#LogLevel.convert)
    :   For a given value from the parser, normalize it and find its
        matching normalized value in the list of choices. Then return the
        matched “original” choice.

celery.bin.base.handle\_preload\_options(*f*)[[source]](../_modules/celery/bin/base.html#handle_preload_options)
:   Extract preload options and return a wrapped callable.

celery.bin.base.handle\_remote\_command\_error(*command: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *exc: [Exception](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/bin/base.html#handle_remote_command_error)