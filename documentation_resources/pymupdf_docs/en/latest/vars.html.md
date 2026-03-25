<!-- Source: https://pymupdf.readthedocs.io/en/latest/vars.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Constants and Enumerations

Constants and enumerations of MuPDF as implemented by PyMuPDF. Each of the following values is accessible as `pymupdf.value`.

## Constants

Base14\_Fonts
:   Predefined Python list of valid [PDF Base 14 Fonts](app3.html#base-14-fonts).

    Type:
    :   list

csRGB
:   Predefined RGB colorspace *pymupdf.Colorspace(pymupdf.CS\_RGB)*.

    Type:
    :   [Colorspace](colorspace.html#colorspace)

csGRAY
:   Predefined GRAY colorspace *pymupdf.Colorspace(pymupdf.CS\_GRAY)*.

    Type:
    :   [Colorspace](colorspace.html#colorspace)

csCMYK
:   Predefined CMYK colorspace *pymupdf.Colorspace(pymupdf.CS\_CMYK)*.

    Type:
    :   [Colorspace](colorspace.html#colorspace)

CS\_RGB
:   1 – Type of [Colorspace](colorspace.html#colorspace) is RGBA

    Type:
    :   int

CS\_GRAY
:   2 – Type of [Colorspace](colorspace.html#colorspace) is GRAY

    Type:
    :   int

CS\_CMYK
:   3 – Type of [Colorspace](colorspace.html#colorspace) is CMYK

    Type:
    :   int

mupdf\_version
:   ‘x.xx.x’ – MuPDF version that is being used by PyMuPDF.

    Type:
    :   string

mupdf\_version\_tuple
:   MuPDF version as a tuple of integers, `(major, minor, patch)`.

    Type:
    :   tuple

pymupdf\_version
:   ‘x.xx.x’ – PyMuPDF version.

    Type:
    :   string

pymupdf\_version\_tuple
:   PyMuPDF version as a tuple of integers, `(major, minor, patch)`.

    Type:
    :   tuple

pymupdf\_date
:   Disabled (set to None) in 1.26.1.

version
:   (pymupdf\_version, mupdf\_version, timestamp) – combined version information where `timestamp` is the generation point in time formatted as “YYYYMMDDhhmmss”.

    Type:
    :   tuple

VersionBind
:   Legacy equivalent to [`mupdf_version`](#mupdf_version "mupdf_version").

VersionFitz
:   Legacy equivalent to [`pymupdf_version`](#pymupdf_version "pymupdf_version").

VersionDate
:   Disabled (set to None) in 1.26.1.

## Document Permissions

| Code | Permitted Action |
| --- | --- |
| PDF\_PERM\_PRINT | Print the document |
| PDF\_PERM\_MODIFY | Modify the document’s contents |
| PDF\_PERM\_COPY | Copy or otherwise extract text and graphics |
| PDF\_PERM\_ANNOTATE | Add or modify text annotations and interactive form fields |
| PDF\_PERM\_FORM | Fill in forms and sign the document |
| PDF\_PERM\_ACCESSIBILITY | Obsolete, always permitted |
| PDF\_PERM\_ASSEMBLE | Insert, rotate, or delete pages, bookmarks, thumbnail images |
| PDF\_PERM\_PRINT\_HQ | High quality printing |

## PDF Optional Content Codes

| Code | Meaning |
| --- | --- |
| PDF\_OC\_ON | Set an OCG to ON temporarily |
| PDF\_OC\_TOGGLE | Toggle OCG status temporarily |
| PDF\_OC\_OFF | Set an OCG to OFF temporarily |

## PDF encryption method codes

| Code | Meaning |
| --- | --- |
| PDF\_ENCRYPT\_KEEP | do not change |
| PDF\_ENCRYPT\_NONE | remove any encryption |
| PDF\_ENCRYPT\_RC4\_40 | RC4 40 bit |
| PDF\_ENCRYPT\_RC4\_128 | RC4 128 bit |
| PDF\_ENCRYPT\_AES\_128 | *Advanced Encryption Standard* 128 bit |
| PDF\_ENCRYPT\_AES\_256 | *Advanced Encryption Standard* 256 bit |
| PDF\_ENCRYPT\_UNKNOWN | unknown |

## Font File Extensions

The table show file extensions you should use when saving fontfile buffers extracted from a PDF. This string is returned by [`Document.get_page_fonts()`](document.html#Document.get_page_fonts "Document.get_page_fonts"), [`Page.get_fonts()`](page.html#Page.get_fonts "Page.get_fonts") and [`Document.extract_font()`](document.html#Document.extract_font "Document.extract_font").

| Ext | Description |
| --- | --- |
| ttf | TrueType font |
| pfa | Postscript for ASCII font (various subtypes) |
| cff | Type1C font (compressed font equivalent to Type1) |
| cid | character identifier font (postscript format) |
| otf | OpenType font |
| n/a | not extractable, e.g. [PDF Base 14 Fonts](app3.html#base-14-fonts), Type 3 fonts and others |

## Text Alignment

TEXT\_ALIGN\_LEFT
:   0 – align left.

TEXT\_ALIGN\_CENTER
:   1 – align center.

TEXT\_ALIGN\_RIGHT
:   2 – align right.

TEXT\_ALIGN\_JUSTIFY
:   3 – align justify.

## Font Properties

Please note that the following bits are derived from what a font has to say about its properties. It may not be (and quite often is not) correct.

TEXT\_FONT\_SUPERSCRIPT
:   1 – the character or span is a superscript. This property is computed by MuPDF and not part of any font information.

TEXT\_FONT\_ITALIC
:   2 – the font is italic.

TEXT\_FONT\_SERIFED
:   4 – the font is serifed.

TEXT\_FONT\_MONOSPACED
:   8 – the font is mono-spaced.

TEXT\_FONT\_BOLD
:   16 – the font is bold.

## Text Extraction Flags

Option bits controlling the amount of data, that are parsed into a [TextPage](textpage.html#textpage).

For the PyMuPDF programmer, some combination (using Python’s `|` operator, or simply use `+`) of these values are aggregated in the `flags` integer, a parameter of all text search and text extraction methods. Depending on the individual method, different default combinations of the values are used. Please use a value that meets your situation. Especially make sure to switch off image extraction unless you really need them. The impact on performance and memory is significant!

TEXT\_PRESERVE\_LIGATURES
:   1 – If set, ligatures are passed through to the application in their original form. Otherwise ligatures are expanded into their constituent parts, e.g. the ligature “ffi” is expanded into three eparate characters f, f and i. Default is “on” in PyMuPDF. MuPDF supports the following 7 ligatures: “ff”, “fi”, “fl”, “ffi”, “ffl”, , “ft”, “st”.

TEXT\_PRESERVE\_WHITESPACE
:   2 – If set, whitespace is passed through. Otherwise any type of horizontal whitespace (including horizontal tabs) will be replaced with space characters of variable width. Default is “on” in PyMuPDF.

TEXT\_PRESERVE\_IMAGES
:   4 – If set, then images will be stored in the [TextPage](textpage.html#textpage). This causes the presence of (usually large!) binary image content in the output of text extractions of types “blocks”, “dict”, “json”, “rawdict”, “rawjson”, “html”, and “xhtml” and is the default there. If used with “blocks” however, only image metadata will be returned, not the image itself.

TEXT\_INHIBIT\_SPACES
:   8 – If set, Mupdf will not try to add missing space characters where there are large gaps between characters. In PDF, the creator often does not insert spaces to point to the next character’s position, but will provide the direct location address. The default in PyMuPDF is “off” – so spaces **will be generated**.

TEXT\_DEHYPHENATE
:   16 – Ignore hyphens at line ends and join with next line. Used internally with the text search functions. However, it is generally available: if on, text extractions will return joined text lines (or spans) with the ending hyphen of the first line eliminated. So two separate spans **“first meth-”** and **“od leads to wrong results”** on different lines will be joined to one span **“first method leads to wrong results”** and correspondingly updated bboxes: the characters of the resulting span will no longer have identical y-coordinates.

TEXT\_PRESERVE\_SPANS
:   32 – Generate a new line for every span. Not used (“off”) in PyMuPDF, but available for your use. Every line in “dict”, “json”, “rawdict”, “rawjson” will contain exactly one span.

TEXT\_MEDIABOX\_CLIP
:   64 – Characters entirely outside a page’s **mediabox** or contained in other “clipped” areas will be ignored. This is default in PyMuPDF.

TEXT\_USE\_CID\_FOR\_UNKNOWN\_UNICODE
:   128 – Use raw character codes instead of U+FFFD. This is the default for **text extraction** in PyMuPDF. If you **want to detect** when encoding information is missing or uncertain, toggle this flag and scan for the presence of U+FFFD (= `chr(0xfffd)`) code points in the resulting text.

TEXT\_COLLECT\_STRUCTURE
:   256 – Extract or generate the [Document](document.html#document) structure. Detail documentation pending.

TEXT\_ACCURATE\_BBOXES
:   512 – Ignore metric values of all fonts when computing character boundary boxes – most prominently the [ascender](https://en.wikipedia.org/wiki/Ascender_(typography)) and [descender](https://en.wikipedia.org/wiki/Descender) values. Instead, follow the drawing commands of each character’s glyph and compute their rectangle hull as the bbox. This is the smallest rectangle wrapping all points used for drawing the visual appearance - see the [Shape](shape.html#shape) class for understanding the background. This will especially result in individual character heights. For instance a (white) space will have a **bbox of zero height** (because nothing is drawn) – in contrast to the non-zero boundary box generated when using font metrics. This option may be useful to cope with failures of getting meaningful boundary boxes, even for fonts containing errors. Its use will slow down text extraction somewhat because of the incurred computational effort.

    Note that this has no effect by default - one must also disable the global quad corrections setting with `pymupdf.TOOLS.unset_quad_corrections(True)`.

TEXT\_COLLECT\_VECTORS
:   1024 – Collect vector drawings into the [TextPage](textpage.html#textpage). These are stored as blocks alongside text and image blocks, depending on other extraction flags. See [`TextPage.extractBLOCKS()`](textpage.html#TextPage.extractBLOCKS "TextPage.extractBLOCKS") and [`TextPage.extractDICT()`](textpage.html#TextPage.extractDICT "TextPage.extractDICT") for details. Beyond these two methods, vector graphics extraction is also available for [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON "TextPage.extractJSON"), [`TextPage.extractRAWDICT()`](textpage.html#TextPage.extractRAWDICT "TextPage.extractRAWDICT"), [`TextPage.extractRAWJSON()`](textpage.html#TextPage.extractRAWJSON "TextPage.extractRAWJSON") and [`TextPage.extractXML()`](textpage.html#TextPage.extractXML "TextPage.extractXML").

TEXT\_IGNORE\_ACTUALTEXT
:   2048 – Ignore built-in differences between text appearing in e.g. PDF viewers versus text stored in the PDF. See [Adobe PDF References](app3.html#adobemanual), page 615 for background. If set, the **stored** (“replacement” text) is ignored in favor of the displayed text.

TEXT\_SEGMENT
:   4096 – Attempt to segment page into different regions. Detail documentation pending.

TEXT\_COLLECT\_STYLES
:   32768 – Request collecting text **decoration** properties. This includes text underlining and strikeout. In contrast to public awareness, these are not font properties, but are drawn separately as vector graphics or annotations on top of the text. In addition, the flag bit will also cause MuPDF to detect “fake bold” text. In many cases, Document creators **simulate bold** text by printing the same text multiple times with slight offsets. If this flag is set, such text will be marked as bold in the resulting text spans.

TEXT\_LAZY\_VECTORS
:   1048576 – Delay vector blocks in the extraction slightly to avoid breaking what would otherwise be continuous lines of text.

TEXT\_FUZZY\_VECTORS
:   2097152 – If this option is set, we ‘fuzzily’ collect rectangular vectors of the same colour together. This enables us to spot where ‘pixels’ or ‘slices’ of vectors are used to create the appearance of characters on the page without exploding the storage and processing time requirements.

The following constants represent the default combinations of the above for text extraction and searching:

TEXTFLAGS\_TEXT
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_WORDS
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_BLOCKS
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_DICT
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_RAWDICT
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_HTML
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_XHTML
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_PRESERVE_IMAGES | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_XML
:   `TEXT_PRESERVE_LIGATURES | TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_USE_CID_FOR_UNKNOWN_UNICODE`

TEXTFLAGS\_SEARCH
:   `TEXT_PRESERVE_WHITESPACE | TEXT_MEDIABOX_CLIP | TEXT_DEHYPHENATE`

## Link Destination Kinds

Possible values of [`linkDest.kind`](linkdest.html#linkDest.kind "linkDest.kind") (link destination kind).

LINK\_NONE
:   0 – No destination. Indicates a dummy link.

    Type:
    :   int

LINK\_GOTO
:   1 – Points to a place in this document.

    Type:
    :   int

LINK\_URI
:   2 – Points to a URI – typically a resource specified with internet syntax.

    - PyMuPDF treats any external link that contains a colon and does not start
      with `file:`, as [`LINK_URI`](#LINK_URI "LINK_URI").

    Type:
    :   int

LINK\_LAUNCH
:   3 – Launch (open) another file (of any “executable” type).

    - PyMuPDF treats any external link that starts with `file:` or doesn’t
      contain a colon, as [`LINK_LAUNCH`](#LINK_LAUNCH "LINK_LAUNCH").

    Type:
    :   int

LINK\_NAMED
:   4 – points to a named location.

    Type:
    :   int

LINK\_GOTOR
:   5 – Points to a place in another PDF document.

    Type:
    :   int

## Link Destination Flags

Note

The rightmost byte of this integer is a bit field, so test the truth of these bits with the *&* operator.

LINK\_FLAG\_L\_VALID
:   1 (bit 0) Top left x value is valid

    Type:
    :   bool

LINK\_FLAG\_T\_VALID
:   2 (bit 1) Top left y value is valid

    Type:
    :   bool

LINK\_FLAG\_R\_VALID
:   4 (bit 2) Bottom right x value is valid

    Type:
    :   bool

LINK\_FLAG\_B\_VALID
:   8 (bit 3) Bottom right y value is valid

    Type:
    :   bool

LINK\_FLAG\_FIT\_H
:   16 (bit 4) Horizontal fit

    Type:
    :   bool

LINK\_FLAG\_FIT\_V
:   32 (bit 5) Vertical fit

    Type:
    :   bool

LINK\_FLAG\_R\_IS\_ZOOM
:   64 (bit 6) Bottom right x is a zoom figure

    Type:
    :   bool

## Annotation Related Constants

See chapter 8.4.5, pp. 615 of the [Adobe PDF References](app3.html#adobemanual) for details.

### Annotation Types

These identifiers also cover **links** and **widgets**: the PDF specification technically handles them all in the same way, whereas MuPDF (and PyMuPDF) treats them as three basically different types of objects.

```
PDF_ANNOT_TEXT 0
PDF_ANNOT_LINK 1  # <=== Link object in PyMuPDF
PDF_ANNOT_FREE_TEXT 2
PDF_ANNOT_LINE 3
PDF_ANNOT_SQUARE 4
PDF_ANNOT_CIRCLE 5
PDF_ANNOT_POLYGON 6
PDF_ANNOT_POLY_LINE 7
PDF_ANNOT_HIGHLIGHT 8
PDF_ANNOT_UNDERLINE 9
PDF_ANNOT_SQUIGGLY 10
PDF_ANNOT_STRIKE_OUT 11
PDF_ANNOT_REDACT 12
PDF_ANNOT_STAMP 13
PDF_ANNOT_CARET 14
PDF_ANNOT_INK 15
PDF_ANNOT_POPUP 16
PDF_ANNOT_FILE_ATTACHMENT 17
PDF_ANNOT_SOUND 18
PDF_ANNOT_MOVIE 19
PDF_ANNOT_RICH_MEDIA 20
PDF_ANNOT_WIDGET 21  # <=== Widget object in PyMuPDF
PDF_ANNOT_SCREEN 22
PDF_ANNOT_PRINTER_MARK 23
PDF_ANNOT_TRAP_NET 24
PDF_ANNOT_WATERMARK 25
PDF_ANNOT_3D 26
PDF_ANNOT_PROJECTION 27
PDF_ANNOT_UNKNOWN -1
```

### Annotation Flag Bits

```
PDF_ANNOT_IS_INVISIBLE 1 << (1-1)
PDF_ANNOT_IS_HIDDEN 1 << (2-1)
PDF_ANNOT_IS_PRINT 1 << (3-1)
PDF_ANNOT_IS_NO_ZOOM 1 << (4-1)
PDF_ANNOT_IS_NO_ROTATE 1 << (5-1)
PDF_ANNOT_IS_NO_VIEW 1 << (6-1)
PDF_ANNOT_IS_READ_ONLY 1 << (7-1)
PDF_ANNOT_IS_LOCKED 1 << (8-1)
PDF_ANNOT_IS_TOGGLE_NO_VIEW 1 << (9-1)
PDF_ANNOT_IS_LOCKED_CONTENTS 1 << (10-1)
```

### Annotation Line Ending Styles

```
PDF_ANNOT_LE_NONE 0
PDF_ANNOT_LE_SQUARE 1
PDF_ANNOT_LE_CIRCLE 2
PDF_ANNOT_LE_DIAMOND 3
PDF_ANNOT_LE_OPEN_ARROW 4
PDF_ANNOT_LE_CLOSED_ARROW 5
PDF_ANNOT_LE_BUTT 6
PDF_ANNOT_LE_R_OPEN_ARROW 7
PDF_ANNOT_LE_R_CLOSED_ARROW 8
PDF_ANNOT_LE_SLASH 9
```

## Widget Constants

### Widget Types (*field\_type*)

```
PDF_WIDGET_TYPE_UNKNOWN 0
PDF_WIDGET_TYPE_BUTTON 1
PDF_WIDGET_TYPE_CHECKBOX 2
PDF_WIDGET_TYPE_COMBOBOX 3
PDF_WIDGET_TYPE_LISTBOX 4
PDF_WIDGET_TYPE_RADIOBUTTON 5
PDF_WIDGET_TYPE_SIGNATURE 6
PDF_WIDGET_TYPE_TEXT 7
```

### Text Widget Subtypes (*text\_format*)

```
PDF_WIDGET_TX_FORMAT_NONE 0
PDF_WIDGET_TX_FORMAT_NUMBER 1
PDF_WIDGET_TX_FORMAT_SPECIAL 2
PDF_WIDGET_TX_FORMAT_DATE 3
PDF_WIDGET_TX_FORMAT_TIME 4
```

### Widget flags (*field\_flags*)

**Common to all field types**:

```
PDF_FIELD_IS_READ_ONLY 1
PDF_FIELD_IS_REQUIRED 1 << 1
PDF_FIELD_IS_NO_EXPORT 1 << 2
```

**Text widgets**:

```
PDF_TX_FIELD_IS_MULTILINE  1 << 12
PDF_TX_FIELD_IS_PASSWORD  1 << 13
PDF_TX_FIELD_IS_FILE_SELECT  1 << 20
PDF_TX_FIELD_IS_DO_NOT_SPELL_CHECK  1 << 22
PDF_TX_FIELD_IS_DO_NOT_SCROLL  1 << 23
PDF_TX_FIELD_IS_COMB  1 << 24
PDF_TX_FIELD_IS_RICH_TEXT  1 << 25
```

**Button widgets**:

```
PDF_BTN_FIELD_IS_NO_TOGGLE_TO_OFF  1 << 14
PDF_BTN_FIELD_IS_RADIO  1 << 15
PDF_BTN_FIELD_IS_PUSHBUTTON  1 << 16
PDF_BTN_FIELD_IS_RADIOS_IN_UNISON  1 << 25
```

**Choice widgets**:

```
PDF_CH_FIELD_IS_COMBO  1 << 17
PDF_CH_FIELD_IS_EDIT  1 << 18
PDF_CH_FIELD_IS_SORT  1 << 19
PDF_CH_FIELD_IS_MULTI_SELECT  1 << 21
PDF_CH_FIELD_IS_DO_NOT_SPELL_CHECK  1 << 22
PDF_CH_FIELD_IS_COMMIT_ON_SEL_CHANGE  1 << 26
```

## PDF Standard Blend Modes

For an explanation see [Adobe PDF References](app3.html#adobemanual), page 324:

```
PDF_BM_Color "Color"
PDF_BM_ColorBurn "ColorBurn"
PDF_BM_ColorDodge "ColorDodge"
PDF_BM_Darken "Darken"
PDF_BM_Difference "Difference"
PDF_BM_Exclusion "Exclusion"
PDF_BM_HardLight "HardLight"
PDF_BM_Hue "Hue"
PDF_BM_Lighten "Lighten"
PDF_BM_Luminosity "Luminosity"
PDF_BM_Multiply "Multiply"
PDF_BM_Normal "Normal"
PDF_BM_Overlay "Overlay"
PDF_BM_Saturation "Saturation"
PDF_BM_Screen "Screen"
PDF_BM_SoftLight "Softlight"
```

## Stamp Annotation Icons

MuPDF has defined the following icons for **rubber stamp** annotations:

```
STAMP_Approved 0
STAMP_AsIs 1
STAMP_Confidential 2
STAMP_Departmental 3
STAMP_Experimental 4
STAMP_Expired 5
STAMP_Final 6
STAMP_ForComment 7
STAMP_ForPublicRelease 8
STAMP_NotApproved 9
STAMP_NotForPublicRelease 10
STAMP_Sold 11
STAMP_TopSecret 12
STAMP_Draft 13
```

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.