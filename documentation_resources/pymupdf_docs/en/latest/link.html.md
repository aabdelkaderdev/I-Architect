<!-- Source: https://pymupdf.readthedocs.io/en/latest/link.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Link

Represents a pointer to somewhere (this document, other documents, the internet). Links exist per document page, and they are forward-chained to each other, starting from an initial link which is accessible by the [`Page.first_link`](page.html#Page.first_link "Page.first_link") property.

There is a parent-child relationship between a link and its page. If the page object becomes unusable (closed document, any document structure change, etc.), then so does every of its existing link objects – an exception is raised saying that the object is “orphaned”, whenever a link property or method is accessed.

| **Attribute** | **Short Description** |
| --- | --- |
| [`Link.set_border()`](#Link.set_border "Link.set_border") | modify border properties |
| [`Link.set_colors()`](#Link.set_colors "Link.set_colors") | modify color properties |
| [`Link.set_flags()`](#Link.set_flags "Link.set_flags") | modify link flags |
| [`Link.border`](#Link.border "Link.border") | border characteristics |
| [`Link.colors`](#Link.colors "Link.colors") | border line color |
| [`Link.dest`](#Link.dest "Link.dest") | points to destination details |
| [`Link.is_external`](#Link.is_external "Link.is_external") | checks if the link is an external destination |
| [`Link.flags`](#Link.flags "Link.flags") | link annotation flags |
| [`Link.next`](#Link.next "Link.next") | points to next link |
| [`Link.rect`](#Link.rect "Link.rect") | clickable area in untransformed coordinates |
| [`Link.uri`](#Link.uri "Link.uri") | link destination |
| [`Link.xref`](#Link.xref "Link.xref") | [`xref`](glossary.html#xref "xref") number of the entry |

**Class API**

*class* Link
:   set\_border(*border=None*, *width=0*, *style=None*, *dashes=None*)
    :   PDF only: Change border width and dashing properties.

        *(Changed in version 1.16.9)* Allow specification without using a dictionary. The direct parameters are used if *border* is not a dictionary.

        Parameters:
        :   - **border** (*dict*) – a dictionary as returned by the [`border`](#Link.border "Link.border") property, with keys *“width”* (*float*), *“style”* (*str*) and *“dashes”* (*sequence*). Omitted keys will leave the resp. property unchanged. To e.g. remove dashing use: *“dashes”: []*. If dashes is not an empty sequence, “style” will automatically be set to “D” (dashed).
            - **width** (*float*) – see above.
            - **style** (*str*) – see above.
            - **dashes** (*sequence*) – see above.

    set\_colors(*colors=None*, *stroke=None*)
    :   PDF only: Changes the “stroke” color.

        Note

        In PDF, links are a subtype of annotations technically and **do not support fill colors**. However, to keep a consistent API, we do allow specifying a `fill=` parameter like with all annotations, which will be ignored with a warning.

        *(Changed in version 1.16.9)* Allow colors to be directly set. These parameters are used if *colors* is not a dictionary.

        Parameters:
        :   - **colors** (*dict*) – a dictionary containing color specifications. For accepted dictionary keys and values see below. The most practical way should be to first make a copy of the *colors* property and then modify this dictionary as required.
            - **stroke** (*sequence*) – see above.

    set\_flags(*flags*)
    :   *New in v1.18.16*

        Set the PDF `/F` property of the link annotation. See [`Annot.set_flags()`](annot.html#Annot.set_flags "Annot.set_flags") for details. If not a PDF, this method is a no-op.

    flags
    :   *New in v1.18.16*

        Return the link annotation flags, an integer (see [`Annot.flags`](annot.html#Annot.flags "Annot.flags") for details). Zero if not a PDF.

    colors
    :   Meaningful for PDF only: A dictionary of two tuples of floats in range `0 <= float <= 1` specifying the *stroke* and the interior (*fill*) colors. If not a PDF, `None` is returned. As mentioned above, the fill color is always `None` for links. The stroke color is used for the border of the link rectangle. The length of the tuple implicitly determines the colorspace: 1 = GRAY, 3 = RGB, 4 = CMYK. So `(1.0, 0.0, 0.0)` stands for RGB color red. The value of each float *f* is mapped to the integer value *i* in range 0 to 255 via the computation *f = i / 255*.

        Return type:
        :   dict

    border
    :   Meaningful for PDF only: A dictionary containing border characteristics. It will be `None` for non-PDFs and an empty dictionary if no border information exists. The following keys can occur:

        - *width* – a float indicating the border thickness in points. The value is -1.0 if no width is specified.
        - *dashes* – a sequence of integers specifying a line dash pattern. *[]* means no dashes, *[n]* means equal on-off lengths of *n* points, longer lists will be interpreted as specifying alternating on-off length values. See the [Adobe PDF References](app3.html#adobemanual) page 126 for more detail.
        - *style* – 1-byte border style: *S* (Solid) = solid rectangle surrounding the annotation, *D* (Dashed) = dashed rectangle surrounding the link, the dash pattern is specified by the *dashes* entry, *B* (Beveled) = a simulated embossed rectangle that appears to be raised above the surface of the page, *I* (Inset) = a simulated engraved rectangle that appears to be recessed below the surface of the page, *U* (Underline) = a single line along the bottom of the annotation rectangle.

        Return type:
        :   dict

    rect
    :   The area that can be clicked in untransformed coordinates.

        Type:
        :   [Rect](rect.html#rect)

    is\_external
    :   A bool specifying whether the link target is outside of the current document.

        Type:
        :   bool

    uri
    :   A string specifying the link target. The meaning of this property should
        be evaluated in conjunction with property [`is_external`](#Link.is_external "Link.is_external"):

        - [`is_external`](#Link.is_external "Link.is_external") is true: [`uri`](#Link.uri "Link.uri") points to some target outside the current
          PDF, which may be an internet resource ([`uri`](#Link.uri "Link.uri") starts with `http://` or
          similar), another file ([`uri`](#Link.uri "Link.uri") starts with “file:” or “<file://>”) or some
          other service like an e-mail address ([`uri`](#Link.uri "Link.uri") starts with `mailto:`).
        - [`is_external`](#Link.is_external "Link.is_external") is false: [`uri`](#Link.uri "Link.uri") will be `None` or point to an
          internal location. In case of PDF documents, this should either be
          *#nnnn* to indicate a 1-based (!) page number *nnnn*, or a named
          location. The format varies for other document types, for example
          “../FixedDoc.fdoc#PG\_2\_LNK\_1” for page number 2 (1-based) in an XPS
          document.

        Type:
        :   str

    xref
    :   An integer specifying the PDF [`xref`](glossary.html#xref "xref"). Zero if not a PDF.

        Type:
        :   int

    next
    :   The next link or `None`.

        Type:
        :   *Link*

    dest
    :   The link destination details object.

        Type:
        :   [linkDest](linkdest.html#linkdest)

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.