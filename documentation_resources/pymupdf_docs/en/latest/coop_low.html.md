<!-- Source: https://pymupdf.readthedocs.io/en/latest/coop_low.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Working together: DisplayList and TextPage

Here are some instructions on how to use these classes together.

In some situations, performance improvements may be achievable, when you fall back to the detail level explained here.

## Create a DisplayList

A [DisplayList](displaylist.html#displaylist) represents an interpreted document page. Methods for pixmap creation, text extraction and text search are – behind the curtain – all using the page’s display list to perform their tasks. If a page must be rendered several times (e.g. because of changed zoom levels), or if text search and text extraction should both be performed, overhead can be saved, if the display list is created only once and then used for all other tasks.

```
>>> dl = page.get_displaylist()              # create the display list
```

You can also create display lists for many pages “on stack” (in a list), may be during document open, during idling times, or you store it when a page is visited for the first time (e.g. in GUI scripts).

Note, that for everything what follows, only the display list is needed – the corresponding [Page](page.html#page) object could have been deleted.

## Generate Pixmap

The following creates a Pixmap from a [DisplayList](displaylist.html#displaylist). Parameters are the same as for [`Page.get_pixmap()`](page.html#Page.get_pixmap "Page.get_pixmap").

```
>>> pix = dl.get_pixmap()                    # create the page's pixmap
```

The execution time of this statement may be up to 50% shorter than that of [`Page.get_pixmap()`](page.html#Page.get_pixmap "Page.get_pixmap").

## Perform Text Search

With the display list from above, we can also search for text.

For this we need to create a [TextPage](textpage.html#textpage).

```
>>> tp = dl.get_textpage()                    # display list from above
>>> rlist = tp.search("needle")              # look up "needle" locations
>>> for r in rlist:                          # work with the found locations, e.g.
        pix.invert_irect(r.irect)             # invert colors in the rectangles
```

## Extract Text

With the same [TextPage](textpage.html#textpage) object from above, we can now immediately use any or all of the 5 text extraction methods.

Note

Above, we have created our text page without argument. This leads to a default argument of 3 (`ligatures` and white-space are preserved), IAW images will **not** be extracted – see below.

```
>>> txt  = tp.extractText()                  # plain text format
>>> json = tp.extractJSON()                  # json format
>>> html = tp.extractHTML()                  # HTML format
>>> xml  = tp.extractXML()                   # XML format
>>> xml  = tp.extractXHTML()                 # XHTML format
```

## Further Performance improvements

### Pixmap

As explained in the [Page](page.html#page) chapter:

If you do not need transparency set *alpha = 0* when creating pixmaps. This will save 25% memory (if RGB, the most common case) and possibly 5% execution time (depending on the GUI software).

### TextPage

If you do not need images extracted alongside the text of a page, you can set the following option:

```
>>> flags = pymupdf.TEXT_PRESERVE_LIGATURES | pymupdf.TEXT_PRESERVE_WHITESPACE
>>> tp = dl.get_textpage(flags)
```

This will save ca. 25% overall execution time for the HTML, XHTML and JSON text extractions and **hugely** reduce the amount of storage (both, memory and disk space) if the document is graphics oriented.

If you however do need images, use a value of 7 for flags:

```
>>> flags = pymupdf.TEXT_PRESERVE_LIGATURES | pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_PRESERVE_IMAGES
```

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.