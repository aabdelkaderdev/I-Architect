<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.app.utils.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.utils.html).

# `celery.app.utils`

App utilities: Compat settings, bug-report tool, pickling apps.

class celery.app.utils.Settings(*\*args*, *deprecated\_settings=None*, *\*\*kwargs*)[[source]](../_modules/celery/app/utils.html#Settings)
:   Celery settings object.

    property broker\_read\_url

    property broker\_url

    property broker\_write\_url

    finalize()[[source]](../_modules/celery/app/utils.html#Settings.finalize)

    find\_option(*name*, *namespace=''*)[[source]](../_modules/celery/app/utils.html#Settings.find_option)
    :   Search for option by name.

        Example

        ```
        >>> from proj.celery import app
        >>> app.conf.find_option('disable_rate_limits')
        ('worker', 'prefetch_multiplier',
         <Option: type->bool default->False>))
        ```

        Parameters:
        :   - **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of option, cannot be partial.
            - **namespace** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Preferred name-space (`None` by default).

        Returns:
        :   of `(namespace, key, type)`.

        Return type:
        :   Tuple

    find\_value\_for\_key(*name*, *namespace='celery'*)[[source]](../_modules/celery/app/utils.html#Settings.find_value_for_key)
    :   Shortcut to `get_by_parts(*find_option(name)[:-1])`.

    get\_by\_parts(*\*parts*)[[source]](../_modules/celery/app/utils.html#Settings.get_by_parts)
    :   Return the current value for setting specified as a path.

        Example

        ```
        >>> from proj.celery import app
        >>> app.conf.get_by_parts('worker', 'disable_rate_limits')
        False
        ```

    humanize(*with\_defaults=False*, *censored=True*)[[source]](../_modules/celery/app/utils.html#Settings.humanize)
    :   Return a human readable text showing configuration changes.

    maybe\_warn\_deprecated\_settings()[[source]](../_modules/celery/app/utils.html#Settings.maybe_warn_deprecated_settings)

    property result\_backend

    table(*with\_defaults=False*, *censored=True*)[[source]](../_modules/celery/app/utils.html#Settings.table)

    property task\_default\_exchange

    property task\_default\_routing\_key

    property timezone

    value\_set\_for(*key*)[[source]](../_modules/celery/app/utils.html#Settings.value_set_for)

    without\_defaults()[[source]](../_modules/celery/app/utils.html#Settings.without_defaults)
    :   Return the current configuration, but without defaults.

celery.app.utils.appstr(*app*)[[source]](../_modules/celery/app/utils.html#appstr)
:   String used in \_\_repr\_\_ etc, to id app instances.

celery.app.utils.bugreport(*app*)[[source]](../_modules/celery/app/utils.html#bugreport)
:   Return a string containing information useful in bug-reports.

celery.app.utils.filter\_hidden\_settings(*conf*)[[source]](../_modules/celery/app/utils.html#filter_hidden_settings)
:   Filter sensitive settings.

celery.app.utils.find\_app(*app*, *symbol\_by\_name=<function symbol\_by\_name>*, *imp=<function import\_from\_cwd>*)[[source]](../_modules/celery/app/utils.html#find_app)
:   Find app by name.