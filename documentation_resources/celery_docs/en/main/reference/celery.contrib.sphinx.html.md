<!-- Source: https://docs.celeryq.dev/en/main/reference/celery.contrib.sphinx.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.sphinx.html).

# celery.contrib.sphinx

Sphinx documentation plugin used to document tasks.

## Introduction

### Usage

The Celery extension for Sphinx requires Sphinx 2.0 or later.

Add the extension to your `docs/conf.py` configuration module:

```
extensions = (...,
              'celery.contrib.sphinx')
```

If you’d like to change the prefix for tasks in reference documentation
then you can change the `celery_task_prefix` configuration value:

```
celery_task_prefix = '(task)'  # < default
```

With the extension installed autodoc will automatically find
task decorated objects (e.g. when using the automodule directive)
and generate the correct (as well as add a `(task)` prefix),
and you can also refer to the tasks using :task:proj.tasks.add
syntax.

Use `.. autotask::` to alternatively manually document a task.

### Sphinx 9.0+ Compatibility

Sphinx 9.0 introduced a rewritten autodoc implementation. The Celery
extension requires the legacy class-based autodoc mode to function
correctly. When using Sphinx 9.0 or later, add the following to your
`conf.py`:

```
autodoc_use_legacy_class_based = True
```

The extension will automatically enable this setting if not configured,
but it is recommended to set it explicitly to avoid warnings.

class celery.contrib.sphinx.TaskDirective(*name*, *arguments*, *options*, *content*, *lineno*, *content\_offset*, *block\_text*, *state*, *state\_machine*)[[source]](../_modules/celery/contrib/sphinx.html#TaskDirective)
:   Sphinx task directive.

    get\_signature\_prefix(*sig*)[[source]](../_modules/celery/contrib/sphinx.html#TaskDirective.get_signature_prefix)
    :   May return a prefix to put before the object name in the
        signature.

class celery.contrib.sphinx.TaskDocumenter(*directive: DocumenterBridge*, *name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *indent: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = ''*)[[source]](../_modules/celery/contrib/sphinx.html#TaskDocumenter)
:   Document task definitions.

    classmethod can\_document\_member(*member*, *membername*, *isattr*, *parent*)[[source]](../_modules/celery/contrib/sphinx.html#TaskDocumenter.can_document_member)
    :   Called to see if a member can be documented by this Documenter.

    check\_module()[[source]](../_modules/celery/contrib/sphinx.html#TaskDocumenter.check_module)
    :   Check if *self.object* is really defined in the module given by
        *self.modname*.

    document\_members(*all\_members=False*)[[source]](../_modules/celery/contrib/sphinx.html#TaskDocumenter.document_members)
    :   Generate reST for member documentation.

        If *all\_members* is True, document all members, else those given by
        *self.options.members*.

    format\_args()[[source]](../_modules/celery/contrib/sphinx.html#TaskDocumenter.format_args)
    :   Format the argument signature of *self.object*.

        Should return None if the object does not have a signature.

    member\_order: ClassVar = 11
    :   order if autodoc\_member\_order is set to ‘groupwise’

    objtype: ClassVar = 'task'
    :   name by which the directive is called (auto…) and the default
        generated directive name

celery.contrib.sphinx.autodoc\_skip\_member\_handler(*app*, *what*, *name*, *obj*, *skip*, *options*)[[source]](../_modules/celery/contrib/sphinx.html#autodoc_skip_member_handler)
:   Handler for autodoc-skip-member event.

celery.contrib.sphinx.setup(*app*)[[source]](../_modules/celery/contrib/sphinx.html#setup)
:   Setup Sphinx extension.