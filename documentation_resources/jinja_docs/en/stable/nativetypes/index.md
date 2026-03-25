<!-- Source: https://jinja.palletsprojects.com/en/stable/nativetypes/ -->

# Native Python Types

The default [`Environment`](../api/#jinja2.Environment "jinja2.Environment") renders templates to strings. With
[`NativeEnvironment`](#jinja2.nativetypes.NativeEnvironment "jinja2.nativetypes.NativeEnvironment"), rendering a template produces a native Python type.
This is useful if you are using Jinja outside the context of creating text
files. For example, your code may have an intermediate step where users may use
templates to define values that will then be passed to a traditional string
environment.

## Examples

Adding two values results in an integer, not a string with a number:

```
>>> env = NativeEnvironment()
>>> t = env.from_string('{{ x + y }}')
>>> result = t.render(x=4, y=2)
>>> print(result)
6
>>> print(type(result))
int
```

Rendering list syntax produces a list:

```
>>> t = env.from_string('[{% for item in data %}{{ item + 1 }},{% endfor %}]')
>>> result = t.render(data=range(5))
>>> print(result)
[1, 2, 3, 4, 5]
>>> print(type(result))
list
```

Rendering something that doesn’t look like a Python literal produces a string:

```
>>> t = env.from_string('{{ x }} * {{ y }}')
>>> result = t.render(x=4, y=2)
>>> print(result)
4 * 2
>>> print(type(result))
str
```

Rendering a Python object produces that object as long as it is the only node:

```
>>> class Foo:
...     def __init__(self, value):
...         self.value = value
...
>>> result = env.from_string('{{ x }}').render(x=Foo(15))
>>> print(type(result).__name__)
Foo
>>> print(result.value)
15
```

## Sandboxed Native Environment

You can combine [`SandboxedEnvironment`](../sandbox/#jinja2.sandbox.SandboxedEnvironment "jinja2.sandbox.SandboxedEnvironment") and [`NativeEnvironment`](#jinja2.nativetypes.NativeEnvironment "jinja2.nativetypes.NativeEnvironment") to
get both behaviors.

```
class SandboxedNativeEnvironment(SandboxedEnvironment, NativeEnvironment):
    pass
```

## API

*class* jinja2.nativetypes.NativeEnvironment([*options*])
:   An environment that renders templates to native Python types.

    Parameters:
    :   - **block\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **block\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **variable\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **variable\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **comment\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **comment\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **line\_statement\_prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **line\_comment\_prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **trim\_blocks** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **lstrip\_blocks** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **newline\_sequence** (*te.Literal**[**'\n'**,* *'\r\n'**,* *'\r'**]*)
        - **keep\_trailing\_newline** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **extensions** ([*Sequence*](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* [*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[*[*Extension*](../extensions/#jinja2.ext.Extension "jinja2.ext.Extension")*]**]*)
        - **optimized** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **undefined** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[*[*Undefined*](../api/#jinja2.Undefined "jinja2.runtime.Undefined")*]*)
        - **finalize** ([*Callable*](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.13)")*[**[**...**]**,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")*]* *|* *None*)
        - **autoescape** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)") *|* [*Callable*](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.13)")*[**[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None**]**,* [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")*]*)
        - **loader** ([*BaseLoader*](../api/#jinja2.BaseLoader "jinja2.BaseLoader") *|* *None*)
        - **cache\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.13)"))
        - **auto\_reload** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **bytecode\_cache** ([*BytecodeCache*](../api/#jinja2.BytecodeCache "jinja2.BytecodeCache") *|* *None*)
        - **enable\_async** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

*class* jinja2.nativetypes.NativeTemplate([*options*])
:   Parameters:
    :   - **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* [*Template*](../extensions/#jinja2.nodes.Template "jinja2.nodes.Template"))
        - **block\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **block\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **variable\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **variable\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **comment\_start\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **comment\_end\_string** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)"))
        - **line\_statement\_prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **line\_comment\_prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None*)
        - **trim\_blocks** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **lstrip\_blocks** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **newline\_sequence** (*te.Literal**[**'\n'**,* *'\r\n'**,* *'\r'**]*)
        - **keep\_trailing\_newline** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **extensions** ([*Sequence*](https://docs.python.org/3/library/typing.html#typing.Sequence "(in Python v3.13)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* [*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[*[*Extension*](../extensions/#jinja2.ext.Extension "jinja2.ext.Extension")*]**]*)
        - **optimized** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))
        - **undefined** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type "(in Python v3.13)")*[*[*Undefined*](../api/#jinja2.Undefined "jinja2.runtime.Undefined")*]*)
        - **finalize** ([*Callable*](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.13)")*[**[**...**]**,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")*]* *|* *None*)
        - **autoescape** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)") *|* [*Callable*](https://docs.python.org/3/library/typing.html#typing.Callable "(in Python v3.13)")*[**[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)") *|* *None**]**,* [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)")*]*)
        - **enable\_async** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.13)"))

    Return type:
    :   [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")

    render(*\*args*, *\*\*kwargs*)
    :   Render the template to produce a native Python type. If the
        result is a single node, its value is returned. Otherwise, the
        nodes are concatenated as strings. If the result can be parsed
        with [`ast.literal_eval()`](https://docs.python.org/3/library/ast.html#ast.literal_eval "(in Python v3.13)"), the parsed value is returned.
        Otherwise, the string is returned.

        Parameters:
        :   - **args** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))
            - **kwargs** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)"))

        Return type:
        :   [*Any*](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.13)")