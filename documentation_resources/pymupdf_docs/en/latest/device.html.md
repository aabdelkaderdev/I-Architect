<!-- Source: https://pymupdf.readthedocs.io/en/latest/device.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Device

The different format handlers (pdf, xps, etc.) interpret pages to a “device”. Devices are the basis for everything that can be done with a page: rendering, text extraction and searching. The device type is determined by the selected construction method.

**Class API**

*class* Device
:   \_\_init\_\_(*self*, *object*, *clip*)
    :   Constructor for either a pixel map or a display list device.

        Parameters:
        :   - **object** ([Pixmap](pixmap.html#pixmap) or [DisplayList](displaylist.html#displaylist)) – either a `Pixmap` or a `DisplayList`.
            - **clip** ([IRect](irect.html#irect)) – An optional [IRect](irect.html#irect) for `Pixmap` devices to restrict rendering to a certain area of the page. If the complete page is required, specify `None`. For display list devices, this parameter must be omitted.

    \_\_init\_\_(*self*, *textpage*, *flags=0*)
    :   Constructor for a text page device.

        Parameters:
        :   - **textpage** ([TextPage](textpage.html#textpage)) – `TextPage` object
            - **flags** (*int*) – control the way how text is parsed into the text page. Currently 3 options can be coded into this parameter, see [Font Properties](vars.html#textpreserve). To set these options use something like `flags=0 | TEXT_PRESERVE_LIGATURES | ...`.

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.