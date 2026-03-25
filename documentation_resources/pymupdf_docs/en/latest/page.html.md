<!-- Source: https://pymupdf.readthedocs.io/en/latest/page.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Page

Class representing a document page. A page object is created by [`Document.load_page()`](document.html#Document.load_page "Document.load_page") or, equivalently, via indexing the document like `doc[n]` - it has no independent constructor.

There is a parent-child relationship between a document and its pages. If the document is closed or deleted, all page objects (and their respective children, too) in existence will become unusable (“orphaned”): If a page property or method is being used, an exception is raised.

Several page methods have a [Document](document.html#document) counterpart for convenience. At the end of this chapter you will find a synopsis.

Note

Many times in this chapter we are using the term **coordinate**. It is of high importance to have at least a basic understanding of what that is and that you feel comfortable with the section [Coordinates](app3.html#coordinates).

## Modifying Pages

Changing page properties and adding or changing page content is available for PDF documents only.

In a nutshell, this is what you can do with PyMuPDF:

- Modify page rotation and the visible part (“cropbox”) of the page.
- Insert images, other PDF pages, text and simple geometrical objects.
- Add annotations and form fields.

Note

Methods require coordinates (points, rectangles) to put content in desired places. Please be aware that these coordinates **must always** be provided relative to the **unrotated** page (since v1.17.0). The reverse is also true: except [`Page.rect`](#Page.rect "Page.rect"), resp. [`Page.bound()`](#Page.bound "Page.bound") (both *reflect* when the page is rotated), all coordinates returned by methods and attributes pertain to the unrotated page.

So the returned value of e.g. [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox") will not change if you do a [`Page.set_rotation()`](#Page.set_rotation "Page.set_rotation"). The same is true for coordinates returned by [`Page.get_text()`](#Page.get_text "Page.get_text"), annotation rectangles, and so on. If you want to find out, where an object is located in **rotated coordinates**, multiply the coordinates with [`Page.rotation_matrix`](#Page.rotation_matrix "Page.rotation_matrix"). There also is its inverse, [`Page.derotation_matrix`](#Page.derotation_matrix "Page.derotation_matrix"), which you can use when interfacing with other readers, which may behave differently in this respect.

Note

If you add or update annotations, links or form fields on the page and immediately afterwards need to work with them (i.e. **without leaving the page**), you should reload the page using [`Document.reload_page()`](document.html#Document.reload_page "Document.reload_page") before referring to these new or updated items.

Reloading the page is generally recommended – although not strictly required in all cases. However, some annotation and widget types have extended features in PyMuPDF compared to MuPDF. More of these extensions may also be added in the future.

Releoading the page ensures all your changes have been fully applied to PDF structures, so you can safely create Pixmaps or successfully iterate over annotations, links and form fields.

| **Method / Attribute** | **Short Description** |
| --- | --- |
| [`Page.add_caret_annot()`](#Page.add_caret_annot "Page.add_caret_annot") | PDF only: add a caret annotation |
| [`Page.add_circle_annot()`](#Page.add_circle_annot "Page.add_circle_annot") | PDF only: add a circle annotation |
| [`Page.add_file_annot()`](#Page.add_file_annot "Page.add_file_annot") | PDF only: add a file attachment annotation |
| [`Page.add_freetext_annot()`](#Page.add_freetext_annot "Page.add_freetext_annot") | PDF only: add a text annotation |
| [`Page.add_highlight_annot()`](#Page.add_highlight_annot "Page.add_highlight_annot") | PDF only: add a “highlight” annotation |
| [`Page.add_ink_annot()`](#Page.add_ink_annot "Page.add_ink_annot") | PDF only: add an ink annotation |
| [`Page.add_line_annot()`](#Page.add_line_annot "Page.add_line_annot") | PDF only: add a line annotation |
| [`Page.add_polygon_annot()`](#Page.add_polygon_annot "Page.add_polygon_annot") | PDF only: add a polygon annotation |
| [`Page.add_polyline_annot()`](#Page.add_polyline_annot "Page.add_polyline_annot") | PDF only: add a multi-line annotation |
| [`Page.add_rect_annot()`](#Page.add_rect_annot "Page.add_rect_annot") | PDF only: add a rectangle annotation |
| [`Page.add_redact_annot()`](#Page.add_redact_annot "Page.add_redact_annot") | PDF only: add a redaction annotation |
| [`Page.add_squiggly_annot()`](#Page.add_squiggly_annot "Page.add_squiggly_annot") | PDF only: add a “squiggly” annotation |
| [`Page.add_stamp_annot()`](#Page.add_stamp_annot "Page.add_stamp_annot") | PDF only: add a “rubber stamp” annotation |
| [`Page.add_strikeout_annot()`](#Page.add_strikeout_annot "Page.add_strikeout_annot") | PDF only: add a “strike-out” annotation |
| [`Page.add_text_annot()`](#Page.add_text_annot "Page.add_text_annot") | PDF only: add a comment |
| [`Page.add_underline_annot()`](#Page.add_underline_annot "Page.add_underline_annot") | PDF only: add an “underline” annotation |
| [`Page.add_widget()`](#Page.add_widget "Page.add_widget") | PDF only: add a PDF Form field |
| [`Page.annot_names()`](#Page.annot_names "Page.annot_names") | PDF only: a list of annotation (and widget) names |
| [`Page.annot_xrefs()`](#Page.annot_xrefs "Page.annot_xrefs") | PDF only: a list of annotation (and widget) xrefs |
| [`Page.annots()`](#Page.annots "Page.annots") | return a generator over the annots on the page |
| [`Page.apply_redactions()`](#Page.apply_redactions "Page.apply_redactions") | PDF only: process the redactions of the page |
| [`Page.clip_to_rect()`](#Page.clip_to_rect "Page.clip_to_rect") | PDF only: remove page content outside a rectangle |
| [`Page.bound()`](#Page.bound "Page.bound") | rectangle of the page |
| [`Page.cluster_drawings()`](#Page.cluster_drawings "Page.cluster_drawings") | PDF only: bounding boxes of vector graphics |
| [`Page.delete_annot()`](#Page.delete_annot "Page.delete_annot") | PDF only: delete an annotation |
| [`Page.delete_image()`](#Page.delete_image "Page.delete_image") | PDF only: delete an image |
| [`Page.delete_link()`](#Page.delete_link "Page.delete_link") | PDF only: delete a link |
| [`Page.delete_widget()`](#Page.delete_widget "Page.delete_widget") | PDF only: delete a widget / field |
| [`Page.draw_bezier()`](#Page.draw_bezier "Page.draw_bezier") | PDF only: draw a cubic Bezier curve |
| [`Page.draw_circle()`](#Page.draw_circle "Page.draw_circle") | PDF only: draw a circle |
| [`Page.draw_curve()`](#Page.draw_curve "Page.draw_curve") | PDF only: draw a special Bezier curve |
| [`Page.draw_line()`](#Page.draw_line "Page.draw_line") | PDF only: draw a line |
| [`Page.draw_oval()`](#Page.draw_oval "Page.draw_oval") | PDF only: draw an oval / ellipse |
| [`Page.draw_polyline()`](#Page.draw_polyline "Page.draw_polyline") | PDF only: connect a point sequence |
| [`Page.draw_quad()`](#Page.draw_quad "Page.draw_quad") | PDF only: draw a quad |
| [`Page.draw_rect()`](#Page.draw_rect "Page.draw_rect") | PDF only: draw a rectangle |
| [`Page.draw_sector()`](#Page.draw_sector "Page.draw_sector") | PDF only: draw a circular sector |
| [`Page.draw_squiggle()`](#Page.draw_squiggle "Page.draw_squiggle") | PDF only: draw a squiggly line |
| [`Page.draw_zigzag()`](#Page.draw_zigzag "Page.draw_zigzag") | PDF only: draw a zig-zagged line |
| [`Page.find_tables()`](#Page.find_tables "Page.find_tables") | locate tables on the page |
| [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings") | get vector graphics on page |
| [`Page.get_fonts()`](#Page.get_fonts "Page.get_fonts") | PDF only: get list of referenced fonts |
| [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox") | PDF only: get bbox and matrix of embedded image |
| [`Page.get_image_info()`](#Page.get_image_info "Page.get_image_info") | get list of meta information for all used images |
| [`Page.get_image_rects()`](#Page.get_image_rects "Page.get_image_rects") | PDF only: improved version of [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox") |
| [`Page.get_images()`](#Page.get_images "Page.get_images") | PDF only: get list of referenced images |
| [`Page.get_label()`](#Page.get_label "Page.get_label") | PDF only: return the label of the page |
| [`Page.get_links()`](#Page.get_links "Page.get_links") | get all links |
| [`Page.get_pixmap()`](#Page.get_pixmap "Page.get_pixmap") | create a page image in raster format |
| [`Page.get_svg_image()`](#Page.get_svg_image "Page.get_svg_image") | create a page image in SVG format |
| [`Page.get_text()`](#Page.get_text "Page.get_text") | extract the page’s text |
| [`Page.get_textbox()`](#Page.get_textbox "Page.get_textbox") | extract text contained in a rectangle |
| [`Page.get_textpage_ocr()`](#Page.get_textpage_ocr "Page.get_textpage_ocr") | create a TextPage with OCR for the page |
| [`Page.get_textpage()`](#Page.get_textpage "Page.get_textpage") | create a TextPage for the page |
| [`Page.get_xobjects()`](#Page.get_xobjects "Page.get_xobjects") | PDF only: get list of referenced xobjects |
| [`Page.insert_font()`](#Page.insert_font "Page.insert_font") | PDF only: insert a font for use by the page |
| [`Page.insert_image()`](#Page.insert_image "Page.insert_image") | PDF only: insert an image |
| [`Page.insert_link()`](#Page.insert_link "Page.insert_link") | PDF only: insert a link |
| [`Page.insert_text()`](#Page.insert_text "Page.insert_text") | PDF only: insert text |
| [`Page.insert_htmlbox()`](#Page.insert_htmlbox "Page.insert_htmlbox") | PDF only: insert html text in a rectangle |
| [`Page.insert_textbox()`](#Page.insert_textbox "Page.insert_textbox") | PDF only: insert a text box |
| [`Page.links()`](#Page.links "Page.links") | return a generator of the links on the page |
| [`Page.load_annot()`](#Page.load_annot "Page.load_annot") | PDF only: load a specific annotation |
| [`Page.load_widget()`](#Page.load_widget "Page.load_widget") | PDF only: load a specific field |
| [`Page.load_links()`](#Page.load_links "Page.load_links") | return the first link on a page |
| [`Page.new_shape()`](#Page.new_shape "Page.new_shape") | PDF only: create a new [Shape](shape.html#shape) |
| [`Page.recolor()`](#Page.recolor "Page.recolor") | PDF only: change the colorspace of objects |
| [`Page.remove_rotation()`](#Page.remove_rotation "Page.remove_rotation") | PDF only: set page rotation to 0 |
| [`Page.replace_image()`](#Page.replace_image "Page.replace_image") | PDF only: replace an image |
| [`Page.search_for()`](#Page.search_for "Page.search_for") | search for a string |
| [`Page.set_artbox()`](#Page.set_artbox "Page.set_artbox") | PDF only: modify `/ArtBox` |
| [`Page.set_bleedbox()`](#Page.set_bleedbox "Page.set_bleedbox") | PDF only: modify `/BleedBox` |
| [`Page.set_cropbox()`](#Page.set_cropbox "Page.set_cropbox") | PDF only: modify the `cropbox` (visible page) |
| [`Page.set_mediabox()`](#Page.set_mediabox "Page.set_mediabox") | PDF only: modify `/MediaBox` |
| [`Page.set_rotation()`](#Page.set_rotation "Page.set_rotation") | PDF only: set page rotation |
| [`Page.set_trimbox()`](#Page.set_trimbox "Page.set_trimbox") | PDF only: modify `/TrimBox` |
| [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page") | PDF only: display PDF page image |
| [`Page.update_link()`](#Page.update_link "Page.update_link") | PDF only: modify a link |
| [`Page.widgets()`](#Page.widgets "Page.widgets") | return a generator over the fields on the page |
| [`Page.write_text()`](#Page.write_text "Page.write_text") | write one or more [TextWriter](textwriter.html#textwriter) objects |
| [`Page.cropbox_position`](#Page.cropbox_position "Page.cropbox_position") | displacement of the `cropbox` |
| [`Page.cropbox`](#Page.cropbox "Page.cropbox") | the page’s `cropbox` |
| [`Page.artbox`](#Page.artbox "Page.artbox") | the page’s `/ArtBox` |
| [`Page.bleedbox`](#Page.bleedbox "Page.bleedbox") | the page’s `/BleedBox` |
| [`Page.trimbox`](#Page.trimbox "Page.trimbox") | the page’s `/TrimBox` |
| [`Page.derotation_matrix`](#Page.derotation_matrix "Page.derotation_matrix") | PDF only: get coordinates in unrotated page space |
| [`Page.first_annot`](#Page.first_annot "Page.first_annot") | first [Annot](annot.html#annot) on the page |
| [`Page.first_link`](#Page.first_link "Page.first_link") | first [Link](link.html#link) on the page |
| [`Page.first_widget`](#Page.first_widget "Page.first_widget") | first widget (form field) on the page |
| [`Page.mediabox_size`](#Page.mediabox_size "Page.mediabox_size") | bottom-right point of `mediabox` |
| [`Page.mediabox`](#Page.mediabox "Page.mediabox") | the page’s `mediabox` |
| [`Page.number`](#Page.number "Page.number") | page number |
| [`Page.parent`](#Page.parent "Page.parent") | owning document object |
| [`Page.rect`](#Page.rect "Page.rect") | rectangle of the page |
| [`Page.rotation_matrix`](#Page.rotation_matrix "Page.rotation_matrix") | PDF only: get coordinates in rotated page space |
| [`Page.rotation`](#Page.rotation "Page.rotation") | PDF only: page rotation |
| [`Page.transformation_matrix`](#Page.transformation_matrix "Page.transformation_matrix") | PDF only: translate between PDF and MuPDF space |
| [`Page.xref`](#Page.xref "Page.xref") | PDF only: page [`xref`](glossary.html#xref "xref") |

**Class API**

*class* Page
:   bound()
    :   Determine the rectangle of the page. Same as property [`Page.rect`](#Page.rect "Page.rect"). For PDF documents this **usually** also coincides with [`mediabox`](#Page.mediabox "Page.mediabox") and [`cropbox`](#Page.cropbox "Page.cropbox"), but not always. For example, if the page is rotated, then this is reflected by this method – the [`Page.cropbox`](#Page.cropbox "Page.cropbox") however will not change.

        Return type:
        :   [Rect](rect.html#rect)

    add\_caret\_annot(*point*)
    :   PDF only: Add a caret icon. A caret annotation is a visual symbol normally used to indicate the presence of text edits on the page.

        Parameters:
        :   **point** (*point\_like*) – the top left point of a 20 x 20 rectangle containing the MuPDF-provided icon.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. Stroke color blue = (0, 0, 1), no fill color support.

        Show/hide history

        - New in v1.16.0

    add\_text\_annot(*point*, *text*, *icon='Note'*)
    :   PDF only: Add a comment icon (“sticky note”) with accompanying text. Only the icon is visible, the accompanying text is hidden and can be visualized by many PDF viewers by hovering the mouse over the symbol.

        Parameters:
        :   - **point** (*point\_like*) – the top left point of a 20 x 20 rectangle containing the MuPDF-provided “note” icon.
            - **text** (*str*) – the commentary text. This will be shown on double clicking or hovering over the icon. May contain any Latin characters.
            - **icon** (*str*) – choose one of “Note” (default), “Comment”, “Help”, “Insert”, “Key”, “NewParagraph”, “Paragraph” as the visual symbol for the embodied text [[4]](#f4). (New in v1.16.0)

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. Stroke color yellow = (1, 1, 0), no fill color support.

    add\_freetext\_annot(*rect*, *text*, *\**, *fontsize=11*, *fontname='helv'*, *text\_color=0*, *fill\_color=None*, *border\_width=0*, *dashes=None*, *callout=None*, *line\_end=PDF\_ANNOT\_LE\_OPEN\_ARROW*, *opacity=1*, *align=TEXT\_ALIGN\_LEFT*, *rotate=0*, *richtext=False*, *style=None*)
    :   PDF only: Add text in a given rectangle. Optionally, the appearance of a “callout” shape can be requested by specifying two or three point-like objects – see below.

        Parameters:
        :   - **rect** (*rect\_like*) – the rectangle into which the text should be inserted. Text is automatically wrapped to a new line at box width. Text portions not fitting into the rectangle will be invisible without warning.
            - **text** (*str*) – the text. May contain any mixture of Latin, Greek, Cyrillic, Chinese, Japanese and Korean characters. If `richtext=True` (see below), the string is interpreted as HTML syntax. This adds a plethora of ways for attractive effects.
            - **fontsize** (*float*) – the [`fontsize`](glossary.html#fontsize "fontsize"). Default is 11. Ignored if `richtext=True`.
            - **fontname** (*str*) –

              The font name. Default is “Helv”. Ignored if `richtext=True`, otherwise the following **restritions apply:**

              - Accepted alternatives are “Helv” (Helvetica), “Cour” (Courier), “TiRo” (Timnes-Roman), “ZaDb” (ZapfDingBats) and “Symb” (Symbol). The name may be abbreviated to the first two characters, like “Co” for “Cour”, lower case accepted.
              - Bold or italic variants of the fonts are **not supported.**
            - **text\_color** (*list**,**tuple**,**float*) – the text color. Default is black. Ignored if `richtext=True`.
            - **fill\_color** (*list**,**tuple**,**float*) – the fill color. This is used for `rect` and the end point of the callout lines when applicable. Default is `None`.
            - **border\_color** (*list**,**tuple**,**float*) – This parameter **only has an effect** if `richtext=True`. Otherwise, `text_color` is used.
            - **border\_width** (*float*) – the width of border and `callout` lines. Default is 0 (no border), in which case callout lines may still appear with some hairline width, depending on the PDF viewer used. In any case, this value must be positive to see a border line.
            - **dashes** (*list**,**tuple*) – a list of floats specifying how border and callout lines should be dashed. Default is `None`.
            - **callout** (*list**,**tuple*) – a list / tuple of two or three [`point_like`](glossary.html#point_like "point_like") objects, which will be interpreted as end point [, knee point] and start point (in this sequence) of up to two line segments, converting this annotation into a call-out shape.
            - **line\_end** (*int*) – the line end symbol of the call-out line. It is drawn at the first point specified in the `callout` list. Default is an open arrow. For possible values see [Annotation Line Ending Styles](vars.html#annotationlineends).
            - **opacity** (*float*) – a float `0 <= opacity < 1` turning the annotation transparent. Default is no transparency.
            - **align** (*int*) – text alignment, one of TEXT\_ALIGN\_LEFT, TEXT\_ALIGN\_CENTER, TEXT\_ALIGN\_RIGHT - justify is **not supported**. Ignored if `richtext=True`.
            - **rotate** (*int*) – the text orientation. Accepted values are integer multiples of 90°. Invalid entries receive a rotation of 0.
            - **richtext** (*bool*) – treat `text` as HTML syntax. This allows to achieve **bold**, *italic*, arbitrary text colors, font sizes, text alignment including justify and more - as far as the PDF subset of HTML and styling instructions supports this. This is similar to what happens in [`Page.insert_htmlbox()`](#Page.insert_htmlbox "Page.insert_htmlbox"). The base library will for example pull in required fonts if it encounters characters not contained in the standard ones. Some parameters are ignored if this option is set, as mentioned above. Default is `False`.
            - **style** (*str*) – supply optional HTML styling information in CSS syntax. Ignored if `richtext=False`.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation.

        Show/hide history

        - Changed in v1.19.6: add border color parameter

    add\_file\_annot(*point*, *buffer\_*, *filename*, *ufilename=None*, *desc=None*, *icon='PushPin'*)
    :   PDF only: Add a file attachment annotation with a “PushPin” icon at the specified location.

        Parameters:
        :   - **pos** (*point\_like*) – the top-left point of a 18x18 rectangle containing the MuPDF-provided “PushPin” icon.
            - **buffer** (*bytes**,**bytearray**,**BytesIO*) –

              the data to be stored (actual file content, any data, etc.).

              Changed in v1.14.13: *io.BytesIO* is now also supported.
            - **filename** (*str*) – the filename to associate with the data.
            - **ufilename** (*str*) – the optional PDF unicode version of filename. Defaults to filename.
            - **desc** (*str*) – an optional description of the file. Defaults to filename.
            - **icon** (*str*) – choose one of “PushPin” (default), “Graph”, “Paperclip”, “Tag” as the visual symbol for the attached data [[4]](#f4). (New in v1.16.0)

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. Stroke color yellow = (1, 1, 0), no fill color support.

    add\_ink\_annot(*list*)
    :   PDF only: Add a “freehand” scribble annotation.

        Parameters:
        :   **list** (*sequence*) – a list of one or more lists, each containing [`point_like`](glossary.html#point_like "point_like") items. Each item in these sublists is interpreted as a [Point](point.html#point) through which a connecting line is drawn. Separate sublists thus represent separate drawing lines.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation in default appearance black =(0, 0, 0),line width 1. No fill color support.

    add\_line\_annot(*p1*, *p2*)
    :   PDF only: Add a line annotation.

        Parameters:
        :   - **p1** (*point\_like*) – the starting point of the line.
            - **p2** (*point\_like*) – the end point of the line.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. It is drawn with line (stroke) color red = (1, 0, 0) and line width 1. No fill color support. The **annot rectangle** is automatically created to contain both points, each one surrounded by a circle of radius 3 \* line width to make room for any line end symbols.

    add\_rect\_annot(*rect*)

    add\_circle\_annot(*rect*)
    :   PDF only: Add a rectangle, resp. circle annotation.

        Parameters:
        :   **rect** (*rect\_like*) – the rectangle in which the circle or rectangle is drawn, must be finite and not empty. If the rectangle is not equal-sided, an ellipse is drawn.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. It is drawn with line (stroke) color red = (1, 0, 0), line width 1, fill color is supported.

    ---

    ### Redactions

    add\_redact\_annot(*quad*, *text=None*, *fontname=None*, *fontsize=11*, *align=TEXT\_ALIGN\_LEFT*, *fill=(1, 1, 1)*, *text\_color=(0, 0, 0)*, *cross\_out=True*)
    :   **PDF only**: Add a redaction annotation. A redaction annotation identifies an area whose content should be removed from the document. Adding such an annotation is the first of two steps. It makes visible what will be removed in the subsequent step, [`Page.apply_redactions()`](#Page.apply_redactions "Page.apply_redactions").

        Parameters:
        :   - **quad** (*quad\_like**,**rect\_like*) – specifies the (rectangular) area to be removed which is always equal to the annotation rectangle. This may be a [`rect_like`](glossary.html#rect_like "rect_like") or [`quad_like`](glossary.html#quad_like "quad_like") object. If a quad is specified, then the enveloping rectangle is taken.
            - **text** (*str*) – text to be placed in the rectangle after applying the redaction (and thus removing old content). (New in v1.16.12)
            - **fontname** (*str*) – the font to use when `text` is given, otherwise ignored. Only CJK and the [PDF Base 14 Fonts](app3.html#base-14-fonts) are supported. Apart from this, the same rules apply as for [`Page.insert_textbox()`](#Page.insert_textbox "Page.insert_textbox") – which is what the method [`Page.apply_redactions()`](#Page.apply_redactions "Page.apply_redactions") internally invokes.
            - **fontsize** (*float*) – the [`fontsize`](glossary.html#fontsize "fontsize") to use for the replacing text. If the text is too large to fit, several insertion attempts will be made, gradually reducing the [`fontsize`](glossary.html#fontsize "fontsize") to no less than 4. If then the text will still not fit, no text insertion will take place at all. (New in v1.16.12)
            - **align** (*int*) – the horizontal alignment for the replacing text. See [`insert_textbox()`](#Page.insert_textbox "Page.insert_textbox") for available values. The vertical alignment is (approximately) centered.
            - **fill** (*sequence*) – the fill color of the rectangle **after applying** the redaction. The default is *white = (1, 1, 1)*, which is also taken if `None` is specified. To suppress a fill color altogether, specify `False`. In this cases the rectangle remains transparent. (New in v1.16.12)
            - **text\_color** (*sequence*) – the color of the replacing text. Default is *black = (0, 0, 0)*. (New in v1.16.12)
            - **cross\_out** (*bool*) – add two diagonal lines to the annotation rectangle. (New in v1.17.2)

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. Its standard appearance looks like a red rectangle (no fill color), optionally showing two diagonal lines. Colors, line width, dashing, opacity and blend mode can now be set and applied via [`Annot.update()`](annot.html#Annot.update "Annot.update") like with other annotations. (Changed in v1.17.2)

        Show/hide history

        - New in v1.16.11

    apply\_redactions(*images=PDF\_REDACT\_IMAGE\_PIXELS | 2*, *graphics=PDF\_REDACT\_LINE\_ART\_REMOVE\_IF\_COVERED | 1*, *text=PDF\_REDACT\_TEXT\_REMOVE | 0*)
    :   **PDF only**: Remove all **content** contained in any redaction rectangle on the page.

        **This method applies and then deletes all redactions from the page.**

        Parameters:
        :   - **images** (*int*) – How to redact overlapping images. The default `PDF_REDACT_IMAGE_PIXELS | 2` blanks out overlapping pixels. `PDF_REDACT_IMAGE_NONE | 0` ignores, and `PDF_REDACT_IMAGE_REMOVE | 1` completely removes images overlapping any redaction annotation. Option `PDF_REDACT_IMAGE_REMOVE_UNLESS_INVISIBLE | 3` only removes images that are actually visible.
            - **graphics** (*int*) – How to redact overlapping vector graphics (also called “line-art” or “drawings”). The default `PDF_REDACT_LINE_ART_REMOVE_IF_COVERED | 1` removes any overlapping vector graphics. `PDF_REDACT_LINE_ART_NONE | 0` ignores, and `PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED | 2` removes graphics fully contained in a redaction annotation. When removing line-art, please be aware that **stroked** vector graphics (i.e. type “s” or “sf”) have a **larger wrapping rectangle** than one might expect: first of all, at least 50% of the path’s line width have to be added in each direction to truly include all of the drawing. If a so-called “miter limit” is provided (see page 121 of the PDF specification), the enlarging value is `miter * width / 2`. So, when letting everything default (width = 1, miter = 10), the redaction rectangle should be at least 5 points larger in every direction.
            - **text** (*int*) – Whether to redact overlapping text. The default `PDF_REDACT_TEXT_REMOVE | 0` removes all characters whose boundary box overlaps any redaction rectangle. This complies with the original legal / data protection intentions of redaction annotations. Other use cases however may require to **keep text** while redacting vector graphics or images. This can be achieved by setting `text=True|PDF_REDACT_TEXT_NONE | 1`. This does **not comply** with the data protection intentions of redaction annotations. **Do so at your own risk.**

        Returns:
        :   `True` if at least one redaction annotation has been processed, `False` otherwise.

        Note

        - Text contained in a redaction rectangle will be **physically** removed from the page (assuming [`Document.save()`](document.html#Document.save "Document.save") with a suitable garbage option) and will no longer appear in e.g. text extractions or anywhere else. All redaction annotations will also be removed. Other annotations are unaffected.
        - All overlapping links will be removed. If the rectangle of the link was covering text, then only the overlapping part of the text is being removed. Similar applies to images covered by link rectangles.
        - The overlapping parts of **images** will be blanked-out for default option `PDF_REDACT_IMAGE_PIXELS` (changed in v1.18.0). Option 0 does not touch any images and 1 will remove any image with an overlap.
        - For option `images=PDF_REDACT_IMAGE_REMOVE` only this page’s **references to the images** are removed - not necessarily the images themselves. Images are completely removed from the file only, if no longer referenced at all (assuming suitable garbage collection options).
        - For option `images=PDF_REDACT_IMAGE_PIXELS` a new image of format PNG is created, which the page will use in place of the original one. The original image is not deleted or replaced as part of this process, so other pages may still show the original. In addition, the new, modified PNG image currently is **stored uncompressed**. Do keep these aspects in mind when choosing the right garbage collection method and compression options during save.
        - **Text removal** is done by character: A character is removed if its bbox has a **non-empty overlap** with a redaction rectangle (changed in MuPDF v1.17). Depending on the font properties and / or the chosen line height, deletion may occur for undesired text parts. Using [`Tools.set_small_glyph_heights()`](tools.html#Tools.set_small_glyph_heights "Tools.set_small_glyph_heights") with a `True` argument before text search may help to prevent this.
        - Redactions are a simple way to replace single words in a PDF, or to just physically remove them. Locate the word “secret” using some text extraction or search method and insert a redaction using “xxxxxx” as replacement text for each occurrence.

          - Be wary if the replacement is longer than the original – this may lead to an awkward appearance, line breaks or no new text at all.
          - For a number of reasons, the new text may not exactly be positioned on the same line like the old one – especially true if the replacement font was not one of CJK or [PDF Base 14 Fonts](app3.html#base-14-fonts).

        Show/hide history

        - New in v1.16.11
        - Changed in v1.16.12: The previous *mark* parameter is gone. Instead, the respective rectangles are filled with the individual *fill* color of each redaction annotation. If a *text* was given in the annotation, then [`insert_textbox()`](#Page.insert_textbox "Page.insert_textbox") is invoked to insert it, using parameters provided with the redaction.
        - Changed in v1.18.0: added option for handling images that overlap redaction areas.
        - Changed in v1.23.27: added option for removing graphics as well.
        - Changed in v1.24.2: added option `keep_text` to leave text untouched.

    ---

    add\_polyline\_annot(*points*)

    add\_polygon\_annot(*points*)
    :   PDF only: Add an annotation consisting of lines which connect the given points. A **Polygon’s** first and last points are automatically connected, which does not happen for a **PolyLine**. The **rectangle** is automatically created as the smallest rectangle containing the points, each one surrounded by a circle of radius 3 (= 3 \* line width). The following shows a ‘PolyLine’ that has been modified with colors and line ends.

        Parameters:
        :   **points** (*list*) – a list of [`point_like`](glossary.html#point_like "point_like") objects.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the created annotation. It is drawn with line color black, line width 1 no fill color but fill color support. Use methods of [Annot](annot.html#annot) to make any changes to achieve something like this:

    add\_underline\_annot(*quads=None*, *start=None*, *stop=None*, *clip=None*)

    add\_strikeout\_annot(*quads=None*, *start=None*, *stop=None*, *clip=None*)

    add\_squiggly\_annot(*quads=None*, *start=None*, *stop=None*, *clip=None*)

    add\_highlight\_annot(*quads=None*, *start=None*, *stop=None*, *clip=None*)
    :   PDF only: These annotations are normally used for **marking text** which has previously been somehow located (for example via [`Page.search_for()`](#Page.search_for "Page.search_for")). But this is not required: you are free to “mark” just anything.

        Standard (stroke only – no fill color support) colors are chosen per annotation type: **yellow** for highlighting, **red** for striking out, **green** for underlining, and **magenta** for wavy underlining.

        All these four methods convert the arguments into a list of [Quad](quad.html#quad) objects. The **annotation** rectangle is then calculated to envelop all these quadrilaterals.

        Note

        [`search_for()`](#Page.search_for "Page.search_for") delivers a list of either [Rect](rect.html#rect) or [Quad](quad.html#quad) objects. Such a list can be directly used as an argument for these annotation types and will deliver **one common annotation** for all occurrences of the search string:

        ```
        >>> # prefer quads=True in text searching for annotations!
        >>> quads = page.search_for("pymupdf", quads=True)
        >>> page.add_highlight_annot(quads)
        ```

        Note

        Obviously, text marker annotations need to know what is the top, the bottom, the left, and the right side of the area(s) to be marked. If the arguments are quads, this information is given by the sequence of the quad points. In contrast, a rectangle delivers much less information – this is illustrated by the fact, that 4! = 24 different quads can be constructed with the four corners of a rectangle.

        Therefore, we **strongly recommend** to use the `quads` option for text searches, to ensure correct annotations. A similar consideration applies to marking **text spans** extracted with the “dict” / “rawdict” options of [`Page.get_text()`](#Page.get_text "Page.get_text"). For more details on how to compute quadrilaterals in this case, see section “How to Mark Non-horizontal Text” of [FAQ](faq.html#faq).

        Parameters:
        :   - **quads** (*rect\_like**,**quad\_like**,**list**,**tuple*) – the location(s) – rectangle(s) or quad(s) – to be marked. (Changed in v1.14.20)
              A list or tuple must consist of [`rect_like`](glossary.html#rect_like "rect_like") or [`quad_like`](glossary.html#quad_like "quad_like") items (or even a mixture of either).
              Every item must be finite, convex and not empty (as applicable).
              **Set this parameter to** `None` if you want to use the following arguments (Changed in v1.16.14).
              And vice versa: if not `None`, the remaining parameters must be `None`.
            - **start** (*point\_like*) – start text marking at this point. Defaults to the top-left point of *clip*. Must be provided if `quads` is `None`. (New in v1.16.14)
            - **stop** (*point\_like*) – stop text marking at this point. Defaults to the bottom-right point of *clip*. Must be used if `quads` is `None`. (New in v1.16.14)
            - **clip** (*rect\_like*) – only consider text lines intersecting this area. Defaults to the page rectangle. Only use if `start` and `stop` are provided. (New in v1.16.14)

        Return type:
        :   [Annot](annot.html#annot) or `None` (changed in v1.16.14).

        Returns:
        :   the created annotation. If *quads* is an empty list, **no annotation** is created (changed in v1.16.14).

        Note

        You can use parameters *start*, *stop* and *clip* to highlight consecutive lines between the points *start* and *stop* (starting with v1.16.14).
        Make use of *clip* to further reduce the selected line bboxes and thus deal with e.g. multi-column pages.
        The following multi-line highlight on a page with three text columns was created by specifying the two red points and setting clip accordingly.

    cluster\_drawings(*clip=None*, *drawings=None*, *x\_tolerance=3*, *y\_tolerance=3*, *final\_filter=True*)
    :   Cluster vector graphics (synonyms are line-art or drawings) based on their geometrical vicinity. The method walks through the output of [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings") and joins paths whose `path["rect"]` are closer to each other than some tolerance values (given in the arguments). The result is a list of rectangles that each wrap things like tables (with gridlines), pie charts, bar charts, etc.

        Parameters:
        :   - **clip** (*rect\_like*) – only consider paths inside this area. The default is the full page.
            - **drawings** (*list*) – (optional) provide a previously generated output of [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings"). If `None` the method will execute the method.
            - **y\_tolerance** (*float x\_tolerance /*) – Assume vector graphics to be close enough neighbors for belonging to the same rectangle. Default is 3 points.
            - **final\_filter** (*bool*) – If `True` (default), the method will to remove rectangles having width or height smaller than the respective tolerance value. If `False` no such filtering is done.

    find\_tables(*clip=None*, *strategy=None*, *vertical\_strategy=None*, *horizontal\_strategy=None*, *vertical\_lines=None*, *horizontal\_lines=None*, *snap\_tolerance=None*, *snap\_x\_tolerance=None*, *snap\_y\_tolerance=None*, *join\_tolerance=None*, *join\_x\_tolerance=None*, *join\_y\_tolerance=None*, *edge\_min\_length=3*, *min\_words\_vertical=3*, *min\_words\_horizontal=1*, *intersection\_tolerance=None*, *intersection\_x\_tolerance=None*, *intersection\_y\_tolerance=None*, *text\_tolerance=None*, *text\_x\_tolerance=None*, *text\_y\_tolerance=None*, *add\_lines=None*, *add\_boxes=None*, *paths=None*)
    :   Find tables on the page and return an object with related information. Typically, the default values of the many parameters will be sufficient. Adjustments should ever only be needed in corner case situations.

        Parameters:
        :   - **clip** (*rect\_like*) – specify a region to consider within the page rectangle and ignore the rest. Default is the full page.
            - **strategy** (*str*) –

              Request a **table detection** strategy. Valid values are “lines”, “lines\_strict” and “text”.

              Default is **“lines”** which uses all vector graphics on the page to detect grid lines.

              Strategy **“lines\_strict”** ignores borderless rectangle vector graphics. Sometimes single text pieces have background colors which may lead to false columns or lines. This strategy ignores them and can thus increase detection precision.

              If **“text”** is specified, text positions are used to generate “virtual” column and / or row boundaries. Use `min_words_*` to request the number of words for considering their coordinates.

              Use parameters `vertical_strategy` and `horizontal_strategy` **instead** for a more fine-grained treatment of the dimensions.
            - **horizontal\_lines** (*sequence**[**floats**]*) – y-coordinates of rows. If provided, there will be no attempt to identify additional table rows. This influences table detection.
            - **vertical\_lines** (*sequence**[**floats**]*) – x-coordinates of columns. If provided, there will be no attempt to identify additional table columns. This influences table detection.
            - **min\_words\_vertical** (*int*) – relevant for vertical strategy option “text”: at least this many words must coincide to establish a **virtual column** boundary.
            - **min\_words\_horizontal** (*int*) – relevant for horizontal strategy option “text”: at least this many words must coincide to establish a **virtual row** boundary.
            - **snap\_tolerance** (*float*) – Any two horizontal lines whose y-values differ by no more than this value will be **snapped** into one. Accordingly for vertical lines. Default is 3. Separate values can be specified instead for the dimensions, using `snap_x_tolerance` and `snap_y_tolerance`.
            - **join\_tolerance** (*float*) – Any two lines will be **joined** to one if the end and the start points differ by no more than this value (in points). Default is 3. Instead of this value, separate values can be specified for the dimensions using `join_x_tolerance` and `join_y_tolerance`.
            - **edge\_min\_length** (*float*) – Ignore a line if its length does not exceed this value (points). Default is 3.
            - **intersection\_tolerance** (*float*) – When combining lines into cell borders, orthogonal lines must be within this value (points) to be considered intersecting. Default is 3. Instead of this value, separate values can be specified for the dimensions using `intersection_x_tolerance` and `intersection_y_tolerance`.
            - **text\_tolerance** (*float*) – Characters will be combined into words only if their distance is no larger than this value (points). Default is 3. Instead of this value, separate values can be specified for the dimensions using `text_x_tolerance` and `text_y_tolerance`.
            - **add\_lines** (*tuple**,**list*) – Specify a list of “lines” (i.e. pairs of [`point_like`](glossary.html#point_like "point_like") objects) as **additional**, “virtual” vector graphics. These lines may help with table and / or cell detection and will not otherwise influence the detection strategy. Especially, in contrast to parameters `horizontal_lines` and `vertical_lines`, they will not prevent detecting rows or columns in other ways. These lines will be treated exactly like “real” vector graphics in terms of joining, snapping, intersecting, minimum length and containment in the `clip` rectangle. Similarly, lines not parallel to any of the coordinate axes will be ignored.
            - **add\_boxes** (*tuple**,**list*) – Specify a list of rectangles ([`rect_like`](glossary.html#rect_like "rect_like") objects) as **additional**, “virtual” vector graphics. These rectangles may help with table and / or cell detection and will not otherwise influence the detection strategy. Especially, in contrast to parameters `horizontal_lines` and `vertical_lines`, they will not prevent detecting rows or columns in other ways. These rectangles will be treated exactly like “real” vector graphics in terms of joining, snapping, intersecting, minimum length and containment in the `clip` rectangle.
            - **paths** (*list*) – list of vector graphics in the format as returned be [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings"). Using this parameter will prevent the method to extract vector graphics itself. This is useful if the vector graphics are already available. This can save execution time significantly.

        Returns:
        :   a [`TableFinder`](#TableFinder "TableFinder") object that has the following significant attributes:

            - [`cells`](#Table.cells "Table.cells"): a list of **all bboxes** on the page, that have been identified as table cells (across all tables). Each cell is a [`rect_like`](glossary.html#rect_like "rect_like") tuple `(x0, y0, x1, y1)` of coordinates or `None`.
            - [`tables`](#TableFinder.tables "TableFinder.tables"): a list of [`Table`](#Table "Table") objects. This is `[]` if the page has no tables. Single tables can be found as items of this list. But the [`TableFinder`](#TableFinder "TableFinder") object itself is also a sequence of its tables. This means that if `tabs` is a [`TableFinder`](#TableFinder "TableFinder") object, then table “n” is delivered by `tabs.tables[n]` as well as by the shorter `tabs[n]`.
            - The [`Table`](#Table "Table") object has the following attributes:

              - `bbox`: the bounding box of the table as a tuple `(x0, y0, x1, y1)`.
              - `cells`: bounding boxes of the table’s cells (list of tuples). A cell may also be `None`.
              - `extract()`: this method returns the text content of each table cell as a list of list of strings.
              - `to_markdown()`: this method returns the table as a **string in markdown format** (compatible to Github). Markdown viewers can render the string as a table. This output is optimized for **small token** sizes, which is especially beneficial for LLM/RAG feeds. Pandas DataFrames (see method [`to_pandas()`](#Table.to_pandas "Table.to_pandas") below) offer an equivalent markdown table output which however is better readable for the human eye. Any line breaks (`\n`) in cells are replaced by HTML line breaks tags `<br>`.
              - [`to_pandas()`](#Table.to_pandas "Table.to_pandas"): this method returns the table as a [pandas](https://pypi.org/project/pandas/) [DataFrame](https://pandas.pydata.org/docs/reference/frame.html). DataFrames are very versatile objects allowing a plethora of table manipulation methods and outputs to almost 20 well-known formats, among them Excel files, CSV, JSON, markdown-formatted tables and more. `DataFrame.to_markdown()` generates a Github-compatible markdown format optimized for human readability. This method however requires the package [tabulate](https://pypi.org/project/tabulate/) to be installed in addition to pandas itself.
              - `header`: a [`TableHeader`](#TableHeader "TableHeader") object containing header information of the table.
              - `col_count`: an integer containing the number of table columns.
              - `row_count`: an integer containing the number of table rows.
              - `rows`: a list of [`TableRow`](#TableRow "TableRow") objects containing two attributes, `bbox` is the boundary box of the row, and [`cells`](#Table.cells "Table.cells") is a list of table cells contained in this row.
            - The [`TableHeader`](#TableHeader "TableHeader") object has the following attributes:

              - `bbox`: the bounding box of the header.
              - [`cells`](#Table.cells "Table.cells"): a list of bounding boxes containing the name of the respective column.
              - [`names`](#TableHeader.names "TableHeader.names"): a list of strings containing the text of each of the cell bboxes. They represent the column names – which are used when exporting the table to pandas DataFrames, markdown, etc.
              - [`external`](#TableHeader.external "TableHeader.external"): a bool indicating whether the header bbox is outside the table body (`True`) or not. Table headers are never identified by the [`TableFinder`](#TableFinder "TableFinder") logic. Therefore, if [`external`](#TableHeader.external "TableHeader.external") is true, then the header cells are not part of any cell identified by [`TableFinder`](#TableFinder "TableFinder"). If `external == False`, then the first table row is the header.

            Please have a look at these [Jupyter notebooks](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/table-analysis), which cover standard situations like multiple tables on one page or joining table fragments across multiple pages.

            Caution

            The lifetime of the [`TableFinder`](#TableFinder "TableFinder") object, as well as that of all its tables **equals the lifetime of the page**. If the page object is deleted or reassigned, all tables are no longer valid.

            The only way to keep table content beyond the page’s availability is to **extract it** via methods [`Table.to_markdown()`](#Table.to_markdown "Table.to_markdown"), [`Table.to_pandas()`](#Table.to_pandas "Table.to_pandas") or a copy of [`Table.extract()`](#Table.extract "Table.extract") (e.g. `Table.extract()[:]`).

            Note

            Once a table has been extracted to a **Pandas DataFrame** with [`to_pandas()`](#Table.to_pandas "Table.to_pandas") it is easy to convert to other file types with the **Pandas API**:

            - table to Markdown, use [to\_markdown](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html#pandas.DataFrame.to_markdown)
            - table to JSON, use: [to\_json](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html)
            - table to Excel, use: [to\_excel](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html)
            - table to CSV, use: [to\_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)
            - table to HTML, use: [to\_html](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html)
            - table to SQL, use: [to\_sql](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html)

        Show/hide history

        - New in version 1.23.0
        - Changed in version 1.23.19: new argument `add_lines`.

        Important

        There is also the [pdf2docx extract tables method](https://pdf2docx.readthedocs.io/en/latest/quickstart.table.html) which is capable of table extraction if you prefer.

    add\_stamp\_annot(*rect*, *stamp=0*)
    :   PDF only: Add a “rubber stamp” annotation to e.g. indicate the document’s intended use (“DRAFT”, “CONFIDENTIAL”, etc.). The parameter may be either an integer to select text from a predefined array of standard texts or an image.

        Parameters:
        :   - **rect** (*rect\_like*) – rectangle where to place the annotation.
            - **stamp** (*multiple*) –

              The following options are available:

              - The id number (int) of the stamp text. For available stamps see [Stamp Annotation Icons](vars.html#stampicons).
              - A string specifying an image file path.
              - A `bytes`, `bytearray` or `io.BytesIO` object for an image in memory.
              - A [Pixmap](pixmap.html#pixmap).

        1. **Text-based stamps**

           - [`Annot.rect`](annot.html#Annot.rect "Annot.rect") is automatically calculated as the largest rectangle with an aspect ratio of `width:height = 3.8` that fits in the provided `rect`. Its position is vertically and horizontally centered.
           - The font chosen is “Times Bold” and the text will be upper case.
           - The appearance can be modified using [`Annot.set_opacity()`](annot.html#Annot.set_opacity "Annot.set_opacity") and by setting the “stroke” color. By PDF specification, stamp annotations have no “fill” color.
        2. **Image-based stamps**

           - The image is scaled to fit into the rectangle [Rect](rect.html) such that the image’s center and the center of [Rect](rect.html) coincide. The aspect ratio of the image is preserved, so the image may not fill the entire rectangle. However, at least one of the given rectangle’s width or height are fully covered.
           - The annotation can be modified via [`Annot.set_opacity()`](annot.html#Annot.set_opacity "Annot.set_opacity"). This method therefore is a way to display images transparently even if no alpha channel is present.
           - Setting colors has no effect on image stamps.
           - Rotating image-based stamps **is not supported**. Setting the rotation may lead to unexpected results.

    add\_widget(*widget*)
    :   PDF only: Add a PDF Form field (“widget”) to a page. This also **turns the PDF into a Form PDF**. Because of the large amount of different options available for widgets, we have developed a new class [Widget](widget.html#widget), which contains the possible PDF field attributes. It must be used for both, form field creation and updates.

        Parameters:
        :   **widget** ([Widget](widget.html#widget)) – a [Widget](widget.html#widget) object which must have been created upfront.

        Returns:
        :   a widget annotation.

    delete\_annot(*annot*)
    :   - The removal will now include any bound ‘Popup’ or response annotations and related objects (changed in v1.16.6).

        PDF only: Delete annotation from the page and return the next one.

        Parameters:
        :   **annot** ([Annot](annot.html#annot)) – the annotation to be deleted.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the annotation following the deleted one. Please remember that physical removal requires saving to a new file with garbage > 0.

    delete\_widget(*widget*)
    :   PDF only: Delete field from the page and return the next one.

        Parameters:
        :   **widget** ([Widget](widget.html#widget)) – the widget to be deleted.

        Return type:
        :   [Widget](widget.html#widget)

        Returns:
        :   the widget following the deleted one. Please remember that physical removal requires saving to a new file with garbage > 0.

        Show/hide history

        (New in v1.18.4)

    delete\_link(*linkdict*)
    :   PDF only: Delete the specified link from the page. The parameter must be an **original item** of [`get_links()`](#Page.get_links "Page.get_links"), see [Description of get\_links() Entries](#link-dict-description). The reason for this is the dictionary’s *“xref”* key, which identifies the PDF object to be deleted.

        Parameters:
        :   **linkdict** (*dict*) – the link to be deleted.

    insert\_link(*linkdict*)
    :   PDF only: Insert a new link on this page. The parameter must be a dictionary of format as provided by [`get_links()`](#Page.get_links "Page.get_links"), see [Description of get\_links() Entries](#link-dict-description).

        Parameters:
        :   **linkdict** (*dict*) – the link to be inserted.

    update\_link(*linkdict*)
    :   PDF only: Modify the specified link. The parameter must be a (modified) **original item** of [`get_links()`](#Page.get_links "Page.get_links"), see [Description of get\_links() Entries](#link-dict-description). The reason for this is the dictionary’s *“xref”* key, which identifies the PDF object to be changed.

        Parameters:
        :   **linkdict** (*dict*) – the link to be modified.

        Warning

        If updating / inserting a URI link (`"kind": LINK_URI`), please make sure to start the value for the `"uri"` key with a disambiguating string like `"http://"`, `"https://"`, `"file://"`, `"ftp://"`, `"mailto:"`, etc. Otherwise – depending on your browser or other “consumer” software – unexpected default assumptions may lead to unwanted behaviours.

    get\_label()
    :   PDF only: Return the label for the page.

        Return type:
        :   str

        Returns:
        :   the label string like “vii” for Roman numbering or “” if not defined.

        Show/hide history

        - New in v1.18.6

    get\_links()
    :   Retrieves **all** links of a page.

        Return type:
        :   list

        Returns:
        :   A list of dictionaries. For a description of the dictionary entries, see [Description of get\_links() Entries](#link-dict-description). Always use this or the [`Page.links()`](#Page.links "Page.links") method if you intend to make changes to the links of a page.

    links(*kinds=None*)
    :   Return a generator over the page’s links. The results equal the entries of [`Page.get_links()`](#Page.get_links "Page.get_links").

        Parameters:
        :   **kinds** (*sequence*) – a sequence of integers to down-select to one or more link kinds. Default is all links. Example: *kinds=(pymupdf.LINK\_GOTO,)* will only return internal links.

        Return type:
        :   generator

        Returns:
        :   an entry of [`Page.get_links()`](#Page.get_links "Page.get_links") for each iteration.

        Show/hide history

        - New in v1.16.4

    annots(*types=None*)
    :   Return a generator over the page’s annotations.

        Parameters:
        :   **types** (*sequence*) – a sequence of integers to down-select to one or more annotation types. Default is all annotations. Example: `types=(pymupdf.PDF_ANNOT_FREETEXT, pymupdf.PDF_ANNOT_TEXT)` will only return ‘FreeText’ and ‘Text’ annotations.

        Return type:
        :   generator

        Returns:
        :   an [Annot](annot.html#annot) for each iteration.

            Caution

            You **cannot safely update annotations** from within this generator. This is because most annotation updates require reloading the page via `page = doc.reload_page(page)`. To circumvent this restriction, make a list of annotations xref numbers first and then iterate over these numbers:

            ```
            In [4]: xrefs = [annot.xref for annot in page.annots(types=[...])]
            In [5]: for xref in xrefs:
               ...:     annot = page.load_annot(xref)
               ...:     annot.update()
               ...:     page = doc.reload_page(page)
            In [6]:
            ```

        Show/hide history

        - New in v1.16.4

    widgets(*types=None*)
    :   Return a generator over the page’s form fields.

        Parameters:
        :   **types** (*sequence*) – a sequence of integers to down-select to one or more widget types. Default is all form fields. Example: `types=(pymupdf.PDF_WIDGET_TYPE_TEXT,)` will only return ‘Text’ fields.

        Return type:
        :   generator

        Returns:
        :   a [Widget](widget.html#widget) for each iteration.

        Show/hide history

        - New in v1.16.4

    write\_text(*rect=None*, *writers=None*, *overlay=True*, *color=None*, *opacity=None*, *keep\_proportion=True*, *rotate=0*, *oc=0*)
    :   PDF only: Write the text of one or more [TextWriter](textwriter.html#textwriter) objects to the page.

        Parameters:
        :   - **rect** (*rect\_like*) – where to place the text. If omitted, the rectangle union of the text writers is used.
            - **writers** (*sequence*) – a non-empty tuple / list of [TextWriter](textwriter.html#textwriter) objects or a single [TextWriter](textwriter.html#textwriter).
            - **opacity** (*float*) – set transparency, overwrites resp. value in the text writers.
            - **color** (*sequ*) – set the text color, overwrites resp. value in the text writers.
            - **overlay** (*bool*) – put the text in foreground or background.
            - **keep\_proportion** (*bool*) – maintain the aspect ratio.
            - **rotate** (*float*) – rotate the text by an arbitrary angle.
            - **oc** (*int*) – the [`xref`](glossary.html#xref "xref") of an [`OCG`](glossary.html#OCG "OCG") or [`OCMD`](glossary.html#OCMD "OCMD"). (New in v1.18.4)

        Note

        Parameters *overlay, keep\_proportion, rotate* and *oc* have the same meaning as in [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page").

        Show/hide history

        - New in v1.16.18

    insert\_text(*point*, *text*, *\**, *fontsize=11*, *fontname='helv'*, *fontfile=None*, *idx=0*, *color=None*, *fill=None*, *render\_mode=0*, *miter\_limit=1*, *border\_width=0.05*, *encoding=TEXT\_ENCODING\_LATIN*, *rotate=0*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *overlay=True*, *oc=0*)
    :   PDF only: Insert text lines starting at [`point_like`](glossary.html#point_like "point_like") `point`. See [`Shape.insert_text()`](shape.html#Shape.insert_text "Shape.insert_text").

        Show/hide history

        - Changed in v1.18.4

    insert\_textbox(*rect*, *buffer*, *\**, *align=TEXT\_ALIGN\_LEFT*, *border\_width=1*, *color=None*, *encoding=TEXT\_ENCODING\_LATIN*, *expandtabs=8*, *fill=None*, *fill\_opacity=1*, *fontfile=None*, *fontname='helv'*, *fontsize=11*, *lineheight=None*, *miter\_limit=1*, *morph=None*, *oc=0*, *overlay=True*, *render\_mode=0*, *rotate=0*, *set\_simple=False*, *stroke\_opacity=1*)
    :   PDF only: Insert text into the specified [`rect_like`](glossary.html#rect_like "rect_like") *rect*.

        Parameters:
        :   **overlay** – see [`Shape.commit()`](shape.html#Shape.commit "Shape.commit").

        For other args, see [`Shape.insert_textbox`](shape.html#Shape.insert_textbox "Shape.insert_textbox").

        Show/hide history

        - Changed in v1.18.4

    insert\_htmlbox(*rect*, *text*, *\**, *css=None*, *scale\_low=0*, *archive=None*, *rotate=0*, *oc=0*, *opacity=1*, *overlay=True*)
    :   **PDF only:** Insert text into the specified rectangle. The method has similarities with methods [`Page.insert_textbox()`](#Page.insert_textbox "Page.insert_textbox") and [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox"), but is **much more powerful**. This is achieved by letting a [Story](story-class.html#story) object do all the required processing.

        - Parameter `text` may be a string as in the other methods. But it will be **interpreted as HTML source** and may therefore also contain HTML language elements – including styling. The `css` parameter may be used to pass in additional styling instructions.
        - Automatic line breaks are generated at word boundaries. The “soft hyphen” character `"&#173;"` (or `&shy;`) can be used to cause hyphenation and thus may also cause line breaks. **Forced** line breaks however are only achievable via the HTML tag `<br>` - `\n` is ignored and will be treated like a space.
        - With this method the following can be achieved:

          - Styling effects like bold, italic, text color, text alignment, font size or font switching.
          - The text may include arbitrary languages – **including right-to-left** languages.
          - Scripts like [Devanagari](https://en.wikipedia.org/wiki/Devanagari) and several others in Asia have a highly complex system of ligatures, where two or more unicodes together yield one glyph. The Story uses the software package [HarfBuzz](https://harfbuzz.github.io/) , to deal with these things and produce correct output.
          - One can also **include images** via HTML tag `<img>` – the Story will take care of the appropriate layout. This is an alternative option to insert images, compared to [`Page.insert_image()`](#Page.insert_image "Page.insert_image").
          - HTML tables (tag `<table>`) may be included in the text and will be handled appropriately.
          - Links are automatically generated when present.
        - If content does not fit in the rectangle, the developer has two choices:

          - **either** only be informed about this (and accept a no-op, just like with the other textbox insertion methods),
          - **or** (`scale_low=0` - the default) scale down the content until it fits.

        Parameters:
        :   - **rect** (*rect\_like*) – rectangle on page to receive the text.
            - **text** (*str**,*[*Story*](story-class.html#Story "Story")) – the text to be written. Can contain a mixture of plain text and HTML tags with styling instructions. Alternatively, a [Story](story-class.html#story) object may be specified (in which case the internal Story generation step will be omitted). A Story must have been generated with all required styling and Archive information.
            - **css** (*str*) – optional string containing additional CSS instructions. This parameter is ignored if `text` is a Story.
            - **scale\_low** (*float*) – if necessary, scale down the content until it fits in the target rectangle. This sets the down scaling limit. Default is 0, no limit. A value of 1 means no down-scaling permitted. A value of e.g. 0.2 means maximum down-scaling by 80%.
            - **archive** ([*Archive*](archive-class.html#Archive "Archive")) – an Archive object that points to locations where to find images or non-standard fonts. If `text` refers to images or non-standard fonts, this parameter is required. This parameter is ignored if `text` is a Story.
            - **rotate** (*int*) –

              one of the values 0, 90, 180, 270. Depending on this, text will be filled:

              - 0: top-left to bottom-right.
              - 90: bottom-left to top-right.
              - 180: bottom-right to top-left.
              - 270: top-right to bottom-left.
            - **oc** (*int*) – the xref of an [`OCG`](glossary.html#OCG "OCG") / [`OCMD`](glossary.html#OCMD "OCMD") or 0. Please refer to [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page") for details.
            - **opacity** (*float*) – set the fill and stroke opacity of the content. Only values `0 <= opacity < 1` are considered.
            - **overlay** (*bool*) – put the text in front of other content. Please refer to [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page") for details.

        Returns:
        :   A tuple of floats `(spare_height, scale)`.

            - spare\_height: The (positive) height of the remaining space in [Rect](rect.html) below the
              text, or -1 if we failed to fit.
            - scale: The scaling required; `0 < scale <= 1`. Will be `scale_low`
              if we failed to fit.

        Please refer to examples in this section of the recipes: [How to Fill a Box with HTML Text](recipes-text.html#recipestext-i-c).

        Show/hide history

        - New in v1.26.5:

          - do additional scaling to fit long words.
          - If we succeeded and scaled down, the returned `spare_height` is now
            generally positive instead of being fixed to zero, because the final
            rect’s height is usually not an exact multiple of the font line
            height.
        - New in v1.23.8: rebased-only.
        - New in v1.23.9: [`opacity`](annot.html#Annot.opacity "Annot.opacity") parameter.

    **Drawing Methods**

    draw\_line(*p1*, *p2*, *color=(0,)*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a line from *p1* to *p2* ([`point_like`](glossary.html#point_like "point_like") s). See [`Shape.draw_line()`](shape.html#Shape.draw_line "Shape.draw_line").

        Show/hide history

        - Changed in v1.18.4

    draw\_zigzag(*p1*, *p2*, *breadth=2*, *color=(0,)*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a zigzag line from *p1* to *p2* ([`point_like`](glossary.html#point_like "point_like") s). See [`Shape.draw_zigzag()`](shape.html#Shape.draw_zigzag "Shape.draw_zigzag").

        Show/hide history

        - Changed in v1.18.4

    draw\_squiggle(*p1*, *p2*, *breadth=2*, *color=(0,)*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a squiggly (wavy, undulated) line from *p1* to *p2* ([`point_like`](glossary.html#point_like "point_like") s). See [`Shape.draw_squiggle()`](shape.html#Shape.draw_squiggle "Shape.draw_squiggle").

        Show/hide history

        - Changed in v1.18.4

    draw\_circle(*center*, *radius*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a circle around *center* ([`point_like`](glossary.html#point_like "point_like")) with a radius of *radius*. See [`Shape.draw_circle()`](shape.html#Shape.draw_circle "Shape.draw_circle").

        Show/hide history

        - Changed in v1.18.4

    draw\_oval(*quad*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw an oval (ellipse) within the given [`rect_like`](glossary.html#rect_like "rect_like") or [`quad_like`](glossary.html#quad_like "quad_like"). See [`Shape.draw_oval()`](shape.html#Shape.draw_oval "Shape.draw_oval").

        Show/hide history

        - Changed in v1.18.4

    draw\_sector(*center*, *point*, *angle*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *fullSector=True*, *overlay=True*, *closePath=False*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a circular sector, optionally connecting the arc to the circle’s center (like a piece of pie). See [`Shape.draw_sector()`](shape.html#Shape.draw_sector "Shape.draw_sector").

        Show/hide history

        - Changed in v1.18.4

    draw\_polyline(*points*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *closePath=False*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw several connected lines defined by a sequence of [`point_like`](glossary.html#point_like "point_like") s. See [`Shape.draw_polyline()`](shape.html#Shape.draw_polyline "Shape.draw_polyline").

        Show/hide history

        - Changed in v1.18.4

    draw\_bezier(*p1*, *p2*, *p3*, *p4*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *closePath=False*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a cubic Bézier curve from *p1* to *p4* with the control points *p2* and *p3* (all are [`point_like`](glossary.html#point_like "point_like") s). See [`Shape.draw_bezier()`](shape.html#Shape.draw_bezier "Shape.draw_bezier").

        Show/hide history

        - Changed in v1.18.4

    draw\_curve(*p1*, *p2*, *p3*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *closePath=False*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: This is a special case of *draw\_bezier()*. See [`Shape.draw_curve()`](shape.html#Shape.draw_curve "Shape.draw_curve").

        Show/hide history

        - Changed in v1.18.4

    draw\_rect(*rect*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *radius=None*, *oc=0*)
    :   PDF only: Draw a rectangle. See [`Shape.draw_rect()`](shape.html#Shape.draw_rect "Shape.draw_rect").

        Show/hide history

        - Changed in v1.18.4
        - Changed in v1.22.0: Added parameter *radius*.

    draw\_quad(*quad*, *color=(0,)*, *fill=None*, *width=1*, *dashes=None*, *lineCap=0*, *lineJoin=0*, *overlay=True*, *morph=None*, *stroke\_opacity=1*, *fill\_opacity=1*, *oc=0*)
    :   PDF only: Draw a quadrilateral. See [`Shape.draw_quad()`](shape.html#Shape.draw_quad "Shape.draw_quad").

        Show/hide history

        - Changed in v1.18.4

    insert\_font(*fontname='helv'*, *fontfile=None*, *fontbuffer=None*, *set\_simple=False*, *encoding=TEXT\_ENCODING\_LATIN*)
    :   PDF only: Add a new font to be used by text output methods and return its [`xref`](glossary.html#xref "xref"). If not already present in the file, the font definition will be added. Supported are the built-in [`Base14_Fonts`](vars.html#Base14_Fonts "Base14_Fonts") and the CJK fonts via **“reserved”** fontnames. Fonts can also be provided as a file path or a memory area containing the image of a font file.

        Parameters:
        :   - **fontname** (*str*) –

              The name by which this font shall be referenced when outputting text on this page. In general, you have a “free” choice here (but consult the [Adobe PDF References](app3.html#adobemanual), page 16, section 7.3.5 for a formal description of building legal PDF names). However, if it matches one of the [`Base14_Fonts`](vars.html#Base14_Fonts "Base14_Fonts") or one of the CJK fonts, *fontfile* and *fontbuffer* **are ignored**.

              In other words, you cannot insert a font via *fontfile* / *fontbuffer* and also give it a reserved *fontname*.

              Note

              A reserved fontname can be specified in any mixture of upper or lower case and still match the right built-in font definition: fontnames “helv”, “Helv”, “HELV”, “Helvetica”, etc. all lead to the same font definition “Helvetica”. But from a [Page](#page) perspective, these are **different references**. You can exploit this fact when using different *encoding* variants (Latin, Greek, Cyrillic) of the same font on a page.
            - **fontfile** (*str*) – a path to a font file. If used, *fontname* must be **different from all reserved names**.
            - **fontbuffer** (*bytes/bytearray*) – the memory image of a font file. If used, *fontname* must be **different from all reserved names**. This parameter would typically be used with [`Font.buffer`](font.html#Font.buffer "Font.buffer") for fonts supported / available via [Font](font.html#font).
            - **set\_simple** (*int*) – applicable for *fontfile* / *fontbuffer* cases only: enforce treatment as a “simple” font, i.e. one that only uses character codes up to 255.
            - **encoding** (*int*) – applicable for the “Helvetica”, “Courier” and “Times” sets of [`Base14_Fonts`](vars.html#Base14_Fonts "Base14_Fonts") only. Select one of the available encodings Latin (0), Cyrillic (2) or Greek (1). Only use the default (0 = Latin) for “Symbol” and “ZapfDingBats”.

        Rytpe:
        :   int

        Returns:
        :   the [`xref`](glossary.html#xref "xref") of the installed font.

        Note

        Built-in fonts will not lead to the inclusion of a font file. So the resulting PDF file will remain small. However, your PDF viewer software is responsible for generating an appropriate appearance – and there **exist** differences on whether or how each one of them does this. This is especially true for the CJK fonts. But also Symbol and ZapfDingbats are incorrectly handled in some cases. Following are the **Font Names** and their correspondingly installed **Base Font** names:

        **Base-14 Fonts** [[1]](#f1)

        | **Font Name** | **Installed Base Font** | **Comments** |
        | --- | --- | --- |
        | helv | Helvetica | normal |
        | heit | Helvetica-Oblique | italic |
        | hebo | Helvetica-Bold | bold |
        | hebi | Helvetica-BoldOblique | bold-italic |
        | cour | Courier | normal |
        | coit | Courier-Oblique | italic |
        | cobo | Courier-Bold | bold |
        | cobi | Courier-BoldOblique | bold-italic |
        | tiro | Times-Roman | normal |
        | tiit | Times-Italic | italic |
        | tibo | Times-Bold | bold |
        | tibi | Times-BoldItalic | bold-italic |
        | symb | Symbol | [[3]](#f3) |
        | zadb | ZapfDingbats | [[3]](#f3) |

        **CJK Fonts** [[2]](#f2) (China, Japan, Korea)

        | **Font Name** | **Installed Base Font** | **Comments** |
        | --- | --- | --- |
        | china-s | Heiti | simplified Chinese |
        | china-ss | Song | simplified Chinese (serif) |
        | china-t | Fangti | traditional Chinese |
        | china-ts | Ming | traditional Chinese (serif) |
        | japan | Gothic | Japanese |
        | japan-s | Mincho | Japanese (serif) |
        | korea | Dotum | Korean |
        | korea-s | Batang | Korean (serif) |

    insert\_image(*rect*, *\**, *alpha=-1*, *filename=None*, *height=0*, *keep\_proportion=True*, *mask=None*, *oc=0*, *overlay=True*, *pixmap=None*, *rotate=0*, *stream=None*, *width=0*, *xref=0*)
    :   PDF only: Put an image inside the given rectangle. The image may already
        exist in the PDF or be taken from a pixmap, a file, or a memory area.

        Parameters:
        :   - **rect** (*rect\_like*) – where to put the image. Must be finite and not empty.
            - **alpha** (*int*) – deprecated and ignored.
            - **filename** (*str*) – name of an image file (all formats supported by MuPDF – see
              [Supported Input Image Formats](pixmap.html#imagefiles)).
            - **height** (*int*)
            - **keep\_proportion** (*bool*) – maintain the aspect ratio of the image.
            - **mask** (*bytes**,**bytearray**,**io.BytesIO*) – image in memory – to be used as image mask (alpha values) for the base
              image. When specified, the base image must be provided as a filename or
              a stream – and must not be an image that already has a mask.
            - **oc** (*int*) – ([`xref`](glossary.html#xref "xref")) make image visibility dependent on this [`OCG`](glossary.html#OCG "OCG")
              or [`OCMD`](glossary.html#OCMD "OCMD"). Ignored after the first of multiple insertions. The
              property is stored with the generated PDF image object and therefore
              controls the image’s visibility throughout the PDF.
            - **overlay** – see [Common Parameters](shape.html#commonparms).
            - **pixmap** ([Pixmap](pixmap.html#pixmap)) – a pixmap containing the image.
            - **rotate** (*int*) – rotate the image.
              Must be an integer multiple of 90 degrees.
              Positive values rotate anti-clockwise.
              If you need a rotation by an arbitrary angle,
              consider converting the image to a PDF
              ([`Document.convert_to_pdf()`](document.html#Document.convert_to_pdf "Document.convert_to_pdf"))
              first and then use [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page") instead.
            - **stream** (*bytes**,**bytearray**,**io.BytesIO*) – image in memory (all formats supported by MuPDF – see [Supported Input Image Formats](pixmap.html#imagefiles)).
            - **width** (*int*)
            - **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of an image already present in the PDF. If given,
              parameters `filename`, [Pixmap](pixmap.html), [`stream`](glossary.html#stream "stream"), [`alpha`](pixmap.html#Pixmap.alpha "Pixmap.alpha") and `mask` are
              ignored. The page will simply receive a reference to the existing
              image.

        Returns:
        :   The [`xref`](glossary.html#xref "xref") of the embedded image. This can be used as the [`xref`](glossary.html#xref "xref")
            argument for very significant performance boosts, if the image is
            inserted again.

        This example puts the same image on every page of a document:

        ```
        >>> doc = pymupdf.open(...)
        >>> rect = pymupdf.Rect(0, 0, 50, 50)       # put thumbnail in upper left corner
        >>> img = open("some.jpg", "rb").read()  # an image file
        >>> img_xref = 0                         # first execution embeds the image
        >>> for page in doc:
              img_xref = page.insert_image(rect, stream=img,
                         xref=img_xref,  2nd time reuses existing image
                  )
        >>> doc.save(...)
        ```

        Note

        1. The method detects multiple insertions of the same image (like
           in the above example) and will store its data only on the first
           execution. This is even true (although less performant), if using
           the default `xref=0`.
        2. The method cannot detect if the same image had already been part of
           the file before opening it.
        3. You can use this method to provide a background or foreground image
           for the page, like a copyright or a watermark. Please remember, that
           watermarks require a transparent image if put in foreground …
        4. The image may be inserted uncompressed, e.g. if a [Pixmap](pixmap.html#pixmap) is used
           or if the image has an alpha channel. Therefore, consider using
           `deflate=True` when saving the file. In addition, there are ways to
           control the image size – even if transparency comes into play. Have
           a look at [How to Add Images to a PDF Page](recipes-images.html#recipesimages-o).
        5. The image is stored in the PDF at its original quality level. This
           may be much better than what you need for your display. Consider
           **decreasing the image size** before insertion – e.g. by using
           the pixmap option and then shrinking it or scaling it down (see
           [Pixmap](pixmap.html#pixmap) chapter). The PIL method `Image.thumbnail()` can
           also be used for that purpose. The file size savings can be very
           significant.
        6. Another efficient way to display the same image on multiple
           pages is another method: [`show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page"). Consult
           [`Document.convert_to_pdf()`](document.html#Document.convert_to_pdf "Document.convert_to_pdf") for how to obtain intermediary PDFs
           usable for that method.

        Show/hide history

        - Changed in v1.14.1: By default, the image keeps its aspect ratio.
        - Changed in v1.14.11: Added args `keep_proportion`, `rotate`.
        - Changed in v1.14.13:

          - The image is now always placed **centered** in the rectangle, i.e.
            the centers of image and rectangle are equal.
          - Added support for [`stream`](glossary.html#stream "stream") as `io.BytesIO`.
        - Changed in v1.17.6:
          Insertion rectangle no longer needs to have a non-empty intersection
          with the page’s [`Page.cropbox`](#Page.cropbox "Page.cropbox") [[5]](#f5).
        - Changed in v1.18.1: Added `mask` arg.
        - Changed in v1.18.3: Added `oc` arg.
        - Changed in v1.18.13:

          - Allow providing the image as the xref of an existing one.
          - Added [`xref`](glossary.html#xref "xref") arg.
          - Return [`xref`](glossary.html#xref "xref") of stored image.
        - Changed in v1.19.3: deprecate and ignore [`alpha`](pixmap.html#Pixmap.alpha "Pixmap.alpha") arg.

    replace\_image(*xref*, *filename=None*, *pixmap=None*, *stream=None*)
    :   Replace the image at xref with another one.

        Parameters:
        :   - **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of the image.
            - **filename** – the filename of the new image.
            - **pixmap** – the [Pixmap](pixmap.html#pixmap) of the new image.
            - **stream** – the memory area containing the new image.

        Arguments `filename`, [Pixmap](pixmap.html), [`stream`](glossary.html#stream "stream") have the same meaning as in [`Page.insert_image()`](#Page.insert_image "Page.insert_image"), especially exactly one of these must be provided.

        This is a **global replacement:** the new image will also be shown wherever the old one has been displayed throughout the file.

        This method mainly exists for technical purposes. Typical uses include replacing large images by smaller versions, like a lower resolution, graylevel instead of colored, etc., or changing transparency.

        Show/hide history

        - New in v1.21.0

    delete\_image(*xref*)
    :   Delete the image at xref. This is slightly misleading: actually the image is being replaced with a small transparent [Pixmap](pixmap.html#pixmap) using above [`Page.replace_image()`](#Page.replace_image "Page.replace_image"). The visible effect however is equivalent.

        Parameters:
        :   **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of the image.

        This is a **global replacement:** the image will disappear wherever the old one has been displayed throughout the file.

        If you inspect / extract a page’s images by methods like [`Page.get_images()`](#Page.get_images "Page.get_images"),
        [`Page.get_image_info()`](#Page.get_image_info "Page.get_image_info") or [`Page.get_text()`](#Page.get_text "Page.get_text"),
        the replacing “dummy” image will be detected like so
        `(45, 47, 1, 1, 8, 'DeviceGray', '', 'Im1', 'FlateDecode')`
        and also seem to “cover” the same boundary box on the page.

        Show/hide history

        - New in v1.21.0

    get\_text(*option*, *\**, *clip=None*, *flags=None*, *textpage=None*, *sort=False*, *delimiters=None*)
    :   Retrieves the content of a page in a variety of formats. Depending on the `flags` value, this may include text, images and several other object types. The method is a wrapper for multiple [TextPage](textpage.html#textpage) methods by choosing the output option `opt` as follows:

        - “text” – [`TextPage.extractTEXT()`](textpage.html#TextPage.extractTEXT "TextPage.extractTEXT"), default. Always includes **text only.**
        - “blocks” – [`TextPage.extractBLOCKS()`](textpage.html#TextPage.extractBLOCKS "TextPage.extractBLOCKS"). Includes text and **may** include image meta information.
        - “words” – [`TextPage.extractWORDS()`](textpage.html#TextPage.extractWORDS "TextPage.extractWORDS"). Always includes **text only.**
        - “html” – [`TextPage.extractHTML()`](textpage.html#TextPage.extractHTML "TextPage.extractHTML"). May include text and images.
        - “xhtml” – [`TextPage.extractXHTML()`](textpage.html#TextPage.extractXHTML "TextPage.extractXHTML"). May include text and images.
        - “xml” – [`TextPage.extractXML()`](textpage.html#TextPage.extractXML "TextPage.extractXML"). Always includes **text only.**
        - “dict” – [`TextPage.extractDICT()`](textpage.html#TextPage.extractDICT "TextPage.extractDICT"). May include text and images.
        - “json” – [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON "TextPage.extractJSON"). May include text and images.
        - “rawdict” – [`TextPage.extractRAWDICT()`](textpage.html#TextPage.extractRAWDICT "TextPage.extractRAWDICT"). May include text and images.
        - “rawjson” – [`TextPage.extractRAWJSON()`](textpage.html#TextPage.extractRAWJSON "TextPage.extractRAWJSON"). May include text and images.

        Parameters:
        :   - **opt** (*str*) – A string indicating the requested format, one of the above. A mixture of upper and lower case is supported. If misspelled, option “text” is silently assumed.
            - **clip** (*rect-like*) – restrict the extraction to this rectangle. If `None` (default), the visible part of the page is taken. Any content (text, images) that is **not fully contained** in `clip` will be completely omitted. To avoid clipping altogether use `clip=pymupdf.INFINITE_RECT()`. Only then the extraction will contain all items. This parameter has **no effect** on options “html”, “xhtml” and “xml”.
            - **flags** (*int*) – indicator bits to control whether to include images or how text should be handled with respect to white spaces and `ligatures`. See [Font Properties](vars.html#textpreserve) for available indicators and [Text Extraction Flags Defaults](app1.html#text-extraction-flags) for default settings. (New in v1.16.2)
            - **textpage** – use a previously created [TextPage](textpage.html#textpage). This reduces execution time **very significantly:** by more than 50% and up to 95%, depending on the extraction option. If specified, the ‘flags’ and ‘clip’ arguments are ignored, because they are textpage-only properties. If omitted, a new, temporary textpage will be created.
            - **sort** (*bool*) – sort the output by vertical, then horizontal coordinates. In many cases, this should suffice to generate a “natural” reading order. Has no effect on (X)HTML and XML. For options “blocks”, “dict”, “json”, “rawdict”, “rawjson”, sorting happens by coordinates `(y1, x0)` of the respective block bbox. For options “words” and “text”, the text lines are completely re-synthesized to follow the reading sequence and appearance in the document – which even establishes the original layout to some extent.
            - **delimiters** (*str*) – use these characters as *additional* word separators with the “words” output option (ignored otherwise). By default, all white spaces (including non-breaking space `0xA0`) indicate start and end of a word. Now you can specify more characters causing this. For instance, the default will return `"john.doe@outlook.com"` as **one** word. If you specify `delimiters="@."` then the **four** words `"john"`, `"doe"`, `"outlook"`, `"com"` will be returned. Other possible uses include ignoring punctuation characters `delimiters=string.punctuation`. The “word” strings will not contain any delimiting character. (New in v1.23.5)

        Return type:
        :   *str, list, dict*

        Returns:
        :   The page’s content as a string, a list or a dictionary. Refer to the corresponding [TextPage](textpage.html#textpage) method for details.

        Note

        1. You can use this method as a **document conversion tool** from [any supported document type](how-to-open-a-file.html#supported-file-types) to one of TEXT, HTML, XHTML or XML documents.
        2. The inclusion of text via the *clip* parameter is decided on a by-character level: a character becomes part of the output, if its bbox is contained in `clip`. This **deviates** from the algorithm used in redaction annotations: a character will be **removed if its bbox intersects** any redaction annotation.

        Show/hide history

        - Changed in v1.19.0: added [TextPage](textpage.html) parameter
        - Changed in v1.19.1: added `sort` parameter
        - Changed in v1.19.6: added new constants for defining default flags per method.
        - Changed in v1.23.5: added `delimiters` parameter
        - Changed in v1.24.11: changed the effect of `sort_True` for “text” and “words” to closely follow natural reading sequence.

    get\_textbox(*rect*, *textpage=None*)
    :   Retrieve the text contained in a rectangle.

        Parameters:
        :   - **rect** (*rect-like*) – rect-like.
            - **textpage** – a [TextPage](textpage.html#textpage) to use. If omitted, a new, temporary textpage will be created.

        Returns:
        :   a string with interspersed linebreaks where necessary. It is based on dedicated code (changed in v1.19.0). A typical use is checking the result of [`Page.search_for()`](#Page.search_for "Page.search_for"):

            ```
            >>> rl = page.search_for("currency:")
            >>> page.get_textbox(rl[0])
            'Currency:'
            >>>
            ```

        Show/hide history

        - New in v1.17.7
        - Changed in v1.19.0: add [TextPage](textpage.html) parameter

    get\_textpage(*clip=None*, *flags=3*)
    :   Create a [TextPage](textpage.html#textpage) for the page.

        Parameters:
        :   - **flags** (*int*) – indicator bits controlling the content available for subsequent text extractions and searches – see the parameter of [`Page.get_text()`](#Page.get_text "Page.get_text").
            - **clip** (*rect-like*) – restrict extracted text to this area. (New in v1.17.7)

        Returns:
        :   [TextPage](textpage.html#textpage)

        Show/hide history

        - New in v1.16.5
        - Changed in v1.17.7: introduced `clip` parameter.

    get\_textpage\_ocr(*flags=3*, *language='eng'*, *dpi=72*, *full=False*, *tessdata=None*)
    :   **Optical Character Recognition** (**OCR**) technology can be used to extract text data for pages where text is in raster image or vector graphic format. Use this method to **OCR** a page for subsequent text extraction.

        This method returns a [TextPage](textpage.html#textpage) for the page that includes OCRed text. MuPDF will invoke Tesseract-OCR if this method is used.

        Parameters:
        :   - **flags** (*int*) – indicator bits controlling the content available for subsequent test extractions and searches – see the parameter of [`Page.get_text()`](#Page.get_text "Page.get_text").
            - **language** (*str*) – the expected language(s). Use “+”-separated values if multiple languages are expected, “eng+spa” for English and Spanish.
            - **dpi** (*int*) – the desired resolution in dots per inch. Influences recognition quality (and execution time).
            - **full** (*bool*) – whether to OCR the full page, or only page areas that contain no legible text.
            - **tessdata** (*str*) – The name of Tesseract’s language support folder `tessdata`. If omitted, the name is determined using function [`get_tessdata()`](functions.html#get_tessdata "get_tessdata").

        Note

        This method does **not** support a clip parameter – OCR (full or partial) will always happen for the complete page rectangle.

        Returns:
        :   a [TextPage](textpage.html#textpage). Execution may be significantly longer than [`Page.get_textpage()`](#Page.get_textpage "Page.get_textpage").

        For `full=True` OCR, **all text** will have the font “GlyphLessFont” from Tesseract. In case of partial OCR (`full=False`), legible normal text will keep its properties, and only recognized text will have the GlyphLessFont.

        Recognized / OCR text will follow (legible) normal text for partial OCR and will thus not be in reading order. Establishing reading order is – as always – your responsibility.

        Note

        Text extraction results, including any OCR, are stored in the returned [TextPage](textpage.html#textpage). To access them, you must use the `textpage` parameter in all subsequent text extraction and search methods.

        [This Jupyter notebook](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/jupyter-notebooks/partial-ocr.ipynb) walks through an example for using OCR textpages.

        Show/hide history

        - New in v.1.19.0
        - Changed in v1.19.1: support full and partial OCRing a page.
        - changed in v1.27.2: For partial OCR, **all** page areas outside legible text are now OCRed, not just those within images. This means that OCR will now also be performed for vector graphics, and for text containing illegible characters.

    get\_drawings(*extended=False*)
    :   Return the vector graphics of the page. These are instructions which draw lines, rectangles, quadruples or curves, including properties like colors, transparency, line width and dashing, etc. Alternative terms are “line art” and “drawings”.

        Returns:
        :   a list of dictionaries. Each dictionary item contains one or more single draw commands belonging together: they have the same properties (colors, dashing, etc.). This is called a **“path”** in PDF, so we adopted that name here, but the method **works for all document types**.

        The path dictionary for fill, stroke and fill-stroke paths has been designed to be compatible with class [Shape](shape.html#shape). There are the following keys:

        | Key | Value |
        | --- | --- |
        | closePath | Same as the parameter in [Shape](shape.html#shape). |
        | color | Stroke color (see [Shape](shape.html#shape)). |
        | dashes | Dashed line specification (see [Shape](shape.html#shape)). |
        | even\_odd | Fill colors of area overlaps – same as the parameter in [Shape](shape.html#shape). |
        | fill | Fill color (see [Shape](shape.html#shape)). |
        | items | List of draw commands: lines, rectangles, quads or curves. |
        | lineCap | Number 3-tuple, use its max value on output with [Shape](shape.html#shape). |
        | lineJoin | Same as the parameter in [Shape](shape.html#shape). |
        | fill\_opacity | fill color transparency (see [Shape](shape.html#shape)). (New in v1.18.17) |
        | stroke\_opacity | stroke color transparency (see [Shape](shape.html#shape)). (New in v1.18.17) |
        | rect | Page area covered by this path. Information only. |
        | layer | name of applicable Optional Content Group. (New in v1.22.0) |
        | level | the hierarchy level if `extended=True`. (New in v1.22.0) |
        | seqno | command number when building page appearance. (New in v1.19.0) |
        | type | type of this path. (New in v1.18.17) |
        | width | Stroke line width. (see [Shape](shape.html#shape)). |

        Key `"opacity"` has been replaced by the new keys `"fill_opacity"` and `"stroke_opacity"`. This is now compatible with the corresponding parameters of [`Shape.finish()`](shape.html#Shape.finish "Shape.finish"). (Changed in v1.18.17)

        For paths other than groups or clips, key `"type"` takes one of the following values:

        - **“f”** – this is a *fill-only* path. Only key-values relevant for this operation have a meaning, not applicable ones are present with a value of `None`: `"color"`, `"lineCap"`, `"lineJoin"`, `"width"`, `"closePath"`, `"dashes"` and should be ignored.
        - **“s”** – this is a *stroke-only* path. Similar to previous, key `"fill"` is present with value `None`.
        - **“fs”** – this is a path performing combined *fill* and *stroke* operations.

        Each item in `path["items"]` is one of the following:

        - `("l", p1, p2)` - a line from p1 to p2 ([Point](point.html#point) objects).
        - `("c", p1, p2, p3, p4)` - cubic Bézier curve **from p1 to p4** (p2 and p3 are the control points). All objects are of type [Point](point.html#point).
        - `("re", rect, orientation)` - a [Rect](rect.html#rect). Multiple rectangles within the same path are now detected (changed in v1.18.17). Integer `orientation` is 1 resp. -1 indicating whether the enclosed area is rotated left (1 = anti-clockwise), or resp. right [[7]](#f7) (changed in v1.19.2).
        - `("qu", quad)` - a [Quad](quad.html#quad). 3 or 4 consecutive lines are detected to actually represent a [Quad](quad.html#quad) (changed in v1.19.2:). (New in v1.18.17)

        Using class [Shape](shape.html#shape), you should be able to recreate the original drawings on a separate (PDF) page with high fidelity under normal, not too sophisticated circumstances. Please see the following comments on restrictions. A coding draft can be found in [How to Extract Drawings](recipes-drawing-and-graphics.html#recipesdrawingandgraphics-extract-drawings).

        Specifying `extended=True` significantly alters the output. Most importantly, new dictionary types are present: “clip” and “group”. All paths will now be organized in a hierarchic structure which is encoded by the new integer key “level”, the hierarchy level. Each group or clip establishes a new hierarchy, which applies to all subsequent paths having a *larger* level value. (New in v1.22.0)

        Any path with a smaller level value than its predecessor will end the scope of (at least) the preceding hierarchy level. A “clip” path with the same level as the preceding clip will end the scope of that clip. Same is true for groups. This is best explained by an example:

        ```
        +------+------+--------+------+--------+
        | line | lvl0 | lvl1   | lvl2 |  lvl3  |
        +------+------+--------+------+--------+
        |  0   | clip |        |      |        |
        |  1   |      | fill   |      |        |
        |  2   |      | group  |      |        |
        |  3   |      |        | clip |        |
        |  4   |      |        |      | stroke |
        |  5   |      |        | fill |        |  ends scope of clip in line 3
        |  6   |      | stroke |      |        |  ends scope of group in line 2
        |  7   |      | clip   |      |        |
        |  8   | fill |        |      |        |  ends scope of line 0
        +------+------+--------+------+--------+
        ```

        The clip in line 0 applies to line including line 7. Group in line 2 applies to lines 3 to 5, clip in line 3 only applies to line 4.

        “stroke” in line 4 is under control of “group” in line 2 and “clip” in line 3 (which in turn is a subset of line 0 clip).

        - **“clip”** dictionary. Its values (most importantly “scissor”) remain valid / apply as long as following dictionaries have a **larger “level”** value.

          | Key | Value |
          | --- | --- |
          | closePath | Same as in “stroke” or “fill” dictionaries |
          | even\_odd | Same as in “stroke” or “fill” dictionaries |
          | items | Same as in “stroke” or “fill” dictionaries |
          | rect | Same as in “stroke” or “fill” dictionaries |
          | layer | Same as in “stroke” or “fill” dictionaries |
          | level | Same as in “stroke” or “fill” dictionaries |
          | scissor | the clip rectangle |
          | type | “clip” |
        - “group” dictionary. Its values remain valid (apply) as long as following dictionaries have a **larger “level”** value. Any dictionary with an equal or lower level end this group.

          | Key | Value |
          | --- | --- |
          | rect | Same as in “stroke” or “fill” dictionaries |
          | layer | Same as in “stroke” or “fill” dictionaries |
          | level | Same as in “stroke” or “fill” dictionaries |
          | isolated | (bool) Whether this group is isolated |
          | knockout | (bool) Whether this is a “Knockout Group” |
          | blendmode | Name of the BlendMode, default is “Normal” |
          | opacity | Float value in range [0, 1]. |
          | type | “group” |

        Note

        The method is based on the output of [`Page.get_cdrawings()`](#Page.get_cdrawings "Page.get_cdrawings") – which is much faster, but requires somewhat more attention processing its output.

        Show/hide history

        - New in v1.18.0
        - Changed in v1.18.17
        - Changed in v1.19.0: add “seqno” key, remove “clippings” key
        - Changed in v1.19.1: “color” / “fill” keys now always are either are RGB tuples or `None`. This resolves issues caused by exotic colorspaces.
        - Changed in v1.19.2: add an indicator for the *“orientation”* of the area covered by an “re” item.
        - Changed in v1.22.0: add new key `"layer"` which contains the name of the Optional Content Group of the path (or `None`).
        - Changed in v1.22.0: add parameter `extended` to also return clipping and group paths.

    get\_cdrawings(*extended=False*)
    :   Extract the vector graphics on the page. Apart from following technical differences, functionally equivalent to [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings"), but much faster:

        - Every path type only contains the relevant keys, e.g. a stroke path has no `"fill"` color key. See comment in method [`Page.get_drawings()`](#Page.get_drawings "Page.get_drawings").
        - Coordinates are given as [`point_like`](glossary.html#point_like "point_like"), [`rect_like`](glossary.html#rect_like "rect_like") and [`quad_like`](glossary.html#quad_like "quad_like") **tuples** – not as [Point](point.html#point), [Rect](rect.html#rect), [Quad](quad.html#quad) objects.

        If performance is a concern, consider using this method: Compared to versions earlier than 1.18.17, you should see much shorter response times. We have seen pages that required 2 seconds then, now only need 200 ms with this method.

        Show/hide history

        - New in v1.18.17
        - Changed in v1.19.0: removed “clippings” key, added “seqno” key.
        - Changed in v1.19.1: always generate RGB color tuples.
        - Changed in v1.22.0: added new key `"layer"` which contains the name of the Optional Content Group of the path (or `None`).
        - Changed in v1.22.0: added parameter `extended` to also return clipping paths.

    get\_fonts(*full=False*)
    :   PDF only: Return a list of fonts referenced by the page. Wrapper for [`Document.get_page_fonts()`](document.html#Document.get_page_fonts "Document.get_page_fonts").

    get\_images(*full=False*)
    :   PDF only: Return a list of images referenced by the page. Wrapper for [`Document.get_page_images()`](document.html#Document.get_page_images "Document.get_page_images").

    get\_image\_info(*hashes=False*, *xrefs=False*)
    :   Return a list of meta information dictionaries for all images displayed by the page. This works for all document types.

        Parameters:
        :   - **hashes** (*bool*) – Compute the MD5 hashcode for each encountered image, which allows identifying image duplicates. This adds the key `"digest"` to the output, whose value is a 16 byte `bytes` object. (New in v1.18.13)
            - **xrefs** (*bool*) – **PDF only.** Try to find the [`xref`](glossary.html#xref "xref") for each image. Implies `hashes=True`. Adds the `"xref"` key to the dictionary. If not found, the value is 0, which means, the image is either “inline” or its xref is undetectable for some reason. Please note that this option has an extended response time, because the MD5 hashcode will be computed at least two times for each image with an xref. (New in v1.18.13)

        Return type:
        :   list[dict]

        Returns:
        :   A list of dictionaries. This includes information for **exactly those** images, that are shown on the page – including *“inline images”*. The dictionary layout is similar to that of image blocks in `page.get_text("dict")`.

            In contrast to images included in [`Page.get_text()`](#Page.get_text "Page.get_text"), image **binary content** is not loaded by this method, which drastically reduces memory usage. Another difference is that image detection is not restricted to the visible part of the page or any `clip` parameter: method [`Page.get_text()`](#Page.get_text "Page.get_text") will only extract images **fully contained** in the provided `clip`.

            | **Key** | **Value** |
            | --- | --- |
            | number | block number (`int`) |
            | bbox | image bbox on page, [`rect_like`](glossary.html#rect_like "rect_like") |
            | width | original image width (`int`) |
            | height | original image height (`int`) |
            | cs-name | colorspace name (`str`) |
            | colorspace | colorspace.n (`int`) |
            | xres | resolution in x-direction (`int`) [[10]](#f10) |
            | yres | resolution in y-direction (`int`) [[10]](#f10) |
            | bpc | bits per component (`int`) |
            | size | storage occupied by image (`int`) |
            | digest | MD5 hashcode (`bytes`), if `hashes` is true |
            | xref | image [`xref`](glossary.html#xref "xref") or 0, if *xrefs* is true |
            | transform | matrix transforming image rect to bbox, [`matrix_like`](glossary.html#matrix_like "matrix_like") |
            | has-mask | whether the image is transparent and has a mask (`bool`) |

            Multiple occurrences of the same image are always reported. You can detect duplicates by comparing their [`digest`](pixmap.html#Pixmap.digest "Pixmap.digest") values.

        Show/hide history

        - New in v1.18.11
        - Changed in v1.18.13: added image MD5 hashcode computation and [`xref`](glossary.html#xref "xref") search.

    get\_xobjects()
    :   PDF only: Return a list of Form XObjects referenced by the page. Wrapper for [`Document.get_page_xobjects()`](document.html#Document.get_page_xobjects "Document.get_page_xobjects").

    get\_image\_rects(*item*, *transform=False*)
    :   PDF only: Return boundary boxes and transformation matrices of an embedded image. This is an improved version of [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox") with the following differences:

        - There is no restriction on **how** the image is invoked (by the page or one of its Form XObjects). The result is always complete and correct.
        - The result is a list of [Rect](rect.html#rect) or ([Rect](rect.html#rect), [Matrix](matrix.html#matrix)) objects – depending on *transform*. Each list item represents one location of the image on the page. Multiple occurrences might not be detectable by [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox").
        - The method invokes [`Page.get_image_info()`](#Page.get_image_info "Page.get_image_info") with `xrefs=True` and therefore has a noticeably longer response time than [`Page.get_image_bbox()`](#Page.get_image_bbox "Page.get_image_bbox").

        Parameters:
        :   - **item** (*list**,**str**,**int*) – an item of the list [`Page.get_images()`](#Page.get_images "Page.get_images"), or the reference **name** entry of such an item (item[7]), or the image [`xref`](glossary.html#xref "xref").
            - **transform** (*bool*) – also return the matrix used to transform the image rectangle to the bbox on the page. If true, then tuples `(bbox, matrix)` are returned.

        Return type:
        :   list

        Returns:
        :   Boundary boxes and respective transformation matrices for each image occurrence on the page. If the item is not on the page, an empty list `[]` is returned.

        Show/hide history

        New in v1.18.13

    get\_image\_bbox(*item*, *transform=False*)
    :   PDF only: Return boundary box and transformation matrix of an embedded image.

        Parameters:
        :   - **item** (*list**,**str*) – an item of the list [`Page.get_images()`](#Page.get_images "Page.get_images") with *full=True* specified, or the reference **name** entry of such an item, which is item[-3] (or item[7] respectively).
            - **transform** (*bool*) – return the matrix used to transform the image rectangle to the bbox on the page (new in v1.18.11). Default is just the bbox. If true, then a tuple `(bbox, matrix)` is returned.

        Return type:
        :   [Rect](rect.html#rect) or ([Rect](rect.html#rect), [Matrix](matrix.html#matrix))

        Returns:
        :   the boundary box of the image – optionally also its transformation matrix.

            Show/hide history

            - (Changed in v1.16.7): If the page in fact does not display this image, an infinite rectangle is returned now. In previous versions, an exception was raised. Formally invalid parameters still raise exceptions.
            - (Changed in v1.17.0): Only images referenced directly by the page are considered. This means that images occurring in embedded PDF pages are ignored and an exception is raised.
            - (Changed in v1.18.5): Removed the restriction introduced in v1.17.0: any item of the page’s image list may be specified.
            - (Changed in v1.18.11): Partially re-instated a restriction: only those images are considered, that are either directly referenced by the page or by a Form XObject directly referenced by the page.
            - (Changed in v1.18.11): Optionally also return the transformation matrix together with the bbox as the tuple `(bbox, transform)`.

        Note

        1. Be aware that [`Page.get_images()`](#Page.get_images "Page.get_images") may contain “dead” entries i.e. images, which the page **does not display**. This is no error, but intended by the PDF creator. No exception will be raised in this case, but an infinite rectangle is returned. You can avoid this from happening by executing [`Page.clean_contents()`](functions.html#Page.clean_contents "Page.clean_contents") before this method.
        2. The image’s “transformation matrix” is defined as the matrix, for which the expression `bbox / transform == pymupdf.Rect(0, 0, 1, 1)` is true, lookup details here: [Image Transformation Matrix](app3.html#imagetransformation).

        Show/hide history

        - Changed in v1.18.11: return image transformation matrix

    get\_svg\_image(*matrix=pymupdf.Identity*, *text\_as\_path=True*)
    :   Create an SVG image from the page. Only full page images are currently supported.

        Parameters:
        :   - **matrix** (*matrix\_like*) – a matrix, default is [Identity](identity.html#identity).
            - **text\_as\_path** (*bool*) – – controls how text is represented. `True` outputs each character as a series of elementary draw commands, which leads to a more precise text display in browsers, but a **very much larger** output for text-oriented pages. Display quality for `False` relies on the presence of the referenced fonts on the current system. For missing fonts, the internet browser will fall back to some default – leading to unpleasant appearances. Choose `False` if you want to parse the text of the SVG. (New in v1.17.5)

        Returns:
        :   a UTF-8 encoded string that contains the image. Because SVG has XML syntax it can be saved in a text file, the standard extension is `.svg`.

            Note

            In case of a PDF, you can circumvent the “full page image only” restriction by modifying the page’s CropBox before using the method.

    get\_pixmap(*\**, *matrix=pymupdf.Identity*, *dpi=None*, *colorspace=pymupdf.csRGB*, *clip=None*, *alpha=False*, *annots=True*)
    :   Create a pixmap from the page. This is probably the most often used method to create a [Pixmap](pixmap.html#pixmap).

        All parameters are *keyword-only.*

        Parameters:
        :   - **matrix** (*matrix\_like*) – default is [Identity](identity.html#identity).
            - **dpi** (*int*) – desired resolution in x and y direction. If not `None`, the `"matrix"` parameter is ignored. (New in v1.19.2)
            - **colorspace** (str or [Colorspace](colorspace.html#colorspace)) – The desired colorspace, one of “GRAY”, “RGB” or “CMYK” (case insensitive). Or specify a [Colorspace](colorspace.html#colorspace), ie. one of the predefined ones: [`csGRAY`](vars.html#csGRAY "csGRAY"), [`csRGB`](vars.html#csRGB "csRGB") or [`csCMYK`](vars.html#csCMYK "csCMYK").
            - **clip** (*irect\_like*) – restrict rendering to the intersection of this area with the page’s rectangle.
            - **alpha** (*bool*) –

              whether to add an alpha channel. Always accept the default `False` if you do not really need transparency. This will save a lot of memory (25% in case of RGB … and pixmaps are typically **large**!), and also processing time. Also note an **important difference** in how the image will be rendered: with `True` the pixmap’s samples area will be pre-cleared with *0x00*. This results in **transparent** areas where the page is empty. With `False` the pixmap’s samples will be pre-cleared with *0xff*. This results in **white** where the page has nothing to show.

              Show/hide history

              Changed in v1.14.17
              :   The default alpha value is now `False`.

                  - Generated with *alpha=True*
                  - Generated with *alpha=False*
            - **annots** (*bool*) – *(new in version 1.16.0)* whether to also render annotations or to suppress them. You can create pixmaps for annotations separately.

        Return type:
        :   [Pixmap](pixmap.html#pixmap)

        Returns:
        :   Pixmap of the page. For fine-controlling the generated image, the by far most important parameter is **matrix**. E.g. you can increase or decrease the image resolution by using **Matrix(xzoom, yzoom)**. If zoom > 1, you will get a higher resolution: zoom=2 will double the number of pixels in that direction and thus generate a 2 times larger image. Non-positive values will flip horizontally, resp. vertically. Similarly, matrices also let you rotate or shear, and you can combine effects via e.g. matrix multiplication. See the [Matrix](matrix.html#matrix) section to learn more.

        Note

        - The pixmap will have *“premultiplied”* pixels if `alpha=True`. To learn about some background, e.g. look for “Premultiplied alpha” [here](https://en.wikipedia.org/wiki/Glossary_of_computer_graphics#P).
        - The method will respect any page rotation and will not exceed the intersection of `clip` and [`Page.cropbox`](#Page.cropbox "Page.cropbox"). If you need the page’s mediabox (and if this is a different rectangle), you can use a snippet like the following to achieve this:

          ```
          In [1]: import pymupdf
          In [2]: doc=pymupdf.open("demo1.pdf")
          In [3]: page=doc[0]
          In [4]: rotation = page.rotation
          In [5]: cropbox = page.cropbox
          In [6]: page.set_cropbox(page.mediabox)
          In [7]: page.set_rotation(0)
          In [8]: pix = page.get_pixmap()
          In [9]: page.set_cropbox(cropbox)
          In [10]: if rotation != 0:
             ...:     page.set_rotation(rotation)
             ...:
          In [11]:
          ```

        Show/hide history

        - Changed in v1.19.2: added support of parameter dpi.

    annot\_names()
    :   PDF only: return a list of the names of annotations, widgets and links. Technically, these are the */NM* values of every PDF object found in the page’s */Annots* array.

        Return type:
        :   list

        Show/hide history

        - New in v1.16.10

    annot\_xrefs()
    :   PDF only: return a list of the [`xref`](glossary.html#xref "xref") numbers of annotations, widgets and links – technically of all entries found in the page’s */Annots* array.

        Return type:
        :   list

        Returns:
        :   a list of items *(xref, type)* where type is the annotation type. Use the type to tell apart links, fields and annotations, see [Annotation Types](vars.html#annotationtypes).

        Show/hide history

        - New in v1.17.1

    load\_annot(*ident*)
    :   PDF only: return the annotation identified by *ident*. This may be its unique name (PDF `/NM` key), or its [`xref`](glossary.html#xref "xref").

        Parameters:
        :   **ident** (*str**,**int*) – the annotation name or xref.

        Return type:
        :   [Annot](annot.html#annot)

        Returns:
        :   the annotation or `None`.

        Note

        Methods [`Page.annot_names()`](#Page.annot_names "Page.annot_names"), [`Page.annot_xrefs()`](#Page.annot_xrefs "Page.annot_xrefs") provide lists of names or xrefs, respectively, from where an item may be picked and loaded via this method.

        Show/hide history

        - New in v1.17.1

    load\_widget(*xref*)
    :   PDF only: return the field identified by [`xref`](glossary.html#xref "xref").

        Parameters:
        :   **xref** (*int*) – the field’s xref.

        Return type:
        :   [Widget](widget.html#widget)

        Returns:
        :   the field or `None`.

        Note

        This is similar to the analogous method [`Page.load_annot()`](#Page.load_annot "Page.load_annot") – except that here only the xref is supported as identifier.

        Show/hide history

        - New in v1.19.6

    load\_links()
    :   Return the first link on a page. Synonym of property [`first_link`](#Page.first_link "Page.first_link").

        Return type:
        :   [Link](link.html#link)

        Returns:
        :   first link on the page (or `None`).

    set\_rotation(*rotate*)
    :   PDF only: Set the rotation of the page.

        Parameters:
        :   **rotate** (*int*) – An integer specifying the required rotation in degrees. Must be an integer multiple of 90. Values will be converted to one of 0, 90, 180, 270.

    recolor(*components=1*)
    :   PDF only: Change the colorspace components of all objects on page.

        Parameters:
        :   **components** (*int*) – The desired count of color components. Must be one of 1, 3 or 4, which results in color spaces DeviceGray, DeviceRGB or DeviceCMYK respectively. The method affects text, images and vector graphics. For instance, with the default value 1, a page will be converted to grayscale. If a page is already grayscale, the method will not cause visible changes – independent of the value of `components`.

        These changes are **permanent** and cannot be reverted.

    clip\_to\_rect(*rect*)
    :   PDF only: Permanently remove page content outside the given rectangle. This is similar to [`Page.set_cropbox()`](#Page.set_cropbox "Page.set_cropbox"), but the page’s rectangle will not be changed, only the content outside the rectangle will be removed.

        Parameters:
        :   **rect** (*rect\_like*) – The rectangle to clip to. Must be finite and its intersection with the page must not be empty.

        The method works best for text: All text on the page will be removed (decided by single character) that has no intersection with the rectangle. For vector graphics, the method will remove all paths that have no intersection with the rectangle. For images, the method will remove all images that have no intersection with the rectangle. Vectors and images **having** an intersection with the rectangle, will be kept in their entirety.

        The method roughly has the same effect as if four redactions had been applied that cover the rectangle’s outside.

        - New in v1.26.4.

    remove\_rotation()
    :   PDF only: Set page rotation to 0 while maintaining appearance and page content.

        Returns:
        :   The inverted matrix used to achieve this change. If the page was not rotated (rotation 0), [Identity](identity.html#identity) is returned. The method automatically recomputes the rectangles of any annotations, links and widgets present on the page.

            This method may come in handy when e.g. used with [`Page.show_pdf_page()`](#Page.show_pdf_page "Page.show_pdf_page").

    show\_pdf\_page(*rect*, *docsrc*, *pno=0*, *keep\_proportion=True*, *overlay=True*, *oc=0*, *rotate=0*, *clip=None*)
    :   PDF only: Display a page of another PDF. This is similar to [`Page.insert_image()`](#Page.insert_image "Page.insert_image") but the source page will appear like a copy of itself and will not be rasterized. This is a multi-purpose method. For example, you can use it to:

        - create “n-up” versions of existing PDF files, combining several input pages into **one output page** (see example [combine.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/combine-pages/combine.py)),
        - create “posterized” PDF files, i.e. every input page is split up in parts which each create a separate output page (see [posterize.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/posterize-document/posterize.py)),
        - include PDF-based vector images like company logos, watermarks, etc., see [svg.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/insert-logo/svg.py), which puts an SVG-based logo on each page.

        Parameters:
        :   - **rect** (*rect\_like*) – where to place the image on current page. Must be finite and its intersection with the page must not be empty.
            - **docsrc** ([Document](document.html#document)) – source PDF document containing the page. Must be a different document object, but may be the same file.
            - **pno** (*int*) – page number (0-based, in `-∞ < pno < docsrc.page_count`) to be shown.
            - **keep\_proportion** (*bool*) – whether to maintain the width-height-ratio (default). If false, all 4 corners are always positioned on the border of the target rectangle – whatever the rotation value. In general, this will deliver distorted and /or non-rectangular images.
            - **overlay** (*bool*) – put image in foreground (default) or background.
            - **oc** (*int*) – ([`xref`](glossary.html#xref "xref")) make visibility dependent on this [`OCG`](glossary.html#OCG "OCG") / [`OCMD`](glossary.html#OCMD "OCMD") (which must be defined in the target PDF) [[9]](#f9). (New in v1.18.3)
            - **rotate** (*float*) – show the source rectangle rotated by some angle. Any angle is supported (changed in v1.14.11). (New in v1.14.10)
            - **clip** (*rect\_like*) – choose which part of the source page to show. Default is the full page, else must be finite and its intersection with the source page must not be empty.

        Note

        In contrast to method [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf"), this method does not copy annotations, widgets or links, so these objects are not included in the target [[6]](#f6). But all its **other resources (text, images, fonts, etc.)** will be imported into the current PDF. They will therefore appear in text extractions and in [`get_fonts()`](#Page.get_fonts "Page.get_fonts") and [`get_images()`](#Page.get_images "Page.get_images") lists – even if they are not contained in the visible area given by *clip*.

        Example: Show the same source page, rotated by 90 and by -90 degrees:

        ```
        >>> doc = pymupdf.open()  # new empty PDF
        >>> page=doc.new_page()  # new page in A4 format
        >>>
        >>> # upper half page
        >>> r1 = pymupdf.Rect(0, 0, page.rect.width, page.rect.height/2)
        >>>
        >>> # lower half page
        >>> r2 = r1 + (0, page.rect.height/2, 0, page.rect.height/2)
        >>>
        >>> src = pymupdf.open("PyMuPDF.pdf")  # show page 0 of this
        >>>
        >>> page.show_pdf_page(r1, src, 0, rotate=90)
        >>> page.show_pdf_page(r2, src, 0, rotate=-90)
        >>> doc.save("show.pdf")
        ```

        Show/hide history

        - Changed in v1.14.11: Parameter *reuse\_xref* has been deprecated. Position the source rectangle centered in target rectangle. Any rotation angle is now supported.
        - Changed in v1.18.3: New parameter `oc`.

    new\_shape()
    :   PDF only: Create a new [Shape](shape.html#shape) object for the page.

        Return type:
        :   [Shape](shape.html#shape)

        Returns:
        :   a new [Shape](shape.html#shape) to use for compound drawings. See description there.

    search\_for(*needle*, *\**, *clip=None*, *quads=False*, *flags=TEXT\_DEHYPHENATE | TEXT\_PRESERVE\_WHITESPACE | TEXT\_PRESERVE\_LIGATURES | TEXT\_MEDIABOX\_CLIP*, *textpage=None*)
    :   Search for *needle* on a page. Wrapper for [`TextPage.search()`](textpage.html#TextPage.search "TextPage.search").

        Parameters:
        :   - **needle** (*str*) – Text to search for. May contain spaces. Upper / lower case is ignored, but only works for ASCII characters: For example, “COMPÉTENCES” will not be found if needle is “compétences” – “compÉtences” however will. Similar is true for German umlauts and the like.
            - **clip** (*rect\_like*) – only search within this area. (New in v1.18.2)
            - **quads** (*bool*) – Return object type [Quad](quad.html#quad) instead of [Rect](rect.html#rect).
            - **flags** (*int*) – Control the data extracted by the underlying [TextPage](textpage.html#textpage). By default, ligatures and white spaces are kept, and hyphenation [[8]](#f8) is detected.
            - **textpage** – use a previously created [TextPage](textpage.html#textpage). This reduces execution time **significantly.** If specified, the ‘flags’ and ‘clip’ arguments are ignored. If omitted, a temporary textpage will be created. (New in v1.19.0)

        Return type:
        :   list

        Returns:
        :   A list of [Rect](rect.html#rect) or [Quad](quad.html#quad) objects, each of which – **normally!** – surrounds one occurrence of *needle*. **However:** if parts of *needle* occur on more than one line, then a separate item is generated for each these parts. So, if `needle = "search string"`, two rectangles may be generated.

            Show/hide history

            Changes in v1.18.2:

            - There no longer is a limit on the list length (removal of the `hit_max` parameter).
            - If a word is **hyphenated** at a line break, it will still be found. E.g. the needle “method” will be found even if hyphenated as “meth-od” at a line break, and two rectangles will be returned: one surrounding “meth” (without the hyphen) and another one surrounding “od”.

        Note

        The method supports multi-line text marker annotations: you can use the full returned list as **one single** parameter for creating the annotation.

        Caution

        - There is a tricky aspect: the search logic regards **contiguous multiple occurrences** of *needle* as one: assuming *needle* is “abc”, and the page contains “abc” and “abcabc”, then only **two** rectangles will be returned, one for “abc”, and a second one for “abcabc”.
        - You can always use [`Page.get_textbox()`](#Page.get_textbox "Page.get_textbox") to check what text actually is being surrounded by each rectangle.

        Note

        A feature repeatedly asked for is supporting **regular expressions** when specifying the `"needle"` string: **There is no way to do this.** If you need something in that direction, first extract text in the desired format and then subselect the result by matching with some regex pattern. Here is an example for matching words:

        ```
        >>> pattern = re.compile(r"...")  # the regex pattern
        >>> words = page.get_text("words")  # extract words on page
        >>> matches = [w for w in words if pattern.search(w[4])]
        ```

        The `matches` list will contain the words matching the given pattern. In the same way you can select `span["text"]` from the output of `page.get_text("dict")`.

        Show/hide history

        - Changed in v1.18.2: added `clip` parameter. Remove `hit_max` parameter. Add default “dehyphenate”.
        - Changed in v1.19.0: added [TextPage](textpage.html) parameter.

    set\_mediabox(*r*)
    :   PDF only: Change the physical page dimension by setting [`mediabox`](#Page.mediabox "Page.mediabox") in the page’s object definition.

        Parameters:
        :   **r** (*rect-like*) – the new [`mediabox`](#Page.mediabox "Page.mediabox") value.

        Note

        This method also removes the page’s other (optional) rectangles ([`cropbox`](#Page.cropbox "Page.cropbox"), ArtBox, TrimBox and Bleedbox) to prevent inconsistent situations. This will cause those to assume their default values.

        Caution

        For non-empty pages this may have undesired effects, because the location of all content depends on this value and will therefore change position or even disappear.

        Show/hide history

        - New in v1.16.13
        - Changed in v1.19.4: remove all other rectangle definitions.

    set\_cropbox(*r*)
    :   PDF only: change the visible part of the page.

        Parameters:
        :   **r** (*rect\_like*) – the new visible area of the page. Note that this **must** be specified in **unrotated coordinates**, not empty, nor infinite and be completely contained in the [`Page.mediabox`](#Page.mediabox "Page.mediabox").

        After execution **(if the page is not rotated)**, [`Page.rect`](#Page.rect "Page.rect") will equal this rectangle, but be shifted to the top-left position (0, 0) if necessary. Example session:

        ```
        >>> page = doc.new_page()
        >>> page.rect
        pymupdf.Rect(0.0, 0.0, 595.0, 842.0)
        >>>
        >>> page.cropbox  # cropbox and mediabox still equal
        pymupdf.Rect(0.0, 0.0, 595.0, 842.0)
        >>>
        >>> # now set cropbox to a part of the page
        >>> page.set_cropbox(pymupdf.Rect(100, 100, 400, 400))
        >>> # this will also change the "rect" property:
        >>> page.rect
        pymupdf.Rect(0.0, 0.0, 300.0, 300.0)
        >>>
        >>> # but mediabox remains unaffected
        >>> page.mediabox
        pymupdf.Rect(0.0, 0.0, 595.0, 842.0)
        >>>
        >>> # revert CropBox change
        >>> # either set it to MediaBox
        >>> page.set_cropbox(page.mediabox)
        >>> # or 'refresh' MediaBox: will remove all other rectangles
        >>> page.set_mediabox(page.mediabox)
        ```

    set\_artbox(*r*)

    set\_bleedbox(*r*)

    set\_trimbox(*r*)
    :   PDF only: Set the resp. rectangle in the page object. For the meaning of these objects see [Adobe PDF References](app3.html#adobemanual), page 77. Parameter and restrictions are the same as for [`Page.set_cropbox()`](#Page.set_cropbox "Page.set_cropbox").

        Show/hide history

        - New in v1.19.4

    rotation
    :   Contains the rotation of the page in degrees (always 0 for non-PDF types). This is a copy of the value in the PDF file. The PDF documentation says:

        > *“The number of degrees by which the page should be rotated clockwise when displayed or printed. The value must be a multiple of 90. Default value: 0.”*
        >
        > In PyMuPDF, we make sure that this attribute is always one of 0, 90, 180 or 270.

        Type:
        :   int

    cropbox\_position
    :   Contains the top-left point of the page’s `/CropBox` for a PDF, otherwise *Point(0, 0)*.

        Type:
        :   [Point](point.html#point)

    cropbox
    :   The page’s `/CropBox` for a PDF. Always the **unrotated** page rectangle is returned. For a non-PDF this will always equal the page rectangle.

        Note

        In PDF, the relationship between `/MediaBox`, `/CropBox` and page rectangle may sometimes be confusing, please do lookup the glossary for [`MediaBox`](glossary.html#MediaBox "MediaBox").

        Type:
        :   [Rect](rect.html#rect)

    artbox

    bleedbox

    trimbox
    :   The page’s `/ArtBox`, `/BleedBox`, `/TrimBox`, respectively. If not provided, defaulting to [`Page.cropbox`](#Page.cropbox "Page.cropbox").

        Type:
        :   [Rect](rect.html#rect)

    mediabox\_size
    :   Contains the width and height of the page’s [`Page.mediabox`](#Page.mediabox "Page.mediabox") for a PDF, otherwise the bottom-right coordinates of [`Page.rect`](#Page.rect "Page.rect").

        Type:
        :   [Point](point.html#point)

    mediabox
    :   The page’s [`mediabox`](#Page.mediabox "Page.mediabox") for a PDF, otherwise [`Page.rect`](#Page.rect "Page.rect").

        Type:
        :   [Rect](rect.html#rect)

        Note

        For most PDF documents and for **all other document types**, `page.rect == page.cropbox == page.mediabox` is true. However, for some PDFs the visible page is a true subset of [`mediabox`](#Page.mediabox "Page.mediabox"). Also, if the page is rotated, its [`Page.rect`](#Page.rect "Page.rect") may not equal [`Page.cropbox`](#Page.cropbox "Page.cropbox"). In these cases the above attributes help to correctly locate page elements.

    transformation\_matrix
    :   This matrix translates coordinates from the PDF space to the MuPDF space. For example, in PDF `/Rect [x0 y0 x1 y1]` the pair (x0, y0) specifies the **bottom-left** point of the rectangle – in contrast to MuPDF’s system, where (x0, y0) specify top-left. Multiplying the PDF coordinates with this matrix will deliver the (Py-) MuPDF rectangle version. Obviously, the inverse matrix will again yield the PDF rectangle.

        Type:
        :   [Matrix](matrix.html#matrix)

    rotation\_matrix

    derotation\_matrix
    :   These matrices may be used for dealing with rotated PDF pages. When adding / inserting anything to a PDF page, the coordinates of the **unrotated** page are always used. These matrices help translating between the two states. Example: if a page is rotated by 90 degrees – what would then be the coordinates of the top-left Point(0, 0) of an A4 page?

        ```
        >>> page.set_rotation(90)  # rotate an ISO A4 page
        >>> page.rect
        Rect(0.0, 0.0, 842.0, 595.0)
        >>> p = pymupdf.Point(0, 0)  # where did top-left point land?
        >>> p * page.rotation_matrix
        Point(842.0, 0.0)
        >>>
        ```

        Type:
        :   [Matrix](matrix.html#matrix)

    first\_link
    :   Contains the first [Link](link.html#link) of a page (or `None`).

        Type:
        :   [Link](link.html#link)

    first\_annot
    :   Contains the first [Annot](annot.html#annot) of a page (or `None`).

        Type:
        :   [Annot](annot.html#annot)

    first\_widget
    :   Contains the first [Widget](widget.html#widget) of a page (or `None`).

        Type:
        :   [Widget](widget.html#widget)

    number
    :   The page number.

        Type:
        :   int

    parent
    :   The owning document object.

        Type:
        :   [Document](document.html#document)

    rect
    :   Contains the rectangle of the page. Same as result of [`Page.bound()`](#Page.bound "Page.bound").

        Type:
        :   [Rect](rect.html#rect)

    xref
    :   The page’s PDF [`xref`](glossary.html#xref "xref"). Zero if not a PDF.

        Type:
        :   [Rect](rect.html#rect)

---

## Description of *get\_links()* Entries

Each entry of the [`Page.get_links()`](#Page.get_links "Page.get_links") list is a dictionary with the following keys:

- *kind*: (required) an integer indicating the kind of link. This is one of *LINK\_NONE*, *LINK\_GOTO*, *LINK\_GOTOR*, *LINK\_LAUNCH*, or *LINK\_URI*. For values and meaning of these names refer to [Link Destination Kinds](vars.html#linkdest-kinds).
- *from*: (required) a [Rect](rect.html#rect) describing the “hot spot” location on the page’s visible representation (where the cursor changes to a hand image, usually).
- *page*: a 0-based integer indicating the destination page. Required for *LINK\_GOTO* and *LINK\_GOTOR*, else ignored.
- *to*: either a *pymupdf.Point*, specifying the destination location on the provided page, default is *pymupdf.Point(0, 0)*, or a symbolic (indirect) name. If an indirect name is specified, *page = -1* is required and the name must be defined in the PDF in order for this to work. Required for *LINK\_GOTO* and *LINK\_GOTOR*, else ignored.
- *file*: a string specifying the destination file. Required for *LINK\_GOTOR* and *LINK\_LAUNCH*, else ignored.
- *uri*: a string specifying the destination internet resource. Required for *LINK\_URI*, else ignored. You should make sure to start this string with an unambiguous substring, that classifies the subtype of the URL, like `"http://"`, `"https://"`, `"file://"`, `"ftp://"`, `"mailto:"`, etc. Otherwise your browser will try to interpret the text and come to unwanted / unexpected conclusions about the intended URL type.
- [`xref`](glossary.html#xref "xref"): an integer specifying the PDF [`xref`](glossary.html#xref "xref") of the link object. Do not change this entry in any way. Required for link deletion and update, otherwise ignored. For non-PDF documents, this entry contains *-1*. It is also *-1* for **all** entries in the *get\_links()* list, if **any** of the links is not supported by MuPDF - see [Notes on Supporting Links](#notes-on-supporting-links).

## Notes on Supporting Links

MuPDF’s support for links has changed in **v1.10a**. These changes affect link types [`LINK_GOTO`](vars.html#LINK_GOTO "LINK_GOTO") and [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR").

### Reading (pertains to method *get\_links()* and the *first\_link* property chain)

If MuPDF detects a link to another file, it will supply either a *LINK\_GOTOR* or a *LINK\_LAUNCH* link kind. In case of *LINK\_GOTOR* destination details may either be given as page number (eventually including position information), or as an indirect destination.

If an indirect destination is given, then this is indicated by *page = -1*, and *link.dest.dest* will contain this name. The dictionaries in the *get\_links()* list will contain this information as the *to* value.

**Internal links are always** of kind *LINK\_GOTO*. If an internal link specifies an indirect destination, it **will always be resolved** and the resulting direct destination will be returned. Names are **never returned for internal links**, and undefined destinations will cause the link to be ignored.

### Writing

PyMuPDF writes (updates, inserts) links by constructing and writing the appropriate PDF object **source**. This makes it possible to specify indirect destinations for *LINK\_GOTOR* **and** *LINK\_GOTO* link kinds (pre *PDF 1.2* file formats are **not supported**).

Warning

If a *LINK\_GOTO* indirect destination specifies an undefined name, this link can later on not be found / read again with MuPDF / PyMuPDF. Other readers however **will** detect it, but flag it as erroneous.

Indirect *LINK\_GOTOR* destinations can in general of course not be checked for validity and are therefore **always accepted**.

**Example: How to insert a link pointing to another page in the same document**

1. Determine the rectangle on the current page, where the link should be placed. This may be the bbox of an image or some text.
2. Determine the target page number (“pno”, 0-based) and a [Point](point.html#point) on it, where the link should be directed to.
3. Create a dictionary `d = {"kind": pymupdf.LINK_GOTO, "page": pno, "from": bbox, "to": point}`.
4. Execute `page.insert_link(d)`.

## Homologous Methods of [Document](document.html#document) and [Page](#page)

This is an overview of homologous methods on the [Document](document.html#document) and on the [Page](#page) level.

| **Document Level** | **Page Level** |
| --- | --- |
| [`Document.get_page_fonts()`](document.html#Document.get_page_fonts "Document.get_page_fonts") | [`Page.get_fonts()`](#Page.get_fonts "Page.get_fonts") |
| [`Document.get_page_images()`](document.html#Document.get_page_images "Document.get_page_images") | [`Page.get_images()`](#Page.get_images "Page.get_images") |
| [`Document.get_page_pixmap()`](document.html#Document.get_page_pixmap "Document.get_page_pixmap") | [`Page.get_pixmap()`](#Page.get_pixmap "Page.get_pixmap") |
| [`Document.get_page_text()`](document.html#Document.get_page_text "Document.get_page_text") | [`Page.get_text()`](#Page.get_text "Page.get_text") |
| [`Document.search_page_for()`](document.html#Document.search_page_for "Document.search_page_for") | [`Page.search_for()`](#Page.search_for "Page.search_for") |

Note

Most document methods (left column) exist for convenience reasons, and are just wrappers for: *Document[pno].<page method>*. So they **load and discard the page** on each execution.

However, the first two methods work differently. They only need a page’s object definition statement - the page itself will **not** be loaded. So e.g. [`Page.get_fonts()`](#Page.get_fonts "Page.get_fonts") is a wrapper the other way round and defined as follows: `page.get_fonts` == `page.parent.get_page_fonts(page.number)`.

When calling the [Document](document.html#document) equivalent methods then the page number is sent through as a parameter, e.g.:

`Document.get_page_images(pno)` or `Document.get_page_text(pno)`

Tip

The page number parameter, `pno`, is a 0-based integer `-∞ < pno < page_count`.

## Tables and Related Classes

The [`TableFinder`](#TableFinder "TableFinder") class is returned by [`Page.find_tables()`](#Page.find_tables "Page.find_tables") and has related classes as follows:

*class* TableFinder
:   An object always returned by [`Page.find_tables()`](#Page.find_tables "Page.find_tables"). Attributes of interest:

    tables
    :   A list of [`Table`](#Table "Table") objects, each of which represents a table found on the page. An empty list if no tables are found.

    page
    :   A reference to the [Page](#page) object.

        Type:
        :   [Page](#page)

*class* Table
:   An object representing a table found on the page.

    page
    :   A back-reference to the owning page.

        Type:
        :   [Page](#page)

    cells
    :   An array of [Rect](rect.html#rect) objects for each cell in the table.

        Type:
        :   list

    header
    :   A [`TableHeader`](#TableHeader "TableHeader") object.

        Type:
        :   [`TableHeader`](#TableHeader "TableHeader")

    bbox
    :   The bounding box of all cells of the table header.

        Type:
        :   [Rect](rect.html#rect)

    row\_count
    :   Number of rows in the table.

        Type:
        :   int

    col\_count
    :   Number of columns in the table.

        Type:
        :   int

    rows
    :   An array of [`TableRow`](#TableRow "TableRow") objects for each row in the table.

        Type:
        :   list

    extract()
    :   Extracts table cell text data into a list.

        Type:
        :   list

    to\_markdown(*clean=False*, *fill\_empty=True*)
    :   Extracts table data into Markdown text format.

        Parameters:
        :   - **clean** (*bool*) – If `True` then markdown syntax is removed from cell content.
            - **fill\_empty** (*bool*) – If `True` then cell content `None` is replaced by the values above (columns) or left (rows) in an effort to approximate row and columns spans.

        Type:
        :   string

    to\_pandas()
    :   Return a [pandas DataFrame](https://pypi.org/project/pandas/) [DataFrame](https://pandas.pydata.org/docs/reference/frame.html) version of the table.

        Type:
        :   pandas DataFrame

*class* TableHeader
:   Dedicated class for table headers.

    bbox
    :   The bounding box of the union of cells belonging to the table header, given as a tuple (x0, y0, x1, y1). This rectangle contains all table header cells.

        Type:
        :   [Rect](rect.html#rect)

    cells
    :   A list of tuples for each bbox of a column header.

        Type:
        :   list

    names
    :   A list of strings with column header text.

        Type:
        :   list

    external
    :   A boolean indicating whether the header is outside the table cells.

        Type:
        :   `bool`

*class* TableRow
:   Dedicated class for table rows.

---

Footnotes

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.