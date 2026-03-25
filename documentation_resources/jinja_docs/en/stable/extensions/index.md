<!-- Source: https://jinja.palletsprojects.com/en/stable/extensions/ -->

# Extensions

Jinja supports extensions that can add extra filters, tests, globals or even
extend the parser. The main motivation of extensions is to move often used
code into a reusable class like adding support for internationalization.

## Adding Extensions

Extensions are added to the Jinja environment at creation time. To add an
extension pass a list of extension classes or import paths to the
`extensions` parameter of the [`Environment`](../api/#jinja2.Environment "jinja2.Environment") constructor. The following
example creates a Jinja environment with the i18n extension loaded:

```
jinja_env = Environment(extensions=['jinja2.ext.i18n'])
```

To add extensions after creation time, use the [`add_extension()`](../api/#jinja2.Environment.add_extension "jinja2.Environment.add_extension") method:

```
jinja_env.add_extension('jinja2.ext.debug')
```

## i18n Extension

**Import name:** `jinja2.ext.i18n`

The i18n extension can be used in combination with [gettext](https://docs.python.org/3/library/gettext.html) or
[Babel](https://babel.pocoo.org/). When it’s enabled, Jinja provides a `trans` statement that
marks a block as translatable and calls `gettext`.

After enabling, an application has to provide functions for `gettext`,
`ngettext`, and optionally `pgettext` and `npgettext`, either
globally or when rendering. A `_()` function is added as an alias to
the `gettext` function.

A convenient way to provide these functions is to call one of the below
methods depending on the translation system in use. If you do not require
actual translation, use `Environment.install_null_translations` to
install no-op functions.

### Environment Methods

After enabling the extension, the environment provides the following
additional methods:

jinja2.Environment.install\_gettext\_translations(*translations*, *newstyle=False*)
:   Installs a translation globally for the environment. The
    `translations` object must implement `gettext`, `ngettext`,
    and optionally `pgettext` and `npgettext`.
    [`gettext.NullTranslations`](https://docs.python.org/3/library/gettext.html#gettext.NullTranslations "(in Python v3.13)"), [`gettext.GNUTranslations`](https://docs.python.org/3/library/gettext.html#gettext.GNUTranslations "(in Python v3.13)"),
    and [Babel](https://babel.pocoo.org/)s `Translations` are supported.

    Changelog

    Changed in version 3.0: Added `pgettext` and `npgettext`.

    Changed in version 2.5: Added new-style gettext support.

jinja2.Environment.install\_null\_translations(*newstyle=False*)
:   Install no-op gettext functions. This is useful if you want to
    prepare the application for internationalization but don’t want to
    implement the full system yet.

    Changelog

    Changed in version 2.5: Added new-style gettext support.

jinja2.Environment.install\_gettext\_callables(*gettext*, *ngettext*, *newstyle=False*, *pgettext=None*, *npgettext=None*)
:   Install the given `gettext`, `ngettext`, `pgettext`, and
    `npgettext` callables into the environment. They should behave
    exactly like [`gettext.gettext()`](https://docs.python.org/3/library/gettext.html#gettext.gettext "(in Python v3.13)"), [`gettext.ngettext()`](https://docs.python.org/3/library/gettext.html#gettext.ngettext "(in Python v3.13)"),
    [`gettext.pgettext()`](https://docs.python.org/3/library/gettext.html#gettext.pgettext "(in Python v3.13)") and [`gettext.npgettext()`](https://docs.python.org/3/library/gettext.html#gettext.npgettext "(in Python v3.13)").

    If `newstyle` is activated, the callables are wrapped to work like
    newstyle callables. See [New Style Gettext](#newstyle-gettext) for more information.

    Changelog

    Changed in version 3.0: Added `pgettext` and `npgettext`.

    Added in version 2.5: Added new-style gettext support.

jinja2.Environment.uninstall\_gettext\_translations()
:   Uninstall the environment’s globally installed translation.

jinja2.Environment.extract\_translations(*source*)
:   Extract localizable strings from the given template node or source.

    For every string found this function yields a `(lineno, function,
    message)` tuple, where:

    - `lineno` is the number of the line on which the string was
      found.
    - `function` is the name of the `gettext` function used (if
      the string was extracted from embedded Python code).
    - `message` is the string itself, or a tuple of strings for
      functions with multiple arguments.

    If [Babel](https://babel.pocoo.org/) is installed, see [Babel](../integration/#babel-integration) to extract
    the strings.

For a web application that is available in multiple languages but gives
all the users the same language (for example, multilingual forum
software installed for a French community), the translation may be
installed when the environment is created.

```
translations = get_gettext_translations()
env = Environment(extensions=["jinja2.ext.i18n"])
env.install_gettext_translations(translations)
```

The `get_gettext_translations` function would return the translator
for the current configuration, for example by using `gettext.find`.

The usage of the `i18n` extension for template designers is covered in
[the template documentation](../templates/#i18n-in-templates).

### Whitespace Trimming

Changelog

Added in version 2.10.

Within `{% trans %}` blocks, it can be useful to trim line breaks and
whitespace so that the block of text looks like a simple string with
single spaces in the translation file.

Linebreaks and surrounding whitespace can be automatically trimmed by
enabling the `ext.i18n.trimmed` [policy](../api/#ext-i18n-trimmed).

### New Style Gettext

Changelog

Added in version 2.5.

New style gettext calls are less to type, less error prone, and support
autoescaping better.

You can use “new style” gettext calls by setting
`env.newstyle_gettext = True` or passing `newstyle=True` to
`env.install_translations`. They are fully supported by the Babel
extraction tool, but might not work as expected with other extraction
tools.

With standard `gettext` calls, string formatting is a separate step
done with the `|format` filter. This requires duplicating work for
`ngettext` calls.

```
{{ gettext("Hello, World!") }}
{{ gettext("Hello, %(name)s!")|format(name=name) }}
{{ ngettext(
       "%(num)d apple", "%(num)d apples", apples|count
   )|format(num=apples|count) }}
{{ pgettext("greeting", "Hello, World!") }}
{{ npgettext(
       "fruit", "%(num)d apple", "%(num)d apples", apples|count
   )|format(num=apples|count) }}
```

New style `gettext` make formatting part of the call, and behind the
scenes enforce more consistency.

```
{{ gettext("Hello, World!") }}
{{ gettext("Hello, %(name)s!", name=name) }}
{{ ngettext("%(num)d apple", "%(num)d apples", apples|count) }}
{{ pgettext("greeting", "Hello, World!") }}
{{ npgettext("fruit", "%(num)d apple", "%(num)d apples", apples|count) }}
```

The advantages of newstyle gettext are:

- There’s no separate formatting step, you don’t have to remember to
  use the `|format` filter.
- Only named placeholders are allowed. This solves a common problem
  translators face because positional placeholders can’t switch
  positions meaningfully. Named placeholders always carry semantic
  information about what value goes where.
- String formatting is used even if no placeholders are used, which
  makes all strings use a consistent format. Remember to escape any
  raw percent signs as `%%`, such as `100%%`.
- The translated string is marked safe, formatting performs escaping
  as needed. Mark a parameter as `|safe` if it has already been
  escaped.

## Expression Statement

**Import name:** `jinja2.ext.do`

The “do” aka expression-statement extension adds a simple `do` tag to the
template engine that works like a variable expression but ignores the
return value.

## Loop Controls

**Import name:** `jinja2.ext.loopcontrols`

This extension adds support for `break` and `continue` in loops. After
enabling, Jinja provides those two keywords which work exactly like in
Python.

## With Statement

**Import name:** `jinja2.ext.with_`

Changelog

Changed in version 2.9: This extension is now built-in and no longer does anything.

## Autoescape Extension

**Import name:** `jinja2.ext.autoescape`

Changelog

Changed in version 2.9: This extension was removed and is now built-in. Enabling the
extension no longer does anything.

## Debug Extension

**Import name:** `jinja2.ext.debug`

Adds a `{% debug %}` tag to dump the current context as well as the
available filters and tests. This is useful to see what’s available to
use in the template without setting up a debugger.

## Writing Extensions

By writing extensions you can add custom tags to Jinja. This is a non-trivial
task and usually not needed as the default tags and expressions cover all
common use cases. The i18n extension is a good example of why extensions are
useful. Another one would be fragment caching.

When writing extensions you have to keep in mind that you are working with the
Jinja template compiler which does not validate the node tree you are passing
to it. If the AST is malformed you will get all kinds of compiler or runtime
errors that are horrible to debug. Always make sure you are using the nodes
you create correctly. The API documentation below shows which nodes exist and
how to use them.

## Example Extensions

### Cache

The following example implements a `cache` tag for Jinja by using the
[cachelib](https://github.com/pallets/cachelib) library:

```
from jinja2 import nodes
from jinja2.ext import Extension

class FragmentCacheExtension(Extension):
    # a set of names that trigger the extension.
    tags = {"cache"}

    def __init__(self, environment):
        super().__init__(environment)

        # add the defaults to the environment
        environment.extend(fragment_cache_prefix="", fragment_cache=None)

    def parse(self, parser):
        # the first token is the token that started the tag.  In our case
        # we only listen to ``'cache'`` so this will be a name token with
        # `cache` as value.  We get the line number so that we can give
        # that line number to the nodes we create by hand.
        lineno = next(parser.stream).lineno

        # now we parse a single expression that is used as cache key.
        args = [parser.parse_expression()]

        # if there is a comma, the user provided a timeout.  If not use
        # None as second parameter.
        if parser.stream.skip_if("comma"):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to `endcache` and
        # drop the needle (which would always be `endcache` in that case)
        body = parser.parse_statements(["name:endcache"], drop_needle=True)

        # now return a `CallBlock` node that calls our _cache_support
        # helper method on this extension.
        return nodes.CallBlock(
            self.call_method("_cache_support", args), [], [], body
        ).set_lineno(lineno)

    def _cache_support(self, name, timeout, caller):
        """Helper callback."""
        key = self.environment.fragment_cache_prefix + name

        # try to load the block from the cache
        # if there is no fragment in the cache, render it and store
        # it in the cache.
        rv = self.environment.fragment_cache.get(key)
        if rv is not None:
            return rv
        rv = caller()
        self.environment.fragment_cache.add(key, rv, timeout)
        return rv
```

And here is how you use it in an environment:

```
from jinja2 import Environment
from cachelib import SimpleCache

env = Environment(extensions=[FragmentCacheExtension])
env.fragment_cache = SimpleCache()
```

Inside the template it’s then possible to mark blocks as cacheable. The
following example caches a sidebar for 300 seconds:

```
{% cache 'sidebar', 300 %}
<div class="sidebar">
    ...
</div>
{% endcache %}
```

### Inline `gettext`

The following example demonstrates using [`Extension.filter_stream()`](#jinja2.ext.Extension.filter_stream "jinja2.ext.Extension.filter_stream")
to parse calls to the `_()` gettext function inline with static data
without needing Jinja blocks.

```
<h1>_(Welcome)</h1>
<p>_(This is a paragraph)</p>
```

It requires the i18n extension to be loaded and configured.

```
import re

from jinja2.exceptions import TemplateSyntaxError
from jinja2.ext import Extension
from jinja2.lexer import count_newlines
from jinja2.lexer import Token

_outside_re = re.compile(r"\\?(gettext|_)\(")
_inside_re = re.compile(r"\\?[()]")

class InlineGettext(Extension):
    """This extension implements support for inline gettext blocks::

        <h1>_(Welcome)</h1>
        <p>_(This is a paragraph)</p>

    Requires the i18n extension to be loaded and configured.
    """

    def filter_stream(self, stream):
        paren_stack = 0

        for token in stream:
            if token.type != "data":
                yield token
                continue

            pos = 0
            lineno = token.lineno

            while True:
                if not paren_stack:
                    match = _outside_re.search(token.value, pos)
                else:
                    match = _inside_re.search(token.value, pos)
                if match is None:
                    break
                new_pos = match.start()
                if new_pos > pos:
                    preval = token.value[pos:new_pos]
                    yield Token(lineno, "data", preval)
                    lineno += count_newlines(preval)
                gtok = match.group()
                if gtok[0] == "\\":
                    yield Token(lineno, "data", gtok[1:])
                elif not paren_stack:
                    yield Token(lineno, "block_begin", None)
                    yield Token(lineno, "name", "trans")
                    yield Token(lineno, "block_end", None)
                    paren_stack = 1
                else:
                    if gtok == "(" or paren_stack > 1:
                        yield Token(lineno, "data", gtok)
                    paren_stack += -1 if gtok == ")" else 1
                    if not paren_stack:
                        yield Token(lineno, "block_begin", None)
                        yield Token(lineno, "name", "endtrans")
                        yield Token(lineno, "block_end", None)
                pos = match.end()

            if pos < len(token.value):
                yield Token(lineno, "data", token.value[pos:])

        if paren_stack:
            raise TemplateSyntaxError(
                "unclosed gettext expression",
                token.lineno,
                stream.name,
                stream.filename,
            )
```

## Extension API

### Extension

Extensions always have to extend the [`jinja2.ext.Extension`](#jinja2.ext.Extension "jinja2.ext.Extension") class:

*class* jinja2.ext.Extension(*environment*)
:   Extensions can be used to add extra functionality to the Jinja template
    system at the parser level. Custom extensions are bound to an environment
    but may not store environment specific data on `self`. The reason for
    this is that an extension can be bound to another environment (for
    overlays) by creating a copy and reassigning the `environment` attribute.

    As extensions are created by the environment they cannot accept any
    arguments for configuration. One may want to work around that by using
    a factory function, but that is not possible as extensions are identified
    by their import name. The correct way to configure the extension is
    storing the configuration values on the environment. Because this way the
    environment ends up acting as central configuration storage the
    attributes may clash which is why extensions have to ensure that the names
    they choose for configuration are not too generic. `prefix` for example
    is a terrible name, `fragment_cache_prefix` on the other hand is a good
    name as includes the name of the extension (fragment cache).

    Parameters:
    :   **environment** ([*Environment*](../api/#jinja2.Environment "jinja2.environment.Environment"))

    identifier
    :   The identifier of the extension. This is always the true import name
        of the extension class and must not be changed.

    tags
    :   If the extension implements custom tags this is a set of tag names
        the extension is listening for.

    preprocess(*source*, *name*, *filename=None*)
    :   This method is called before the actual lexing and can be used to
        preprocess the source. The `filename` is optional. The return value
        must be the preprocessed source.

        Parameters:
        :   - **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
            - **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
            - **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)

        Return type:
        :   [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")

    filter\_stream(*stream*)
    :   It’s passed a [`TokenStream`](#jinja2.lexer.TokenStream "jinja2.lexer.TokenStream") that can be used
        to filter tokens returned. This method has to return an iterable of
        [`Token`](#jinja2.lexer.Token "jinja2.lexer.Token")s, but it doesn’t have to return a
        [`TokenStream`](#jinja2.lexer.TokenStream "jinja2.lexer.TokenStream").

        Parameters:
        :   **stream** ([*TokenStream*](#jinja2.lexer.TokenStream "jinja2.lexer.TokenStream"))

        Return type:
        :   [TokenStream](#jinja2.lexer.TokenStream "jinja2.lexer.TokenStream") | [*Iterable*](https://docs.python.org/3/library/typing.html#typing.Iterable "(in Python v3.13)")[[Token](#jinja2.lexer.Token "jinja2.lexer.Token")]

    parse(*parser*)
    :   If any of the [`tags`](#jinja2.ext.Extension.tags "jinja2.ext.Extension.tags") matched this method is called with the
        parser as first argument. The token the parser stream is pointing at
        is the name token that matched. This method has to return one or a
        list of multiple nodes.

        Parameters:
        :   **parser** ([*Parser*](#jinja2.parser.Parser "jinja2.parser.Parser"))

        Return type:
        :   [*Node*](#jinja2.nodes.Node "jinja2.nodes.Node") | [*List*](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.13)")[[*Node*](#jinja2.nodes.Node "jinja2.nodes.Node")]

    attr(*name*, *lineno=None*)
    :   Return an attribute node for the current extension. This is useful
        to pass constants on extensions to generated template code.

        ```
        self.attr('_my_attribute', lineno=lineno)
        ```

        Parameters:
        :   - **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
            - **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)") *|* *None*)

        Return type:
        :   [*ExtensionAttribute*](#jinja2.nodes.ExtensionAttribute "jinja2.nodes.ExtensionAttribute")

    call\_method(*name*, *args=None*, *kwargs=None*, *dyn\_args=None*, *dyn\_kwargs=None*, *lineno=None*)
    :   Call a method of the extension. This is a shortcut for
        [`attr()`](#jinja2.ext.Extension.attr "jinja2.ext.Extension.attr") + [`jinja2.nodes.Call`](#jinja2.nodes.Call "jinja2.nodes.Call").

        Parameters:
        :   - **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
            - **args** ([*List*](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.13)")*[*[*Expr*](#jinja2.nodes.Expr "jinja2.nodes.Expr")*]* *|* *None*)
            - **kwargs** ([*List*](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.13)")*[*[*Keyword*](#jinja2.nodes.Keyword "jinja2.nodes.Keyword")*]* *|* *None*)
            - **dyn\_args** ([*Expr*](#jinja2.nodes.Expr "jinja2.nodes.Expr") *|* *None*)
            - **dyn\_kwargs** ([*Expr*](#jinja2.nodes.Expr "jinja2.nodes.Expr") *|* *None*)
            - **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)") *|* *None*)

        Return type:
        :   [*Call*](#jinja2.nodes.Call "jinja2.nodes.Call")

### Parser

The parser passed to [`Extension.parse()`](#jinja2.ext.Extension.parse "jinja2.ext.Extension.parse") provides ways to parse
expressions of different types. The following methods may be used by
extensions:

*class* jinja2.parser.Parser(*environment*, *source*, *name=None*, *filename=None*, *state=None*)
:   This is the central parsing class Jinja uses. It’s passed to
    extensions and can be used to parse expressions or statements.

    Parameters:
    :   - **environment** ([*Environment*](../api/#jinja2.Environment "jinja2.Environment"))
        - **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **state** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)

    filename
    :   The filename of the template the parser processes. This is **not**
        the load name of the template. For the load name see [`name`](#jinja2.parser.Parser.name "jinja2.parser.Parser.name").
        For templates that were not loaded form the file system this is
        `None`.

    name
    :   The load name of the template.

    stream
    :   The current [`TokenStream`](#jinja2.lexer.TokenStream "jinja2.lexer.TokenStream")

    fail(*msg*, *lineno=None*, *exc=TemplateSyntaxError*)
    :   Convenience method that raises `exc` with the message, passed
        line number or last line number as well as the current name and
        filename.

        Parameters:
        :   - **msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
            - **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)") *|* *None*)
            - **exc** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[*[*TemplateSyntaxError*](../api/#jinja2.TemplateSyntaxError "jinja2.exceptions.TemplateSyntaxError")*]*)

        Return type:
        :   te.NoReturn

    free\_identifier(*lineno=None*)
    :   Return a new free identifier as [`InternalName`](#jinja2.nodes.InternalName "jinja2.nodes.InternalName").

        Parameters:
        :   **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)") *|* *None*)

        Return type:
        :   [*InternalName*](#jinja2.nodes.InternalName "jinja2.nodes.InternalName")

    parse\_statements(*end\_tokens*, *drop\_needle=False*)
    :   Parse multiple statements into a list until one of the end tokens
        is reached. This is used to parse the body of statements as it also
        parses template data if appropriate. The parser checks first if the
        current token is a colon and skips it if there is one. Then it checks
        for the block end and parses until if one of the `end_tokens` is
        reached. Per default the active token in the stream at the end of
        the call is the matched end token. If this is not wanted `drop_needle`
        can be set to `True` and the end token is removed.

        Parameters:
        :   - **end\_tokens** ([*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*,* *...**]*)
            - **drop\_needle** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

        Return type:
        :   [*List*](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.13)")[[*Node*](#jinja2.nodes.Node "jinja2.nodes.Node")]

    parse\_assign\_target(*with\_tuple=True*, *name\_only=False*, *extra\_end\_rules=None*, *with\_namespace=False*)
    :   Parse an assignment target. As Jinja allows assignments to
        tuples, this function can parse all allowed assignment targets. Per
        default assignments to tuples are parsed, that can be disable however
        by setting `with_tuple` to `False`. If only assignments to names are
        wanted `name_only` can be set to `True`. The `extra_end_rules`
        parameter is forwarded to the tuple parsing function. If
        `with_namespace` is enabled, a namespace assignment may be parsed.

        Parameters:
        :   - **with\_tuple** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
            - **name\_only** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
            - **extra\_end\_rules** ([*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*,* *...**]* *|* *None*)
            - **with\_namespace** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

        Return type:
        :   [*NSRef*](#jinja2.nodes.NSRef "jinja2.nodes.NSRef") | [*Name*](#jinja2.nodes.Name "jinja2.nodes.Name") | [*Tuple*](#jinja2.nodes.Tuple "jinja2.nodes.Tuple")

    parse\_expression(*with\_condexpr=True*)
    :   Parse an expression. Per default all expressions are parsed, if
        the optional `with_condexpr` parameter is set to `False` conditional
        expressions are not parsed.

        Parameters:
        :   **with\_condexpr** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

        Return type:
        :   [*Expr*](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    parse\_tuple(*simplified=False*, *with\_condexpr=True*, *extra\_end\_rules=None*, *explicit\_parentheses=False*, *with\_namespace=False*)
    :   Works like `parse_expression` but if multiple expressions are
        delimited by a comma a [`Tuple`](#jinja2.nodes.Tuple "jinja2.nodes.Tuple") node is created.
        This method could also return a regular expression instead of a tuple
        if no commas where found.

        The default parsing mode is a full tuple. If `simplified` is `True`
        only names and literals are parsed; `with_namespace` allows namespace
        attr refs as well. The `no_condexpr` parameter is forwarded to
        [`parse_expression()`](#jinja2.parser.Parser.parse_expression "jinja2.parser.Parser.parse_expression").

        Because tuples do not require delimiters and may end in a bogus comma
        an extra hint is needed that marks the end of a tuple. For example
        for loops support tuples between `for` and `in`. In that case the
        `extra_end_rules` is set to `['name:in']`.

        `explicit_parentheses` is true if the parsing was triggered by an
        expression in parentheses. This is used to figure out if an empty
        tuple is a valid expression or not.

        Parameters:
        :   - **simplified** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
            - **with\_condexpr** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
            - **extra\_end\_rules** ([*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*,* *...**]* *|* *None*)
            - **explicit\_parentheses** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
            - **with\_namespace** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

        Return type:
        :   [*Tuple*](#jinja2.nodes.Tuple "jinja2.nodes.Tuple") | [*Expr*](#jinja2.nodes.Expr "jinja2.nodes.Expr")

*class* jinja2.lexer.TokenStream(*generator*, *name*, *filename*)
:   A token stream is an iterable that yields [`Token`](#jinja2.lexer.Token "jinja2.lexer.Token")s. The
    parser however does not iterate over it but calls `next()` to go
    one token ahead. The current active token is stored as [`current`](#jinja2.lexer.TokenStream.current "jinja2.lexer.TokenStream.current").

    Parameters:
    :   - **generator** ([*Iterable*](https://docs.python.org/3/library/typing.html#typing.Iterable "(in Python v3.13)")*[*[*Token*](#jinja2.lexer.Token "jinja2.lexer.Token")*]*)
        - **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)

    current
    :   The current [`Token`](#jinja2.lexer.Token "jinja2.lexer.Token").

    *property* eos*: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")*
    :   Are we at the end of the stream?

    push(*token*)
    :   Push a token back to the stream.

        Parameters:
        :   **token** ([*Token*](#jinja2.lexer.Token "jinja2.lexer.Token"))

        Return type:
        :   None

    look()
    :   Look at the next token.

        Return type:
        :   [*Token*](#jinja2.lexer.Token "jinja2.lexer.Token")

    skip(*n=1*)
    :   Got n tokens ahead.

        Parameters:
        :   **n** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)"))

        Return type:
        :   None

    next\_if(*expr*)
    :   Perform the token test and return the token if it matched.
        Otherwise the return value is `None`.

        Parameters:
        :   **expr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [*Token*](#jinja2.lexer.Token "jinja2.lexer.Token") | None

    skip\_if(*expr*)
    :   Like [`next_if()`](#jinja2.lexer.TokenStream.next_if "jinja2.lexer.TokenStream.next_if") but only returns `True` or `False`.

        Parameters:
        :   **expr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")

    \_\_next\_\_()
    :   Go one token ahead and return the old one.

        Use the built-in [`next()`](https://docs.python.org/3/library/functions.html#next "(in Python v3.13)") instead of calling this directly.

        Return type:
        :   [*Token*](#jinja2.lexer.Token "jinja2.lexer.Token")

    expect(*expr*)
    :   Expect a given token type and return it. This accepts the same
        argument as [`jinja2.lexer.Token.test()`](#jinja2.lexer.Token.test "jinja2.lexer.Token.test").

        Parameters:
        :   **expr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [*Token*](#jinja2.lexer.Token "jinja2.lexer.Token")

*class* jinja2.lexer.Token(*lineno*, *type*, *value*)
:   Parameters:
    :   - **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)"))
        - **type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

    lineno
    :   The line number of the token

    type
    :   The type of the token. This string is interned so you may compare
        it with arbitrary strings using the `is` operator.

    value
    :   The value of the token.

    test(*expr*)
    :   Test a token against a token expression. This can either be a
        token type or `'token_type:token_value'`. This can only test
        against string values and types.

        Parameters:
        :   **expr** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")

    test\_any(*\*iterable*)
    :   Test against multiple token expressions.

        Parameters:
        :   **iterable** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")

There is also a utility function in the lexer module that can count newline
characters in strings:

jinja2.lexer.count\_newlines(*value*)
:   Count the number of newline characters in the string. This is
    useful for extensions that filter a stream.

    Parameters:
    :   **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

    Return type:
    :   [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)")

### AST

The AST (Abstract Syntax Tree) is used to represent a template after parsing.
It’s build of nodes that the compiler then converts into executable Python
code objects. Extensions that provide custom statements can return nodes to
execute custom Python code.

The list below describes all nodes that are currently available. The AST may
change between Jinja versions but will stay backwards compatible.

For more information have a look at the repr of [`jinja2.Environment.parse()`](../api/#jinja2.Environment.parse "jinja2.Environment.parse").

*class* jinja2.nodes.Node
:   Baseclass for all Jinja nodes. There are a number of nodes available
    of different types. There are four major types:

    - [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt"): statements
    - [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr"): expressions
    - [`Helper`](#jinja2.nodes.Helper "jinja2.nodes.Helper"): helper nodes
    - [`Template`](#jinja2.nodes.Template "jinja2.nodes.Template"): the outermost wrapper node

    All nodes have fields and attributes. Fields may be other nodes, lists,
    or arbitrary values. Fields are passed to the constructor as regular
    positional arguments, attributes as keyword arguments. Each node has
    two attributes: `lineno` (the line number of the node) and `environment`.
    The `environment` attribute is set at the end of the parsing process for
    all nodes automatically.

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

    iter\_fields(*exclude=None*, *only=None*)
    :   This method iterates over all fields that are defined and yields
        `(key, value)` tuples. Per default all fields are returned, but
        it’s possible to limit that to some fields by providing the `only`
        parameter or to exclude some using the `exclude` parameter. Both
        should be sets or tuples of field names.

        Parameters:
        :   - **exclude** ([*Container*](https://docs.python.org/3/library/typing.html#typing.Container "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*]* *|* *None*)
            - **only** ([*Container*](https://docs.python.org/3/library/typing.html#typing.Container "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*]* *|* *None*)

        Return type:
        :   [*Iterator*](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.13)")[[*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.13)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")]]

    iter\_child\_nodes(*exclude=None*, *only=None*)
    :   Iterates over all direct child nodes of the node. This iterates
        over all fields and yields the values of they are nodes. If the value
        of a field is a list all the nodes in that list are returned.

        Parameters:
        :   - **exclude** ([*Container*](https://docs.python.org/3/library/typing.html#typing.Container "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*]* *|* *None*)
            - **only** ([*Container*](https://docs.python.org/3/library/typing.html#typing.Container "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")*]* *|* *None*)

        Return type:
        :   [*Iterator*](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.13)")[[*Node*](#jinja2.nodes.Node "jinja2.nodes.Node")]

    find(*node\_type*)
    :   Find the first node of a given type. If no such node exists the
        return value is `None`.

        Parameters:
        :   **node\_type** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[**\_NodeBound**]*)

        Return type:
        :   *\_NodeBound* | None

    find\_all(*node\_type*)
    :   Find all the nodes of a given type. If the type is a tuple,
        the check is performed for any of the tuple items.

        Parameters:
        :   **node\_type** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[**\_NodeBound**]* *|* [*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple "(in Python v3.13)")*[*[*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[**\_NodeBound**]**,* *...**]*)

        Return type:
        :   [*Iterator*](https://docs.python.org/3/library/typing.html#typing.Iterator "(in Python v3.13)")[*\_NodeBound*]

    set\_ctx(*ctx*)
    :   Reset the context of a node and all child nodes. Per default the
        parser will all generate nodes that have a ‘load’ context as it’s the
        most common one. This method is used in the parser to set assignment
        targets and other nodes to a store context.

        Parameters:
        :   **ctx** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))

        Return type:
        :   [*Node*](#jinja2.nodes.Node "jinja2.nodes.Node")

    set\_lineno(*lineno*, *override=False*)
    :   Set the line numbers of the node and children.

        Parameters:
        :   - **lineno** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)"))
            - **override** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

        Return type:
        :   [*Node*](#jinja2.nodes.Node "jinja2.nodes.Node")

    set\_environment(*environment*)
    :   Set the environment for all nodes.

        Parameters:
        :   **environment** ([*Environment*](../api/#jinja2.Environment "jinja2.Environment"))

        Return type:
        :   [Node](#jinja2.nodes.Node "jinja2.nodes.Node")

*class* jinja2.nodes.Expr
:   Baseclass for all expressions.

    Node type:
    :   [`Node`](#jinja2.nodes.Node "jinja2.nodes.Node")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

    as\_const(*eval\_ctx=None*)
    :   Return the value of the expression as constant or raise
        [`Impossible`](#jinja2.nodes.Impossible "jinja2.nodes.Impossible") if this was not possible.

        An [`EvalContext`](../api/#jinja2.nodes.EvalContext "jinja2.nodes.EvalContext") can be provided, if none is given
        a default context is created which requires the nodes to have
        an attached environment.

        Changelog

        Changed in version 2.4: the `eval_ctx` parameter was added.

        Parameters:
        :   **eval\_ctx** ([*EvalContext*](../api/#jinja2.nodes.EvalContext "jinja2.nodes.EvalContext") *|* *None*)

        Return type:
        :   [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")

    can\_assign()
    :   Check if it’s possible to assign something to this node.

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")

*class* jinja2.nodes.\_FilterTestCommon(*node*, *name*, *args*, *kwargs*, *dyn\_args*, *dyn\_kwargs*)
:   Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Filter(*node*, *name*, *args*, *kwargs*, *dyn\_args*, *dyn\_kwargs*)
:   Apply a filter to an expression. `name` is the name of the
    filter, the other fields are the same as [`Call`](#jinja2.nodes.Call "jinja2.nodes.Call").

    If `node` is `None`, the filter is being used in a filter block
    and is applied to the content of the block.

    Node type:
    :   [`_FilterTestCommon`](#jinja2.nodes._FilterTestCommon "jinja2.nodes._FilterTestCommon")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Test(*node*, *name*, *args*, *kwargs*, *dyn\_args*, *dyn\_kwargs*)
:   Apply a test to an expression. `name` is the name of the test,
    the other field are the same as [`Call`](#jinja2.nodes.Call "jinja2.nodes.Call").

    Changelog

    Changed in version 3.0: `as_const` shares the same logic for filters and tests. Tests
    check for volatile, async, and `@pass_context` etc.
    decorators.

    Node type:
    :   [`_FilterTestCommon`](#jinja2.nodes._FilterTestCommon "jinja2.nodes._FilterTestCommon")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.BinExpr(*left*, *right*)
:   Baseclass for all binary expressions.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Add(*left*, *right*)
:   Add the left to the right node.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.And(*left*, *right*)
:   Short circuited AND.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Div(*left*, *right*)
:   Divides the left by the right node.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.FloorDiv(*left*, *right*)
:   Divides the left by the right node and converts the
    result into an integer by truncating.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Mod(*left*, *right*)
:   Left modulo right.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Mul(*left*, *right*)
:   Multiplies the left with the right node.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Or(*left*, *right*)
:   Short circuited OR.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Pow(*left*, *right*)
:   Left to the power of right.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Sub(*left*, *right*)
:   Subtract the right from the left node.

    Node type:
    :   [`BinExpr`](#jinja2.nodes.BinExpr "jinja2.nodes.BinExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Call(*node*, *args*, *kwargs*, *dyn\_args*, *dyn\_kwargs*)
:   Calls an expression. `args` is a list of arguments, `kwargs` a list
    of keyword arguments (list of [`Keyword`](#jinja2.nodes.Keyword "jinja2.nodes.Keyword") nodes), and `dyn_args`
    and `dyn_kwargs` has to be either `None` or a node that is used as
    node for dynamic positional (`*args`) or keyword (`**kwargs`)
    arguments.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Compare(*expr*, *ops*)
:   Compares an expression with some other expressions. `ops` must be a
    list of [`Operand`](#jinja2.nodes.Operand "jinja2.nodes.Operand")s.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Concat(*nodes*)
:   Concatenates the list of expressions provided after converting
    them to strings.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.CondExpr(*test*, *expr1*, *expr2*)
:   A conditional expression (inline if expression). (`{{
    foo if bar else baz }}`)

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.ContextReference
:   Returns the current template context. It can be used like a
    [`Name`](#jinja2.nodes.Name "jinja2.nodes.Name") node, with a `'load'` ctx and will return the
    current [`Context`](../api/#jinja2.runtime.Context "jinja2.runtime.Context") object.

    Here an example that assigns the current template name to a
    variable named `foo`:

    ```
    Assign(Name('foo', ctx='store'),
           Getattr(ContextReference(), 'name'))
    ```

    This is basically equivalent to using the
    [`pass_context()`](../api/#jinja2.pass_context "jinja2.pass_context") decorator when using the high-level
    API, which causes a reference to the context to be passed as the
    first argument to a function.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.DerivedContextReference
:   Return the current template context including locals. Behaves
    exactly like [`ContextReference`](#jinja2.nodes.ContextReference "jinja2.nodes.ContextReference"), but includes local
    variables, such as from a `for` loop.

    Changelog

    Added in version 2.11.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.EnvironmentAttribute(*name*)
:   Loads an attribute from the environment object. This is useful for
    extensions that want to call a callback stored on the environment.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.ExtensionAttribute(*identifier*, *name*)
:   Returns the attribute of an extension bound to the environment.
    The identifier is the identifier of the `Extension`.

    This node is usually constructed by calling the
    [`attr()`](#jinja2.ext.Extension.attr "jinja2.ext.Extension.attr") method on an extension.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Getattr(*node*, *attr*, *ctx*)
:   Get an attribute or item from an expression that is a ascii-only
    bytestring and prefer the attribute.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Getitem(*node*, *arg*, *ctx*)
:   Get an attribute or item from an expression and prefer the item.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.ImportedName(*importname*)
:   If created with an import name the import name is returned on node
    access. For example `ImportedName('cgi.escape')` returns the `escape`
    function from the cgi module on evaluation. Imports are optimized by the
    compiler so there is no need to assign them to local variables.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.InternalName(*name*)
:   An internal name in the compiler. You cannot create these nodes
    yourself but the parser provides a
    [`free_identifier()`](#jinja2.parser.Parser.free_identifier "jinja2.parser.Parser.free_identifier") method that creates
    a new identifier for you. This identifier is not available from the
    template and is not treated specially by the compiler.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

*class* jinja2.nodes.Literal
:   Baseclass for literals.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Const(*value*)
:   All constant values. The parser will return this node for simple
    constants such as `42` or `"foo"` but it can be used to store more
    complex values such as lists too. Only constants with a safe
    representation (objects where `eval(repr(x)) == x` is true).

    Node type:
    :   [`Literal`](#jinja2.nodes.Literal "jinja2.nodes.Literal")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Dict(*items*)
:   Any dict literal such as `{1: 2, 3: 4}`. The items must be a list of
    [`Pair`](#jinja2.nodes.Pair "jinja2.nodes.Pair") nodes.

    Node type:
    :   [`Literal`](#jinja2.nodes.Literal "jinja2.nodes.Literal")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.List(*items*)
:   Any list literal such as `[1, 2, 3]`

    Node type:
    :   [`Literal`](#jinja2.nodes.Literal "jinja2.nodes.Literal")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.TemplateData(*data*)
:   A constant template string.

    Node type:
    :   [`Literal`](#jinja2.nodes.Literal "jinja2.nodes.Literal")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Tuple(*items*, *ctx*)
:   For loop unpacking and some other things like multiple arguments
    for subscripts. Like for [`Name`](#jinja2.nodes.Name "jinja2.nodes.Name") `ctx` specifies if the tuple
    is used for loading the names or storing.

    Node type:
    :   [`Literal`](#jinja2.nodes.Literal "jinja2.nodes.Literal")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.MarkSafe(*expr*)
:   Mark the wrapped expression as safe (wrap it as `Markup`).

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.MarkSafeIfAutoescape(*expr*)
:   Mark the wrapped expression as safe (wrap it as `Markup`) but
    only if autoescaping is active.

    Changelog

    Added in version 2.5.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Name(*name*, *ctx*)
:   Looks up a name or stores a value in a name.
    The `ctx` of the node can be one of the following values:

    - `store`: store a value in the name
    - `load`: load that name
    - `param`: like `store` but if the name was defined as function parameter.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.NSRef(*name*, *attr*)
:   Reference to a namespace value assignment

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Slice(*start*, *stop*, *step*)
:   Represents a slice object. This must only be used as argument for
    `Subscript`.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.UnaryExpr(*node*)
:   Baseclass for all unary expressions.

    Node type:
    :   [`Expr`](#jinja2.nodes.Expr "jinja2.nodes.Expr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Neg(*node*)
:   Make the expression negative.

    Node type:
    :   [`UnaryExpr`](#jinja2.nodes.UnaryExpr "jinja2.nodes.UnaryExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Not(*node*)
:   Negate the expression.

    Node type:
    :   [`UnaryExpr`](#jinja2.nodes.UnaryExpr "jinja2.nodes.UnaryExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Pos(*node*)
:   Make the expression positive (noop for most expressions)

    Node type:
    :   [`UnaryExpr`](#jinja2.nodes.UnaryExpr "jinja2.nodes.UnaryExpr")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Helper
:   Nodes that exist in a specific context only.

    Node type:
    :   [`Node`](#jinja2.nodes.Node "jinja2.nodes.Node")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Keyword(*key*, *value*)
:   A key, value pair for keyword arguments where key is a string.

    Node type:
    :   [`Helper`](#jinja2.nodes.Helper "jinja2.nodes.Helper")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Operand(*op*, *expr*)
:   Holds an operator and an expression.

    Node type:
    :   [`Helper`](#jinja2.nodes.Helper "jinja2.nodes.Helper")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Pair(*key*, *value*)
:   A key, value pair for dicts.

    Node type:
    :   [`Helper`](#jinja2.nodes.Helper "jinja2.nodes.Helper")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Stmt
:   Base node for all statements.

    Node type:
    :   [`Node`](#jinja2.nodes.Node "jinja2.nodes.Node")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Assign(*target*, *node*)
:   Assigns an expression to a target.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.AssignBlock(*target*, *filter*, *body*)
:   Assigns a block to a target.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Block(*name*, *body*, *scoped*, *required*)
:   A node that represents a block.

    Changelog

    Changed in version 3.0.0: the `required` field was added.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Break
:   Break a loop.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.CallBlock(*call*, *args*, *defaults*, *body*)
:   Like a macro without a name but a call instead. `call` is called with
    the unnamed macro as `caller` argument this node holds.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Continue
:   Continue a loop.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.EvalContextModifier(*options*)
:   Modifies the eval context. For each option that should be modified,
    a [`Keyword`](#jinja2.nodes.Keyword "jinja2.nodes.Keyword") has to be added to the `options` list.

    Example to change the `autoescape` setting:

    ```
    EvalContextModifier(options=[Keyword('autoescape', Const(True))])
    ```

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.ScopedEvalContextModifier(*options*, *body*)
:   Modifies the eval context and reverts it later. Works exactly like
    [`EvalContextModifier`](#jinja2.nodes.EvalContextModifier "jinja2.nodes.EvalContextModifier") but will only modify the
    [`EvalContext`](../api/#jinja2.nodes.EvalContext "jinja2.nodes.EvalContext") for nodes in the `body`.

    Node type:
    :   [`EvalContextModifier`](#jinja2.nodes.EvalContextModifier "jinja2.nodes.EvalContextModifier")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.ExprStmt(*node*)
:   A statement that evaluates an expression and discards the result.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Extends(*template*)
:   Represents an extends statement.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.FilterBlock(*body*, *filter*)
:   Node for filter sections.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.For(*target*, *iter*, *body*, *else\_*, *test*, *recursive*)
:   The for loop. `target` is the target for the iteration (usually a
    [`Name`](#jinja2.nodes.Name "jinja2.nodes.Name") or [`Tuple`](#jinja2.nodes.Tuple "jinja2.nodes.Tuple")), `iter` the iterable. `body` is a list
    of nodes that are used as loop-body, and `else_` a list of nodes for the
    `else` block. If no else node exists it has to be an empty list.

    For filtered nodes an expression can be stored as `test`, otherwise `None`.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.FromImport(*template*, *names*, *with\_context*)
:   A node that represents the from import tag. It’s important to not
    pass unsafe names to the name attribute. The compiler translates the
    attribute lookups directly into getattr calls and does *not* use the
    subscript callback of the interface. As exported variables may not
    start with double underscores (which the parser asserts) this is not a
    problem for regular Jinja code, but if this node is used in an extension
    extra care must be taken.

    The list of names may contain tuples if aliases are wanted.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.If(*test*, *body*, *elif\_*, *else\_*)
:   If `test` is true, `body` is rendered, else `else_`.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Import(*template*, *target*, *with\_context*)
:   A node that represents the import tag.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Include(*template*, *with\_context*, *ignore\_missing*)
:   A node that represents the include tag.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Macro(*name*, *args*, *defaults*, *body*)
:   A macro definition. `name` is the name of the macro, `args` a list of
    arguments and `defaults` a list of defaults if there are any. `body` is
    a list of nodes for the macro body.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Output(*nodes*)
:   A node that holds multiple expressions which are then printed out.
    This is used both for the `print` statement and the regular template data.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.OverlayScope(*context*, *body*)
:   An overlay scope for extensions. This is a largely unoptimized scope
    that however can be used to introduce completely arbitrary variables into
    a sub scope from a dictionary or dictionary like object. The `context`
    field has to evaluate to a dictionary object.

    Example usage:

    ```
    OverlayScope(context=self.call_method('get_context'),
                 body=[...])
    ```

    Changelog

    Added in version 2.10.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Scope(*body*)
:   An artificial scope.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.With(*targets*, *values*, *body*)
:   Specific node for with statements. In older versions of Jinja the
    with statement was implemented on the base of the `Scope` node instead.

    Changelog

    Added in version 2.9.3.

    Node type:
    :   [`Stmt`](#jinja2.nodes.Stmt "jinja2.nodes.Stmt")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*class* jinja2.nodes.Template(*body*)
:   Node that represents a template. This must be the outermost node that
    is passed to the compiler.

    Node type:
    :   [`Node`](#jinja2.nodes.Node "jinja2.nodes.Node")

    Parameters:
    :   - **fields** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
        - **attributes** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

*exception* jinja2.nodes.Impossible
:   Raised if the node could not perform a requested action.