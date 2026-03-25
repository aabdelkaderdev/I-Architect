<!-- Source: https://pymupdf.readthedocs.io/en/latest/outline.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Outline

The document outline (otherwise known as “bookmarks”) is a property of [Document](document.html#document) (see [`Document.outline`](document.html#Document.outline "Document.outline")). If not `None`, it stands for the first outline item of the document. Its properties in turn define the characteristics of this item and also point to other outline items in “horizontal” or downward direction. The full tree of all outline items for e.g. a conventional table of contents (TOC) can be recovered by following these “pointers”.

| **Method / Attribute** | **Short Description** |
| --- | --- |
| [`Outline.down`](#Outline.down "Outline.down") | next item downwards |
| [`Outline.next`](#Outline.next "Outline.next") | next item same level |
| [`Outline.page`](#Outline.page "Outline.page") | page number (0-based) |
| [`Outline.title`](#Outline.title "Outline.title") | title |
| [`Outline.uri`](#Outline.uri "Outline.uri") | string further specifying outline target |
| [`Outline.is_external`](#Outline.is_external "Outline.is_external") | target outside document |
| [`Outline.is_open`](#Outline.is_open "Outline.is_open") | whether sub-outlines are open or collapsed |
| [`Outline.dest`](#Outline.dest "Outline.dest") | points to destination details object |

**Class API**

*class* Outline
:   down
    :   The next outline item on the next level down. Is `None` if the item has no children.

        Type:
        :   [Outline](#outline)

    next
    :   The next outline item at the same level as this item. Is `None` if this is the last one in its level.

        Type:
        :   [Outline](#outline)

    page
    :   The page number (0-based) this bookmark points to.

        Type:
        :   int

    title
    :   The item’s title as a string or `None`.

        Type:
        :   str

    is\_open
    :   Indicator showing whether any sub-outlines should be expanded (`True`) or be collapsed (`False`). This information is interpreted by PDF reader software.

        Type:
        :   bool

    is\_external
    :   A bool specifying whether the target is outside (`True`) of the current document.

        Type:
        :   bool

    uri
    :   A string specifying the link target. The meaning of this property should
        be evaluated in conjunction with property [`is_external`](link.html#Link.is_external "Link.is_external"):

        - [`is_external`](link.html#Link.is_external "Link.is_external") is true: `uri` points to some target outside the current
          PDF, which may be an internet resource (`uri` starts with `http://` or
          similar), another file (`uri` starts with `file:` or `file://`) or some
          other service like an e-mail address (`uri` starts with `mailto:`).
        - [`is_external`](link.html#Link.is_external "Link.is_external") is false: `uri` will be `None` or point to an
          internal location. In case of PDF documents, this should either be
          *#nnnn* to indicate a 1-based (!) page number *nnnn*, or a named
          location. The format varies for other document types, for example
          “../FixedDoc.fdoc#PG\_2\_LNK\_1” for page number 2 (1-based) in an XPS
          document.

        Type:
        :   str

    dest
    :   The link destination details object.

        Type:
        :   [linkDest](linkdest.html#linkdest)

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.