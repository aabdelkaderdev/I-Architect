<!-- Source: https://pymupdf.readthedocs.io/en/latest/document.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Document

This class represents a document. It can be constructed from a file or from memory.

There exists the alias *open* for this class, i.e. `pymupdf.Document(...)` and `pymupdf.open(...)` do exactly the same thing.

For details on **embedded files** refer to Appendix 3.

Note

Starting with v1.17.0, a new page addressing mechanism for **EPUB files only** is supported. This document type is internally organized in chapters such that pages can most efficiently be found by their so-called “location”. The location is a tuple *(chapter, pno)* consisting of the chapter number and the page number **in that chapter**. Both numbers are zero-based.

While it is still possible to locate a page via its (absolute) number, doing so may mean that the complete EPUB document must be laid out before the page can be addressed. This may have a significant performance impact if the document is very large. Using the page’s *(chapter, pno)* prevents this from happening.

To maintain a consistent API, PyMuPDF supports the page *location* syntax for **all file types** – documents without this feature simply have just one chapter. [`Document.load_page()`](#Document.load_page "Document.load_page") and the equivalent index access now also support a *location* argument.

There are a number of methods for converting between page numbers and locations, for determining the chapter count, the page count per chapter, for computing the next and the previous locations, and the last page location of a document.

| **Method / Attribute** | **Short Description** |
| --- | --- |
| [`Document.add_layer()`](#Document.add_layer "Document.add_layer") | PDF only: make new optional content configuration |
| [`Document.add_ocg()`](#Document.add_ocg "Document.add_ocg") | PDF only: add new optional content group |
| [`Document.authenticate()`](#Document.authenticate "Document.authenticate") | gain access to an encrypted document |
| [`Document.bake()`](#Document.bake "Document.bake") | PDF only: make annotations / fields permanent content |
| [`Document.can_save_incrementally()`](#Document.can_save_incrementally "Document.can_save_incrementally") | check if incremental save is possible |
| [`Document.chapter_page_count()`](#Document.chapter_page_count "Document.chapter_page_count") | number of pages in chapter |
| [`Document.close()`](#Document.close "Document.close") | close the document |
| [`Document.convert_to_pdf()`](#Document.convert_to_pdf "Document.convert_to_pdf") | write a PDF version to memory |
| [`Document.copy_page()`](#Document.copy_page "Document.copy_page") | PDF only: copy a page reference |
| [`Document.del_toc_item()`](#Document.del_toc_item "Document.del_toc_item") | PDF only: remove a single TOC item |
| [`Document.delete_page()`](#Document.delete_page "Document.delete_page") | PDF only: delete a page |
| [`Document.delete_pages()`](#Document.delete_pages "Document.delete_pages") | PDF only: delete multiple pages |
| [`Document.embfile_add()`](#Document.embfile_add "Document.embfile_add") | PDF only: add a new embedded file from buffer |
| [`Document.embfile_count()`](#Document.embfile_count "Document.embfile_count") | PDF only: number of embedded files |
| [`Document.embfile_del()`](#Document.embfile_del "Document.embfile_del") | PDF only: delete an embedded file entry |
| [`Document.embfile_get()`](#Document.embfile_get "Document.embfile_get") | PDF only: extract an embedded file buffer |
| [`Document.embfile_info()`](#Document.embfile_info "Document.embfile_info") | PDF only: metadata of an embedded file |
| [`Document.embfile_names()`](#Document.embfile_names "Document.embfile_names") | PDF only: list of embedded files |
| [`Document.embfile_upd()`](#Document.embfile_upd "Document.embfile_upd") | PDF only: change an embedded file |
| [`Document.extract_font()`](#Document.extract_font "Document.extract_font") | PDF only: extract a font by [`xref`](glossary.html#xref "xref") |
| [`Document.extract_image()`](#Document.extract_image "Document.extract_image") | PDF only: extract an embedded image by [`xref`](glossary.html#xref "xref") |
| [`Document.ez_save()`](#Document.ez_save "Document.ez_save") | PDF only: [`Document.save()`](#Document.save "Document.save") with different defaults |
| [`Document.find_bookmark()`](#Document.find_bookmark "Document.find_bookmark") | retrieve page location after laid out document |
| [`Document.fullcopy_page()`](#Document.fullcopy_page "Document.fullcopy_page") | PDF only: duplicate a page |
| [`Document.get_layer()`](#Document.get_layer "Document.get_layer") | PDF only: lists of OCGs in ON, OFF, RBGroups |
| [`Document.get_layers()`](#Document.get_layers "Document.get_layers") | PDF only: list of optional content configurations |
| [`Document.get_oc()`](#Document.get_oc "Document.get_oc") | PDF only: get OCG /OCMD xref of image / form xobject |
| [`Document.get_ocgs()`](#Document.get_ocgs "Document.get_ocgs") | PDF only: info on all optional content groups |
| [`Document.get_ocmd()`](#Document.get_ocmd "Document.get_ocmd") | PDF only: retrieve definition of an [`OCMD`](glossary.html#OCMD "OCMD") |
| [`Document.get_page_fonts()`](#Document.get_page_fonts "Document.get_page_fonts") | PDF only: list of fonts referenced by a page |
| [`Document.get_page_images()`](#Document.get_page_images "Document.get_page_images") | PDF only: list of images referenced by a page |
| [`Document.get_page_labels()`](#Document.get_page_labels "Document.get_page_labels") | PDF only: list of page label definitions |
| [`Document.get_page_numbers()`](#Document.get_page_numbers "Document.get_page_numbers") | PDF only: get page numbers having a given label |
| [`Document.get_page_pixmap()`](#Document.get_page_pixmap "Document.get_page_pixmap") | create a pixmap of a page by page number |
| [`Document.get_page_text()`](#Document.get_page_text "Document.get_page_text") | extract the text of a page by page number |
| [`Document.get_page_xobjects()`](#Document.get_page_xobjects "Document.get_page_xobjects") | PDF only: list of XObjects referenced by a page |
| [`Document.get_sigflags()`](#Document.get_sigflags "Document.get_sigflags") | PDF only: determine signature state |
| [`Document.get_toc()`](#Document.get_toc "Document.get_toc") | extract the table of contents |
| [`Document.get_xml_metadata()`](#Document.get_xml_metadata "Document.get_xml_metadata") | PDF only: read the XML metadata |
| [`Document.has_annots()`](#Document.has_annots "Document.has_annots") | PDF only: check if PDF contains any annots |
| [`Document.has_links()`](#Document.has_links "Document.has_links") | PDF only: check if PDF contains any links |
| [`Document.insert_page()`](#Document.insert_page "Document.insert_page") | PDF only: insert a new page |
| [`Document.insert_pdf()`](#Document.insert_pdf "Document.insert_pdf") | PDF only: insert pages from another PDF |
| [`Document.insert_file()`](#Document.insert_file "Document.insert_file") | PDF only: insert pages from arbitrary document |
| [`Document.journal_can_do()`](#Document.journal_can_do "Document.journal_can_do") | PDF only: which journal actions are possible |
| [`Document.journal_enable()`](#Document.journal_enable "Document.journal_enable") | PDF only: enables journalling for the document |
| [`Document.journal_load()`](#Document.journal_load "Document.journal_load") | PDF only: load journal from a file |
| [`Document.journal_op_name()`](#Document.journal_op_name "Document.journal_op_name") | PDF only: return name of a journalling step |
| [`Document.journal_position()`](#Document.journal_position "Document.journal_position") | PDF only: return journalling status |
| [`Document.journal_redo()`](#Document.journal_redo "Document.journal_redo") | PDF only: redo current operation |
| [`Document.journal_save()`](#Document.journal_save "Document.journal_save") | PDF only: save journal to a file |
| [`Document.journal_start_op()`](#Document.journal_start_op "Document.journal_start_op") | PDF only: start an “operation” giving it a name |
| [`Document.journal_stop_op()`](#Document.journal_stop_op "Document.journal_stop_op") | PDF only: end current operation |
| [`Document.journal_undo()`](#Document.journal_undo "Document.journal_undo") | PDF only: undo current operation |
| [`Document.layer_ui_configs()`](#Document.layer_ui_configs "Document.layer_ui_configs") | PDF only: list of optional content intents |
| [`Document.layout()`](#Document.layout "Document.layout") | re-paginate the document (if supported) |
| [`Document.load_page()`](#Document.load_page "Document.load_page") | read a page |
| [`Document.make_bookmark()`](#Document.make_bookmark "Document.make_bookmark") | create a page pointer in reflowable documents |
| [`Document.move_page()`](#Document.move_page "Document.move_page") | PDF only: move a page to different location in doc |
| [`Document.need_appearances()`](#Document.need_appearances "Document.need_appearances") | PDF only: get/set `/NeedAppearances` property |
| [`Document.new_page()`](#Document.new_page "Document.new_page") | PDF only: insert a new empty page |
| [`Document.next_location()`](#Document.next_location "Document.next_location") | return (chapter, pno) of following page |
| [`Document.outline_xref()`](#Document.outline_xref "Document.outline_xref") | PDF only: [`xref`](glossary.html#xref "xref") a TOC item |
| [`Document.page_cropbox()`](#Document.page_cropbox "Document.page_cropbox") | PDF only: the unrotated page rectangle |
| [`Document.page_xref()`](#Document.page_xref "Document.page_xref") | PDF only: [`xref`](glossary.html#xref "xref") of a page number |
| [`Document.pages()`](#Document.pages "Document.pages") | iterator over a page range |
| [`Document.pdf_catalog()`](#Document.pdf_catalog "Document.pdf_catalog") | PDF only: [`xref`](glossary.html#xref "xref") of catalog (root) |
| [`Document.pdf_trailer()`](#Document.pdf_trailer "Document.pdf_trailer") | PDF only: trailer source |
| [`Document.prev_location()`](#Document.prev_location "Document.prev_location") | return (chapter, pno) of preceding page |
| [`Document.rewrite_images()`](#Document.rewrite_images "Document.rewrite_images") | PDF only: rewrite / extra compression for images |
| [`Document.recolor()`](#Document.recolor "Document.recolor") | PDF only: execute [`Page.recolor()`](page.html#Page.recolor "Page.recolor") for all pages |
| [`Document.reload_page()`](#Document.reload_page "Document.reload_page") | PDF only: provide a new copy of a page |
| [`Document.resolve_names()`](#Document.resolve_names "Document.resolve_names") | PDF only: Convert destination names into a Python dict |
| [`Document.save()`](#Document.save "Document.save") | PDF only: save the document |
| [`Document.saveIncr()`](#Document.saveIncr "Document.saveIncr") | PDF only: save the document incrementally |
| [`Document.scrub()`](#Document.scrub "Document.scrub") | PDF only: remove sensitive data |
| [`Document.search_page_for()`](#Document.search_page_for "Document.search_page_for") | search for a string on a page |
| [`Document.select()`](#Document.select "Document.select") | PDF only: select a subset of pages |
| [`Document.set_layer_ui_config()`](#Document.set_layer_ui_config "Document.set_layer_ui_config") | PDF only: set OCG visibility temporarily |
| [`Document.set_layer()`](#Document.set_layer "Document.set_layer") | PDF only: mass changing OCG states |
| [`Document.set_markinfo()`](#Document.set_markinfo "Document.set_markinfo") | PDF only: set the MarkInfo values |
| [`Document.set_metadata()`](#Document.set_metadata "Document.set_metadata") | PDF only: set the metadata |
| [`Document.set_oc()`](#Document.set_oc "Document.set_oc") | PDF only: attach OCG/OCMD to image / form xobject |
| [`Document.set_ocmd()`](#Document.set_ocmd "Document.set_ocmd") | PDF only: create or update an [`OCMD`](glossary.html#OCMD "OCMD") |
| [`Document.set_page_labels()`](#Document.set_page_labels "Document.set_page_labels") | PDF only: add/update page label definitions |
| [`Document.set_pagemode()`](#Document.set_pagemode "Document.set_pagemode") | PDF only: set the PageMode |
| [`Document.set_pagelayout()`](#Document.set_pagelayout "Document.set_pagelayout") | PDF only: set the PageLayout |
| [`Document.set_toc_item()`](#Document.set_toc_item "Document.set_toc_item") | PDF only: change a single TOC item |
| [`Document.set_toc()`](#Document.set_toc "Document.set_toc") | PDF only: set the table of contents (TOC) |
| [`Document.set_xml_metadata()`](#Document.set_xml_metadata "Document.set_xml_metadata") | PDF only: create or update document XML metadata |
| [`Document.subset_fonts()`](#Document.subset_fonts "Document.subset_fonts") | PDF only: create font subsets |
| [`Document.switch_layer()`](#Document.switch_layer "Document.switch_layer") | PDF only: activate OC configuration |
| [`Document.tobytes()`](#Document.tobytes "Document.tobytes") | PDF only: writes document to memory |
| [`Document.xref_copy()`](#Document.xref_copy "Document.xref_copy") | PDF only: copy a PDF dictionary to another [`xref`](glossary.html#xref "xref") |
| [`Document.xref_get_key()`](#Document.xref_get_key "Document.xref_get_key") | PDF only: get the value of a dictionary key |
| [`Document.xref_get_keys()`](#Document.xref_get_keys "Document.xref_get_keys") | PDF only: list the keys of object at [`xref`](glossary.html#xref "xref") |
| [`Document.xref_object()`](#Document.xref_object "Document.xref_object") | PDF only: get the definition source of [`xref`](glossary.html#xref "xref") |
| [`Document.xref_set_key()`](#Document.xref_set_key "Document.xref_set_key") | PDF only: set the value of a dictionary key |
| [`Document.xref_stream_raw()`](#Document.xref_stream_raw "Document.xref_stream_raw") | PDF only: raw stream source at [`xref`](glossary.html#xref "xref") |
| [`Document.xref_xml_metadata()`](#Document.xref_xml_metadata "Document.xref_xml_metadata") | PDF only: [`xref`](glossary.html#xref "xref") of XML metadata |
| [`Document.chapter_count`](#Document.chapter_count "Document.chapter_count") | number of chapters |
| [`Document.FormFonts`](#Document.FormFonts "Document.FormFonts") | PDF only: list of global widget fonts |
| [`Document.is_closed`](#Document.is_closed "Document.is_closed") | has document been closed? |
| [`Document.is_dirty`](#Document.is_dirty "Document.is_dirty") | PDF only: has document been changed yet? |
| [`Document.is_encrypted`](#Document.is_encrypted "Document.is_encrypted") | document (still) encrypted? |
| [`Document.is_fast_webaccess`](#Document.is_fast_webaccess "Document.is_fast_webaccess") | is PDF linearized? |
| [`Document.is_form_pdf`](#Document.is_form_pdf "Document.is_form_pdf") | is this a Form PDF? |
| [`Document.is_pdf`](#Document.is_pdf "Document.is_pdf") | is this a PDF? |
| [`Document.is_reflowable`](#Document.is_reflowable "Document.is_reflowable") | is this a reflowable document? |
| [`Document.is_repaired`](#Document.is_repaired "Document.is_repaired") | PDF only: has this PDF been repaired during open? |
| [`Document.last_location`](#Document.last_location "Document.last_location") | (chapter, pno) of last page |
| [`Document.metadata`](#Document.metadata "Document.metadata") | metadata |
| [`Document.markinfo`](#Document.markinfo "Document.markinfo") | PDF MarkInfo value |
| [`Document.name`](#Document.name "Document.name") | filename of document |
| [`Document.needs_pass`](#Document.needs_pass "Document.needs_pass") | require password to access data? |
| [`Document.outline`](#Document.outline "Document.outline") | first [Outline](outline.html#outline) item |
| [`Document.page_count`](#Document.page_count "Document.page_count") | number of pages |
| [`Document.permissions`](#Document.permissions "Document.permissions") | permissions to access the document |
| [`Document.pagemode`](#Document.pagemode "Document.pagemode") | PDF PageMode value |
| [`Document.pagelayout`](#Document.pagelayout "Document.pagelayout") | PDF PageLayout value |
| [`Document.version_count`](#Document.version_count "Document.version_count") | PDF count of versions |

**Class API**

*class* Document
:   \_\_init\_\_(*self*, *filename=None*, *stream=None*, *\**, *filetype=None*, *rect=None*, *width=0*, *height=0*, *fontsize=11*)
    :   Create a `Document` object.

        - With default parameters, a **new empty PDF** document will be created.
        - If `stream` is given, then the document is created from memory.
        - If `stream` is `None`, then a document is created from the file given by `filename`.

        Parameters:
        :   - **filename** (*str**,**pathlib*) – A UTF-8 string or `pathlib.Path` object containing a file path. The document type is always determined from the file content. The `filetype` parameter is ignored, except when content inspection was unsuccessful. This is regularly the case for plain text types like “txt”, “html”, “xml” etc. with a wrong or missing file extension.
            - **stream** (*bytes**,**bytearray**,**BytesIO*) – A memory area containing file data. The document type is always detected from the data content. The `filetype` parameter is ignored, except when content inspection was unsuccessful. This is regularly the case for plain text types like “txt”, “html”, “xml” etc.
            - **filetype** (*str*) – A string specifying the type of document. This is only ever needed when file content inspection fails. Text types like “txt”, “html”, “xml” etc. cannot be disambiguated by their content. When such files are provided in memory or being provided with the wrong file extension, this parameter **must** be used.
            - **rect** (*rect\_like*) – a rectangle specifying the desired page size. This parameter is only meaningful for documents with a variable page layout (“reflowable” documents), like e-books or HTML, and ignored otherwise. If specified, it must be a non-empty, finite rectangle with top-left coordinates (0, 0). Together with parameter [`fontsize`](glossary.html#fontsize "fontsize"), each page will be accordingly laid out and hence also determine the number of pages.
            - **width** (*float*) – may used together with `height` as an alternative to `rect` to specify layout information.
            - **height** (*float*) – may used together with `width` as an alternative to `rect` to specify layout information.
            - **fontsize** (*float*) – the default [`fontsize`](glossary.html#fontsize "fontsize") for reflowable document types. This parameter is ignored if none of the parameters `rect` or `width` and `height` are specified. Will be used to calculate the page layout.

        Raises:
        :   - **TypeError** – if the *type* of any parameter does not conform.
            - **FileNotFoundError** – if the file / path cannot be found. Re-implemented as subclass of `RuntimeError`.
            - **EmptyFileError** – if the file / path is empty or the `bytes` object in memory has zero length. A subclass of `FileDataError` and `RuntimeError`.
            - **ValueError** – if an unknown file type is explicitly specified.
            - **FileDataError** – if the document has an invalid structure for the given type – or is no file at all (but e.g. a folder). A subclass of `RuntimeError`.

        Returns:
        :   A document object. If the document cannot be created, an exception is raised in the above sequence. Note that PyMuPDF-specific exceptions, `FileNotFoundError`, `EmptyFileError` and `FileDataError` are intercepted if you check for `RuntimeError`.

            In case of problems you can see more detail in the internal messages store: `print(pymupdf.TOOLS.mupdf_warnings())` (which will be emptied by this call, but you can also prevent this – consult [`Tools.mupdf_warnings()`](tools.html#Tools.mupdf_warnings "Tools.mupdf_warnings")).

        Overview of possible forms, note: `open` is a synonym of [Document](#document):

        ```
        >>> # from a file
        >>> doc = pymupdf.open("some.xps")
        >>> # handle wrong extension
        >>> doc = pymupdf.open("some.file", filetype="xps")  # assert expected type
        >>> doc = pymupdf.open("some.file", filetype="txt")  # treat as plain text
        >>>
        >>> # from memory
        >>> doc = pymupdf.open(stream=mem_area)  # works for any supported type
        >>> doc = pymupdf.open(stream=unknown-type, filetype="txt")  # treat as plain text
        >>>
        >>> # new empty PDF
        >>> doc = pymupdf.open()
        >>> doc = pymupdf.open(None)
        >>> doc = pymupdf.open("")
        ```

        Note

        Raster images with a wrong (but supported) file extension **are no problem**. MuPDF will determine the correct image type when file **content** is actually accessed and will process it without complaint.

        The Document class can be also be used as a **context manager**. Exiting the content manager will close the document automatically.

        ```
        >>> import pymupdf
        >>> with pymupdf.open(...) as doc:
                for page in doc: print(f"page {page.number}")
        page 0
        page 1
        page 2
        page 3
        >>> doc.is_closed
        True
        >>>
        ```

    get\_oc(*xref*)
    :   - New in v1.18.4

        Return the cross reference number of an [`OCG`](glossary.html#OCG "OCG") or [`OCMD`](glossary.html#OCMD "OCMD") attached to an image or form xobject.

        Parameters:
        :   **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of an image or form xobject. Valid such cross reference numbers are returned by [`Document.get_page_images()`](#Document.get_page_images "Document.get_page_images"), resp. [`Document.get_page_xobjects()`](#Document.get_page_xobjects "Document.get_page_xobjects"). For invalid numbers, an exception is raised.

        Return type:
        :   int

        Returns:
        :   the cross reference number of an optional contents object or zero if there is none.

    set\_oc(*xref*, *ocxref*)
    :   - New in v1.18.4

        If [`xref`](glossary.html#xref "xref") represents an image or form xobject, set or remove the cross reference number *ocxref* of an optional contents object.

        Parameters:
        :   - **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of an image or form xobject [[5]](#f5). Valid such cross reference numbers are returned by [`Document.get_page_images()`](#Document.get_page_images "Document.get_page_images"), resp. [`Document.get_page_xobjects()`](#Document.get_page_xobjects "Document.get_page_xobjects"). For invalid numbers, an exception is raised.
            - **ocxref** (*int*) – the [`xref`](glossary.html#xref "xref") number of an [`OCG`](glossary.html#OCG "OCG") / [`OCMD`](glossary.html#OCMD "OCMD"). If not zero, an invalid reference raises an exception. If zero, any OC reference is removed.

    get\_layers()
    :   - New in v1.18.3

        Show optional layer configurations. There always is a standard one, which is not included in the response.

        ```
        >>> for item in doc.get_layers(): print(item)
        {'number': 0, 'name': 'my-config', 'creator': ''}
        >>> # use 'number' as config identifier in add_ocg
        ```

    add\_layer(*name*, *creator=None*, *on=None*)
    :   - New in v1.18.3

        Add an optional content configuration. Layers serve as a collection of ON / OFF states for optional content groups and allow fast visibility switches between different views on the same document.

        Parameters:
        :   - **name** (*str*) – arbitrary name.
            - **creator** (*str*) – (optional) creating software.
            - **on** (*sequ*) – a sequence of OCG [`xref`](glossary.html#xref "xref") numbers which should be set to ON when this layer gets activated. All OCGs not listed here will be set to OFF.

    switch\_layer(*number*, *as\_default=False*)
    :   - New in v1.18.3

        Switch to a document view as defined by the optional layer’s configuration number. This is temporary, except if established as default.

        Parameters:
        :   - **number** (*int*) – config number as returned by `Document.layer_configs()`.
            - **as\_default** (*bool*) – make this the default configuration.

        Activates the ON / OFF states of OCGs as defined in the identified layer. If `as_default=True`, then additionally all layers, including the standard one, are merged and the result is written back to the standard layer, and **all optional layers are deleted**.

    add\_ocg(*name*, *config=-1*, *on=True*, *intent='View'*, *usage='Artwork'*)
    :   - New in v1.18.3

        Add an optional content group. An OCG is the most important unit of information to determine object visibility. For a PDF, in order to be regarded as having optional content, at least one OCG must exist.

        Parameters:
        :   - **name** (*str*) – arbitrary name. Will show up in supporting PDF viewers.
            - **config** (*int*) – layer configuration number. Default -1 is the standard configuration.
            - **on** (*bool*) – standard visibility status for objects pointing to this OCG.
            - **intent** (*str**,**list*) – a string or list of strings declaring the visibility intents. There are two PDF standard values to choose from: “View” and “Design”. Default is “View”. Correct **spelling is important**.
            - **usage** (*str*) – another influencer for OCG visibility. This will become part of the OCG’s `/Usage` key. There are two PDF standard values to choose from: “Artwork” and “Technical”. Default is “Artwork”. Please only change when required.

        Returns:
        :   [`xref`](glossary.html#xref "xref") of the created OCG. Use as entry for `oc` parameter in supporting objects.

        Note

        Multiple OCGs with identical parameters may be created. This will not cause problems. Garbage option 3 of [`Document.save()`](#Document.save "Document.save") will get rid of any duplicates.

    set\_ocmd(*xref=0*, *ocgs=None*, *policy='AnyOn'*, *ve=None*)
    :   - New in v1.18.4

        Create or update an [`OCMD`](glossary.html#OCMD "OCMD"), **Optional Content Membership Dictionary.**

        Parameters:
        :   - **xref** (*int*) – [`xref`](glossary.html#xref "xref") of the OCMD to be updated, or 0 for a new OCMD.
            - **ocgs** (*list*) – a sequence of [`xref`](glossary.html#xref "xref") numbers of existing [`OCG`](glossary.html#OCG "OCG") PDF objects.
            - **policy** (*str*) – one of “AnyOn” (default), “AnyOff”, “AllOn”, “AllOff” (mixed or lower case).
            - **ve** (*list*) – a “visibility expression”. This is a list of arbitrarily nested other lists – see explanation below. Use as an alternative to the combination *ocgs* / *policy* if you need to formulate more complex conditions.

        Return type:
        :   int

        Returns:
        :   [`xref`](glossary.html#xref "xref") of the OCMD. Use as `oc=xref` parameter in supporting objects, and respectively in [`Document.set_oc()`](#Document.set_oc "Document.set_oc") or [`Annot.set_oc()`](annot.html#Annot.set_oc "Annot.set_oc").

        Note

        Like an OCG, an OCMD has a visibility state ON or OFF, and it can be used like an OCG. In contrast to an OCG, the OCMD state is determined by evaluating the state of one or more OCGs via special forms of **boolean expressions.** If the expression evaluates to true, the OCMD state is ON and OFF for false.

        There are two ways to formulate OCMD visibility:

        1. Use the combination of *ocgs* and *policy*: The *policy* value is interpreted as follows:

        > - AnyOn – (default) true if at least one OCG is ON.
        > - AnyOff – true if at least one OCG is OFF.
        > - AllOn – true if all OCGs are ON.
        > - AllOff – true if all OCGs are OFF.
        >
        > Suppose you want two PDF objects be displayed exactly one at a time (if one is ON, then the other one must be OFF):
        >
        > Solution: use an **OCG** for object 1 and an **OCMD** for object 2. Create the OCMD via `set_ocmd(ocgs=[xref], policy="AllOff")`, with the [`xref`](glossary.html#xref "xref") of the OCG.

        2. Use the **visibility expression** *ve*: This is a list of two or more items. The **first item** is a logical keyword: one of the strings **“and”**, **“or”**, or **“not”**. The **second** and all subsequent items must either be an integer or another list. An integer must be the [`xref`](glossary.html#xref "xref") number of an OCG. A list must again have at least two items starting with one of the boolean keywords. This syntax is a bit awkward, but quite powerful:

        > - Each list must start with a logical keyword.
        > - If the keyword is a **“not”**, then the list must have exactly two items. If it is **“and”** or **“or”**, any number of other items may follow.
        > - Items following the logical keyword may be either integers or again a list. An *integer* must be the xref of an OCG. A *list* must conform to the previous rules.
        >
        > **Examples:**
        >
        > - `set_ocmd(ve=["or", 4, ["not", 5], ["and", 6, 7]])`. This delivers ON if the following is true: **“4 is ON, or 5 is OFF, or 6 and 7 are both ON”**.
        > - `set_ocmd(ve=["not", xref])`. This has the same effect as the OCMD example created under 1.
        >
        > For more details and examples see page 224 of [Adobe PDF References](app3.html#adobemanual). Also do have a look at example scripts [here](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/optional-content).
        >
        > Visibility expressions, `/VE`, are part of PDF specification version 1.6. So not all PDF viewers / readers may already support this feature and hence will react in some standard way for those cases.

    get\_ocmd(*xref*)
    :   - New in v1.18.4

        Retrieve the definition of an [`OCMD`](glossary.html#OCMD "OCMD").

        Parameters:
        :   **xref** (*int*) – the [`xref`](glossary.html#xref "xref") of the OCMD.

        Return type:
        :   dict

        Returns:
        :   a dictionary with the keys [`xref`](glossary.html#xref "xref"), *ocgs*, *policy* and *ve*.

    get\_layer(*config=-1*)
    :   - New in v1.18.3

        List of optional content groups by status in the specified configuration. This is a dictionary with lists of cross reference numbers for OCGs that occur in the arrays `/ON`, `/OFF` or in some radio button group (`/RBGroups`).

        Parameters:
        :   **config** (*int*) – the configuration layer (default is the standard config layer).

        ```
        >>> pprint(doc.get_layer())
        {'off': [8, 9, 10], 'on': [5, 6, 7], 'rbgroups': [[7, 10]]}
        >>>
        ```

    set\_layer(*config*, *\**, *on=None*, *off=None*, *basestate=None*, *rbgroups=None*, *locked=None*)
    :   - New in v1.18.3
        - Changed in v1.22.5: Support list of *locked* OCGs.

        Mass status changes of optional content groups. **Permanently** sets the status of OCGs.

        Parameters:
        :   - **config** (*int*) – desired configuration layer, choose -1 for the default one.
            - **on** (*list*) – list of [`xref`](glossary.html#xref "xref") of OCGs to set ON. Replaces previous values. An empty list will cause no OCG being set to ON anymore. Should be specified if `basestate="ON"` is used.
            - **off** (*list*) – list of [`xref`](glossary.html#xref "xref") of OCGs to set OFF. Replaces previous values. An empty list will cause no OCG being set to OFF anymore. Should be specified if `basestate="OFF"` is used.
            - **basestate** (*str*) – state of OCGs that are not mentioned in *on* or *off*. Possible values are “ON”, “OFF” or “Unchanged”. Upper / lower case possible.
            - **rbgroups** (*list*) – a list of lists. Replaces previous values. Each sublist should contain two or more OCG xrefs. OCGs in the same sublist are handled like buttons in a radio button group: setting one to ON automatically sets all other group members to OFF.
            - **locked** (*list*) – a list of OCG xref number that cannot be changed by the user interface.

        Values `None` will not change the corresponding PDF array.

        ```
        >>> doc.set_layer(-1, basestate="OFF")  # only changes the base state
        >>> pprint(doc.get_layer())
        {'basestate': 'OFF', 'off': [8, 9, 10], 'on': [5, 6, 7], 'rbgroups': [[7, 10]]}
        ```

    get\_ocgs()
    :   - New in v1.18.3

        Details of all optional content groups. This is a dictionary of dictionaries like this (key is the OCG’s [`xref`](glossary.html#xref "xref")):

        ```
        >>> pprint(doc.get_ocgs())
        {13: {'on': True,
              'intent': ['View', 'Design'],
              'name': 'Circle',
              'usage': 'Artwork'},
        14: {'on': True,
              'intent': ['View', 'Design'],
              'name': 'Square',
              'usage': 'Artwork'},
        15: {'on': False, 'intent': ['View'], 'name': 'Square', 'usage': 'Artwork'}}
        >>>
        ```

    layer\_ui\_configs()
    :   - New in v1.18.3

        Show the visibility status of optional content that is modifiable by the user interface of supporting PDF viewers.

        > - Only reports items contained in the currently selected layer configuration.
        > - The meaning of the dictionary keys is as follows:
        >   :   - *depth:* item’s nesting level in the `/Order` array
        >       - *locked:* true if cannot be changed via user interfaces
        >       - *number:* running sequence number
        >       - *on:* item state
        >       - *text:* text string or name field of the originating OCG
        >       - *type:* one of “label” (set by a text string), “checkbox” (set by a single OCG) or “radiobox” (set by a set of connected OCGs)

    set\_layer\_ui\_config(*number*, *action=0*)
    :   - New in v1.18.3

        Modify OC visibility status of content groups. This is analog to what supporting PDF viewers would offer.

        > Please note that visibility is **not** a property stored with the OCG. It is not even information necessarily present in the PDF document at all. Instead, the current visibility is **temporarily** set using the user interface of some supporting PDF consumer software. The same type of functionality is offered by this method.
        >
        > To make **permanent** changes, use [`Document.set_layer()`](#Document.set_layer "Document.set_layer").

        Parameters:
        :   - **number** (*int**,**str*) – either the sequence number of the item in list `Document.layer_configs()` or the “text” of one of these items.
            - **action** (*int*) – `PDF_OC_ON` = set on (default), `PDF_OC_TOGGLE` = toggle on/off, `PDF_OC_OFF` = set off.

    authenticate(*password*)
    :   Decrypts the document with the string *password*. If successful, document data can be accessed. For PDF documents, the “owner” and the “user” have different privileges, and hence different passwords may exist for these authorization levels. The method will automatically establish the appropriate (owner or user) access rights for the provided password.

        Parameters:
        :   **password** (*str*) – owner or user password.

        Return type:
        :   int

        Returns:
        :   a positive value if successful, zero otherwise (the string does not match either password). If positive, the indicator [`Document.is_encrypted`](#Document.is_encrypted "Document.is_encrypted") is set to `False`. **Positive** return codes carry the following information detail:

            - 1 => authenticated, but the PDF has neither owner nor user passwords.
            - 2 => authenticated with the **user** password.
            - 4 => authenticated with the **owner** password.
            - 6 => authenticated and both passwords are equal – probably a rare situation.

            Note

            The document may be protected by an owner, but **not** by a user password. Detect this situation via `doc.authenticate("") == 2`. This allows opening and reading the document without authentication, but, depending on the [`Document.permissions`](#Document.permissions "Document.permissions") value, other actions may be prohibited. PyMuPDF (like MuPDF) in this case **ignores those restrictions**. So, – in contrast to any PDF viewers – you can for example extract text and add or modify content, even if the respective permission flags `PDF_PERM_COPY`, `PDF_PERM_MODIFY`, `PDF_PERM_ANNOTATE`, etc. are set off! It is your responsibility building a legally compliant application where applicable.

    get\_page\_numbers(*label*, *only\_one=False*)
    :   - New in v 1.18.6

        PDF only: Return a list of page numbers that have the specified label – note that labels may not be unique in a PDF. This implies a sequential search through **all page numbers** to compare their labels.

        Note

        Implementation detail – pages are **not loaded** for this purpose.

        Parameters:
        :   - **label** (*str*) – the label to look for, e.g. “vii” (Roman number 7).
            - **only\_one** (*bool*) – stop after first hit. Useful e.g. if labelling is known to be unique, or there are many pages, etc. The default will check every page number.

        Return type:
        :   list

        Returns:
        :   list of page numbers that have this label. Empty if none found, no labels defined, etc.

    get\_page\_labels()
    :   - New in v1.18.7

        PDF only: Extract the list of page label definitions. Typically used for modifications before feeding it into [`Document.set_page_labels()`](#Document.set_page_labels "Document.set_page_labels").

        Returns:
        :   a list of dictionaries as defined in [`Document.set_page_labels()`](#Document.set_page_labels "Document.set_page_labels").

    set\_page\_labels(*labels*)
    :   - New in v1.18.6

        PDF only: Add or update the page label definitions of the PDF.

        Parameters:
        :   **labels** (*list*) –

            a list of dictionaries. Each dictionary defines a label building rule and a 0-based “start” page number. That start page is the first for which the label definition is valid. Each dictionary has up to 4 items and looks like `{'startpage': int, 'prefix': str, 'style': str, 'firstpagenum': int}` and has the following items.

            - `startpage`: (int) the first page number (0-based) to apply the label rule. This key **must be present**. The rule is applied to all subsequent pages until either end of document or superseded by the rule with the next larger page number.
            - `prefix`: (str) an arbitrary string to start the label with, e.g. “A-”. Default is “”.
            - `style`: (str) the numbering style. Available are “D” (decimal), “r”/”R” (Roman numbers, lower / upper case), and “a”/”A” (lower / upper case alphabetical numbering: “a” through “z”, then “aa” through “zz”, etc.). Default is “”. If “”, no numbering will take place and the pages in that range will receive the same label consisting of the `prefix` value. If prefix is also omitted, then the label will be “”.
            - `firstpagenum`: (int) start numbering with this value. Default is 1, smaller values are ignored.

        For example:

        ```
        [{'startpage': 6, 'prefix': 'A-', 'style': 'D', 'firstpagenum': 10},
         {'startpage': 10, 'prefix': '', 'style': 'D', 'firstpagenum': 1}]
        ```

        will generate the labels “A-10”, “A-11”, “A-12”, “A-13”, “1”, “2”, “3”, … for pages 6, 7 and so on until end of document. Pages 0 through 5 will have the label “”.

    make\_bookmark(*loc*)
    :   - New in v.1.17.3

        Return a page pointer in a reflowable document. After re-layouting the document, the result of this method can be used to find the new location of the page.

        Note

        Do not confuse with items of a table of contents, TOC.

        Parameters:
        :   **loc** (*list**,**tuple*) – page location. Must be a valid *(chapter, pno)*.

        Return type:
        :   pointer

        Returns:
        :   a long integer in pointer format. To be used for finding the new location of the page after re-layouting the document. Do not touch or re-assign.

    find\_bookmark(*bookmark*)
    :   - New in v.1.17.3

        Return the new page location after re-layouting the document.

        Parameters:
        :   **bookmark** (*pointer*) – created by [`Document.make_bookmark()`](#Document.make_bookmark "Document.make_bookmark").

        Return type:
        :   tuple

        Returns:
        :   the new (chapter, pno) of the page.

    chapter\_page\_count(*chapter*)
    :   - New in v.1.17.0

        Return the number of pages of a chapter.

        Parameters:
        :   **chapter** (*int*) – the 0-based chapter number.

        Return type:
        :   int

        Returns:
        :   number of pages in chapter. Relevant only for document types with chapter support (EPUB currently).

    next\_location(*page\_id*)
    :   - New in v.1.17.0

        Return the location of the following page.

        Parameters:
        :   **page\_id** (*tuple*) – the current page id. This must be a tuple *(chapter, pno)* identifying an existing page.

        Returns:
        :   The tuple of the following page, i.e. either *(chapter, pno + 1)* or *(chapter + 1, 0)*, **or** the empty tuple *()* if the argument was the last page. Relevant only for document types with chapter support (EPUB currently).

    prev\_location(*page\_id*)
    :   - New in v.1.17.0

        Return the locator of the preceding page.

        Parameters:
        :   **page\_id** (*tuple*) – the current page id. This must be a tuple *(chapter, pno)* identifying an existing page.

        Returns:
        :   The tuple of the preceding page, i.e. either *(chapter, pno - 1)* or the last page of the preceding chapter, **or** the empty tuple *()* if the argument was the first page. Relevant only for document types with chapter support (EPUB currently).

    load\_page(*page\_id=0*)
    :   - Changed in v1.17.0: For document types supporting a so-called “chapter structure” (like EPUB), pages can also be loaded via the combination of chapter number and relative page number, instead of the absolute page number. This should **significantly speed up access** for large documents.

        Create a [Page](page.html#page) object for further processing (like rendering, text searching, etc.).

        Parameters:
        :   **page\_id** (*int**,**tuple*) –

            *(Changed in v1.17.0)*

            Either a 0-based page number, or a tuple *(chapter, pno)*. For an **integer**, any `-∞ < page_id < page_count` is acceptable. While page\_id is negative, [`page_count`](#Document.page_count "Document.page_count") will be added to it. For example: to load the last page, you can use *doc.load\_page(-1)*. After this you have page.number = doc.page\_count - 1.

            For a tuple, *chapter* must be in range [`Document.chapter_count`](#Document.chapter_count "Document.chapter_count"), and *pno* must be in range [`Document.chapter_page_count()`](#Document.chapter_page_count "Document.chapter_page_count") of that chapter. Both values are 0-based. Using this notation, [`Page.number`](page.html#Page.number "Page.number") will equal the given tuple. Relevant only for document types with chapter support (EPUB currently).

        Return type:
        :   [Page](page.html#page)

    Note

    Documents also follow the Python sequence protocol with page numbers as indices: *doc.load\_page(n) == doc[n]*.

    For **absolute page numbers** only, expressions like *“for page in doc: …”* and *“for page in reversed(doc): …”* will successively yield the document’s pages. Refer to [`Document.pages()`](#Document.pages "Document.pages") which allows processing pages as with slicing.

    You can also use index notation with the new chapter-based page identification: use *page = doc[(5, 2)]* to load the third page of the sixth chapter.

    To maintain a consistent API, for document types not supporting a chapter structure (like PDFs), [`Document.chapter_count`](#Document.chapter_count "Document.chapter_count") is 1, and pages can also be loaded via tuples *(0, pno)*. See this [[3]](#f3) footnote for comments on performance improvements.

    rewrite\_images(*dpi\_threshold=None*, *dpi\_target=0*, *quality=0*, *lossy=True*, *lossless=True*, *bitonal=True*, *color=True*, *gray=True*, *set\_to\_gray=False*, *options=None*)
    :   PDF only: Walk through all images and rewrite them according to the specified parameters. This is useful for reducing file size, changing image formats, or converting color spaces.

        The typical usage is extra compression of images for significantly reducing the file size of the PDF. When setting quality and the dpi parameters to positive values and accepting defaults for the rest, the following will happen:

        - Lossy and lossless images will be rewritten as JPEG images (FZ\_RECOMPRESS\_JPEG) as far as technically possible.
        - Bitonal (monochrome) images will be rewritten in FAX format (FZ\_RECOMPRESS\_FAX).
        - Subsampling method is **FZ\_SUBSAMPLE\_AVERAGE** (see below).

        Parameters:
        :   - **dpi\_target** (*int*) – target DPI value for the resampled images. Ignored if `dpi_threshold` is `None`, otherwise must be less than `dpi_threshold` and positive.
            - **dpi\_threshold** (*int*) – If None (the default) no resampling takes place. Otherwise images with a DPI value larger than this will be resampled to `dpi_target` (which must be less than `dpi_threshold`).
            - **quality** (*int*) – desired target JPEG quality, a value between 0 and 100. 0 means no quality change, 100 means best quality.
            - **lossy** (*bool*) – include lossy image types (e.g. JPEG).
            - **lossless** (*bool*) – include lossless image types (e.g. PNG).
            - **bitonal** (*bool*) – include black-and-white images (e.g. FAX).
            - **color** (*bool*) – include colored images.
            - **gray** (*bool*) – include grayscale images.
            - **set\_to\_gray** (*bool*) – if True, the PDF will be converted to grayscale by executing [`Document.recolor()`](#Document.recolor "Document.recolor") before all image processing. Please note that this will also change text and vector graphics to grayscale – not just the images.
            - **options** (*dict*) – This parameter is intended for expert users. Except `set_to_gray`, all other parameters are ignored. It must be an object prepared in the following way: `options = pymupdf.mupdf.PdfImageRewriterOptions()`. Then attributes of this object can be set to achieve fine-grained control. Following are the adjustable attributes of the `options` object and their default (do nothing) values.

        ```
        options.bitonal_image_recompress_method = FZ_RECOMPRESS_NEVER
        options.bitonal_image_recompress_quality = None
        options.bitonal_image_subsample_method = FZ_SUBSAMPLE_AVERAGE
        options.bitonal_image_subsample_threshold = 0
        options.bitonal_image_subsample_to = 0
        options.color_lossless_image_recompress_method = FZ_RECOMPRESS_NEVER
        options.color_lossless_image_recompress_quality = None
        options.color_lossless_image_subsample_method = FZ_SUBSAMPLE_AVERAGE
        options.color_lossless_image_subsample_threshold = 0
        options.color_lossless_image_subsample_to = 0
        options.color_lossy_image_recompress_method = FZ_RECOMPRESS_NEVER
        options.color_lossy_image_recompress_quality = None
        options.color_lossy_image_subsample_method = FZ_SUBSAMPLE_AVERAGE
        options.color_lossy_image_subsample_threshold = 0
        options.color_lossy_image_subsample_to = 0
        options.gray_lossless_image_recompress_method = FZ_RECOMPRESS_NEVER
        options.gray_lossless_image_recompress_quality = None
        options.gray_lossless_image_subsample_method = FZ_SUBSAMPLE_AVERAGE
        options.gray_lossless_image_subsample_threshold = 0
        options.gray_lossless_image_subsample_to = 0
        options.gray_lossy_image_recompress_method = FZ_RECOMPRESS_NEVER
        options.gray_lossy_image_recompress_quality = None
        options.gray_lossy_image_subsample_method = FZ_SUBSAMPLE_AVERAGE
        options.gray_lossy_image_subsample_threshold = 0
        options.gray_lossy_image_subsample_to = 0
        ```

        The `*_recompress_method` attributes may be one of the values **FZ\_RECOMPRESS\_NEVER (0), FZ\_RECOMPRESS\_SAME (1), FZ\_RECOMPRESS\_LOSSLESS (2), FZ\_RECOMPRESS\_JPEG (3), FZ\_RECOMPRESS\_J2K (4), FZ\_RECOMPRESS\_FAX (5)**. Value FZ\_RECOMPRESS\_NEVER will skip this image type altogether and FZ\_RECOMPRESS\_SAME will not change the type. The other values will execute type conversions (as far as technically possible).

        The `*_quality` values are strings of integers from “0” to “100” or `None`.

        The `*_subsample_method` attributes are either **FZ\_SUBSAMPLE\_AVERAGE (0)** or **FZ\_SUBSAMPLE\_BICUBIC (1)** and refer to how a pixel value is derived from its neighboring pixels during subsampling. For some background see [this Wikipedia article about bicubic interpolation](https://en.wikipedia.org/wiki/Bicubic_interpolation).

        Attributes `*_subsample_threshold` excludes images from subsampling which have a lower DPI. Participating images will be subsampled to the DPI values given by the `*_subsample_to` values. Values of 0 mean that no subsampling will take place.

        The `*_subsample_threshold` values should be chosen notably larger than the `*_subsample_to` values to ensure that there are enough size savings. After all, every subsampling inevitably incurs quality losses.

        An example for a good choice is `threshold=100` and `to=72`.

    recolor(*components=1*)
    :   PDF only: Change the color component counts for all object types text, images and vector graphics for all pages.

        Parameters:
        :   **components** (*int*) – desired color space indicated by the number of color components: 1 = DeviceGRAY, 3 = DeviceRGB, 4 = DeviceCMYK.

        The typical use case is 1 (DeviceGRAY) which converts the PDF to grayscale.

    reload\_page(*page*)
    :   - New in v1.16.10

        PDF only: Provide a new copy of a page after finishing and updating all pending changes.

        Parameters:
        :   **page** ([Page](page.html#page)) – page object.

        Return type:
        :   [Page](page.html#page)

        Returns:
        :   a new copy of the same page. All pending updates (e.g. to annotations or widgets) will be finalized and a fresh copy of the page will be loaded.

            Note

            In a typical use case, a page [Pixmap](pixmap.html#pixmap) should be taken after annotations / widgets have been added or changed. To force all those changes being reflected in the page structure, this method re-instates a fresh copy while keeping the object hierarchy “document -> page -> annotations/widgets” intact.

    resolve\_names()
    :   PDF only: Convert destination names into a Python dict.

        Returns:
        :   A dictionary with the following layout:

            - *key*: (str) the name.
            - *value*: (dict) with the following layout:
              :   - ”page”: target page number (0-based). If no page number found -1.
                  - ”to”: (x, y) target point on page. Currently in PDF coordinates,
                    i.e. point (0,0) is the bottom-left of the page.
                  - ”zoom”: (float) the zoom factor.
                  - ”dest”: (str) only present if the target location on the page has
                    not been provided as “/XYZ” or if no page number was found.

            Examples:

            ```
            {
                '__bookmark_1': {'page': 0, 'to': (0.0, 541.0), 'zoom': 0.0},
                '__bookmark_2': {'page': 0, 'to': (0.0, 481.45), 'zoom': 0.0},
            }
            ```

            or:

            ```
            {
                '21154a7c20684ceb91f9c9adc3b677c40': {'page': -1, 'dest': '/XYZ 15.75 1486 0'},
                ...
            }
            ```

        All names found in the catalog under keys “/Dests” and “/Names/Dests” are
        included.

        - New in v1.23.6

    page\_cropbox(*pno*)
    :   - New in v1.17.7

        PDF only: Return the unrotated page rectangle – **without loading the page** (via [`Document.load_page()`](#Document.load_page "Document.load_page")). This is meant for internal purpose requiring best possible performance.

        Parameters:
        :   **pno** (*int*) – 0-based page number.

        Returns:
        :   [Rect](rect.html#rect) of the page like [`Page.rect()`](page.html#Page.rect "Page.rect"), but ignoring any rotation.

    page\_xref(*pno*)
    :   - New in v1.17.7

        PDF only: Return the [`xref`](glossary.html#xref "xref") of the page – **without loading the page** (via [`Document.load_page()`](#Document.load_page "Document.load_page")). This is meant for internal purpose requiring best possible performance.

        Parameters:
        :   **pno** (*int*) – 0-based page number.

        Returns:
        :   [`xref`](glossary.html#xref "xref") of the page like [`Page.xref`](page.html#Page.xref "Page.xref").

    pages(*start=None*[, *stop=None*[, *step=None*]])
    :   - New in v1.16.4

        A generator for a range of pages. Parameters have the same meaning as in the built-in function *range()*. Intended for expressions of the form *“for page in doc.pages(start, stop, step): …”*.

        Parameters:
        :   - **start** (*int*) – start iteration with this page number. Default is zero, allowed values are `-∞ < start < page_count`. While this is negative, [`page_count`](#Document.page_count "Document.page_count") is added **before** starting the iteration.
            - **stop** (*int*) – stop iteration at this page number. Default is [`page_count`](#Document.page_count "Document.page_count"), possible are `-∞ < stop <= page_count`. Larger values are **silently replaced** by the default. Negative values will cyclically emit the pages in reversed order. As with the built-in *range()*, this is the first page **not** returned.
            - **step** (*int*) – stepping value. Defaults are 1 if start < stop and -1 if start > stop. Zero is not allowed.

        Returns:
        :   a generator iterator over the document’s pages. Some examples:

            - ”doc.pages()” emits all pages.
            - ”doc.pages(4, 9, 2)” emits pages 4, 6, 8.
            - ”doc.pages(0, None, 2)” emits all pages with even numbers.
            - ”doc.pages(-2)” emits the last two pages.
            - ”doc.pages(-1, -1)” emits all pages in reversed order.
            - ”doc.pages(-1, -10)” always emits 10 pages in reversed order, starting with the last page – **repeatedly** if the document has less than 10 pages. So for a 4-page document the following page numbers are emitted: 3, 2, 1, 0, 3, 2, 1, 0, 3, 2, 1, 0, 3.

    convert\_to\_pdf(*from\_page=-1*, *to\_page=-1*, *rotate=0*)
    :   Create a PDF version of the current document and write it to memory. **All document types** are supported. The parameters have the same meaning as in [`insert_pdf()`](#Document.insert_pdf "Document.insert_pdf"). In essence, you can restrict the conversion to a page subset, specify page rotation, and revert page sequence.

        Parameters:
        :   - **from\_page** (*int*) – first page to copy (0-based). Default is first page.
            - **to\_page** (*int*) – last page to copy (0-based). Default is last page.
            - **rotate** (*int*) – rotation angle. Default is 0 (no rotation). Should be *n \* 90* with an integer n (not checked).

        Return type:
        :   bytes

        Returns:
        :   a Python *bytes* object containing a PDF file image. It is created by internally using `tobytes(garbage=4, deflate=True)`. See [`tobytes()`](#Document.tobytes "Document.tobytes"). You can output it directly to disk or open it as a PDF. Here are some examples:

            ```
            >>> # convert an XPS file to PDF
            >>> xps = pymupdf.open("some.xps")
            >>> pdfbytes = xps.convert_to_pdf()
            >>>
            >>> # either do this -->
            >>> pdf = pymupdf.open("pdf", pdfbytes)
            >>> pdf.save("some.pdf")
            >>>
            >>> # or this -->
            >>> pdfout = open("some.pdf", "wb")
            >>> pdfout.tobytes(pdfbytes)
            >>> pdfout.close()
            ```

            ```
            >>> # copy image files to PDF pages
            >>> # each page will have image dimensions
            >>> doc = pymupdf.open()                     # new PDF
            >>> imglist = [ ... image file names ...] # e.g. a directory listing
            >>> for img in imglist:
                    imgdoc=pymupdf.open(img)           # open image as a document
                    pdfbytes=imgdoc.convert_to_pdf()  # make a 1-page PDF of it
                    imgpdf=pymupdf.open("pdf", pdfbytes)
                    doc.insert_pdf(imgpdf)             # insert the image PDF
            >>> doc.save("allmyimages.pdf")
            ```

        Note

        The method uses the same logic as the *mutool convert* CLI. This works very well in most cases – however, beware of the following limitations.

        - Image files: perfect, no issues detected. However, image transparency is ignored. If you need that (like for a watermark), use [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image") instead. Otherwise, this method is recommended for its much better performance.
        - XPS: appearance very good. Links work fine, outlines (bookmarks) are lost, but can easily be recovered [[2]](#f2).
        - EPUB, CBZ, FB2: similar to XPS.
        - SVG: medium. Roughly comparable to [svglib](https://github.com/deeplook/svglib).

    get\_toc(*simple=True*)
    :   Creates a table of contents (TOC) out of the document’s outline chain.

        Parameters:
        :   **simple** (*bool*) – Indicates whether a simple or a detailed TOC is required. If `False`, each item of the list also contains a dictionary with [linkDest](linkdest.html#linkdest) details for each outline entry.

        Return type:
        :   list

        Returns:
        :   a list of lists. Each entry has the form *[lvl, title, page, dest]*. Its entries have the following meanings:

            - *lvl* – hierarchy level (positive *int*). The first entry is always 1. Entries in a row are either **equal**, **increase** by 1, or **decrease** by any number.
            - *title* – title (*str*)
            - *page* – 1-based source page number (*int*). `-1` if no destination or outside document.
            - *dest* – (*dict*) included only if *simple=False*. Contains details of the TOC item as follows:

              - kind: destination kind, see [Link Destination Kinds](vars.html#linkdest-kinds).
              - file: filename if kind is [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR") or [`LINK_LAUNCH`](vars.html#LINK_LAUNCH "LINK_LAUNCH").
              - page: target page, 0-based, [`LINK_GOTOR`](vars.html#LINK_GOTOR "LINK_GOTOR") or [`LINK_GOTO`](vars.html#LINK_GOTO "LINK_GOTO") only.
              - to: position on target page ([Point](point.html#point)).
              - zoom: (float) zoom factor on target page.
              - xref: [`xref`](glossary.html#xref "xref") of the item (0 if no PDF).
              - color: item color in PDF RGB format `(red, green, blue)`, or omitted (always omitted if no PDF).
              - bold: true if bold item text or omitted. PDF only.
              - italic: true if italic item text, or omitted. PDF only.
              - collapse: true if sub-items are folded, or omitted. PDF only.
              - nameddest: target name if kind=4. PDF only. (New in 1.23.7.)

    xref\_get\_keys(*xref*)
    :   - New in v1.18.7

        PDF only: Return the PDF dictionary keys of the [`dictionary`](glossary.html#dictionary "dictionary") object provided by its xref number.

        Parameters:
        :   **xref** (*int*) – the [`xref`](glossary.html#xref "xref"). *(Changed in v1.18.10)* Use `-1` to access the special dictionary “PDF trailer”.

        Returns:
        :   a tuple of dictionary keys present in object [`xref`](glossary.html#xref "xref"). Examples:

            ```
            >>> from pprint import pprint
            >>> import pymupdf
            >>> doc=pymupdf.open("pymupdf.pdf")
            >>> xref = doc.page_xref(0)  # xref of page 0
            >>> pprint(doc.xref_get_keys(xref))  # primary level keys of a page
            ('Type', 'Contents', 'Resources', 'MediaBox', 'Parent')
            >>> pprint(doc.xref_get_keys(-1))  # primary level keys of the trailer
            ('Type', 'Index', 'Size', 'W', 'Root', 'Info', 'ID', 'Length', 'Filter')
            >>>
            ```

    xref\_get\_key(*xref*, *key*)
    :   - New in v1.18.7

        PDF only: Return type and value of a PDF dictionary key of a [`dictionary`](glossary.html#dictionary "dictionary") object given by its xref.

        Parameters:
        :   - **xref** (*int*) – the [`xref`](glossary.html#xref "xref"). *Changed in v1.18.10:* Use `-1` to access the special dictionary “PDF trailer”.
            - **key** (*str*) – the desired PDF key. Must **exactly** match (case-sensitive) one of the keys contained in [`Document.xref_get_keys()`](#Document.xref_get_keys "Document.xref_get_keys").

        Return type:
        :   tuple

        Returns:
        :   A tuple (type, value) of strings, where type is one of “xref”, “array”, “dict”, “int”, “float”, “null”, “bool”, “name”, “string” or “unknown” (should not occur). Independent of “type”, the value of the key is **always** formatted as a string – see the following example – and (almost always) a faithful reflection of what is stored in the PDF. In most cases, the format of the value string also gives a clue about the key type:

        - A “name” always starts with a “/” slash.
        - An “xref” always ends with “ 0 R”.
        - An “array” is always enclosed in “[…]” brackets.
        - A “dict” is always enclosed in “<<…>>” brackets.
        - A “bool”, resp. “null” always equal either “true”, “false”, resp. “null”.
        - “float” and “int” are represented by their string format – and are thus not always distinguishable.
        - A “string” is converted to UTF-8 and may therefore deviate from what is stored in the PDF. For example, the PDF key “Author” may have a value of “<FEFF004A006F0072006A00200058002E0020004D0063004B00690065>” in the file, but the method will return `('string', 'Jorj X. McKie')`.

          ```
          >>> for key in doc.xref_get_keys(xref):
                  print(key, "=" , doc.xref_get_key(xref, key))
          Type = ('name', '/Page')
          Contents = ('xref', '1297 0 R')
          Resources = ('xref', '1296 0 R')
          MediaBox = ('array', '[0 0 612 792]')
          Parent = ('xref', '1301 0 R')
          >>> #
          >>> # Now same thing for the PDF trailer.
          >>> # It has no xref, so -1 must be used instead.
          >>> #
          >>> for key in doc.xref_get_keys(-1):
                  print(key, "=", doc.xref_get_key(-1, key))
          Type = ('name', '/XRef')
          Index = ('array', '[0 8802]')
          Size = ('int', '8802')
          W = ('array', '[1 3 1]')
          Root = ('xref', '8799 0 R')
          Info = ('xref', '8800 0 R')
          ID = ('array', '[<DC9D56A6277EFFD82084E64F9441E18C><DC9D56A6277EFFD82084E64F9441E18C>]')
          Length = ('int', '21111')
          Filter = ('name', '/FlateDecode')
          >>>
          ```

    xref\_set\_key(*xref*, *key*, *value*)
    :   - New in v1.18.7, changed in v 1.18.13
        - Changed in v1.19.4: remove a key “physically” if set to “null”.

        PDF only: Set (add, update, delete) the value of a PDF key for the [`dictionary`](glossary.html#dictionary "dictionary") object given by its xref.

        Caution

        This is an expert function: if you do not know what you are doing, there is a high risk to render (parts of) the PDF unusable. Please do consult [Adobe PDF References](app3.html#adobemanual) about object specification formats (page 18) and the structure of special dictionary types like page objects.

        Parameters:
        :   - **xref** (*int*) – the [`xref`](glossary.html#xref "xref"). *Changed in v1.18.13:* To update the PDF trailer, specify -1.
            - **key** (*str*) – the desired PDF key (without leading “/”). Must not be empty. Any valid PDF key – whether already present in the object (which will be overwritten) – or new. It is possible to use PDF path notation like `"Resources/ExtGState"` – which sets the value for key `"/ExtGState"` as a sub-object of `"/Resources"`.
            - **value** (*str*) – the value for the key. It must be a non-empty string and, depending on the desired PDF object type, the following rules must be observed. There is some syntax checking, but **no type checking** and no checking if it makes sense PDF-wise, i.e. **no semantics checking**. Upper / lower case is important!

        - *:data:`xref`* – must be provided as `"nnn 0 R"` with a valid [`xref`](glossary.html#xref "xref") number nnn of the PDF. The suffix “`0 R`” is required to be recognizable as an xref by PDF applications.
        - **array** – a string like `"[a b c d e f]"`. The brackets are required. Array items must be separated by at least one space (not commas like in Python). An empty array `"[]"` is possible and *equivalent* to removing the key. Array items may be any PDF objects, like dictionaries, xrefs, other arrays, etc. Like in Python, array items may be of different types.
        - **dict** – a string like `"<< ... >>"`. The brackets are required and must enclose a valid PDF dictionary definition. The empty dictionary `"<<>>"` is possible and *equivalent* to removing the key.
        - **int** – an integer formatted **as a string**.
        - **float** – a float formatted **as a string**. Scientific notation (with exponents) is **not allowed by PDF**.
        - **null** – the string `"null"`. This is the PDF equivalent to Python’s `None` and causes the key to be ignored – however not necessarily removed, resp. removed on saves with garbage collection. *Changed in v1.19.4:* If the key is no path hierarchy (i.e. contains no slash “/”), then it will be completely removed.
        - **bool** – one of the strings `"true"` or `"false"`.
        - **name** – a valid PDF name with a leading slash like this: `"/PageLayout"`. See page 16 of the [Adobe PDF References](app3.html#adobemanual).
        - **string** – a valid PDF string. **All PDF strings must be enclosed by brackets**. Denote the empty string as `"()"`. Depending on its content, the possible brackets are

          - “(…)” for ASCII-only text. Reserved PDF characters must be backslash-escaped and non-ASCII characters must be provided as 3-digit backslash-escaped octals – including leading zeros. Example: 12 = 0x0C must be encoded as `014`.
          - “<…>” for hex-encoded text. Every character must be represented by two hex-digits (lower or upper case).
          - If in doubt, we **strongly recommend** to use [`get_pdf_str()`](functions.html#get_pdf_str "get_pdf_str")! This function automatically generates the right brackets, escapes, and overall format. It will for example do conversions like these:

            ```
            >>> # because of the € symbol, the following yields UTF-16BE BOM
            >>> pymupdf.get_pdf_str("Pay in $ or €.")
            '<feff00500061007900200069006e002000240020006f0072002020ac002e>'
            >>> # escapes for brackets and non-ASCII
            >>> pymupdf.get_pdf_str("Prices in EUR (USD also accepted). Areas are in m².")
            '(Prices in EUR \\(USD also accepted\\). Areas are in m\\262.)'
            ```

    get\_page\_pixmap(*pno: int*, *\**, *matrix: matrix\_like = Identity*, *dpi=None*, *colorspace: [Colorspace](colorspace.html#Colorspace "Colorspace") = csRGB*, *clip: rect\_like = None*, *alpha: bool = False*, *annots: bool = True*)
    :   Creates a pixmap from page *pno* (zero-based). Invokes [`Page.get_pixmap()`](page.html#Page.get_pixmap "Page.get_pixmap").

        All parameters except `pno` are *keyword-only.*

        Parameters:
        :   **pno** (*int*) – page number, 0-based in `-∞ < pno < page_count`.

        Return type:
        :   [Pixmap](pixmap.html#pixmap)

    get\_page\_xobjects(*pno*)
    :   - New in v1.16.13
        - Changed in v1.18.11

        PDF only: Return a list of all XObjects referenced by a page.

        Parameters:
        :   **pno** (*int*) – page number, 0-based, `-∞ < pno < page_count`.

        Return type:
        :   list

        Returns:
        :   a list of (non-image) XObjects. These objects typically represent pages *embedded* (not copied) from other PDFs. For example, [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") will create this type of object. An item of this list has the following layout: `(xref, name, invoker, bbox)`, where

            - *:data:`xref`* (*int*) is the XObject’s [`xref`](glossary.html#xref "xref").
            - **name** (*str*) is the symbolic name to reference the XObject.
            - **invoker** (*int*) the [`xref`](glossary.html#xref "xref") of the invoking XObject or zero if the page directly invokes it.
            - **bbox** ([Rect](rect.html#rect)) the boundary box of the XObject’s location on the page **in untransformed coordinates**. To get actual, non-rotated page coordinates, multiply with the page’s transformation matrix [`Page.transformation_matrix`](page.html#Page.transformation_matrix "Page.transformation_matrix"). *Changed in v.18.11:* the bbox is now formatted as [Rect](rect.html#rect).

    get\_page\_images(*pno*, *full=False*)
    :   PDF only: Return a list of all images (directly or indirectly) referenced by the page.

        Parameters:
        :   - **pno** (*int*) – page number, 0-based, `-∞ < pno < page_count`.
            - **full** (*bool*) – whether to also include the referencer’s [`xref`](glossary.html#xref "xref") (which is zero if this is the page).

        Return type:
        :   list

        Returns:
        :   a list of images **referenced** by this page. Each item looks like:

            `(xref, smask, width, height, bpc, colorspace, alt_colorspace, name, filter, referencer)`

            > - `xref` (*int*) is the image object number
            > - `smask` (*int*) is the object number of its soft-mask image
            > - `width` (*int*) is the image width
            > - `height` (*int*) is the image height
            > - `bpc` (*int*) denotes the number of bits per component (normally 8)
            > - `colorspace` (*str*) a string naming the colorspace (like **DeviceRGB**)
            > - `alt_colorspace` (*str*) is any alternate colorspace depending on the value of **colorspace**
            > - `name` (*str*) is the symbolic name by which the image is referenced
            > - `filter` (*str*) is the decode filter of the image ([Adobe PDF References](app3.html#adobemanual), pp. 22).
            > - `referencer` (*int*) the [`xref`](glossary.html#xref "xref") of the referencer. Zero if directly referenced by the page. Only present if *full=True*.

        Note

        In general, this is not the list of images that are **actually displayed**. This method only parses several PDF objects to collect references to embedded images. It does not analyse the page’s [`contents`](glossary.html#contents "contents"), where all the actual image display commands are defined. To get this information, please use [`Page.get_image_info()`](page.html#Page.get_image_info "Page.get_image_info"). Also have a look at the discussion in section [Structure of Dictionary Outputs](textpage.html#textpagedict).

    get\_page\_fonts(*pno*, *full=False*)
    :   PDF only: Return a list of all fonts (directly or indirectly) referenced by the page object definition.

        Parameters:
        :   - **pno** (*int*) – page number, 0-based, `-∞ < pno < page_count`.
            - **full** (*bool*) – whether to also include the referencer’s [`xref`](glossary.html#xref "xref"). If `True`, the returned items are one entry longer. Use this option if you need to know, whether the page directly references the font. In this case the last entry is 0. If the font is referenced by an `/XObject` of the page, you will find its [`xref`](glossary.html#xref "xref") here.

        Return type:
        :   list

        Returns:
        :   a list of fonts referenced by the object definition of the page. Each entry looks like:

            `(xref, ext, type, basefont, name, encoding, referencer)`

            > - `xref` (*int*) is the font object number (may be zero if the PDF uses one of the builtin fonts directly)
            > - `ext` (*str*) font file extension (e.g. “ttf”, see [Font File Extensions](vars.html#fontextensions))
            > - `type` (*str*) is the font type (like “Type1” or “TrueType” etc.)
            > - `basefont` (*str*) is the base font name,
            > - `name` (*str*) is the symbolic name, by which the font is referenced
            > - `encoding` (*str*) the font’s character encoding if different from its built-in encoding ([Adobe PDF References](app3.html#adobemanual), p. 254):
            > - `referencer` (*int* optional) the [`xref`](glossary.html#xref "xref") of the referencer. Zero if directly referenced by the page, otherwise the xref of an XObject. Only present if *full=True*.

        Example:

        ```
        >>> pprint(doc.get_page_fonts(0, full=False))
        [(12, 'ttf', 'TrueType', 'FNUUTH+Calibri-Bold', 'R8', ''),
         (13, 'ttf', 'TrueType', 'DOKBTG+Calibri', 'R10', ''),
         (14, 'ttf', 'TrueType', 'NOHSJV+Calibri-Light', 'R12', ''),
         (15, 'ttf', 'TrueType', 'NZNDCL+CourierNewPSMT', 'R14', ''),
         (16, 'ttf', 'Type0', 'MNCSJY+SymbolMT', 'R17', 'Identity-H'),
         (17, 'cff', 'Type1', 'UAEUYH+Helvetica', 'R20', 'WinAnsiEncoding'),
         (18, 'ttf', 'Type0', 'ECPLRU+Calibri', 'R23', 'Identity-H'),
         (19, 'ttf', 'Type0', 'TONAYT+CourierNewPSMT', 'R27', 'Identity-H')]
        ```

        Note

        - This list has no duplicate entries: the combination of [`xref`](glossary.html#xref "xref"), *name* and *referencer* is unique.
        - In general, this is a true superset of the fonts actually in use by this page. The PDF creator may e.g. have specified some global list, of which each page make only partial use.
        - Be aware that font names returned by some variants of [`Page.get_text()`](page.html#Page.get_text "Page.get_text") (respectively [TextPage](textpage.html#textpage) methods) need not (exactly) equal the base font name shown here. Reasons for any differences include:

          > - This method always shows any subset prefixes (the pattern `ABCDEF+`), whereas text extractions do not do this by default.
          > - Text extractions use the base library to access the font name, which has a length cap of 31 bytes and generally interrogates the font file binary to access the name. Method `get_page_fonts()` however looks at the PDF definition source.
          > - Text extractions work for all supported document types in exactly the same way – not just for PDFs. Consequently they do not contain PDF-specifics.

    get\_page\_text(*pno*, *output='text'*, *flags=3*, *textpage=None*, *sort=False*)
    :   Extracts the text of a page given its page number *pno* (zero-based). Invokes [`Page.get_text()`](page.html#Page.get_text "Page.get_text").

        Parameters:
        :   **pno** (*int*) – page number, 0-based, any value `-∞ < pno < page_count`.

        For other parameter refer to the page method.

        Return type:
        :   str

    layout(*rect=None*, *width=0*, *height=0*, *fontsize=11*)
    :   Re-paginate (“reflow”) the document based on the given page dimension and fontsize. This only affects some document types like e-books and HTML. Ignored if not supported. Supported documents have `True` in property [`is_reflowable`](#Document.is_reflowable "Document.is_reflowable").

        Parameters:
        :   - **rect** (*rect\_like*) – desired page size. Must be finite, not empty and start at point (0, 0).
            - **width** (*float*) – use it together with `height` as alternative to `rect`.
            - **height** (*float*) – use it together with `width` as alternative to `rect`.
            - **fontsize** (*float*) – the desired default fontsize.

    select(*s*)
    :   PDF only: Keeps only those pages of the document whose numbers occur in the list. Empty sequences or elements outside `range(doc.page_count)` will cause a *ValueError*. For more details see remarks at the bottom or this chapter.

        Parameters:
        :   **s** (*sequence*) – The sequence (see [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes)) of page numbers (zero-based) to be included. Pages not in the sequence will be deleted (from memory) and become unavailable until the document is reopened. **Page numbers can occur multiple times and in any order:** the resulting document will reflect the sequence exactly as specified.

        Note

        - Page numbers in the sequence need not be unique nor be in any particular order. This makes the method a versatile utility to e.g. select only the even or the odd pages or meeting some other criteria and so forth.
        - On a technical level, the method will always create a new [`pagetree`](glossary.html#pagetree "pagetree").
        - When dealing with only a few pages, methods [`copy_page()`](#Document.copy_page "Document.copy_page"), [`move_page()`](#Document.move_page "Document.move_page"), [`delete_page()`](#Document.delete_page "Document.delete_page") are easier to use. In fact, they are also **much faster** – by at least one order of magnitude when the document has many pages.

    set\_metadata(*m*)
    :   PDF only: Sets or updates the metadata of the document as specified in *m*, a Python dictionary.

        Parameters:
        :   **m** (*dict*) – A dictionary with the same keys as *metadata* (see below). All keys are optional. A PDF’s format and encryption method cannot be set or changed and will be ignored. If any value should not contain data, do not specify its key or set the value to `None`. If you use *{}* all metadata information will be cleared to the string *“none”*. If you want to selectively change only some values, modify a copy of *doc.metadata* and use it as the argument. Arbitrary unicode values are possible if specified as UTF-8-encoded.

        *(Changed in v1.18.4)* Empty values or “none” are no longer written, but completely omitted.

    get\_xml\_metadata()
    :   PDF only: Get the document XML metadata.

        Return type:
        :   str

        Returns:
        :   XML metadata of the document. Empty string if not present or not a PDF.

    set\_xml\_metadata(*xml*)
    :   PDF only: Sets or updates XML metadata of the document.

        Parameters:
        :   **xml** (*str*) – the new XML metadata. Should be XML syntax, however no checking is done by this method and any string is accepted.

    set\_pagelayout(*value*)
    :   - New in v1.22.2

        PDF only: Set the `/PageLayout`.

        Parameters:
        :   **value** (*str*) – one of the strings “SinglePage”, “OneColumn”, “TwoColumnLeft”, “TwoColumnRight”, “TwoPageLeft”, “TwoPageRight”. Lower case is supported.

    set\_pagemode(*value*)
    :   - New in v1.22.2

        PDF only: Set the `/PageMode`.

        Parameters:
        :   **value** (*str*) – one of the strings “UseNone”, “UseOutlines”, “UseThumbs”, “FullScreen”, “UseOC”, “UseAttachments”. Lower case is supported.

    set\_markinfo(*value*)
    :   - New in v1.22.2

        PDF only: Set the `/MarkInfo` values.

        Parameters:
        :   **value** (*dict*) – a dictionary like this one: `{"Marked": False, "UserProperties": False, "Suspects": False}`. This dictionary contains information about the usage of Tagged PDF conventions. For details please see the [PDF specifications](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf).

    set\_toc(*toc*, *collapse=1*)
    :   PDF only: Replaces the **complete current outline** tree (table of contents) with the one provided as the argument. After successful execution, the new outline tree can be accessed as usual via [`Document.get_toc()`](#Document.get_toc "Document.get_toc") or via [`Document.outline`](#Document.outline "Document.outline"). Like with other output-oriented methods, changes become permanent only via [`save()`](#Document.save "Document.save") (incremental save supported). Internally, this method consists of the following two steps. For a demonstration see example below.

        - Step 1 deletes all existing bookmarks.
        - Step 2 creates a new TOC from the entries contained in *toc*.

        Parameters:
        :   - **toc** (*sequence*) –

              A list / tuple with **all bookmark entries** that should form the new table of contents. Output variants of [`get_toc()`](#Document.get_toc "Document.get_toc") are acceptable. To completely remove the table of contents specify an empty sequence or None. Each item must be a list with the following format.

              - [lvl, title, page [, dest]] where

                - **lvl** is the hierarchy level (int > 0) of the item, which **must be 1** for the first item and at most 1 larger than the previous one.
                - **title** (str) is the title to be displayed. It is assumed to be UTF-8-encoded (relevant for multibyte code points only).
                - **page** (int) is the target page number **(attention: 1-based)**. Must be in valid range if positive. Set it to -1 if there is no target, or the target is external.
                - **dest** (optional) is a dictionary or a number. If a number, it will be interpreted as the desired height (in points) this entry should point to on the page. Use a dictionary (like the one given as output by `get_toc(False)`) for a detailed control of the bookmark’s properties, see [`Document.get_toc()`](#Document.get_toc "Document.get_toc") for a description.
            - **collapse** (*int*) – *(new in v1.16.9)* controls the hierarchy level beyond which outline entries should initially show up collapsed. The default 1 will hence only display level 1, higher levels must be unfolded using the PDF viewer. To unfold everything, specify either a large integer, 0 or None.

        Return type:
        :   int

        Returns:
        :   the number of inserted, resp. deleted items.

        Changed in v1.23.8: Destination ‘to’ coordinates should now be in the
        same coordinate system as those returned by [`get_toc()`](#Document.get_toc "Document.get_toc") (internally they
        are now transformed with `page.cropbox` and `page.rotation_matrix`). So
        for example `set_toc(get_toc())` now gives unchanged destination ‘to’
        coordinates.

    outline\_xref(*idx*)
    :   - New in v1.17.7

        PDF only: Return the [`xref`](glossary.html#xref "xref") of the outline item. This is mainly used for internal purposes.

        Parameters:
        :   **idx** (*int*) – index of the item in list [`Document.get_toc()`](#Document.get_toc "Document.get_toc").

        Returns:
        :   [`xref`](glossary.html#xref "xref").

    del\_toc\_item(*idx*)
    :   - New in v1.17.7
        - Changed in v1.18.14: no longer remove the item’s text, but show it grayed-out.

        PDF only: Remove this TOC item. This is a high-speed method, which **disables** the respective item, but leaves the overall TOC structure intact. Physically, the item still exists in the TOC tree, but is shown grayed-out and will no longer point to any destination.

        This also implies that you can reassign the item to a new destination using [`Document.set_toc_item()`](#Document.set_toc_item "Document.set_toc_item"), when required.

        Parameters:
        :   **idx** (*int*) – the index of the item in list [`Document.get_toc()`](#Document.get_toc "Document.get_toc").

    set\_toc\_item(*idx*, *dest\_dict=None*, *kind=None*, *pno=None*, *uri=None*, *title=None*, *to=None*, *filename=None*, *zoom=0*)
    :   - New in v1.17.7
        - Changed in v1.18.6

        PDF only: Changes the TOC item identified by its index. Change the item **title**, **destination**, **appearance** (color, bold, italic) or collapsing sub-items – or to remove the item altogether.

        Use this method if you need specific changes for selected entries only and want to avoid replacing the complete TOC. This is beneficial especially when dealing with large table of contents.

        Parameters:
        :   - **idx** (*int*) – the index of the entry in the list created by [`Document.get_toc()`](#Document.get_toc "Document.get_toc").
            - **dest\_dict** (*dict*) – the new destination. A dictionary like the last entry of an item in `doc.get_toc(False)`. Using this as a template is recommended. When given, **all other parameters are ignored** – except title.
            - **kind** (*int*) – the link kind, see [Link Destination Kinds](vars.html#linkdest-kinds). If [`LINK_NONE`](vars.html#LINK_NONE "LINK_NONE"), then all remaining parameter will be ignored, and the TOC item will be removed – same as [`Document.del_toc_item()`](#Document.del_toc_item "Document.del_toc_item"). If None, then only the title is modified and the remaining parameters are ignored. All other values will lead to making a new destination dictionary using the subsequent arguments.
            - **pno** (*int*) – the 1-based page number, i.e. a value 1 <= pno <= doc.page\_count. Required for LINK\_GOTO.
            - **uri** (*str*) – the URL text. Required for LINK\_URI.
            - **title** (*str*) – the desired new title. None if no change.
            - **to** (*point\_like*) – (optional) points to a coordinate on the target page. Relevant for LINK\_GOTO. If omitted, a point near the page’s top is chosen.
            - **filename** (*str*) – required for LINK\_GOTOR and LINK\_LAUNCH.
            - **zoom** (*float*) – use this zoom factor when showing the target page.

        **Example use:** Change the TOC of the SWIG manual to achieve this:

        Collapse everything below top level and show the chapter on Python support in red, bold and italic:

        ```
        >>> import pymupdf
        >>> doc=pymupdf.open("SWIGDocumentation.pdf")
        >>> toc = doc.get_toc(False)  # we need the detailed TOC
        >>> # list of level 1 indices and their titles
        >>> lvl1 = [(i, item[1]) for i, item in enumerate(toc) if item[0] == 1]
        >>> for i, title in lvl1:
                d = toc[i][3]  # get the destination dict
                d["collapse"] = True  # collapse items underneath
                if "Python" in title:  # show the 'Python' chapter
                    d["color"] = (1, 0, 0)  # in red,
                    d["bold"] = True  # bold and
                    d["italic"] = True  # italic
                doc.set_toc_item(i, dest_dict=d)  # update this toc item
        >>> doc.save("NEWSWIG.pdf",garbage=3,deflate=True)
        ```

        In the previous example, we have changed only 42 of the 1240 TOC items of the file.

    bake(*\**, *annots=True*, *widgets=True*)
    :   PDF only: Convert annotations and / or widgets to become permanent parts of the pages. The PDF **will be changed** by this method. If [`widgets`](page.html#Page.widgets "Page.widgets") is `True`, the document will also no longer be a “Form PDF”.

        All pages will look the same, but will no longer have annotations, respectively fields. The visible parts will be converted to standard text, vector graphics or images as required.

        The method may thus be a viable **alternative for PDF-to-PDF conversions** using [`Document.convert_to_pdf()`](#Document.convert_to_pdf "Document.convert_to_pdf").

        Please consider that annotations are complex objects and may consist of more data “underneath” their visual appearance. Examples are “Text” and “FileAttachment” annotations. When “baking in” annotations / widgets with this method, all this underlying information (attached files, comments, associated PopUp annotations, etc.) will be lost and be removed on next garbage collection.

        Use this feature for instance for [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") (which supports neither annotations nor widgets) when the source pages should look exactly the same in the target.

        Parameters:
        :   - **annots** (*bool*) – convert annotations.
            - **widgets** (*bool*) – convert fields / widgets. After execution, the document will no longer be a “Form PDF”.

    can\_save\_incrementally()
    :   - New in v1.16.0

        Check whether the document can be saved incrementally. Use it to choose the right option without encountering exceptions.

    repair()
    :   Repair document.

        - Slow for large documents.
        - Does nothing on non-PDF documents.
        - New in v1.27.0

    scrub(*attached\_files=True*, *clean\_pages=True*, *embedded\_files=True*, *hidden\_text=True*, *javascript=True*, *metadata=True*, *redactions=True*, *redact\_images=0*, *remove\_links=True*, *reset\_fields=True*, *reset\_responses=True*, *thumbnails=True*, *xml\_metadata=True*)
    :   - New in v1.16.14

        PDF only: Remove potentially sensitive data from the PDF. This function is inspired by the similar “Sanitize” function in Adobe Acrobat products. The process is configurable by a number of options.

        Parameters:
        :   - **attached\_files** (*bool*) – Search for ‘FileAttachment’ annotations and remove the file content.
            - **clean\_pages** (*bool*) – Remove any comments from page painting sources. If this option is set to `False`, then this is also done for *hidden\_text* and *redactions*.
            - **embedded\_files** (*bool*) – Remove embedded files.
            - **hidden\_text** (*bool*) – Remove OCRed text and invisible text [[7]](#f7).
            - **javascript** (*bool*) – Remove JavaScript sources.
            - **metadata** (*bool*) – Remove PDF standard metadata.
            - **redactions** (*bool*) – Apply redaction annotations.
            - **redact\_images** (*int*) – how to handle images if applying redactions. One of 0 (ignore), 1 (blank out overlaps) or 2 (remove).
            - **remove\_links** (*bool*) – Remove all links.
            - **reset\_fields** (*bool*) – Reset all form fields to their defaults.
            - **reset\_responses** (*bool*) – Remove all responses from all annotations.
            - **thumbnails** (*bool*) – Remove thumbnail images from pages.
            - **xml\_metadata** (*bool*) – Remove XML metadata.

    save(*outfile*, *garbage=0*, *clean=False*, *deflate=False*, *deflate\_images=False*, *deflate\_fonts=False*, *incremental=False*, *ascii=False*, *expand=0*, *linear=False*, *pretty=False*, *no\_new\_id=False*, *encryption=PDF\_ENCRYPT\_NONE*, *permissions=-1*, *owner\_pw=None*, *user\_pw=None*, *use\_objstms=0*, *compression\_effort=0*, *raise\_on\_repair=False*)
    :   - Changed in v1.18.7
        - Changed in v1.19.0
        - Changed in v1.24.1

        PDF only: Saves the document in its **current state**.

        Parameters:
        :   - **outfile** (*str**,**Path**,**fp*) – The file path, `pathlib.Path` or file object to save to. A file object must have been created before via `open(...)` or `io.BytesIO()`. Choosing `io.BytesIO()` is similar to [`Document.tobytes()`](#Document.tobytes "Document.tobytes") below, which equals the `getvalue()` output of an internally created `io.BytesIO()`.
            - **garbage** (*int*) –

              Do garbage collection. Positive values exclude “incremental”.

              - 0 = none
              - 1 = remove unused (unreferenced) objects.
              - 2 = in addition to 1, compact the [`xref`](glossary.html#xref "xref") table.
              - 3 = in addition to 2, merge duplicate objects.
              - 4 = in addition to 3, check [`stream`](glossary.html#stream "stream") objects for duplication. This may be slow because such data are typically large.
            - **clean** (*bool*) – Clean and sanitize content streams [[1]](#f1). Corresponds to “mutool clean -sc”.
            - **deflate** (*bool*) – Deflate (compress) uncompressed streams.
            - **deflate\_images** (*bool*) – *(new in v1.18.3)* Deflate (compress) uncompressed image streams [[4]](#f4).
            - **deflate\_fonts** (*bool*) – *(new in v1.18.3)* Deflate (compress) uncompressed fontfile streams [[4]](#f4).
            - **incremental** (*bool*) – Only save changes to the PDF. Excludes “garbage” and “linear”. Can only be used if *outfile* is a string or a `pathlib.Path` and equal to [`Document.name`](#Document.name "Document.name"). Cannot be used for files that are decrypted or repaired and also in some other cases. To be sure, check [`Document.can_save_incrementally()`](#Document.can_save_incrementally "Document.can_save_incrementally"). If this is false, saving to a new file is required.
            - **ascii** (*bool*) – convert binary data to ASCII.
            - **expand** (*int*) –

              Decompress objects. Generates versions that can be better read by some other programs and will lead to larger files.

              - 0 = none
              - 1 = images
              - 2 = fonts
              - 255 = all
            - **linear** (*bool*) – Save a linearised version of the document. This option creates a file format for improved performance for Internet access. Excludes “incremental” and “use\_objstms”.
            - **pretty** (*bool*) – Prettify the document source for better readability. PDF objects will be reformatted to look like the default output of [`Document.xref_object()`](#Document.xref_object "Document.xref_object").
            - **no\_new\_id** (*bool*) – Suppress the update of the file’s `/ID` field. If the file happens to have no such field at all, also suppress creation of a new one. Default is `False`, so every save will lead to an updated file identification.
            - **permissions** (*int*) – *(new in v1.16.0)* Set the desired permission levels. See [Document Permissions](vars.html#permissioncodes) for possible values. Default is granting all.
            - **encryption** (*int*) – *(new in v1.16.0)* set the desired encryption method. See [PDF encryption method codes](vars.html#encryptionmethods) for possible values.
            - **owner\_pw** (*str*) – *(new in v1.16.0)* set the document’s owner password. *(Changed in v1.18.3)* If not provided, the user password is taken if provided. The string length must not exceed 40 characters.
            - **user\_pw** (*str*) – *(new in v1.16.0)* set the document’s user password. The string length must not exceed 40 characters.
            - **use\_objstms** (*int*) –

              *(new in v1.24.0)* compression option that converts eligible PDF object definitions to information that is stored in some other object’s [`stream`](glossary.html#stream "stream") data. Depending on the `deflate` parameter value, the converted object definitions will be compressed – which can lead to very significant file size reductions.

              Warning

              The method does not check, whether a file of that name already exists, will hence not ask for confirmation, and overwrite the file. It is your responsibility as a programmer to handle this.
            - **compression\_effort** (*int*) –

              - 0 for default
              - 1 for minimum effort.
              - 100 for maximum effort.
            - **raise\_on\_repair** (*bool*) –

              *(new in v1.27.0)* If true we raise an exception if the save caused a repair.
              This is useful because repairs can cause changes to be lost.

              Also see [`Document.repair()`](#Document.repair "Document.repair").

        Note

        **File size reduction**

        1. Use the save options like `garbage=3|4, deflate=True, use_objstms=True|1`. Do not touch the default values `expand=False|0, clean=False|0, incremental=False|0, linear=False|0`.
        This is a “lossless” file size reduction. There is a convenience version of this method with these values set by default, [`Document.ez_save()`](#Document.ez_save "Document.ez_save") – please see below.

        2. “Lossy” file size reduction in essence must give up something with respect to images, like (a) remove all images (b) replace images by their grayscale versions (c) reduce image resolutions. Find examples in the [PyMuPDF Utilities “replace-image” folder](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/replace-image).

    ez\_save(*\*args*, *\*\*kwargs*)
    :   - New in v1.18.11

        PDF only: The same as [`Document.save()`](#Document.save "Document.save") but with changed defaults `deflate=True, garbage=3, use_objstms=1`.

    saveIncr()
    :   PDF only: saves the document incrementally. This is a convenience abbreviation for `doc.save(doc.name, incremental=True, encryption=PDF_ENCRYPT_KEEP)`.

    Note

    Saving incrementally may be required if the document contains verified signatures which would be invalidated by saving to a new file.

    tobytes(*garbage=0*, *clean=False*, *deflate=False*, *deflate\_images=False*, *deflate\_fonts=False*, *ascii=False*, *expand=0*, *linear=False*, *pretty=False*, *no\_new\_id=False*, *encryption=PDF\_ENCRYPT\_NONE*, *permissions=-1*, *owner\_pw=None*, *user\_pw=None*, *use\_objstms=0*)
    :   - Changed in v1.18.7
        - Changed in v1.19.0
        - Changed in v1.24.1

        PDF only: Writes the **current content of the document** to a bytes object instead of to a file. Obviously, you should be wary about memory requirements. The meanings of the parameters exactly equal those in [`save()`](#Document.save "Document.save"). Chapter [FAQ](faq.html#faq) contains an example for using this method as a pre-processor to [pdfrw](https://pypi.python.org/pypi/pdfrw/0.3).

        *(Changed in v1.16.0)* for extended encryption support.

        Return type:
        :   bytes

        Returns:
        :   a bytes object containing the complete document.

    search\_page\_for(*pno*, *text*, *quads=False*)
    :   Search for “text” on page number “pno”. Works exactly like the corresponding [`Page.search_for()`](page.html#Page.search_for "Page.search_for"). Any integer `-∞ < pno < page_count` is acceptable.

    insert\_pdf(*docsrc*, *\**, *from\_page=-1*, *to\_page=-1*, *start\_at=-1*, *rotate=-1*, *links=True*, *annots=True*, *widgets=True*, *join\_duplicates=False*, *show\_progress=0*, *final=1*)
    :   PDF only: Copy the page range **[from\_page, to\_page]** (including both) of PDF document *docsrc* into the current one. Inserts will start with page number *start\_at*. Value -1 indicates default values. All pages thus copied will be rotated as specified. Links, annotations and widgets can be excluded in the target, see below. All page numbers are 0-based.

        Parameters:
        :   - **docsrc** (*Document*) – An opened PDF *Document* which must not be the current document. However, it may refer to the same underlying file.
            - **from\_page** (*int*) – First page number in *docsrc*. Default is zero.
            - **to\_page** (*int*) – Last page number in *docsrc* to copy. Defaults to last page.
            - **start\_at** (*int*) – First copied page, will become page number *start\_at* in the target. Default -1 appends the page range to the end. If zero, the page range will be inserted before current first page.
            - **rotate** (*int*) – All copied pages will be rotated by the provided value (degrees, integer multiple of 90).
            - **links** (*bool*) – Choose whether (internal and external) links should be included in the copy. Default is `True`. *Named* links ([`LINK_NAMED`](vars.html#LINK_NAMED "LINK_NAMED")) and internal links to outside the copied page range are **always excluded**.
            - **annots** (*bool*) – choose whether annotations should be included in the copy.
            - **widgets** (*bool*) – choose whether annotations should be included in the copy. If `True` and at least one of the source pages contains form fields, the target PDF will be turned into a Form PDF (if not already being one).
            - **join\_duplicates** (*bool*) –

              *(New in version 1.25.5)* Choose how to handle duplicate root field names in the source pages. This parameter is ignored if `widgets=False`.

              Default is `False` which will add unifying strings to the name of those source root fields which have a duplicate in the target. For instance, if “name” already occurs in the target, the source widget’s name will be changed to “name [text]” with a suitably chosen string “text”.

              If `True`, root fields with duplicate names in source and target will be converted to so-called “Kids” of a “Parent” object (which lists all kid widgets in a PDF array). This will effectively turn those kids into instances of the “same” widget: if e.g. one of the kids is changed, then all its instances will automatically inherit this change – no matter on which page they happen to be displayed.
            - **show\_progress** (*int*) – *(new in v1.17.7)* specify an interval size greater zero to see progress messages on `sys.stdout`. After each interval, a message like `Inserted 30 of 47 pages.` will be printed.
            - **final** (*int*) – *(new in v1.18.0)* controls whether the list of already copied objects should be **dropped** after this method, default `True`. Set it to 0 except for the last one of multiple insertions from the same source PDF. This saves target file size and speeds up execution considerably.

    Note

    1. This is a page-based method. Document-level information of source documents is therefore mostly ignored. Examples include Optional Content, Embedded Files, `StructureElem`, table of contents, page labels, metadata, named destinations (and other named entries) and some more.
    2. If `from_page > to_page`, pages will be **copied in reverse order**. If `0 <= from_page == to_page`, then one page will be copied.
    3. `docsrc` TOC entries **will not be copied**. It is easy however, to recover a table of contents for the resulting document. Look at the examples below and at program [join.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/join-documents/join.py) in the *examples* directory: it can join PDF documents and at the same time piece together respective parts of the tables of contents.

    insert\_file(*infile*, *from\_page=-1*, *to\_page=-1*, *start\_at=-1*, *rotate=-1*, *links=True*, *annots=True*, *show\_progress=0*, *final=1*)
    :   - New in v1.22.0

        PDF only: Add an arbitrary supported document to the current PDF. Opens “infile” as a document, converts it to a PDF and then invokes [`Document.insert_pdf()`](#Document.insert_pdf "Document.insert_pdf"). Parameters are the same as for that method. Among other things, this features an easy way to append images as full pages to an output PDF.

        Parameters:
        :   **infile** (*multiple*) – the input document to insert. May be a filename specification as is valid for creating a [Document](#document) or a [Pixmap](pixmap.html#pixmap).

    new\_page(*pno=-1*, *width=595*, *height=842*)
    :   PDF only: Insert an empty page.

        Parameters:
        :   - **pno** (*int*) – page number index (zero-indexed) at which to insert page. Special values -1 and *doc.page\_count* insert **after** the last page.
            - **width** (*float*) – page width.
            - **height** (*float*) – page height.

        Return type:
        :   [Page](page.html#page)

        Returns:
        :   the created page object. Be aware that the page numbers of pages after the inserted one will have changed after method execution. For the same reason, **all existing page objects will be invalidated.** Using them will lead to exceptions.

    insert\_page(*pno*, *text=None*, *fontsize=11*, *width=595*, *height=842*, *fontname='helv'*, *fontfile=None*, *color=None*)
    :   PDF only: Insert a new page and insert some text. Convenience function which combines [`Document.new_page()`](#Document.new_page "Document.new_page") and (parts of) [`Page.insert_text()`](page.html#Page.insert_text "Page.insert_text").

        Parameters:
        :   **pno** (*int*) –

            page number index (zero-indexed) at which to insert page. Special values -1 and `doc.page_count` insert **after** the last page.

            Changed in v1.14.12
            :   This is now a positional parameter

        For the other parameters, please consult the aforementioned methods.

        Return type:
        :   int

        Returns:
        :   the result of [`Page.insert_text()`](page.html#Page.insert_text "Page.insert_text") (number of successfully inserted lines).

    delete\_page(*pno=-1*)
    :   PDF only: Delete a page given by its 0-based number in `-∞ < pno < page_count`.

        - Changed in v1.18.14: support Python’s `del` statement.

        Parameters:
        :   **pno** (*int*) – the page to be deleted. Negative number count backwards from the end of the document (like with indices). Default is the last page.

    delete\_pages(*\*args*, *\*\*kwds*)
    :   - Changed in v1.18.13: more flexibility specifying pages to delete.
        - Changed in v1.18.14: support Python’s `del` statement.

        PDF only: Delete multiple pages given as 0-based numbers.

        **Format 1:** Use keywords. Represents the old format. A contiguous range of pages is removed.
        :   - “from\_page”: first page to delete. Zero if omitted.
            - “to\_page”: last page to delete. Last page in document if omitted. Must not be less then “from\_page”.

        **Format 2:** Two page numbers as positional parameters. Handled like Format 1.

        **Format 3:** One positional integer parameter. Equivalent to `Page.delete_page()`.

        **Format 4:** One positional parameter of type *list*, *tuple* or *range()* of page numbers. The items of this sequence may be in any order and may contain duplicates.

        **Format 5:** *(New in v1.18.14)* Using the Python `del` statement and index / slice notation is now possible.

        Note

        *(Changed in v1.14.17, optimized in v1.17.7)* In an effort to maintain a valid PDF structure, this method and [`delete_page()`](#Document.delete_page "Document.delete_page") will also deactivate items in the table of contents which point to deleted pages. “Deactivation” here means, that the bookmark will point to nowhere and the title will be shown grayed-out by supporting PDF viewers. The overall TOC structure is left intact.

        It will also remove any **links on remaining pages** which point to a deleted one. This action may have an extended response time for documents with many pages.

        Following examples will all delete pages 500 through 519:

        - `doc.delete_pages(500, 519)`
        - `doc.delete_pages(from_page=500, to_page=519)`
        - `doc.delete_pages((500, 501, 502, ... , 519))`
        - `doc.delete_pages(range(500, 520))`
        - `del doc[500:520]`
        - `del doc[(500, 501, 502, ... , 519)]`
        - `del doc[range(500, 520)]`

        For the [Adobe PDF References](app3.html#adobemanual) the above takes about 0.6 seconds, because the remaining 1290 pages must be cleaned from invalid links.

        In general, the performance of this method is dependent on the number of remaining pages – **not** on the number of deleted pages: in the above example, **deleting all pages except** those 20, will need much less time.

    copy\_page(*pno*, *to=-1*)
    :   PDF only: Copy a page reference within the document.

        Parameters:
        :   - **pno** (*int*) – the page to be copied. Must be in range `0 <= pno < page_count`.
            - **to** (*int*) – the page number in front of which to copy. The default inserts **after** the last page.

        Note

        Only a new **reference** to the page object will be created – not a new page object, all copied pages will have identical attribute values, including the [`Page.xref`](page.html#Page.xref "Page.xref"). This implies that any changes to one of these copies will appear on all of them.

    fullcopy\_page(*pno*, *to=-1*)
    :   - New in v1.14.17

        PDF only: Make a full copy (duplicate) of a page.

        Parameters:
        :   - **pno** (*int*) – the page to be duplicated. Must be in range `0 <= pno < page_count`.
            - **to** (*int*) – the page number in front of which to copy. The default inserts **after** the last page.

        Note

        - In contrast to [`copy_page()`](#Document.copy_page "Document.copy_page"), this method creates a new page object (with a new [`xref`](glossary.html#xref "xref")), which can be changed independently from the original.
        - Any Popup and “IRT” (“in response to”) annotations are **not copied** to avoid potentially incorrect situations.

    move\_page(*pno*, *to=-1*)
    :   PDF only: Move (copy and then delete original) a page within the document.

        Parameters:
        :   - **pno** (*int*) – the page to be moved. Must be in range `0 <= pno < page_count`.
            - **to** (*int*) – the page number in front of which to insert the moved page. The default moves **after** the last page.

    need\_appearances(*value=None*)
    :   - New in v1.17.4

        PDF only: Get or set the */NeedAppearances* property of Form PDFs. Quote: *“(Optional) A flag specifying whether to construct appearance streams and appearance dictionaries for all widget annotations in the document … Default value: false.”* This may help controlling the behavior of some readers / viewers.

        Parameters:
        :   **value** (*bool*) – set the property to this value. If omitted or `None`, inquire the current value.

        Return type:
        :   bool

        Returns:
        :   - None: not a Form PDF, or property not defined.
            - True / False: the value of the property (either just set or existing for inquiries). Has no effect if no Form PDF.

    get\_sigflags()
    :   PDF only: Return whether the document contains signature fields. This is an optional PDF property: if not present (return value -1), no conclusions can be drawn – the PDF creator may just not have bothered using it.

        Return type:
        :   int

        Returns:
        :   - -1: not a Form PDF / no signature fields recorded / no *SigFlags* found.
            - 1: at least one signature field exists.
            - 3: contains signatures that may be invalidated if the file is saved (written) in a way that alters its previous contents, as opposed to an incremental update.

    embfile\_add(*name*, *buffer*, *filename=None*, *ufilename=None*, *desc=None*)
    :   - Changed in v1.14.16: The sequence of positional parameters “name” and “buffer” has been changed to comply with the call pattern of other functions.

        PDF only: Embed a new file. All string parameters except the name may be unicode (in previous versions, only ASCII worked correctly). File contents will be compressed (where beneficial).

        Parameters:
        :   - **name** (*str*) – entry identifier, **must not already exist**.
            - **buffer** (*bytes**,**bytearray**,**BytesIO*) –

              file contents.

              *(Changed in v1.14.13)* *io.BytesIO* is now also supported.
            - **filename** (*str*) – optional filename. Documentation only, will be set to *name* if `None`.
            - **ufilename** (*str*) – optional unicode filename. Documentation only, will be set to *filename* if `None`.
            - **desc** (*str*) – optional description. Documentation only, will be set to *name* if `None`.

        Return type:
        :   int

        Returns:
        :   *(Changed in v1.18.13)* The method now returns the [`xref`](glossary.html#xref "xref") of the inserted file. In addition, the file object now will be automatically given the PDF keys `/CreationDate` and `/ModDate` based on the current date-time.

    embfile\_count()
    :   - Changed in v1.14.16: This is now a method. In previous versions, this was a property.

        PDF only: Return the number of embedded files.

    embfile\_get(*item*)
    :   PDF only: Retrieve the content of embedded file by its entry number or name. If the document is not a PDF, or entry cannot be found, an exception is raised.

        Parameters:
        :   **item** (*int**,**str*) – index or name of entry. An integer must be in `range(embfile_count())`.

        Return type:
        :   bytes

    embfile\_del(*item*)
    :   - Changed in v1.14.16: Items can now be deleted by index, too.

        PDF only: Remove an entry from `/EmbeddedFiles`. As always, physical deletion of the embedded file content (and file space regain) will occur only when the document is saved to a new file with a suitable garbage option.

        Parameters:
        :   **item** (*int/str*) – index or name of entry.

        Warning

        When specifying an entry name, this function will only **delete the first item** with that name. Be aware that PDFs not created with PyMuPDF may contain duplicate names. So you may want to take appropriate precautions.

    embfile\_info(*item*)
    :   - Changed in v1.18.13

        PDF only: Retrieve information of an embedded file given by its number or by its name.

        Parameters:
        :   **item** (*int/str*) – index or name of entry. An integer must be in `range(embfile_count())`.

        Return type:
        :   dict

        Returns:
        :   a dictionary with the following keys:

            - `name` – (*str*) name under which this entry is stored
            - `filename` – (*str*) filename
            - `ufilename` – (*unicode*) filename
            - `description` – (*str*) description
            - `size` – (*int*) original file size
            - `length` – (*int*) compressed file length
            - `creationDate` – (*str*) date-time of item creation in PDF format
            - `modDate` – (*str*) date-time of last change in PDF format
            - `collection` – (*int*) [`xref`](glossary.html#xref "xref") of the associated PDF portfolio item if any, else zero.
            - `checksum` – (*str*) a hashcode of the stored file content as a hexadecimal string. Should be MD5 according to PDF specifications, but be prepared to see other hashing algorithms.

    embfile\_names()
    :   PDF only: Return a list of embedded file names. The sequence of the names equals the physical sequence in the document.

        Return type:
        :   list

    embfile\_upd(*item*, *buffer=None*, *filename=None*, *ufilename=None*, *desc=None*)
    :   PDF only: Change an embedded file given its entry number or name. All parameters are optional. Letting them default leads to a no-operation.

        Parameters:
        :   - **item** (*int/str*) – index or name of entry. An integer must be in `range(embfile_count())`.
            - **buffer** (*bytes**,**bytearray**,**BytesIO*) –

              the new file content.

              *(Changed in v1.14.13)* *io.BytesIO* is now also supported.
            - **filename** (*str*) – the new filename.
            - **ufilename** (*str*) – the new unicode filename.
            - **desc** (*str*) – the new description.

        *(Changed in v1.18.13)* The method now returns the [`xref`](glossary.html#xref "xref") of the file object.

        Return type:
        :   int

        Returns:
        :   xref of the file object. Automatically, its `/ModDate` PDF key will be updated with the current date-time.

    close()
    :   Release objects and space allocations associated with the document. If created from a file, also closes *filename* (releasing control to the OS). Explicitly closing a document is equivalent to deleting it, `del doc`, or assigning it to something else like `doc = None`.

    xref\_object(*xref*, *compressed=False*, *ascii=False*)
    :   - New in v1.16.8
        - Changed in v1.18.10

        PDF only: Return the definition source of a PDF object.

        Parameters:
        :   - **xref** (*int*) – the object’s [`xref`](glossary.html#xref "xref"). *Changed in v1.18.10:* A value of `-1` returns the PDF trailer source.
            - **compressed** (*bool*) – whether to generate a compact output with no line breaks or spaces.
            - **ascii** (*bool*) – whether to ASCII-encode binary data.

        Return type:
        :   str

        Returns:
        :   The object definition source.

    pdf\_catalog()
    :   - New in v1.16.8

        PDF only: Return the [`xref`](glossary.html#xref "xref") number of the PDF catalog (or root) object. Use that number with [`Document.xref_object()`](#Document.xref_object "Document.xref_object") to see its source.

    pdf\_trailer(*compressed=False*)
    :   - New in v1.16.8

        PDF only: Return the trailer source of the PDF, which is usually located at the PDF file’s end. This is [`Document.xref_object()`](#Document.xref_object "Document.xref_object") with an [`xref`](glossary.html#xref "xref") argument of -1.

    xref\_stream(*xref*)
    :   - New in v1.16.8

        PDF only: Return the **decompressed** contents of the [`xref`](glossary.html#xref "xref") stream object.

        Parameters:
        :   **xref** (*int*) – [`xref`](glossary.html#xref "xref") number.

        Return type:
        :   bytes

        Returns:
        :   the (decompressed) stream of the object.

    xref\_stream\_raw(*xref*)
    :   - New in v1.16.8

        PDF only: Return the **unmodified** (esp. **not decompressed**) contents of the [`xref`](glossary.html#xref "xref") stream object. Otherwise equal to [`Document.xref_stream()`](#Document.xref_stream "Document.xref_stream").

        Return type:
        :   bytes

        Returns:
        :   the (original, unmodified) stream of the object.

    update\_object(*xref*, *obj\_str*, *page=None*)
    :   - New in v1.16.8

        PDF only: Replace object definition of [`xref`](glossary.html#xref "xref") with the provided string. The xref may also be new, in which case this instruction completes the object definition. If a page object is also given, its links and annotations will be reloaded afterwards.

        Parameters:
        :   - **xref** (*int*) – [`xref`](glossary.html#xref "xref") number.
            - **obj\_str** (*str*) – a string containing a valid PDF object definition.
            - **page** ([Page](page.html#page)) – a page object. If provided, indicates, that annotations of this page should be refreshed (reloaded) to reflect changes incurred with links and / or annotations.

        Return type:
        :   int

        Returns:
        :   zero if successful, otherwise an exception will be raised.

    update\_stream(*xref*, *data*, *new=False*, *compress=True*)
    :   - New in v.1.16.8
        - Changed in v1.19.2: added parameter “compress”
        - Changed in v1.19.6: deprecated parameter “new”. Now confirms that the object is a PDF dictionary object.

        Replace the stream of an object identified by [`xref`](glossary.html#xref "xref"), which must be a PDF dictionary. If the object is no [`stream`](glossary.html#stream "stream"), it will be turned into one. The function automatically performs a compress operation (“deflate”) where beneficial.

        Parameters:
        :   - **xref** (*int*) – [`xref`](glossary.html#xref "xref") number.
            - **stream** (*bytes**|**bytearray**|**BytesIO*) –

              the new content of the stream.

              *(Changed in v1.14.13:)* *io.BytesIO* objects are now also supported.
            - **new** (*bool*) – *deprecated* and ignored. Will be removed some time after v1.20.0.
            - **compress** (*bool*) – whether to compress the inserted stream. If `True` (default), the stream will be inserted using `/FlateDecode` compression (if beneficial), otherwise the stream will inserted as is.

        Raises:
        :   **ValueError** – if [`xref`](glossary.html#xref "xref") does not represent a PDF `dict`. An empty dictionary `<<>>` is accepted. So if you just created the xref and want to give it a stream, first execute `doc.update_object(xref, "<<>>")`, and then insert the stream data with this method.

        The method is primarily (but not exclusively) intended to manipulate streams containing PDF operator syntax (see pp. 643 of the [Adobe PDF References](app3.html#adobemanual)) as it is the case for e.g. page content streams.

        If you update a contents stream, consider using save parameter *clean=True* to ensure consistency between PDF operator source and the object structure.

        Example: Let us assume that you no longer want a certain image appear on a page. This can be achieved by deleting the respective reference in its contents source(s) – and indeed: the image will be gone after reloading the page. But the page’s [`resources`](glossary.html#resources "resources") object would still show the image as being referenced by the page. This save option will clean up any such mismatches.

    xref\_copy(*source*, *target*, *\**, *keep=None*)
    :   - New in v1.19.5

        PDF Only: Make `target` xref an exact copy of `source`. If `source` is a [`stream`](glossary.html#stream "stream"), then this data is also copied.

        Parameters:
        :   - **source** (*int*) – the source [`xref`](glossary.html#xref "xref"). It must be an existing **dictionary** object.
            - **target** (*int*) – the target xref. Must be an existing **dictionary** object. If the xref has just been created, make sure to initialize it as a PDF dictionary with the minimum specification `<<>>`.
            - **keep** (*list*) – an optional list of top-level keys in `target`, that should not be removed in preparation of the copy process.

        Note

        - This method has much in common with Python’s *dict* method [`copy()`](pixmap.html#Pixmap.copy "Pixmap.copy").
        - Both xref numbers must represent existing dictionaries.
        - Before data is copied from *source*, all *target* dictionary keys are deleted. You can specify exceptions from this in the `keep` list. If *source* however has a same-named key, its value will still replace the target.
        - If `source` is a [`stream`](glossary.html#stream "stream") object, then these data will also be copied over, and `target` will be converted to a stream object.
        - A typical use case is to replace or remove an existing image without using redaction annotations. Example scripts can be seen [in this PyMuPDF Utilities example](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/replace-image).

    extract\_image(*xref*)
    :   PDF Only: Extract data and meta information of an image stored in the document. The output can directly be used to be stored as an image file, as input for PIL, [Pixmap](pixmap.html#pixmap) creation, etc. This method avoids using pixmaps wherever possible to present the image in its original format (e.g. as JPEG).

        Parameters:
        :   **xref** (*int*) – [`xref`](glossary.html#xref "xref") of an image object. If this is not in `range(1, doc.xref_length())`, or the object is no image or other errors occur, `None` is returned and no exception is raised.

        Return type:
        :   dict

        Returns:
        :   a dictionary with the following keys

            - *ext* (*str*) image type (e.g. *‘jpeg’*), usable as image file extension
            - *smask* (*int*) [`xref`](glossary.html#xref "xref") number of a stencil (/SMask) image or zero
            - `width` (*int*) image width
            - `height` (*int*) image height
            - *colorspace* (*int*) the image’s *colorspace.n* number.
            - *cs-name* (*str*) the image’s *colorspace.name*.
            - *xres* (*int*) resolution in x direction. Please also see [`resolution`](glossary.html#resolution "resolution").
            - *yres* (*int*) resolution in y direction. Please also see [`resolution`](glossary.html#resolution "resolution").
            - *image* (*bytes*) image data, usable as image file content

        ```
        >>> d = doc.extract_image(1373)
        >>> d
        {'ext': 'png', 'smask': 2934, 'width': 5, 'height': 629, 'colorspace': 3, 'xres': 96,
        'yres': 96, 'cs-name': 'DeviceRGB',
        'image': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x05\ ...'}
        >>> imgout = open(f"image.{d['ext']}", "wb")
        >>> imgout.write(d["image"])
        102
        >>> imgout.close()
        ```

        Note

        There is a functional overlap with *pix = pymupdf.Pixmap(doc, xref)*, followed by a *pix.tobytes()*. Main differences are that extract\_image, **(1)** does not always deliver PNG image formats, **(2)** is **very** much faster with non-PNG images, **(3)** usually results in much less disk storage for extracted images, **(4)** returns `None` in error cases (generates no exception). Look at the following example images within the same PDF.

        - xref 1268 is a PNG – Comparable execution time and identical output:

          ```
          In [23]: %timeit pix = pymupdf.Pixmap(doc, 1268);pix.tobytes()
          10.8 ms ± 52.4 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
          In [24]: len(pix.tobytes())
          Out[24]: 21462

          In [25]: %timeit img = doc.extract_image(1268)
          10.8 ms ± 86 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
          In [26]: len(img["image"])
          Out[26]: 21462
          ```
        - xref 1186 is a JPEG – [`Document.extract_image()`](#Document.extract_image "Document.extract_image") is **many times faster** and produces a **much smaller** output (2.48 MB vs. 0.35 MB):

          ```
          In [27]: %timeit pix = pymupdf.Pixmap(doc, 1186);pix.tobytes()
          341 ms ± 2.86 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
          In [28]: len(pix.tobytes())
          Out[28]: 2599433

          In [29]: %timeit img = doc.extract_image(1186)
          15.7 µs ± 116 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
          In [30]: len(img["image"])
          Out[30]: 371177
          ```

    extract\_font(*xref*, *info\_only=False*, *named=None*)
    :   - Changed in v1.19.4: return a dictionary if `named == True`.

        PDF Only: Return an embedded font file’s data and appropriate file extension. This can be used to store the font as an external file. The method does not throw exceptions (other than via checking for PDF and valid [`xref`](glossary.html#xref "xref")).

        Parameters:
        :   - **xref** (*int*) – PDF object number of the font to extract.
            - **info\_only** (*bool*) – only return font information, not the buffer. To be used for information-only purposes, avoids allocation of large buffer areas.
            - **named** (*bool*) – If true, a dictionary with the following keys is returned: ‘name’ (font base name), ‘ext’ (font file extension), ‘type’ (font type), ‘content’ (font file content).

        Return type:
        :   tuple,dict

        Returns:
        :   a tuple `(basename, ext, type, content)`, where *ext* is a 3-byte suggested file extension (*str*), *basename* is the font’s name (*str*), *type* is the font’s type (e.g. “Type1”) and *content* is a bytes object containing the font file’s content (or *b””*). For possible extension values and their meaning see [Font File Extensions](vars.html#fontextensions). Return details on error:

            - `("", "", "", b"")` – invalid xref or xref is not a (valid) font object.
            - `(basename, "n/a", "Type1", b"")` – *basename* is not embedded and thus cannot be extracted. This is the case for e.g. the [PDF Base 14 Fonts](app3.html#base-14-fonts) and Type 3 fonts.

        Example:

        ```
        >>> # store font as an external file
        >>> name, ext, _, content = doc.extract_font(4711)
        >>> # assuming content is not None:
        >>> ofile = open(name + "." + ext, "wb")
        >>> ofile.write(content)
        >>> ofile.close()
        ```

        Warning

        The basename is returned unchanged from the PDF. So it may contain characters (such as blanks) which may disqualify it as a filename for your operating system. Take appropriate action.

        Note

        - The returned *basename* in general is **not** the original file name, but it probably has some similarity.
        - If parameter `named == True`, a dictionary with the following keys is returned: `{'name': 'T1', 'ext': 'n/a', 'type': 'Type3', 'content': b''}`.

    xref\_xml\_metadata()
    :   - New in v1.16.8

        PDF only: Return the [`xref`](glossary.html#xref "xref") of the document’s XML metadata.

    has\_links()

    has\_annots()
    :   - New in v1.18.7

        PDF only: Check whether there are links, resp. annotations anywhere in the document.

        Returns:
        :   `True` / `False`. As opposed to fields, which are also stored in a central place of a PDF document, the existence of links / annotations can only be detected by parsing each page. These methods are tuned to do this efficiently and will immediately return, if the answer is `True` for a page. For PDFs with many thousand pages however, an answer may take some time [[6]](#f6) if no link, resp. no annotation is found.

    subset\_fonts(*verbose=False*, *fallback=False*)
    :   PDF only: Investigate eligible fonts for their use by text in the document. If a font is supported and a size reduction is possible, that font is replaced by a version with a subset of its characters.

        Use this method immediately before saving the document.

        Parameters:
        :   - **verbose** (*bool*) – write various progress information to sysout. This currently only has an effect if `fallback` is `True`.
            - **fallback** (*bool*) – if `True` use the deprecated algorithm that makes use of package [fontTools](https://pypi.org/project/fonttools/) (which hence must be installed). If using the recommended value `False` (default), MuPDF’s native function is used – which is **very much faster** and can subset a broader range of font types. Package fontTools is not required then.

        The greatest benefit can be achieved when creating new PDFs using large fonts like is typical for Asian scripts. When using the [Story](story-class.html#story) class or method [`Page.insert_htmlbox()`](page.html#Page.insert_htmlbox "Page.insert_htmlbox"), multiple fonts may automatically be included – without the programmer becoming aware of it.

        In all these cases, the set of actually used unicodes mostly is very small compared to the number of glyphs available in the used fonts. Using this method can easily reduce the embedded font binaries by two orders of magnitude – from several megabytes down to a low two-digit kilobyte amount.

        Creating font subsets leaves behind a large number of large, now unused PDF objects (“ghosts”). Therefore, make sure to compress and garbage-collect when saving the file. We recommend to use [`Document.ez_save()`](#Document.ez_save "Document.ez_save").

        Show/hide history

        - New in v1.18.7
        - Changed in v1.18.9
        - Changed in v1.24.2 use native function of MuPDF.

    journal\_enable()
    :   - New in v1.19.0

        PDF only: Enable journalling. Use this before you start logging operations.

    journal\_start\_op(*name*)
    :   - New in v1.19.0

        PDF only: Start journalling an *“operation”* identified by a string “name”. Updates will fail for a journal-enabled PDF, if no operation has been started.

    journal\_stop\_op()
    :   - New in v1.19.0

        PDF only: Stop the current operation. The updates between start and stop of an operation belong to the same unit of work and will be undone / redone together.

    journal\_position()
    :   - New in v1.19.0

        PDF only: Return the numbers of the current operation and the total operation count.

        Returns:
        :   a tuple `(step, steps)` containing the current operation number and the total number of operations in the journal. If **step** is 0, we are at the top of the journal. If **step** equals **steps**, we are at the bottom. Updating the PDF with anything other than undo or redo will automatically remove all journal entries after the current one and the new update will become the new last entry in the journal. The updates corresponding to the removed journal entries will be permanently lost.

    journal\_op\_name(*step*)
    :   - New in v1.19.0

        PDF only: Return the name of operation number *step.*

    journal\_can\_do()
    :   - New in v1.19.0

        PDF only: Show whether forward (“redo”) and / or backward (“undo”) executions are possible from the current journal position.

        Returns:
        :   a dictionary `{"undo": bool, "redo": bool}`. The respective method is available if its value is `True`.

    journal\_undo()
    :   - New in v1.19.0

        PDF only: Revert (undo) the current step in the journal. This moves towards the journal’s top.

    journal\_redo()
    :   - New in v1.19.0

        PDF only: Re-apply (redo) the current step in the journal. This moves towards the journal’s bottom.

    journal\_save(*filename*)
    :   - New in v1.19.0

        PDF only: Save the journal to a file.

        Parameters:
        :   **filename** (*str**,**fp*) – either a filename as string or a file object opened as “wb” (or an `io.BytesIO()` object).

    journal\_load(*filename*)
    :   - New in v1.19.0

        PDF only: Load journal from a file. Enables journalling for the document. If journalling is already enabled, an exception is raised.

        Parameters:
        :   **filename** (*str**,**fp*) – the filename (str) of the journal or a file object opened as “rb” (or an `io.BytesIO()` object).

    save\_snapshot()
    :   - New in v1.19.0

        PDF only: Saves a “snapshot” of the document. This is a PDF document with a special, incremental-save format compatible with journalling – therefore no save options are available. Saving a snapshot is not possible for new documents.

        This is a normal PDF document with no usage restrictions whatsoever. If it is not being changed in any way, it can be used together with its journal to undo / redo operations or continue updating.

    outline
    :   Contains the first [Outline](outline.html#outline) entry of the document (or `None`). Can be used as a starting point to walk through all outline items. Accessing this property for encrypted, not authenticated documents will raise an *AttributeError*.

        Type:
        :   [Outline](outline.html#outline)

    is\_closed
    :   `False` if document is still open. If closed, most other attributes and methods will have been deleted / disabled. In addition, [Page](page.html#page) objects referring to this document (i.e. created with [`Document.load_page()`](#Document.load_page "Document.load_page")) and their dependent objects will no longer be usable. For reference purposes, [`Document.name`](#Document.name "Document.name") still exists and will contain the filename of the original document (if applicable).

        Type:
        :   bool

    is\_dirty
    :   `True` if this is a PDF document and contains unsaved changes, else `False`.

        Type:
        :   bool

    is\_pdf
    :   `True` if this is a PDF document, else `False`.

        Type:
        :   bool

    is\_form\_pdf
    :   `False` if this is not a PDF or has no form fields, otherwise the number of root form fields (fields with no ancestors).

        *(Changed in v1.16.4)* Returns the total number of (root) form fields.

        Type:
        :   bool,int

    is\_reflowable
    :   `True` if document has a variable page layout (like e-books or HTML). In this case you can set the desired page dimensions during document creation (open) or via method [`layout()`](#Document.layout "Document.layout").

        Type:
        :   bool

    is\_repaired
    :   - New in v1.18.2

        `True` if PDF has been repaired during open (because of major structure issues). Always `False` for non-PDF documents. If true, more details have been stored in `TOOLS.mupdf_warnings()`, and [`Document.can_save_incrementally()`](#Document.can_save_incrementally "Document.can_save_incrementally") will return `False`.

        Type:
        :   bool

    is\_fast\_webaccess
    :   - New in v1.22.2

        `True` if PDF is in linearized format. `False` for non-PDF documents.

        Type:
        :   bool

    markinfo
    :   - New in v1.22.2

        A dictionary indicating the `/MarkInfo` value. If not specified, the empty dictionary is returned. If not a PDF, `None` is returned.

        Type:
        :   dict

    pagemode
    :   - New in v1.22.2

        A string containing the `/PageMode` value. If not specified, the default “UseNone” is returned. If not a PDF, `None` is returned.

        Type:
        :   str

    pagelayout
    :   - New in v1.22.2

        A string containing the `/PageLayout` value. If not specified, the default “SinglePage” is returned. If not a PDF, `None` is returned.

        Type:
        :   str

    version\_count
    :   - New in v1.22.2

        An integer counting the number of versions present in the document. Zero if not a PDF, otherwise the number of incremental saves plus one.

        Type:
        :   int

    needs\_pass
    :   Indicates whether the document is password-protected against access. This indicator remains unchanged – **even after the document has been authenticated**. Precludes incremental saves if true.

        Type:
        :   bool

    is\_encrypted
    :   This indicator initially equals [`Document.needs_pass`](#Document.needs_pass "Document.needs_pass"). After successful authentication, it is set to `False` to reflect the situation.

        Type:
        :   bool

    permissions
    :   - Changed in v1.16.0: This is now an integer comprised of bit indicators. Was a dictionary previously.

        Contains the permissions to access the document. This is an integer containing bool values in respective bit positions. For example, if *doc.permissions & pymupdf.PDF\_PERM\_MODIFY > 0*, you may change the document. See [Document Permissions](vars.html#permissioncodes) for details.

        Type:
        :   int

    metadata
    :   Contains the document’s meta data as a Python dictionary or `None` (if *is\_encrypted=True* and *needPass=True*). Keys are *format*, *encryption*, *title*, *author*, *subject*, *keywords*, *creator*, *producer*, *creationDate*, *modDate*, *trapped*. All item values are strings or `None`.

        Except *format* and *encryption*, for PDF documents, the key names correspond in an obvious way to the PDF keys */Creator*, */Producer*, */CreationDate*, */ModDate*, */Title*, */Author*, */Subject*, */Trapped* and */Keywords* respectively.

        - *format* contains the document format (e.g. ‘PDF-1.6’, ‘XPS’, ‘EPUB’).
        - *encryption* either contains `None` (no encryption), or a string naming an encryption method (e.g. *‘Standard V4 R4 128-bit RC4’*). Note that an encryption method may be specified **even if** *needs\_pass=False*. In such cases not all permissions will probably have been granted. Check [`Document.permissions`](#Document.permissions "Document.permissions") for details.
        - If the date fields contain valid data (which need not be the case at all!), they are strings in the PDF-specific timestamp format “D:<TS><TZ>”, where

          > - <TS> is the 12 character ISO timestamp *YYYYMMDDhhmmss* (*YYYY* - year, *MM* - month, *DD* - day, *hh* - hour, *mm* - minute, *ss* - second), and
          > - <TZ> is a time zone value (time interval relative to GMT) containing a sign (‘+’ or ‘-‘), the hour (*hh*), and the minute (*‘mm’*, note the apostrophes!).
        - A Paraguayan value might hence look like *D:20150415131602-04’00’*, which corresponds to the timestamp April 15, 2015, at 1:16:02 pm local time Asuncion.

        Type:
        :   dict

    name
    :   Contains the *filename* or *filetype* value with which *Document* was created.

        Type:
        :   str

    page\_count
    :   Contains the number of pages of the document. May return 0 for documents with no pages. Function `len(doc)` will also deliver this result.

        Type:
        :   int

    chapter\_count
    :   - New in v1.17.0

        Contains the number of chapters in the document. Always at least 1. Relevant only for document types with chapter support (EPUB currently). Other documents will return 1.

        Type:
        :   int

    last\_location
    :   - New in v1.17.0

        Contains (chapter, pno) of the document’s last page. Relevant only for document types with chapter support (EPUB currently). Other documents will return `(0, page_count - 1)` and `(0, -1)` if it has no pages.

        Type:
        :   int

    FormFonts
    :   A list of form field font names defined in the */AcroForm* object. `None` if not a PDF.

        Type:
        :   list

Note

For methods that change the structure of a PDF (`insert_pdf()`, `select()`, `copy_page()`, `delete_page()` and others), be aware that objects or properties in your program may have been invalidated or orphaned. Examples are [Page](page.html#page) objects and their children (links, annotations, widgets), variables holding old page counts, tables of content and the like. Remember to keep such variables up to date or delete orphaned objects. Also refer to [Ensuring Consistency of Important Objects in PyMuPDF](app3.html#referenialintegrity).

## `set_metadata()` Example

Clear metadata information. If you do this out of privacy / data protection concerns, make sure you save the document as a new file with *garbage > 0*. Only then the old */Info* object will also be physically removed from the file. In this case, you may also want to clear any XML metadata inserted by several PDF editors:

```
>>> import pymupdf
>>> doc=pymupdf.open("pymupdf.pdf")
>>> doc.metadata             # look at what we currently have
{'producer': 'rst2pdf, reportlab', 'format': 'PDF 1.4', 'encryption': None, 'author':
'Jorj X. McKie', 'modDate': "D:20160611145816-04'00'", 'keywords': 'PDF, XPS, EPUB, CBZ',
'title': 'The PyMuPDF Documentation', 'creationDate': "D:20160611145816-04'00'",
'creator': 'sphinx', 'subject': 'PyMuPDF 1.9.1'}
>>> doc.set_metadata({})      # clear all fields
>>> doc.metadata             # look again to show what happened
{'producer': 'none', 'format': 'PDF 1.4', 'encryption': None, 'author': 'none',
'modDate': 'none', 'keywords': 'none', 'title': 'none', 'creationDate': 'none',
'creator': 'none', 'subject': 'none'}
>>> doc.del_xml_metadata()    # clear any XML metadata
>>> doc.save("anonymous.pdf", garbage = 4)       # save anonymized doc
```

## `set_toc()` Demonstration

This shows how to modify or add a table of contents. Also have a look at [import.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/import-toc/import.py) and [export.py](https://github.com/pymupdf/PyMuPDF-Utilities/tree/master/examples/export-toc/export.py) in the examples directory.

```
>>> import pymupdf
>>> doc = pymupdf.open("test.pdf")
>>> toc = doc.get_toc()
>>> for t in toc: print(t)                           # show what we have
[1, 'The PyMuPDF Documentation', 1]
[2, 'Introduction', 1]
[3, 'Note on the Name fitz', 1]
[3, 'License', 1]
>>> toc[1][1] += " modified by set_toc"               # modify something
>>> doc.set_toc(toc)                                  # replace outline tree
3                                                    # number of bookmarks inserted
>>> for t in doc.get_toc(): print(t)                  # demonstrate it worked
[1, 'The PyMuPDF Documentation', 1]
[2, 'Introduction modified by set_toc', 1]            # <<< this has changed
[3, 'Note on the Name fitz', 1]
[3, 'License', 1]
```

## `insert_pdf()` Examples

**(1) Concatenate two documents including their TOCs:**

```
>>> doc1 = pymupdf.open("file1.pdf")          # must be a PDF
>>> doc2 = pymupdf.open("file2.pdf")          # must be a PDF
>>> pages1 = len(doc1)                     # save doc1's page count
>>> toc1 = doc1.get_toc(False)     # save TOC 1
>>> toc2 = doc2.get_toc(False)     # save TOC 2
>>> doc1.insert_pdf(doc2)                   # doc2 at end of doc1
>>> for t in toc2:                         # increase toc2 page numbers
        t[2] += pages1                     # by old len(doc1)
>>> doc1.set_toc(toc1 + toc2)               # now result has total TOC
```

Obviously, similar ways can be found in more general situations. Just make sure that hierarchy levels in a row do not increase by more than one. Inserting dummy bookmarks before and after *toc2* segments would heal such cases. A ready-to-use GUI (wxPython) solution can be found in script [join.py](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/join-documents/join.py) of the examples directory.

**(2) More examples:**

```
>>> # insert 5 pages of doc2, where its page 21 becomes page 15 in doc1
>>> doc1.insert_pdf(doc2, from_page=21, to_page=25, start_at=15)
```

```
>>> # same example, but pages are rotated and copied in reverse order
>>> doc1.insert_pdf(doc2, from_page=25, to_page=21, start_at=15, rotate=90)
```

```
>>> # put copied pages in front of doc1
>>> doc1.insert_pdf(doc2, from_page=21, to_page=25, start_at=0)
```

## Other Examples

**Extract all page-referenced images of a PDF into separate PNG files**:

```
for i in range(doc.page_count):
    imglist = doc.get_page_images(i)
    for img in imglist:
        xref = img[0]                  # xref number
        pix = pymupdf.Pixmap(doc, xref)   # make pixmap from image
        if pix.n - pix.alpha < 4:      # can be saved as PNG
            pix.save(f"p{i}-{xref}.png")
        else:                          # CMYK: must convert first
            pix0 = pymupdf.Pixmap(pymupdf.csRGB, pix)
            pix0.save(f"p{i}-{xref}.png")
            pix0 = None                # free Pixmap resources
        pix = None                     # free Pixmap resources
```

**Rotate all pages of a PDF:**

```
>>> for page in doc: page.set_rotation(90)
```

Footnotes

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.