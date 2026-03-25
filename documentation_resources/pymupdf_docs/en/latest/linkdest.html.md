<!-- Source: https://pymupdf.readthedocs.io/en/latest/linkdest.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# linkDest

Class representing the [`dest`](link.html#Link.dest "Link.dest") property of an outline entry or a link. Describes the destination to which such entries point.

Note

Up to MuPDF v1.9.0 this class existed inside MuPDF and was dropped in version 1.10.0. For backward compatibility, PyMuPDF is still maintaining it, although some of its attributes are no longer backed by data actually available via MuPDF.

| **Attribute** | **Short Description** |
| --- | --- |
| [`linkDest.dest`](#linkDest.dest "linkDest.dest") | destination |
| [`linkDest.fileSpec`](#linkDest.fileSpec "linkDest.fileSpec") | file specification (path, filename) |
| [`linkDest.flags`](#linkDest.flags "linkDest.flags") | descriptive flags |
| [`linkDest.isMap`](#linkDest.isMap "linkDest.isMap") | is this a MAP? |
| [`linkDest.isUri`](#linkDest.isUri "linkDest.isUri") | is this a URI? |
| [`linkDest.kind`](#linkDest.kind "linkDest.kind") | kind of destination |
| [`linkDest.lt`](#linkDest.lt "linkDest.lt") | top left coordinates |
| [`linkDest.named`](#linkDest.named "linkDest.named") | name if named destination |
| [`linkDest.newWindow`](#linkDest.newWindow "linkDest.newWindow") | name of new window |
| [`linkDest.page`](#linkDest.page "linkDest.page") | page number |
| [`linkDest.rb`](#linkDest.rb "linkDest.rb") | bottom right coordinates |
| [`linkDest.uri`](#linkDest.uri "linkDest.uri") | URI |

**Class API**

*class* linkDest
:   dest
    :   Target destination name if [`linkDest.kind`](#linkDest.kind "linkDest.kind") is [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR") and [`linkDest.page`](#linkDest.page "linkDest.page") is *-1*.

        Type:
        :   str

    fileSpec
    :   Contains the filename and path this link points to, if [`linkDest.kind`](#linkDest.kind "linkDest.kind") is [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR") or [`LINK_LAUNCH`](vars.html#LINK_LAUNCH "LINK_LAUNCH").

        Type:
        :   str

    flags
    :   A bitfield describing the validity and meaning of the different aspects of the destination. As far as possible, link destinations are constructed such that e.g. [`linkDest.lt`](#linkDest.lt "linkDest.lt") and [`linkDest.rb`](#linkDest.rb "linkDest.rb") can be treated as defining a bounding box. But the flags indicate which of the values were actually specified, see [Link Destination Flags](vars.html#linkdest-flags).

        Type:
        :   int

    isMap
    :   This flag specifies whether to track the mouse position when the URI is resolved. Default value: False.

        Type:
        :   bool

    isUri
    :   Specifies whether this destination is an internet resource (as opposed to e.g. a local file specification in URI format).

        Type:
        :   bool

    kind
    :   Indicates the type of this destination, like a place in this document, a URI, a file launch, an action or a place in another file. Look at [Link Destination Kinds](vars.html#linkdest-kinds) to see the names and numerical values.

        Type:
        :   int

    lt
    :   The top left [Point](point.html#point) of the destination.

        Type:
        :   [Point](point.html#point)

    named
    :   This destination refers to some named action to perform (e.g. a javascript, see [Adobe PDF References](app3.html#adobemanual)). Standard actions provided are *NextPage*, *PrevPage*, *FirstPage*, and *LastPage*.

        Type:
        :   str

    newWindow
    :   If true, the destination should be launched in a new window.

        Type:
        :   bool

    page
    :   The page number (in this or the target document) this destination points to. Only set if [`linkDest.kind`](#linkDest.kind "linkDest.kind") is [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR") or [`LINK_GOTO`](vars.html#LINK_GOTO "LINK_GOTO"). May be *-1* if [`linkDest.kind`](#linkDest.kind "linkDest.kind") is [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR"). In this case [`linkDest.dest`](#linkDest.dest "linkDest.dest") contains the **name** of a destination in the target document.

        Type:
        :   int

    rb
    :   The bottom right [Point](point.html#point) of this destination.

        Type:
        :   [Point](point.html#point)

    uri
    :   The name of the URI this destination points to.

        Type:
        :   str

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.