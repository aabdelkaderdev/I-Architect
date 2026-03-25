<!-- Source: https://jinja.palletsprojects.com/en/stable/integration/ -->

# Integration

## Flask

The [Flask](https://flask.palletsprojects.com) web application framework, also maintained by Pallets, uses
Jinja templates by default. Flask sets up a Jinja environment and
template loader for you, and provides functions to easily render
templates from view functions.

## Django

Django supports using Jinja as its template engine, see
<https://docs.djangoproject.com/en/stable/topics/templates/#support-for-template-engines>.

## Babel

Jinja provides support for extracting gettext messages from templates
via a [Babel](https://babel.readthedocs.io/) extractor entry point called
`jinja2.ext.babel_extract`. The support is implemented as part of the
[i18n Extension](../extensions/#i18n-extension) extension.

Gettext messages are extracted from both `trans` tags and code
expressions.

To extract gettext messages from templates, the project needs a Jinja
section in its Babel extraction method [mapping file](https://babel.readthedocs.io/en/latest/messages.html#extraction-method-mapping-and-configuration):

```
[jinja2: **/templates/**.html]
encoding = utf-8
```

The syntax related options of the `Environment` are also
available as configuration values in the mapping file. For example, to
tell the extractor that templates use `%` as
`line_statement_prefix` you can use this code:

```
[jinja2: **/templates/**.html]
encoding = utf-8
line_statement_prefix = %
```

[Extensions](../extensions/#jinja-extensions) may also be defined by passing a comma separated
list of import paths as the `extensions` value. The i18n extension is
added automatically.

Template syntax errors are ignored by default. The assumption is that
tests will catch syntax errors in templates. If you don’t want to ignore
errors, add `silent = false` to the settings.

## Pylons

It’s easy to integrate Jinja into a [Pylons](https://pylonsproject.org/) application.

The template engine is configured in `config/environment.py`. The
configuration for Jinja looks something like this:

```
from jinja2 import Environment, PackageLoader
config['pylons.app_globals'].jinja_env = Environment(
    loader=PackageLoader('yourapplication', 'templates')
)
```

After that you can render Jinja templates by using the `render_jinja`
function from the `pylons.templating` module.

Additionally it’s a good idea to set the Pylons `c` object to strict
mode. By default attribute access on missing attributes on the `c`
object returns an empty string and not an undefined object. To change
this add this to `config/environment.py`:

```
config['pylons.strict_c'] = True
```