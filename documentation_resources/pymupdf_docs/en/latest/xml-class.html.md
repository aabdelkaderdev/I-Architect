<!-- Source: https://pymupdf.readthedocs.io/en/latest/xml-class.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Xml

- New in v1.21.0

This represents an HTML or an XML node. It is a helper class intended to access the DOM (Document Object Model) content of a [Story](story-class.html#story) object.

There is no need to ever directly construct an [Xml](#xml) object: after creating a [Story](story-class.html#story), simply take [`Story.body`](story-class.html#Story.body "Story.body") – which is an Xml node – and use it to navigate your way through the story’s DOM.

| **Method / Attribute** | **Description** |
| --- | --- |
| [`add_bullet_list()`](#Xml.add_bullet_list "Xml.add_bullet_list") | Add a *ul* tag - bulleted list, context manager. |
| [`add_codeblock()`](#Xml.add_codeblock "Xml.add_codeblock") | Add a *pre* tag, context manager. |
| [`add_description_list()`](#Xml.add_description_list "Xml.add_description_list") | Add a *dl* tag, context manager. |
| [`add_division()`](#Xml.add_division "Xml.add_division") | add a *div* tag (renamed from “section”), context manager. |
| [`add_header()`](#Xml.add_header "Xml.add_header") | Add a header tag (one of *h1* to *h6*), context manager. |
| [`add_horizontal_line()`](#Xml.add_horizontal_line "Xml.add_horizontal_line") | Add a *hr* tag. |
| [`add_image()`](#Xml.add_image "Xml.add_image") | Add a *img* tag. |
| [`add_link()`](#Xml.add_link "Xml.add_link") | Add a *a* tag. |
| [`add_number_list()`](#Xml.add_number_list "Xml.add_number_list") | Add a *ol* tag, context manager. |
| [`add_paragraph()`](#Xml.add_paragraph "Xml.add_paragraph") | Add a *p* tag. |
| [`add_span()`](#Xml.add_span "Xml.add_span") | Add a *span* tag, context manager. |
| [`add_subscript()`](#Xml.add_subscript "Xml.add_subscript") | Add subscript text(*sub* tag) - inline element, treated like text. |
| [`add_superscript()`](#Xml.add_superscript "Xml.add_superscript") | Add subscript text (*sup* tag) - inline element, treated like text. |
| [`add_code()`](#Xml.add_code "Xml.add_code") | Add code text (*code* tag) - inline element, treated like text. |
| [`add_var()`](#Xml.add_var "Xml.add_var") | Add code text (*code* tag) - inline element, treated like text. |
| [`add_samp()`](#Xml.add_samp "Xml.add_samp") | Add code text (*code* tag) - inline element, treated like text. |
| [`add_kbd()`](#Xml.add_kbd "Xml.add_kbd") | Add code text (*code* tag) - inline element, treated like text. |
| [`add_text()`](#Xml.add_text "Xml.add_text") | Add a text string. Line breaks `\n` are honored as *br* tags. |
| [`append_child()`](#Xml.append_child "Xml.append_child") | Append a child node. |
| [`clone()`](#Xml.clone "Xml.clone") | Make a copy if this node. |
| [`create_element()`](#Xml.create_element "Xml.create_element") | Make a new node with a given tag name. |
| [`create_text_node()`](#Xml.create_text_node "Xml.create_text_node") | Create direct text for the current node. |
| [`find()`](#Xml.find "Xml.find") | Find a sub-node with given properties. |
| [`find_next()`](#Xml.find_next "Xml.find_next") | Repeat previous “find” with the same criteria. |
| [`insert_after()`](#Xml.insert_after "Xml.insert_after") | Insert an element after current node. |
| [`insert_before()`](#Xml.insert_before "Xml.insert_before") | Insert an element before current node. |
| [`remove()`](#Xml.remove "Xml.remove") | Remove this node. |
| [`set_align()`](#Xml.set_align "Xml.set_align") | Set the alignment using a CSS style spec. Only works for block-level tags. |
| [`set_attribute()`](#Xml.set_attribute "Xml.set_attribute") | Set an arbitrary key to some value (which may be empty). |
| [`set_bgcolor()`](#Xml.set_bgcolor "Xml.set_bgcolor") | Set the background color. Only works for block-level tags. |
| [`set_bold()`](#Xml.set_bold "Xml.set_bold") | Set bold on or off or to some string value. |
| [`set_color()`](#Xml.set_color "Xml.set_color") | Set text color. |
| [`set_columns()`](#Xml.set_columns "Xml.set_columns") | Set the number of columns. Argument may be any valid number or string. |
| [`set_font()`](#Xml.set_font "Xml.set_font") | Set the font-family, e.g. “sans-serif”. |
| [`set_fontsize()`](#Xml.set_fontsize "Xml.set_fontsize") | Set the font size. Either a float or a valid HTML/CSS string. |
| [`set_id()`](#Xml.set_id "Xml.set_id") | Set a *id*. A check for uniqueness is performed. |
| [`set_italic()`](#Xml.set_italic "Xml.set_italic") | Set italic on or off or to some string value. |
| [`set_leading()`](#Xml.set_leading "Xml.set_leading") | Set inter-block text distance (`-mupdf-leading`), only works on block-level nodes. |
| [`set_lineheight()`](#Xml.set_lineheight "Xml.set_lineheight") | Set height of a line. Float like 1.5, which sets to `1.5 * fontsize`. |
| [`set_margins()`](#Xml.set_margins "Xml.set_margins") | Set the margin(s), float or string with up to 4 values. |
| [`set_pagebreak_after()`](#Xml.set_pagebreak_after "Xml.set_pagebreak_after") | Insert a page break after this node. |
| [`set_pagebreak_before()`](#Xml.set_pagebreak_before "Xml.set_pagebreak_before") | Insert a page break before this node. |
| [`set_properties()`](#Xml.set_properties "Xml.set_properties") | Set any or all desired properties in one call. |
| [`add_style()`](#Xml.add_style "Xml.add_style") | Set (add) a “style” that is not supported by its own `set_` method. |
| [`add_class()`](#Xml.add_class "Xml.add_class") | Set (add) a “class” attribute. |
| [`set_text_indent()`](#Xml.set_text_indent "Xml.set_text_indent") | Set indentation for first textblock line. Only works for block-level nodes. |
| [`tagname`](#Xml.tagname "Xml.tagname") | Either the HTML tag name like *p* or `None` if a text node. |
| [`text`](#Xml.text "Xml.text") | Either the node’s text or `None` if a tag node. |
| [`is_text`](#Xml.is_text "Xml.is_text") | Check if the node is a text. |
| [`first_child`](#Xml.first_child "Xml.first_child") | Contains the first node one level below this one (or `None`). |
| [`last_child`](#Xml.last_child "Xml.last_child") | Contains the last node one level below this one (or `None`). |
| [`next`](annot.html#Annot.next "Annot.next") | The next node at the same level (or `None`). |
| [`previous`](#Xml.previous "Xml.previous") | The previous node at the same level. |
| [`root`](#Xml.root "Xml.root") | The top node of the DOM, which hence has the tagname *html*. |

**Class API**

*class* Xml
:   add\_bullet\_list()
    :   Add an *ul* tag - bulleted list, context manager. See [ul](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul).

    add\_codeblock()
    :   Add a *pre* tag, context manager. See [pre](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/pre).

    add\_description\_list()
    :   Add a *dl* tag, context manager. See [dl](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dl).

    add\_division()
    :   Add a *div* tag, context manager. See [div](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div).

    add\_header(*value*)
    :   Add a header tag (one of *h1* to *h6*), context manager. See [headings](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements).

        Parameters:
        :   **value** (*int*) – a value 1 - 6.

    add\_horizontal\_line()
    :   Add a *hr* tag. See [hr](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/hr).

    add\_image(*name*, *width=None*, *height=None*)
    :   Add an *img* tag. This causes the inclusion of the named image in the DOM.

        Parameters:
        :   - **name** (*str*) – the filename of the image. This **must be the member name** of some entry of the [Archive](archive-class.html#archive) parameter of the [Story](story-class.html#story) constructor.
            - **width** – if provided, either an absolute (int) value, or a percentage string like “30%”. A percentage value refers to the width of the specified `where` rectangle in [`Story.place()`](story-class.html#Story.place "Story.place"). If this value is provided and [`height`](irect.html#IRect.height "IRect.height") is omitted, the image will be included keeping its aspect ratio.
            - **height** – if provided, either an absolute (int) value, or a percentage string like “30%”. A percentage value refers to the height of the specified `where` rectangle in [`Story.place()`](story-class.html#Story.place "Story.place"). If this value is provided and [`width`](irect.html#IRect.width "IRect.width") is omitted, the image’s aspect ratio will be honored.

    add\_link(*href*, *text=None*)
    :   Add an *a* tag - inline element, treated like text.

        Parameters:
        :   - **href** (*str*) – the URL target.
            - **text** (*str*) – the text to display. If omitted, the `href` text is shown instead.

    add\_number\_list()
    :   Add an *ol* tag, context manager.

    add\_paragraph()
    :   Add a *p* tag, context manager.

    add\_span()
    :   Add a *span* tag, context manager. See [span](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/span)

    add\_subscript(*text*)
    :   Add “subscript” text(*sub* tag) - inline element, treated like text.

    add\_superscript(*text*)
    :   Add “superscript” text (*sup* tag) - inline element, treated like text.

    add\_code(*text*)
    :   Add “code” text (*code* tag) - inline element, treated like text.

    add\_var(*text*)
    :   Add “variable” text (*var* tag) - inline element, treated like text.

    add\_samp(*text*)
    :   Add “sample output” text (*samp* tag) - inline element, treated like text.

    add\_kbd(*text*)
    :   Add “keyboard input” text (*kbd* tag) - inline element, treated like text.

    add\_text(*text*)
    :   Add a text string. Line breaks `\n` are honored as *br* tags.

    set\_align(*value*)
    :   Set the text alignment. Only works for block-level tags.

        Parameters:
        :   **value** – either one of the [Text Alignment](vars.html#textalign) or the [text-align](https://developer.mozilla.org/en-US/docs/Web/CSS/text-align) values.

    set\_attribute(*key*, *value=None*)
    :   Set an arbitrary key to some value (which may be empty).

        Parameters:
        :   - **key** (*str*) – the name of the attribute.
            - **value** (*str*) – the (optional) value of the attribute.

    get\_attributes()
    :   Retrieve all attributes of the current nodes as a dictionary.

        Returns:
        :   a dictionary with the attributes and their values of the node.

    get\_attribute\_value(*key*)
    :   Get the attribute value of `key`.

        Parameters:
        :   **key** (*str*) – the name of the attribute.

        Returns:
        :   a string with the value of `key`.

    remove\_attribute(*key*)
    :   Remove the attribute `key` from the node.

        Parameters:
        :   **key** (*str*) – the name of the attribute.

    set\_bgcolor(*value*)
    :   Set the background color. Only works for block-level tags.

        Parameters:
        :   **value** – either an RGB value like (255, 0, 0) (for “red”) or a valid [background-color](https://developer.mozilla.org/en-US/docs/Web/CSS/background-color) value.

    set\_bold(*value*)
    :   Set bold on or off or to some string value.

        Parameters:
        :   **value** – `True`, `False` or a valid [font-weight](https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight) value.

    set\_color(*value*)
    :   Set the color of the text following.

        Parameters:
        :   **value** – either an RGB value like (255, 0, 0) (for “red”) or a valid [color](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) value.

    set\_columns(*value*)
    :   Set the number of columns.

        Parameters:
        :   **value** – a valid [columns](https://developer.mozilla.org/en-US/docs/Web/CSS/columns) value.

        Note

        Currently ignored - supported in a future MuPDF version.

    set\_font(*value*)
    :   Set the font-family.

        Parameters:
        :   **value** (*str*) – e.g. “sans-serif”.

    set\_fontsize(*value*)
    :   Set the font size for text following.

        Parameters:
        :   **value** – a float or a valid [font-size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size) value.

    set\_id(*unqid*)
    :   Set a *id*. This serves as a unique identification of the node within the DOM. Use it to easily locate the node to inspect or modify it. A check for uniqueness is performed.

        Parameters:
        :   **unqid** (*str*) – id string of the node.

    set\_italic(*value*)
    :   Set italic on or off or to some string value for the text following it.

        Parameters:
        :   **value** – `True`, `False` or some valid [font-style](https://developer.mozilla.org/en-US/docs/Web/CSS/font-style) value.

    set\_leading(*value*)
    :   Set inter-block text distance (`-mupdf-leading`), only works on block-level nodes.

        Parameters:
        :   **value** (*float*) – the distance in points to the previous block.

    set\_lineheight(*value*)
    :   Set height of a line.

        Parameters:
        :   **value** – a float like 1.5 (which sets to `1.5 * fontsize`), or some valid [line-height](https://developer.mozilla.org/en-US/docs/Web/CSS/line-height) value.

    set\_margins(*value*)
    :   Set the margin(s).

        Parameters:
        :   **value** – float or string with up to 4 values. See [CSS documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/margin).

    set\_pagebreak\_after()
    :   Insert a page break after this node.

    set\_pagebreak\_before()
    :   Insert a page break before this node.

    set\_properties(*align=None*, *bgcolor=None*, *bold=None*, *color=None*, *columns=None*, *font=None*, *fontsize=None*, *indent=None*, *italic=None*, *leading=None*, *lineheight=None*, *margins=None*, *pagebreak\_after=False*, *pagebreak\_before=False*, *unqid=None*, *cls=None*)
    :   Set any or all desired properties in one call. The meaning of argument values equal the values of the corresponding `set_` methods.

        Note

        The properties set by this method are directly attached to the node, whereas every `set_` method generates a new *span* below the current node that has the respective property. So to e.g. “globally” set some property for the *body*, this method must be used.

    add\_style(*value*)
    :   Set (add) some style attribute not supported by its own `set_` method.

        Parameters:
        :   **value** (*str*) – any valid CSS style value.

    add\_class(*value*)
    :   Set (add) some “class” attribute.

        Parameters:
        :   **value** (*str*) – the name of the class. Must have been defined in either the HTML or the CSS source of the DOM.

    set\_text\_indent(*value*)
    :   Set indentation for the first textblock line. Only works for block-level nodes.

        Parameters:
        :   **value** – a valid [text-indent](https://developer.mozilla.org/en-US/docs/Web/CSS/text-indent) value. Please note that negative values do not work.

    append\_child(*node*)
    :   Append a child node. This is a low-level method used by other methods like [`Xml.add_paragraph()`](#Xml.add_paragraph "Xml.add_paragraph").

        Parameters:
        :   **node** – the [Xml](#xml) node to append.

    create\_text\_node(*text*)
    :   Create direct text for the current node.

        Parameters:
        :   **text** (*str*) – the text to append.

        Return type:
        :   [Xml](#xml)

        Returns:
        :   the created element.

    create\_element(*tag*)
    :   Create a new node with a given tag. This a low-level method used by other methods like [`Xml.add_paragraph()`](#Xml.add_paragraph "Xml.add_paragraph").

        Parameters:
        :   **tag** (*str*) – the element tag.

        Return type:
        :   [Xml](#xml)

        Returns:
        :   the created element. To actually bind it to the DOM, use [`Xml.append_child()`](#Xml.append_child "Xml.append_child").

    insert\_before(*elem*)
    :   Insert the given element `elem` before this node.

        Parameters:
        :   **elem** – some [Xml](#xml) element.

    insert\_after(*elem*)
    :   Insert the given element `elem` after this node.

        Parameters:
        :   **elem** – some [Xml](#xml) element.

    clone()
    :   Make a copy of this node, which then may be appended (using [`Xml.append_child()`](#Xml.append_child "Xml.append_child")) or inserted (using one of [`Xml.insert_before()`](#Xml.insert_before "Xml.insert_before"), [`Xml.insert_after()`](#Xml.insert_after "Xml.insert_after")) in this DOM.

        Returns:
        :   the clone ([Xml](#xml)) of the current node.

    remove()
    :   Remove this node from the DOM.

    debug()
    :   For debugging purposes, print this node’s structure in a simplified form.

    find(*tag*, *att*, *match*)
    :   Under the current node, find the first node with the given `tag`, attribute `att` and value `match`.

        Parameters:
        :   - **tag** (*str*) – restrict search to this tag. May be `None` for unrestricted searches.
            - **att** (*str*) – check this attribute. May be `None`.
            - **match** (*str*) – the desired attribute value to match. May be `None`.

        Return type:
        :   [Xml](#xml).

        Returns:
        :   `None` if nothing found, otherwise the first matching node.

    find\_next(*tag*, *att*, *match*)
    :   Continue a previous [`Xml.find()`](#Xml.find "Xml.find") (or [`find_next()`](#Xml.find_next "Xml.find_next")) with the same values.

        Return type:
        :   [Xml](#xml).

        Returns:
        :   `None` if none more found, otherwise the next matching node.

    tagname
    :   Either the HTML tag name like *p* or `None` if a text node.

    text
    :   Either the node’s text or `None` if a tag node.

    is\_text
    :   Check if a text node.

    first\_child
    :   Contains the first node one level below this one (or `None`).

    last\_child
    :   Contains the last node one level below this one (or `None`).

    next
    :   The next node at the same level (or `None`).

    previous
    :   The previous node at the same level.

    root
    :   The top node of the DOM, which hence has the tagname *html*.

## Setting Text properties

In HTML tags can be nested such that innermost text **inherits properties** from the tag enveloping its parent tag. For example `<p>`.

To achieve the same effect, methods like [`Xml.set_bold()`](#Xml.set_bold "Xml.set_bold") and [`Xml.set_italic()`](#Xml.set_italic "Xml.set_italic") each open a temporary *span* with the desired property underneath the current node.

In addition, these methods return there parent node, so they can be concatenated with each other.

## Context Manager support

The standard way to add nodes to a DOM is this:

```
body = story.body
para = body.add_paragraph()  # add a paragraph
para.set_bold()  # text that follows will be bold
para.add_text("some bold text")
para.set_italic()  # text that follows will additionally be italic
para.add_txt("this is bold and italic")
para.set_italic(False).set_bold(False)  # all following text will be regular
para.add_text("regular text")
```

Methods that are flagged as “context managers” can conveniently be used in this way:

```
body = story.body
with body.add_paragraph() as para:
   para.set_bold().add_text("some bold text")
   para.set_italic().add_text("this is bold and italic")
   para.set_italic(False).set_bold(False).add_text("regular text")
   para.add_text("more regular text")
```

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.