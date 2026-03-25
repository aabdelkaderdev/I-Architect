<!-- Source: https://pymupdf.readthedocs.io/en/latest/colorspace.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Colorspace

Represents the color space of a [Pixmap](pixmap.html#pixmap).

**Class API**

*class* Colorspace
:   \_\_init\_\_(*self*, *n*)
    :   Constructor

        Parameters:
        :   **n** (*int*) – A number identifying the colorspace. Possible values are [`CS_RGB`](vars.html#CS_RGB "CS_RGB"), [`CS_GRAY`](vars.html#CS_GRAY "CS_GRAY") and [`CS_CMYK`](vars.html#CS_CMYK "CS_CMYK").

    name
    :   The name identifying the colorspace. Example: *pymupdf.csCMYK.name = ‘DeviceCMYK’*.

        Type:
        :   str

    n
    :   > The number of bytes required to define the color of one pixel. Example: *pymupdf.csCMYK.n == 4*.
        >
        > type:
        > :   int

        **Predefined Colorspaces**

        For saving some typing effort, there exist predefined colorspace objects for the three available cases.

        - [`csRGB`](vars.html#csRGB "csRGB") = *pymupdf.Colorspace(pymupdf.CS\_RGB)*
        - [`csGRAY`](vars.html#csGRAY "csGRAY") = *pymupdf.Colorspace(pymupdf.CS\_GRAY)*
        - [`csCMYK`](vars.html#csCMYK "csCMYK") = *pymupdf.Colorspace(pymupdf.CS\_CMYK)*

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.