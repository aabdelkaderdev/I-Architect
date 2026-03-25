<!-- Source: https://pymupdf.readthedocs.io/en/latest/identity.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Identity

Identity is a [Matrix](matrix.html#matrix) that performs no action – to be used whenever the syntax requires a matrix, but no actual transformation should take place. It has the form *pymupdf.Matrix(1, 0, 0, 1, 0, 0)*.

Identity is a constant, an “immutable” object. So, all of its matrix properties are read-only and its methods are disabled.

If you need a **mutable** identity matrix as a starting point, use one of the following statements:

```
>>> m = pymupdf.Matrix(1, 0, 0, 1, 0, 0)  # specify the values
>>> m = pymupdf.Matrix(1, 1)              # use scaling by factor 1
>>> m = pymupdf.Matrix(0)                 # use rotation by zero degrees
>>> m = pymupdf.Matrix(pymupdf.Identity)     # make a copy of Identity
```

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.