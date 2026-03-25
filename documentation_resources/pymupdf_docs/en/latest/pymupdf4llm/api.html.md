<!-- Source: https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/api.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# The PyMuPDF4LLM API

*property* version
:   Prints the version of the library.

to\_markdown(*doc: pymupdf.Document | str*, *\**, *detect\_bg\_color: bool = True*, *dpi: int = 150*, *embed\_images: bool = False*, *extract\_words: bool = False*, *filename: str | None = None*, *fontsize\_limit: float = 3*, *footer: bool = True*, *force\_ocr: bool = False*, *force\_text: bool = True*, *graphics\_limit: int = None*, *hdr\_info: Any = None*, *header: bool = True*, *ignore\_alpha: bool = False*, *ignore\_code: bool = False*, *ignore\_graphics: bool = False*, *ignore\_images: bool = False*, *image\_format: str = 'png'*, *image\_path: str = ''*, *image\_size\_limit: float = 0.05*, *margins: float | list = 0*, *ocr\_dpi: int = 300*, *ocr\_function: callable = None*, *ocr\_language: str = 'eng'*, *page\_chunks: bool = False*, *page\_height: float = None*, *page\_separators: bool = False*, *page\_width: float = 612*, *pages: list | range | None = None*, *show\_progress: bool = False*, *table\_strategy: str = 'lines\_strict'*, *use\_glyphs: bool = False*, *use\_ocr: bool = True*, *write\_images: bool = False*) → str | list[dict]
:   Reads the pages of the file and outputs the text of its pages in Markdown format. How this should happen in detail can be influenced by a number of parameters. Please note that **support for building page chunks** from the Markdown text is supported.

    Parameters:
    :   - **doc** ([*Document*](../document.html#Document "Document")*,**str*) – the file, to be specified either as a file path string, or as a PyMuPDF [`Document`](../document.html#Document "Document") (created via `pymupdf.open`). In order to use `pathlib.Path` specifications, Python file-like objects, documents in memory etc. you **must** use a PyMuPDF [`Document`](../document.html#Document "Document").
        - **detect\_bg\_color** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False does a simple check for the general background color of the pages (default is `True`). If any text or vector has this color it will be ignored. May increase detection accuracy.
        - **dpi** (*int*) – specify the desired image resolution in dots per inch. Relevant only if `write_images=True` or `embed_images=True`. Default value is 150.
        - **embed\_images** (*bool*) – like `write_images`, but images will be included in the markdown text as base64-encoded strings. Mutually exclusive with `write_images` and ignores `image_path`. This may drastically increase the size of your markdown text.
        - **extract\_words** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False a value of `True` enforces `page_chunks=True` and adds key “words” to each page dictionary. Its value is a list of words as delivered by PyMuPDF’s [Page](../page.html#page) method `get_text("words")`. The sequence of the words in this list is the same as the extracted text.
        - **filename** (*str*) – Overwrites or sets the desired image file name of written images. Useful when the document is provided as a memory object (which has no inherent file name).
        - **fontsize\_limit** (*float*) – [use\_layout()](#pymupdf4llm-api-layout) must be False limit the font size to consider for text extraction. If the font size is lower than what is set then the text won’t be considered for extraction. Default is `3`, meaning only text with a font size `>= 3` will be considered for extraction.
        - **footer** (*bool*) –  boolean to switch on/off page footer content. This parameter controls whether to include or omit footer text from all the document pages. Useful if the document has repetitive footer content which doesn’t add any value to the overall extraction data. Default is `True` meaning that footer content will be considered.
        - **force\_ocr** (*bool*) –

          if `True`, OCR will be applied to all pages regardless of their content.

          This may be useful for documents which are known to be image-based and thus profit from OCR, but which do not meet the default criteria for applying OCR. Default is `False` meaning that OCR will only be applied to pages which meet the default criteria.

          Warning

          Requires that either one of the default supported OCR engines is installed or `ocr_function` specifies a callable OCR function. Otherwise, an exception will be raised.
        - **force\_text** (*bool*) – generate text output even when overlapping images / graphics. This text then appears after the respective image.
        - **graphics\_limit** (*int*) – [use\_layout()](#pymupdf4llm-api-layout) must be False use this to limit dealing with excess amounts of vector graphics elements. Scientific documents, or pages simulating text via graphics commands may contain tens of thousands of these objects. As vector graphics are analyzed for multiple purposes, runtime may quickly become intolerable. With this parameter, all vector graphics will be ignored if their count exceeds the threshold.
        - **hdr\_info** – [use\_layout()](#pymupdf4llm-api-layout) must be False use this if you want to provide your own header detection logic. This may be a callable or an object having a method named [`get_header_id`](#IdentifyHeaders.get_header_id "IdentifyHeaders.get_header_id"). It must accept a text span (a span dictionary as contained in [`extractDICT()`](../textpage.html#TextPage.extractDICT "TextPage.extractDICT")) and a keyword parameter “page” (which is the owning [Page](../page.html#page) object). It must return a string “” or up to 6 “#” characters followed by 1 space. If omitted (`None`), a full document scan will be performed to find the most popular font sizes and derive header levels based on them. To completely avoid this behavior specify `hdr_info=lambda s, page=None: ""` or `hdr_info=False`.
        - **header** (*bool*) –  boolean to switch on/off page header content. This parameter controls whether we want to include or omit the header content from all the document pages. Useful if the document has repetitive header content which doesn’t add any value to the overall extraction data. Default is `True` meaning that header content will be considered.
        - **ignore\_alpha** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False if `True` includes text even when completely transparent. Default is `False`: transparent text will be ignored which usually increases detection accuracy.
        - **ignore\_code** (*bool*) – if `True` then mono-spaced text lines do not receive special formatting. Code blocks will no longer be generated. This value is set to `True` if `extract_words=True` is used.
        - **ignore\_graphics** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False (New in v.0.0.20) Disregard vector graphics on the page. This may help detecting text correctly when pages are very crowded (often the case for documents representing presentation slides). Also speeds up processing time. This automatically prevents table detection.
        - **ignore\_images** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False (New in v.0.0.20) Disregard images on the page. This may help detecting text correctly when pages are very crowded (often the case for documents representing presentation slides). Also speeds up processing time.
        - **image\_format** (*str*) – specify the desired image format via its extension. Default is “png” (portable network graphics). Another popular format may be “jpg”. Possible values are all [supported output formats](../how-to-open-a-file.html#supported-file-types).
        - **image\_path** (*str*) – store images in this folder. Relevant if `write_images=True`. Default is the path of the script directory.
        - **image\_size\_limit** (*float*) – [use\_layout()](#pymupdf4llm-api-layout) must be False this must be a `0 <= value < 1`. Images are ignored if `width / page.rect.width <= image_size_limit` or `height / page.rect.height <= image_size_limit`. For instance, the default value 0.05 means that to be considered for inclusion, an image’s width and height must be larger than 5% of the page’s width and height, respectively.
        - **margins** (*float**,**list*) –

          [use\_layout()](#pymupdf4llm-api-layout) must be False a float or a sequence of 2 or 4 floats specifying page borders. Only objects inside the margins will be considered for output.

          - `margin=f` yields `(f, f, f, f)` for `(left, top, right, bottom)`.
          - `(top, bottom)` yields `(0, top, 0, bottom)`.
          - To always read full pages **(default)**, use `margins=0`.
        - **ocr\_dpi** (*int*) –  specify the desired image resolution in dots per inch for applying OCR to the intermediate image of the page. Default value is 300. Only relevant if the page has been determined to profit from OCR (no or few text, most of the page covered by images or character-like vectors, etc.). Larger values do not usually increase the OCR precision. There also is a risk of over-sharpening the image which may decrease OCR precision. So the default value should probably be sufficiently high - in many cases you should see satisfactory results already with values of 150 or 200. Be aware that processing time and memory requirements grow quadratically with this value (an O(ocr\_dpi²) impact).
        - **ocr\_function** (*callable*) –  if you want to provide your own OCR function, specify it here. If omitted (`None`), one of the available built-in OCR engines will be used.
        - **ocr\_language** (*str*) –  specify the language to be used by the Tesseract OCR engine. Default is “eng” (English). Make sure that the respective language data files are installed. Remember to use correct Tesseract language codes. Multiple languages can be specified by concatenating the respective codes with a plus sign “+”, for example “eng+deu” for English and German.
        - **page\_chunks** (*bool*) –

          if `True` the output will be a list of [`Document.page_count`](../document.html#Document.page_count "Document.page_count") dictionaries (one per page). Each dictionary has the following structure:

          - **”metadata”** - a dictionary consisting of the document’s metadata [`Document.metadata`](../document.html#Document.metadata "Document.metadata"), enriched with additional keys **“file\_path”** (the file name), **“page\_count”** (number of pages in document), and **“page\_number”** (1-based page number).
          - **”toc\_items”** - a list of Table of Contents items pointing to this page. Each item of this list has the format `[lvl, title, pagenumber]`, where `lvl` is the hierarchy level, [`title`](../outline.html#Outline.title "Outline.title") a string and `pagenumber` as a 1-based page number.
          - **”tables”** - Only if [use\_layout()](#pymupdf4llm-api-layout) is False a list of tables on this page. Each item is a dictionary with keys “bbox”, “row\_count” and “col\_count”. Key “bbox” is a `pymupdf.Rect` in tuple format of the table’s position on the page.
          - **”images”** - Only if [use\_layout()](#pymupdf4llm-api-layout) is False a list of images on the page. This a copy of page method [`Page.get_image_info()`](../page.html#Page.get_image_info "Page.get_image_info").
          - **”graphics”** - Only if [use\_layout()](#pymupdf4llm-api-layout) is False a list of vector graphics rectangles on the page. This is a list of boundary boxes of clustered vector graphics as delivered by method [`Page.cluster_drawings()`](../page.html#Page.cluster_drawings "Page.cluster_drawings").
          - **”text”** - page content as Markdown text.
          - **”words”** - Only if [use\_layout()](#pymupdf4llm-api-layout) is False if `extract_words=True` was used. This is a list of tuples `(x0, y0, x1, y1, "wordstring", bno, lno, wno)` as delivered by `page.get_text("words")`. The **sequence** of these tuples however is the same as produced in the markdown text string and thus honors multi-column text. This is also true for text in tables: words are extracted in the sequence of table row cells.
          - **”text”** - page content as Markdown text.
          - **”page\_boxes”** -  a list of dictionaries representing the layout boundary boxes. Each dictionary has the following structure:

            ```
            {
                "index": int,              # 0-based integer index of the box in reading sequence
                "class": str,              # one of "text", "picture", "table", etc.
                "bbox": [x0, y0, x1, y1],  # boundary box coordinates
                "pos": (start, stop),      # 0-based integers: bbox_text = chunk["text"][start:stop]
            }
            ```
        - **page\_height** (*float*) – specify a desired page height. For relevance see the `page_width` parameter. If using the default `None`, the document will appear as one large page with a width of `page_width`. Consequently in this case, no markdown page separators will occur (except the final one), respectively only one page chunk will be returned.
        - **page\_separators** (*bool*) – if `True` inserts a string `--- end of page=n ---` at the end of each page output. Intended for debugging purposes. The page number is 0-based. The separator string is wrapped with line breaks. Default is `False`.
        - **page\_width** (*float*) – specify a desired page width. This is ignored for documents with a fixed page width like PDF, XPS etc. **Reflowable** documents however, like e-books, office [[2]](#f2) or text files have no fixed page dimensions. They by default are assumed to have Letter format width (612) and an **unlimited** page height. This means that the **full document is treated as one large page.**
        - **pages** (*list*) – optional, the pages to consider for output (caution: specify 0-based page numbers). If omitted (`None`) all pages are processed. Any Python sequence with integer items is accepted. The sequence is sorted and processed to only contain unique items.
        - **show\_progress** (*bool*) – Default is `False`. A value of `True` displays a progress bar as pages are being converted. Package [tqdm](https://pypi.org/project/tqdm/) is used if installed, otherwise the built-in text based progress bar is used.
        - **table\_strategy** (*str*) – [use\_layout()](#pymupdf4llm-api-layout) must be False see: [`table detection strategy`](../page.html#Page.find_tables "Page.find_tables"). Default is `"lines_strict"` which ignores background colors. In some occasions, other strategies may be more successful, for example `"lines"` which uses all vector graphics objects for detection.
        - **use\_glyphs** (*bool*) – [use\_layout()](#pymupdf4llm-api-layout) must be False (New in v.0.0.19) Default is `False`. A value of `True` will use the glyph number of the characters instead of the character itself if the font does not store the Unicode value.
        - **use\_ocr** (*bool*) –  use OCR capability to help analyse the page. This will OCR pages as determined by the default criteria.
        - **write\_images** (*bool*) –

          when encountering images or vector graphics, images will be created from the respective page area and stored in the specified folder. Markdown references will be generated pointing to these images. Any text contained in these areas will not be included in the text output (but appear as part of the images). Therefore, if for instance your document has text written on full page images, make sure to set this parameter to `False`.

          If using PyMuPDF Layout, boundary boxes that are classified as “picture” by the layout module will be treated as images - independent from the mixture of text, images or vector graphics they may be covering. If `force_text=True` is used, text will still be extracted from these areas and included in the output after the respective image reference.

    Returns:
    :   Either a string of the combined text of all selected document pages, or a list of dictionaries if `page_chunks=True`.

to\_text(*doc: pymupdf.Document | str*, *\**, *\*\*kwargs*) → str
:   Reads the pages of the file and outputs the text of its pages in plain text (TXT) format.

    Parameters:
    :   - **doc** ([*Document*](../document.html#Document "Document")*,**str*) – the file, to be specified either as a file path string, or as a PyMuPDF [`Document`](../document.html#Document "Document") (created via `pymupdf.open`). In order to use `pathlib.Path` specifications, Python file-like objects, documents in memory etc. you **must** use a PyMuPDF [`Document`](../document.html#Document "Document").
        - **use\_ocr** (*bool*) –  use OCR capability to help analyse the page.
        - **ocr\_language** (*str*) –  specify the language to be used by the Tesseract OCR engine. Default is “eng” (English). Make sure that the respective language data files are installed. Remember to use correct Tesseract language codes. Multiple languages can be specified by concatenating the respective codes with a plus sign “+”, for example “eng+deu” for English and German.
        - **ocr\_dpi** (*int*) –  specify the desired image resolution in dots per inch for applying OCR to the intermediate image of the page. Default value is 400. Only relevant if the page has been determined to profit from OCR (no or few text, most of the page covered by images or character-like vectors, etc.). Large values may increase the OCR precision but increase memory requirements and processing time. There also is a risk of over-sharpening the image which may decrease OCR precision. So the default value should probably be sufficiently high.
        - **header** (*bool*) – boolean to switch on/off page header content. This parameter controls whether to include or omit the header content from all the document pages. Useful if the document has repetitive header content which doesn’t add any value to the overall extraction data. Default is `True` meaning that header content will be written.
        - **footer** (*bool*) – boolean to switch on/off page footer content. This parameter controls whether to include or omit the footer content from all the document pages. Useful if the document has repetitive footer content which doesn’t add any value to the overall extraction data. Default is `True` meaning that footer content will be written.
        - **ignore\_code** (*bool*) – if `True` then mono-spaced text lines do not receive special formatting. No blocks will be written and text lines will be written continuously.
        - **pages** (*list*) – optional, the pages to consider for output (caution: specify 0-based page numbers). If omitted (`None`) all pages are processed. Any Python sequence with integer items is accepted. The sequence is sorted and processed to only contain unique items.
        - **force\_text** (*bool*) – generate text output also when overlapping images / graphics. This text then appears after the respective image reference. Images (i.e. “picture” areas) however will not be written to the text output but appear as a text line in the output like `==> picture [width x height] <==`.
        - **show\_progress** (*bool*) –

          Default is `False`. A value of `True` displays a progress bar as pages are being converted. Package [tqdm](https://pypi.org/project/tqdm/) is used if installed, otherwise the built-in text based progress bar is used.
        - **page\_chunks** (*bool*) –

          if `True` the output will be a list of [`Document.page_count`](../document.html#Document.page_count "Document.page_count") dictionaries (one per page). Each dictionary has the following structure:

          - **”metadata”** - a dictionary consisting of the document’s metadata [`Document.metadata`](../document.html#Document.metadata "Document.metadata"), enriched with additional keys **“file\_path”** (the file name), **“page\_count”** (number of pages in document), and **“page\_number”** (1-based page number).
          - **”toc\_items”** - a list of Table of Contents items pointing to this page. Each item of this list has the format `[lvl, title, pagenumber]`, where `lvl` is the hierarchy level, [`title`](../outline.html#Outline.title "Outline.title") a string and `pagenumber` as a 1-based page number.
          - **”tables”** - empty list.
          - **”images”** - empty list.
          - **”graphics”** - empty list.
          - **”words”** - empty list.
          - **”text”** - page content as plain text.
          - **”page\_boxes”** - a list of dictionaries representing the layout boundary boxes. Each dictionary has the following structure:

            ```
            {
                "index": int,              # 0-based integer index of the box in reading sequence
                "class": str,              # one of "text", "picture", "table", etc.
                "bbox": [x0, y0, x1, y1],  # boundary box coordinates
                "pos": (start, stop),      # 0-based integers: bbox_text = chunk["text"][start:stop]
            }
            ```

to\_json(*doc: pymupdf.Document | str*, *\**, *\*\*kwargs*) → str
:   Parses the document and the specified pages and converts the result into a JSON-formatted string.

    Parameters:
    :   - **doc** ([*Document*](../document.html#Document "Document")*,**str*) – the file, to be specified either as a file path string, or as a PyMuPDF [`Document`](../document.html#Document "Document") (created via `pymupdf.open`). In order to use `pathlib.Path` specifications, Python file-like objects, documents in memory etc. you **must** use a PyMuPDF [`Document`](../document.html#Document "Document").
        - **use\_ocr** (*bool*) –  use OCR capability to help analyse the page.
        - **ocr\_language** (*str*) –  specify the language to be used by the Tesseract OCR engine. Default is “eng” (English). Make sure that the respective language data files are installed. Remember to use correct Tesseract language codes. Multiple languages can be specified by concatenating the respective codes with a plus sign “+”, for example “eng+deu” for English and German.
        - **ocr\_dpi** (*int*) –  specify the desired image resolution in dots per inch for applying OCR to the intermediate image of the page. Default value is 400. Only relevant if the page has been determined to profit from OCR (no or few text, most of the page covered by images or character-like vectors, etc.). Large values may increase the OCR precision but increase memory requirements and processing time. There also is a risk of over-sharpening the image which may decrease OCR precision. So the default value should probably be sufficiently high.
        - **image\_dpi** (*int*) – specify the desired image resolution in dots per inch. Default value is 150. Only relevant if one of the parameters `write_images=True` or `embed_images=True` is used.
        - **image\_format** (*str*) – specify the desired image format via its extension. Default is “png” (portable network graphics). Another popular format may be “jpg”. Possible values are all [supported output formats](../how-to-open-a-file.html#supported-file-types). Only relevant if one of the parameters `write_images=True` or `embed_images=True` is used.
        - **image\_path** (*str*) – store images in this folder. Relevant if `write_images=True`. Default is the path of the script directory. Page areas classified as “picture” will be written as image files to the specified location. The image file names will be of the format `{image_path}/{filename}-pagenumber-image_number.{image_format}`.
        - **force\_text** (*bool*) – generate text output for text that is written upon areas that are classified as “picture” by the layout module. This may be especially be useful when picture content is not stored.
        - **show\_progress** (*bool*) – display a progress bar during processing.
        - **embed\_images** (*bool*) – store image binaries for “picture” boundary boxes. Base64-encoded images are included in the JSON output. Ignores `image_path` if used. This may drastically increase the size of your JSON text.
        - **write\_images** (*bool*) – store image files “picture” boundary boxes.when encountering images, image files will be created from the respective page area and stored in the specified folder. Any text contained in these areas will still be included in the text output.
        - **pages** (*list*) – optional, the pages to consider for output (caution: specify 0-based page numbers). If omitted (`None`) all pages are processed. Specify any valid Python sequence containing integers between `0` and `page_count - 1`.

use\_layout(*yes: bool = True*)
:   Switch on/off the use of the [PyMuPDF Layout module](index.html#pymupdf4llm-and-layout).

    If `yes=True` (default), the layout module will be used for page analysis for optimal results. If `yes=False`, the layout module will not be used.

get\_key\_values(*doc: pymupdf.Document | str*) → list[dict]
:   Parse the document if it is a **Form PDF** and extract key-value pairs from all form fields (widgets).

    Please note that this method is only relevant for PDF documents that contain widgets. Otherwise, an empty list will be returned.

    The function is always available – independently of whether you are using the PyMuPDF Layout module or not.

    Each dictionary item has the following structure:

    ```
    {
        "field_name": str,      # the full name of the form field, components separated by dots
        {
            "value": str,       # the field value as string
            "pages": list,      # list of 0-based page numbers where the field appears
        }
    }
    ```

Note

Please see [this site](https://github.com/pymupdf/pymupdf4llm/discussions/327) for more background and the current status of further improvements regarding usage with PyMuPDF Layout.

LlamaMarkdownReader(*\*args*, *\*\*kwargs*)
:   Create a [`pdf_markdown_reader.PDFMarkdownReader`](#pdf_markdown_reader.PDFMarkdownReader "pdf_markdown_reader.PDFMarkdownReader") using the [LlamaIndex](https://pypi.org/project/llama-index/) package. Please note that this package will **not automatically be installed** when installing **pymupdf4llm**.

    For details on the possible arguments, please consult the LlamaIndex documentation [[1]](#f1).

    Raises:
    :   `NotImplementedError`: Please install required [LlamaIndex](https://pypi.org/project/llama-index/) package.

    Returns:
    :   a [`pdf_markdown_reader.PDFMarkdownReader`](#pdf_markdown_reader.PDFMarkdownReader "pdf_markdown_reader.PDFMarkdownReader") and issues message “Successfully imported LlamaIndex”. Please note that this method needs several seconds to execute. For details on using the markdown reader please see below.

---

*class* IdentifyHeaders
:   Note

    Only if [use\_layout()](#pymupdf4llm-api-layout) is False

    \_\_init\_\_(*self*, *doc: pymupdf.Document | str*, *\**, *pages: list | range | None = None*, *body\_limit: float = 11*, *max\_levels: int = 6*)
    :   Create an object which maps text font sizes to the respective number of ‘#’ characters which are used by Markdown syntax to indicate header levels. The object is created by scanning the document for font size “popularity”. The most popular font size and all smaller sizes are used for body text. Larger font sizes are mapped to the respective header levels - which correspond to the HTML tags `<h1>` to `<h6>`.

        All font sizes are rounded to integer values.

        If more than 6 header levels would be required, then the largest number smaller than the `<h6>` font size is used for body text.

        Please note that creating the object will read and inspect the text of the entire document - independently of reading the document again in the [`to_markdown()`](#to_markdown "to_markdown") method subsequently. Method [`to_markdown()`](#to_markdown "to_markdown") by default **will create this object** if you do not override its `hdr_info=None` parameter.

        Parameters:
        :   - **doc** ([*Document*](../document.html#Document "Document")*,**str*) – the file, to be specified either as a file path string, or as a PyMuPDF Document (created via `pymupdf.open`). In order to use `pathlib.Path` specifications, Python file-like objects, documents in memory etc. you **must** use a PyMuPDF Document.
            - **pages** (*list*) – optional, the pages to consider. If omitted all pages are processed.
            - **body\_limit** (*float*) – the default font size limit for body text. Only used when the document scan does not deliver valid information.
            - **max\_levels** (*int*) – the maximum number of header levels to be used. Valid values are in `range(1, 7)`. The default is 6, which corresponds to the HTML tags `<h1>` to `<h6>`. A smaller value will limit the number of generated header levels. For instance, a value of 3 will only generate header tags “#”, “##” and “###”. Body text will be assumed for all font sizes smaller than the one corresponding to “###”.

    get\_header\_id(*self*, *span: dict*, *page=None*) → str
    :   Return appropriate markdown header prefix. This is either “” or a string of “#” characters followed by a space.

        Given a text span from a “dict” extraction, determine the markdown header prefix string of 0 to n concatenated ‘#’ characters.

        Parameters:
        :   - **span** (*dict*) – a dictionary containing the text span information. This is the same dictionary as returned by `page.get_text("dict")`.
            - **page** ([*Page*](../page.html#Page "Page")) – the owning page object. This can be used when additional information needs to be extracted.

        Returns:
        :   a string of “#” characters followed by a space.

    header\_id
    :   A dictionary mapping (integer) font sizes to Markdown header strings like `{14: '# ', 12: '## '}`. The dictionary is created by the [`IdentifyHeaders`](#IdentifyHeaders "IdentifyHeaders") constructor. The keys are the font sizes of the text spans in the document. The values are the respective header strings.

    body\_limit
    :   An integer value indicating the font size limit for body text. This is computed as `min(header_id.keys()) - 1`. In the above example, body\_limit would be 11.

---

**How to limit header levels (example)**

Limit the generated header levels to 3:

```
import pymupdf, pymupdf4llm

filename = "input.pdf"
doc = pymupdf.open(filename)  # use a Document for subsequent processing
my_headers = pymupdf4llm.IdentifyHeaders(doc, max_levels=3)  # generate header info
md_text = pymupdf4llm.to_markdown(doc, hdr_info=my_headers)
```

**How to provide your own header logic (example 1)**

Provide your own function which uses pre-determined, fixed font sizes:

```
import pymupdf, pymupdf4llm

filename = "input.pdf"
doc = pymupdf.open(filename)  # use a Document for subsequent processing

def my_headers(span, page=None):
    """
    Provide some custom header logic.
    This is a callable which accepts a text span and the page.
    Could be extended to check for other properties of the span, for
    instance the font name, text color and other attributes.
    """
    # header level is h1 if font size is larger than 14
    # header level is h2 if font size is larger than 10
    # otherwise it is body text
    if span["size"] > 14:
        return "# "
    elif span["size"] > 10:
        return "## "
    else:
        return ""

# this will *NOT* scan the document for font sizes!
md_text = pymupdf4llm.to_markdown(doc, hdr_info=my_headers)
```

**How to provide your own header logic (example 2)**

This user function uses the document’s Table of Contents – under the assumption that the bookmark text is also present as a header line on the page (which certainly need not be the case!):

```
import pymupdf, pymupdf4llm

filename = "input.pdf"
doc = pymupdf.open(filename)  # use a Document for subsequent processing
TOC = doc.get_toc()  # use the table of contents for determining headers

def my_headers(span, page=None):
    """
    Provide some custom header logic (experimental!).
    This callable checks whether the span text matches any of the
    TOC titles on this page.
    If so, use TOC hierarchy level as header level.
    """
    # TOC items on this page:
    toc = [t for t in TOC if t[-1] == page.number + 1]

    if not toc:  # no TOC items on this page
        return ""

    # look for a match in the TOC items
    for lvl, title, _ in toc:
        if span["text"].startswith(title):
            return "#" * lvl + " "
        if title.startswith(span["text"]):
            return "#" * lvl + " "

    return ""

# this will *NOT* scan the document for font sizes!
md_text = pymupdf4llm.to_markdown(doc, hdr_info=my_headers)
```

---

*class* TocHeaders
:   Note

    Only if [use\_layout()](#pymupdf4llm-api-layout) is False

    \_\_init\_\_(*self*, *doc: pymupdf.Document | str*)
    :   Create an object which uses the document’s Table of Contents (TOC) to determine header levels. Upon object creation, the table of contents is read via the [`Document.get_toc()`](../document.html#Document.get_toc "Document.get_toc") method. The TOC data is then used to determine header levels in the [`to_markdown()`](#to_markdown "to_markdown") method.

        This is an alternative to [`IdentifyHeaders`](#IdentifyHeaders "IdentifyHeaders"). Instead of running through the full document to identify font sizes, it uses the document’s Table Of Contents (TOC) to identify headers on pages. Like [`IdentifyHeaders`](#IdentifyHeaders "IdentifyHeaders"), this also is no guarantee to find headers, but for well-built Table of Contents, there is a good chance for more correctly identifying header lines on document pages than the font-size-based approach.

        It also has the advantage of being much faster than the font-size-based approach, as it does not execute a full document scan or even access any of the document pages.

        Examples where this approach works very well are the Adobe’s files on PDF documentation.

        Please note that this feature **does not read document pages** where the table of contents may exist as normal standard text. It only accesses data as provided by the [`Document.get_toc()`](../document.html#Document.get_toc "Document.get_toc") method. It will not identify any headers for documents where the table of contents is not available as a collection of bookmarks.

    get\_header\_id(*self*, *span: dict*, *page=None*) → str
    :   Return appropriate markdown header prefix. This is either an empty string or a string of “#” characters followed by a space.

        Given a text span from a “dict” extraction variant, determine the markdown header prefix string of 0 to n concatenated “#” characters.

        Parameters:
        :   - **span** (*dict*) – a dictionary containing the text span information. This is the same dictionary as returned by `page.get_text("dict")`.
            - **page** ([*Page*](../page.html#Page "Page")) – the owning page object. This can be used when additional information needs to be extracted.

        Returns:
        :   a string of “#” characters followed by a space.

**How to use class TocHeaders**

This is a version of previous **example 2** that uses [`TocHeaders`](#TocHeaders "TocHeaders") for header identification:

```
import pymupdf, pymupdf4llm

filename = "input.pdf"

doc = pymupdf.open(filename)  # use a Document for subsequent processing
my_headers = pymupdf4llm.TocHeaders(doc)  # use the table of contents for determining headers

# this will *NOT* scan the document for font sizes!
md_text = pymupdf4llm.to_markdown(doc, hdr_info=my_headers)
```

---

*class* pdf\_markdown\_reader.PDFMarkdownReader
:   load\_data(*file\_path: Path | str*, *extra\_info: Dict | None = None*, *\*\*load\_kwargs: Any*) → List[LlamaIndexDocument]
    :   This is the only method of the markdown reader you should currently use to extract markdown data. Please in any case ignore methods `aload_data()` and `lazy_load_data()`. Other methods like `use_doc_meta()` may or may not make sense. For more information, please consult the LlamaIndex documentation [[1]](#f1).

        Under the hood the method will execute [`to_markdown()`](#to_markdown "to_markdown").

        Returns:
        :   a list of `LlamaIndexDocument` documents - one for each page.

---

For a list of changes, please see file [CHANGES.md](https://github.com/pymupdf/pymupdf4llm/blob/main/CHANGES.md).

Footnotes

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.

/\* this script is used to adjust the search widget and to add line breaks after parameters in the signature blocks for better readability \*/