<!-- Source: https://pymupdf.readthedocs.io/en/latest/displaylist.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# DisplayList

DisplayList is a list containing drawing commands (text, images, etc.). The intent is two-fold:

1. as a caching-mechanism to reduce parsing of a page
2. as a data structure in multi-threading setups, where one thread parses the page and another one renders pages. This aspect is currently not supported by PyMuPDF.

A display list is populated with objects from a page, usually by executing [`Page.get_displaylist()`](functions.html#Page.get_displaylist "Page.get_displaylist"). There also exists an independent constructor.

“Replay” the list (once or many times) by invoking one of its methods [`run()`](#DisplayList.run "DisplayList.run"), [`get_pixmap()`](#DisplayList.get_pixmap "DisplayList.get_pixmap") or [`get_textpage()`](#DisplayList.get_textpage "DisplayList.get_textpage").

| **Method** | **Short Description** |
| --- | --- |
| [`run()`](#DisplayList.run "DisplayList.run") | Run a display list through a device. |
| [`get_pixmap()`](#DisplayList.get_pixmap "DisplayList.get_pixmap") | generate a pixmap |
| [`get_textpage()`](#DisplayList.get_textpage "DisplayList.get_textpage") | generate a text page |
| [`rect`](#DisplayList.rect "DisplayList.rect") | mediabox of the display list |

**Class API**

*class* DisplayList
:   \_\_init\_\_(*self*, *mediabox*)
    :   Create a new display list.

        Parameters:
        :   **mediabox** ([Rect](rect.html#rect)) – The page’s rectangle.

        Return type:
        :   `DisplayList`

    run(*device*, *matrix*, *area*)
    :   Run the display list through a device. The device will populate the display list with its “commands” (i.e. text extraction or image creation). The display list can later be used to “read” a page many times without having to re-interpret it from the document file.

        You will most probably instead use one of the specialized run methods below – [`get_pixmap()`](#DisplayList.get_pixmap "DisplayList.get_pixmap") or [`get_textpage()`](#DisplayList.get_textpage "DisplayList.get_textpage").

        Parameters:
        :   - **device** ([Device](device.html#device)) – Device
            - **matrix** ([Matrix](matrix.html#matrix)) – Transformation matrix to apply to the display list contents.
            - **area** ([Rect](rect.html#rect)) – Only the part visible within this area will be considered when the list is run through the device.

    get\_pixmap(*matrix=pymupdf.Identity*, *colorspace=pymupdf.csRGB*, *alpha=0*, *clip=None*)
    :   Run the display list through a draw device and return a pixmap.

        Parameters:
        :   - **matrix** ([Matrix](matrix.html#matrix)) – matrix to use. Default is the identity matrix.
            - **colorspace** ([Colorspace](colorspace.html#colorspace)) – the desired colorspace. Default is RGB.
            - **alpha** (*int*) – determine whether or not (0, default) to include a transparency channel.
            - **clip** (*irect\_like*) – restrict rendering to the intersection of this area with [`DisplayList.rect`](#DisplayList.rect "DisplayList.rect").

        Return type:
        :   [Pixmap](pixmap.html#pixmap)

        Returns:
        :   pixmap of the display list.

    get\_textpage(*flags*)
    :   Run the display list through a text device and return a text page.

        Parameters:
        :   **flags** (*int*) – control which information is parsed into a text page. Default value in PyMuPDF is `3 = TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE`, i.e. `ligatures` are **passed through**, white spaces are **passed through** (not translated to spaces), and images are **not included**. See [Font Properties](vars.html#textpreserve).

        Return type:
        :   [TextPage](textpage.html#textpage)

        Returns:
        :   text page of the display list.

    rect
    :   Contains the display list’s mediabox. This will equal the page’s rectangle if it was created via [`Page.get_displaylist()`](functions.html#Page.get_displaylist "Page.get_displaylist").

        Type:
        :   [Rect](rect.html#rect)

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.