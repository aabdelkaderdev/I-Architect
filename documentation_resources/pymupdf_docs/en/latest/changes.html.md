<!-- Source: https://pymupdf.readthedocs.io/en/latest/changes.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Change Log

**Changes in version 1.27.2.2** (2026-03-20)

- Fixed issues:

  - **Fixed** [4902](https://github.com/pymupdf/PyMuPDF/issues/4902): Incorrect linewidth in elements returned by Page.get\_texttrace()
  - **Fixed** [4932](https://github.com/pymupdf/PyMuPDF/issues/4932): “Page” has no attribute “find\_tables” in PyMuPDF 1.27
- Other:

  - Added `Annot.__bool__()`.

**Changes in version 1.27.2.** (2026-03-10)

- Use MuPDF-1.27.2.
- Fixed issues:

  - **Fixed** [4903](https://github.com/pymupdf/PyMuPDF/issues/4903): Typing broken because of `*_forward_decl`
- Other:

  - Retrospectively marked #4907 as fixed in pymupdf-1.27.1.
  - Improved [`get_textpage_ocr()`](page.html#Page.get_textpage_ocr "Page.get_textpage_ocr").

    For partial OCR, **all** page areas outside legible text are now OCRed, not
    just those within images. This means that OCR will now also be performed
    for vector graphics, and for text containing illegible characters.

**Changes in version 1.27.1** (2026-02-11)

- Use MuPDF-1.27.1.
- Fixed issues:

  - **Fixed** [4599](https://github.com/pymupdf/PyMuPDF/issues/4599): page.cluster\_drawings extract a lot of small clusters once upgraded to 1.26
  - **Fixed** [4751](https://github.com/pymupdf/PyMuPDF/issues/4751): Memory leaking in page.widgets()
  - **Fixed** [4762](https://github.com/pymupdf/PyMuPDF/issues/4762): Importing pymupdf make pillow segmentation fault for converting jp2 file on ArchLinux
  - **Fixed** [4790](https://github.com/pymupdf/PyMuPDF/issues/4790): Problem to delete pages on PDF
  - **Fixed** [4857](https://github.com/pymupdf/PyMuPDF/issues/4857): Package is missing py.typed file required for type checking
  - **Fixed** [4886](https://github.com/pymupdf/PyMuPDF/issues/4886): <IMG> width attribute behaviour seems wrong
  - **Fixed** [4907](https://github.com/pymupdf/PyMuPDF/issues/4907): signal 11:SIGSEGV while using display\_list.get\_textpage()
- Other:

  - Added `pymupdf.TEXT_CLIP`.
  - Removed support for mupdf < 1.26.
  - New arg `raise_on_repair` in [`Document.save()`](document.html#Document.save "Document.save").
  - New method [`Document.repair()`](document.html#Document.repair "Document.repair").

**Changes in version 1.26.7** (2025-12-11)

- Use MuPDF-1.26.12.

  - **Fixed** [4801](https://github.com/pymupdf/PyMuPDF/issues/4801): Build failure dumping all environment variables

Other:

> - Retrospectively mark [4756](https://github.com/pymupdf/PyMuPDF/issues/4756) as fixed in 1.26.6.
> - Improved safety of `pymupdf embed-extract`. This now refuses to write to
>   an existing file or outside current directory, unless `-output` or new flag
>   `-unsafe` is specified.

**Changes in version 1.26.6** (2025-11-05)

- Use MuPDF-1.26.11.
- Supported Python versions are now 3.10-3.14.
- Fixed issues:

  - **Fixed** [4699](https://github.com/pymupdf/PyMuPDF/issues/4699): cannot find ExtGState resource
  - **Fixed** [4712](https://github.com/pymupdf/PyMuPDF/issues/4712): Crash with “corrupted double-linked list”
  - **Fixed** [4720](https://github.com/pymupdf/PyMuPDF/issues/4720): Memory leaking in rewrite\_images?
  - **Fixed** [4742](https://github.com/pymupdf/PyMuPDF/issues/4742): ‘Rect’ object has no attribute ‘get\_area’
  - **Fixed** [4746](https://github.com/pymupdf/PyMuPDF/issues/4746): Document.\_\_init\_\_() got an unexpected keyword argument ‘encoding’
  - **Fixed** [4756](https://github.com/pymupdf/PyMuPDF/issues/4756): swig –version doesn’t work in all versions of swig; -version should be used instead

**Changes in version 1.26.5** (2025-10-10)

- Use MuPDF-1.26.10.
- Fixed issues:

  - **Fixed** [2883](https://github.com/pymupdf/PyMuPDF/issues/2883): Improve the Python type annotations for fitz\_new
  - **Fixed** [4507](https://github.com/pymupdf/PyMuPDF/issues/4507): Bugs in pyodide
  - **Fixed** [4613](https://github.com/pymupdf/PyMuPDF/issues/4613): Thai and number blocks are not auto-scaled and get wrong hyphen when using in insert\_htmlbox
  - **Fixed** [4700](https://github.com/pymupdf/PyMuPDF/issues/4700): pymupdf.open() processes .zip file without raising
  - **Fixed** [4716](https://github.com/pymupdf/PyMuPDF/issues/4716): Problems with unreadable characters
- Other:

  - Supported Python versions are now 3.9-3.14.
  - We now define all class methods explicitly instead of with dynamic assignment; this improves type hints.
  - Removed `pymupdf.utils.Shape` class, was duplicate of `pymupdf.Shape`.
  - Allow use of cibuildwheel to build and test on Pyodide.
  - Fixed various Pyodide bugs.
  - In documentation, added section about Linux wheels and glibc compatibility.
  - Improved documentation of pymupdf.open()’s <filetype> arg.
  - Retrospectively mark [4544](https://github.com/pymupdf/PyMuPDF/issues/4544) as fixed in 1.26.4.

**Changes in version 1.26.4 (2025-08-25)**

- Use MuPDF-1.26.7.
- Fixed issues:

  - **Fixed** [3806](https://github.com/pymupdf/PyMuPDF/issues/3806): pdf to image rendering ignore optional content offs
  - **Fixed** [4388](https://github.com/pymupdf/PyMuPDF/issues/4388): Incorrect PixMap from page due to cached data from other PDF
  - **Fixed** [4457](https://github.com/pymupdf/PyMuPDF/issues/4457): Wrong characters displayed after font subsetting (w/ native method)
  - **Fixed** [4462](https://github.com/pymupdf/PyMuPDF/issues/4462): delete\_pages() does not accept a single int
  - **Fixed** [4533](https://github.com/pymupdf/PyMuPDF/issues/4533): Open PDF error segmentation fault
  - **Fixed** [4544](https://github.com/pymupdf/PyMuPDF/issues/4544): About pdf\_clip\_page
  - **Fixed** [4565](https://github.com/pymupdf/PyMuPDF/issues/4565): MacOS uses Tesseract and not Tesseract-OCR
  - **Fixed** [4571](https://github.com/pymupdf/PyMuPDF/issues/4571): Broken merged pdfs.
  - **Fixed** [4590](https://github.com/pymupdf/PyMuPDF/issues/4590): TypeError in utils.py scrub(): annot.update\_file(buffer=…) is invalid
  - **Fixed** [4614](https://github.com/pymupdf/PyMuPDF/issues/4614): Intercept bad widgets when inserting to another PDF
  - **Fixed** [4639](https://github.com/pymupdf/PyMuPDF/issues/4639): pymupdf.mupdf.FzErrorGeneric: code=1: Director error: <class ‘AttributeError’>: ‘JM\_new\_bbox\_device\_Device’ object has no attribute ‘layer\_name’
- Other:

  - Check that #4392 `Segfault when running with pytest and -Werror` is fixed if PyMuPDF is built with swig>=4.4.
  - Add [`Page.clip_to_rect()`](page.html#Page.clip_to_rect "Page.clip_to_rect").
  - Improved search for Tesseract data.
  - Retrospectively mark #4496 as fixed in 1.26.1.
  - Retrospectively mark #4503 as fixed in 1.26.3.
  - Added experimental support for Graal.

**Changes in version 1.26.3 (2025-07-02)**

- Use MuPDF-1.26.3.
- Fixed issues:

  - **Fixed** [4462](https://github.com/pymupdf/PyMuPDF/issues/4462): delete\_pages() does not accept a single int
  - **Fixed** [4503](https://github.com/pymupdf/PyMuPDF/issues/4503): Undetected character styles
  - **Fixed** [4527](https://github.com/pymupdf/PyMuPDF/issues/4527): Rect.intersects() is much slower than necessary
  - **Fixed** [4564](https://github.com/pymupdf/PyMuPDF/issues/4564): Possible encoding issue in PDF metadata
  - **Fixed** [4575](https://github.com/pymupdf/PyMuPDF/issues/4575): Bug with IRect contains method
- Other:

  - Class Shape is now available as pymupdf.Shape.
  - Added table cell markdown support.

**Changes in version 1.26.2**

[Skipped.]

**Changes in version 1.26.1 (2025-06-11)**

- Use MuPDF-1.26.2.
- Fixed issues:

  - **Fixed** [4520](https://github.com/pymupdf/PyMuPDF/issues/4520): show\_pdf\_page does not like empty pages created by new\_page
  - **Fixed** [4524](https://github.com/pymupdf/PyMuPDF/issues/4524): fitz.get\_text ignores ‘pages’ kwarg
  - **Fixed** [4412](https://github.com/pymupdf/PyMuPDF/issues/4412): Regression? Spurious error? in insert\_pdf in v1.25.4
  - **Fixed** [4496](https://github.com/pymupdf/PyMuPDF/issues/4496): pymupdf4llm with pymupdfpro
- Other:

  - Partial fix for [4503](https://github.com/pymupdf/PyMuPDF/issues/4503): Undetected character styles
  - New method [`Document.rewrite_images()`](document.html#Document.rewrite_images "Document.rewrite_images"), useful for reducing file size, changing image formats, or converting color spaces.
  - [`Page.get_text()`](page.html#Page.get_text "Page.get_text"): restrict positional args to match docs.
  - Removed bogus definition of class [Shape](shape.html#shape).
  - Removed release date from module, docs and changelog.
    \* `pymupdf.pymupdf_date` and `pymupdf.VersionDate` are now both None.
    \* They will be removed in a future release.

**Changes in version 1.26.0 (2025-05-22)**

- Use MuPDF-1.26.1.
- Fixed issues:

  - **Fixed** [4324](https://github.com/pymupdf/PyMuPDF/issues/4324): cluster\_drawings() fails to cluster horizontal and vertical thin lines
  - **Fixed** [4363](https://github.com/pymupdf/PyMuPDF/issues/4363): Trouble with searching
  - **Fixed** [4404](https://github.com/pymupdf/PyMuPDF/issues/4404): IndexError in page.get\_links()
  - **Fixed** [4412](https://github.com/pymupdf/PyMuPDF/issues/4412): Regression? Spurious error? in insert\_pdf in v1.25.4
  - **Fixed** [4423](https://github.com/pymupdf/PyMuPDF/issues/4423): pymupdf.mupdf.FzErrorFormat: code=7: cannot find object in xref error encountered after version 1.25.3
  - **Fixed** [4435](https://github.com/pymupdf/PyMuPDF/issues/4435): get\_pixmap method stuck on one page
  - **Fixed** [4439](https://github.com/pymupdf/PyMuPDF/issues/4439): New Xml class from data does not work - bug in code
  - **Fixed** [4445](https://github.com/pymupdf/PyMuPDF/issues/4445): Broken XREF table incorrectly repaired
  - **Fixed** [4447](https://github.com/pymupdf/PyMuPDF/issues/4447): Stroke color of annotations cannot be correctly set
  - **Fixed** [4479](https://github.com/pymupdf/PyMuPDF/issues/4479): set\_layer\_ui\_config() toggles all layers rather than just one
  - **Fixed** [4505](https://github.com/pymupdf/PyMuPDF/issues/4505): Follow Widget flag values up its parent structure
- Other:

  - Partial fixed for [4457](https://github.com/pymupdf/PyMuPDF/issues/4457): Wrong characters displayed after font subsetting (w/ native method)
  - Support image stamp annotations.
  - Support recoloring pages.
  - Added example of using Django’s file storage API to open files with pymupdf.
  - Clarified FreeText annotation color options.
    We now raise an exception if an attempt is made to set attributes that can not be supported.
  - Fixed potential segv in Pixmap.is\_unicolor().
  - Added runtime assert that that PyMuPDF and MuPDF were built with compatible
    NDEBUG settings (related to [4390](https://github.com/pymupdf/PyMuPDF/issues/4390)).
  - Simplified handling of filename/filetype when opening documents.
  - Removed PDF linearization support.
    \* Calls to [`Document.save()`](document.html#Document.save "Document.save") with `linear` set to true will now raise an exception.
    \* See <https://artifex.com/blog/mupdf-removes-linearisation> for more information.

**Changes in version 1.25.5 (2025-03-31)**

- Fixed issues:

  - **Fixed** [4372](https://github.com/pymupdf/PyMuPDF/issues/4372): Text insertion fails due to missing /Resources object
  - **Fixed** [4400](https://github.com/pymupdf/PyMuPDF/issues/4400): Infinite loop in fill\_textbox
  - **Fixed** [4403](https://github.com/pymupdf/PyMuPDF/issues/4403): Unable to get\_text() - layer/clip nesting too deep
  - **Fixed** [4415](https://github.com/pymupdf/PyMuPDF/issues/4415): PDF page is mirrored, origin is at bottom-left
- Other:

  - Use MuPDF-1.25.6.
  - Fixed MuPDF SEGV on MacOS with particular fonts.
  - Fixed [`Annot.get_textpage()`](annot.html#Annot.get_textpage "Annot.get_textpage")’s `clip` arg.
  - Fixed Python-3.14 (pre-release) build error.

**Changes in version 1.25.4 (2025-03-14)**

- Use MuPDF-1.25.5.
- Fixed issues:

  - **Fixed** [4079](https://github.com/pymupdf/PyMuPDF/issues/4079): Unexpected result for apply\_redactions()
  - **Fixed** [4224](https://github.com/pymupdf/PyMuPDF/issues/4224): MuPDF error: format error: negative code in 1d faxd
  - **Fixed** [4303](https://github.com/pymupdf/PyMuPDF/issues/4303): page.get\_image\_info() returns outdated cached results after replacing image
  - **Fixed** [4309](https://github.com/pymupdf/PyMuPDF/issues/4309): FzErrorFormat Error When Deleting First Page
  - **Fixed** [4336](https://github.com/pymupdf/PyMuPDF/issues/4336): Major Performance Regression: pix.color\_count is 150x slower in version 1.25.3 compared to 1.23.8
  - **Fixed** [4341](https://github.com/pymupdf/PyMuPDF/issues/4341): Invalid label retrieval when /Kids is an array of multiple /Nums
- Other:

  - Fixed handling of duplicate widget names when joining PDFs (PR #4347).
  - Improved Pyodide build.
  - Avoid SWIG-related build errors with Python-3.13 by disabling PY\_LIMITED\_API.

**Changes in version 1.25.3 (2025-02-06)**

- Use MuPDF-1.25.4.
- Fixed issues:

  - **Fixed** [4139](https://github.com/pymupdf/PyMuPDF/issues/4139): Text color numbers change between 1.24.14 and 1.25.0
  - **Fixed** [4141](https://github.com/pymupdf/PyMuPDF/issues/4141): Some insertion methods fails for pages without a /Resources object
  - **Fixed** [4180](https://github.com/pymupdf/PyMuPDF/issues/4180): Search problems
  - **Fixed** [4182](https://github.com/pymupdf/PyMuPDF/issues/4182): Text coordinate extraction error
  - **Fixed** [4245](https://github.com/pymupdf/PyMuPDF/issues/4245): Highlighting issue distorted on recent versions
  - **Fixed** [4254](https://github.com/pymupdf/PyMuPDF/issues/4254): add\_freetext\_annot is drawing text outside the annotation box
- Other:

  - In annotations:
    \* Added support for subtype FreeTextCallout.
    \* Added support for rich text.
  - Added miter\_limit arg to insert\_text\*() to allow suppression of spikes caused by long miters.
  - Add Widget Support to [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf").
  - Add `bibi` to span dicts.
  - Add [`](#id75)synthetic’ to char dict.
  - Fixed Pyodide builds.

**Changes in version 1.25.2 (2025-01-17)**

- Fixed issues:

  - **Fixed** [4055](https://github.com/pymupdf/PyMuPDF/issues/4055): “Yes” for all checkboxes does not work for all PDF rendering engines.
  - **Fixed** [4155](https://github.com/pymupdf/PyMuPDF/issues/4155): samples\_mv is unsafe
  - **Fixed** [4162](https://github.com/pymupdf/PyMuPDF/issues/4162): Got AttributeError, when tried to add Signature field
  - **Fixed** [4186](https://github.com/pymupdf/PyMuPDF/issues/4186): Incorrect handling of JPEG with color space CMYK image extraction
  - **Fixed** [4195](https://github.com/pymupdf/PyMuPDF/issues/4195): Pixmaps that are inverted and have an alpha channel are not rendered properly
  - **Fixed** [4225](https://github.com/pymupdf/PyMuPDF/issues/4225): pixmap.pil\_save() fails due to colorspace definition
  - **Fixed** [4232](https://github.com/pymupdf/PyMuPDF/issues/4232): Incorrect Font style and Size
- Other:

  - Use Python’s built-in glyphname <> unicode conversion.
  - Improve speed of pixmap color inversion.
  - Add new `char_flags` member to span dictionary, for example allows detection of invisible text.
  - Detect image masks in TextPage output.
  - Added [`Pixmap.pil_image()`](pixmap.html#Pixmap.pil_image "Pixmap.pil_image").

**Changes in version 1.25.1 (2024-12-11)**

- Use MuPDF-1.25.2.
- Fixed issues:

  - **Fixed** [4125](https://github.com/pymupdf/PyMuPDF/issues/4125): memory leak while convert Pixmap’s colorspace
  - **Fixed** [4034](https://github.com/pymupdf/PyMuPDF/issues/4034): Possible regression in pdf cleaning during save.

**Changes in version 1.25.0 (2024-12-05)**

- Use MuPDF-1.25.1.
- Fixed issues:

  - **Fixed** [4026](https://github.com/pymupdf/PyMuPDF/issues/4026): page.get\_text(‘blocks’) output two piece of very similar text with different bbox
  - **Fixed** [4004](https://github.com/pymupdf/PyMuPDF/issues/4004): Segmentation Fault When Updating PDF Form Field Value
  - **Fixed** [3887](https://github.com/pymupdf/PyMuPDF/issues/3887): Subset Fonts problem using Fallback Font
  - **Fixed** [3886](https://github.com/pymupdf/PyMuPDF/issues/3886): Another issue with destroying PDF when inserting html
  - **Fixed** [3751](https://github.com/pymupdf/PyMuPDF/issues/3751): apply\_redactions causes part of the page content to be hidden / transparent

**Changes in version 1.24.14 (2024-11-19)**

- Use MuPDF-1.24.11.
- Fixed issues:

  - **Fixed** [3448](https://github.com/pymupdf/PyMuPDF/issues/3448): get\_pixmap function removes the table and leaves just the content behind
  - **Fixed** [3758](https://github.com/pymupdf/PyMuPDF/issues/3758): Got “malloc(): unaligned tcache chunk detected Aborted (core dumped)” while using add\_redact\_annot/apply\_redactions
  - **Fixed** [3813](https://github.com/pymupdf/PyMuPDF/issues/3813): Stories: Ordered list count broken with nested unordered list
  - **Fixed** [3933](https://github.com/pymupdf/PyMuPDF/issues/3933): font.valid\_codepoints() - malfunction
  - **Fixed** [4018](https://github.com/pymupdf/PyMuPDF/issues/4018): PyMuPDF hangs when iterating over zero page PDF pages backwards
  - **Fixed** [4043](https://github.com/pymupdf/PyMuPDF/issues/4043): fullcopypage bug
  - **Fixed** [4047](https://github.com/pymupdf/PyMuPDF/issues/4047): Segmentation Fault in add\_redact\_annot
  - **Fixed** [4050](https://github.com/pymupdf/PyMuPDF/issues/4050): Content of dict returned by doc.embfile\_info() does not fit to documentation
- Other:

  - Ensure that words from [`Page.get_text()`](page.html#Page.get_text "Page.get_text") never contain RTL/LTR char mixtures.
  - Fix building with system MuPDF.
  - Add dot product for points and vectors.

**Changes in version 1.24.13 (2024-10-29)**

- Fixed issues:

  - **Fixed** [3848](https://github.com/pymupdf/PyMuPDF/issues/3848): Piximap program crash
  - **Fixed** [3950](https://github.com/pymupdf/PyMuPDF/issues/3950): Unable to consistently extract field labels from PDFs
  - **Fixed** [3981](https://github.com/pymupdf/PyMuPDF/issues/3981): PyMuPDF 1.24.12 with pyinstaller throws error.
  - **Fixed** [3994](https://github.com/pymupdf/PyMuPDF/issues/3994): pix.color\_topusage raise Segmentation fault (core dumped)

**Changes in version 1.24.12 (2024-10-21)**

- Fixed issues:

  - **Fixed** [3914](https://github.com/pymupdf/PyMuPDF/issues/3914): Ability to print MuPDF errors to logging instead of stdout
  - **Fixed** [3916](https://github.com/pymupdf/PyMuPDF/issues/3916): insert\_htmlbox error: int too large to convert to float
  - **Fixed** [3950](https://github.com/pymupdf/PyMuPDF/issues/3950): Unable to consistently extract field labels from PDFs
- Supported Python versions are now 3.9-3.13.

  - Dropped support for Python-3.8 because end-of-life.
  - Added support for Python-3.13 because now released.
  - See: <https://devguide.python.org/versions/>

**Changes in version 1.24.11 (2024-10-03)**

- Use MuPDF-1.24.10.
- Fixed issues:

  - **Fixed** [3624](https://github.com/pymupdf/PyMuPDF/issues/3624): Pdf file transform to image have a black block
  - **Fixed** [3859](https://github.com/pymupdf/PyMuPDF/issues/3859): doc.need\_appearances() fails with “AttributeError: module ‘pymupdf.mupdf’ has no attribute ‘PDF\_TRUE’ “
  - **Fixed** [3863](https://github.com/pymupdf/PyMuPDF/issues/3863): apply\_redactions() does not work as expected
  - **Fixed** [3905](https://github.com/pymupdf/PyMuPDF/issues/3905): open stream can raise a FzErrorFormat error instead of FileDataError
- Wheels now use the Python Stable ABI:

  - There is one PyMuPDF wheel for each platform.
  - Each wheel works with all supported Python versions.
  - Each wheel is built using the oldest supported Python version (currently 3.8).
  - There is no PyMuPDFb wheel.
- Other:

  - Improvements to get\_text\_words() with sort=True.
  - Tests now always get the latest versions of required Python packages.
  - Removed dependency on setuptools.
  - Added item to PyMuPDF-1.24.10 changes below - fix of #3630.

**Changes in version 1.24.10 (2024-09-02)**

- Use MuPDF-1.24.9.
- Fixed issues:

  - **Fixed** [3450](https://github.com/pymupdf/PyMuPDF/issues/3450): get\_pixmap function takes too long to process
  - **Fixed** [3569](https://github.com/pymupdf/PyMuPDF/issues/3569): Invalid OCGs not ignored by SVG image creation
  - **Fixed** [3603](https://github.com/pymupdf/PyMuPDF/issues/3603): ObjStm compression and PDF linearization doesn’t work together
  - **Fixed** [3650](https://github.com/pymupdf/PyMuPDF/issues/3650): Linebreak inserted between each letter
  - **Fixed** [3661](https://github.com/pymupdf/PyMuPDF/issues/3661): Update Document to check the /XYZ len
  - **Fixed** [3698](https://github.com/pymupdf/PyMuPDF/issues/3698): documentation issue - old code in the annotations documentation
  - **Fixed** [3705](https://github.com/pymupdf/PyMuPDF/issues/3705): Document.select() behaves weirdly in some particular kind of pdf files
  - **Fixed** [3706](https://github.com/pymupdf/PyMuPDF/issues/3706): extend Document.\_\_getitem\_\_ type annotation to reflect that the method also accepts slices
  - **Fixed** [3727](https://github.com/pymupdf/PyMuPDF/issues/3727): Method get\_pixmap() make the program exit without any exceptions or messages
  - **Fixed** [3767](https://github.com/pymupdf/PyMuPDF/issues/3767): Cannot get Tessdata with Tesseract-OCR 5
  - **Fixed** [3773](https://github.com/pymupdf/PyMuPDF/issues/3773): Link.set\_border gives TypeError: ‘<’ not supported between instances of ‘NoneType’ and ‘int’
  - **Fixed** [3774](https://github.com/pymupdf/PyMuPDF/issues/3774): fitz.\_\_version\_\_` does not work anymore
  - **Fixed** [3789](https://github.com/pymupdf/PyMuPDF/issues/3789): ValueError: not enough values to unpack (expected 3, got 2) is thrown when call insert\_pdf
  - **Fixed** [3820](https://github.com/pymupdf/PyMuPDF/issues/3820): class improves namedDest handling
  - **Fixed** [3630](https://github.com/pymupdf/PyMuPDF/issues/3630): page.apply\_redactions gives unwanted black rectangle
- Other:

  - Object streams and linearization cannot be used together; attempting to do
    so will raise an exception. (#3603)
  - Fixed handling of non-existing /Contents object.

**Changes in version 1.24.9 (2024-07-24)**

- Use MuPDF-1.24.8.

**Changes in version 1.24.8 (2024-07-22)**

- Fixed issues:

  - **Fixed** [3636](https://github.com/pymupdf/PyMuPDF/issues/3636): API documentation for the open function is not obvious to find.
  - **Fixed** [3654](https://github.com/pymupdf/PyMuPDF/issues/3654): docx parsing was broken in 1.24.7
  - **Fixed** [3677](https://github.com/pymupdf/PyMuPDF/issues/3677): Unable to extract subset font name using the newer versions of PyMuPDF : 1.24.6 and 1.24.7.
  - **Fixed** [3687](https://github.com/pymupdf/PyMuPDF/issues/3687): Page.get\_text results in AssertionError for epub files

Other:

- Fixed various spelling mistakes spotted by codespell.
- Improved how we modify MuPDF’s default configuration on Windows.
- Make text search to work with ligatures.

**Changes in version 1.24.7 (2024-06-26)**

- Fixed issues:

  - **Fixed** [3615](https://github.com/pymupdf/PyMuPDF/issues/3615): Document.pagemode or Document.pagelayout crashes for epub files
  - **Fixed** [3616](https://github.com/pymupdf/PyMuPDF/issues/3616): not last version reported

**Changes in version 1.24.6 (2024-06-25)**

- Use MuPDF-1.24.4
- Fixed issues:

  - **Fixed** [3599](https://github.com/pymupdf/PyMuPDF/issues/3599): Story.fit\_width() has a weird line
  - **Fixed** [3594](https://github.com/pymupdf/PyMuPDF/issues/3594): Garbled extraction for Amazon Sustainability Report
  - **Fixed** [3591](https://github.com/pymupdf/PyMuPDF/issues/3591): ‘width’ in Page.get\_drawings() returns width equal as 0
  - **Fixed** [3561](https://github.com/pymupdf/PyMuPDF/issues/3561): ZeroDivisionError: float division by zero with page.apply\_redactions()
  - **Fixed** [3559](https://github.com/pymupdf/PyMuPDF/issues/3559): SegFault 11 when empty H1 H2 H3 H4 etc element is used in insert\_htmlbox
  - **Fixed** [3539](https://github.com/pymupdf/PyMuPDF/issues/3539): Add dotted gridline detection to table recognition
  - **Fixed** [3519](https://github.com/pymupdf/PyMuPDF/issues/3519): get\_toc(simple=False) AttributeError: ‘Outline’ object has no attribute ‘rect’
  - **Fixed** [3510](https://github.com/pymupdf/PyMuPDF/issues/3510): page.get\_label() gets wrong label on the first page of doc
  - **Fixed** [3494](https://github.com/pymupdf/PyMuPDF/issues/3494): 1.24.2/1.24.3: spurious characters introduced when using subset\_fonts and insert\_pdf
  - **Fixed** [3470](https://github.com/pymupdf/PyMuPDF/issues/3470): subset\_fonts error exit without exception/warning
  - **Fixed** [3400](https://github.com/pymupdf/PyMuPDF/issues/3400): set\_toc alters link coordinates for some rotated pages on pymupdf 1.24.2
  - **Fixed** [3347](https://github.com/pymupdf/PyMuPDF/issues/3347): Incorrect links to points on pages having different heights
  - **Fixed** [3237](https://github.com/pymupdf/PyMuPDF/issues/3237): Set\_metadata() does not work
  - **Fixed** [3493](https://github.com/pymupdf/PyMuPDF/discussions/3493): Isolate PyMuPDF from other libraries; issues when PyMuPDF is loaded with other libraries like GdkPixbuf
- Other:

  - Fixed concurrent use of PyMuPDF caused by use of constant temporary filenames.
  - Add musllinux x86\_64 wheels to release.
  - Added clearer version information:

    - `pymupdf.pymupdf_version`.
    - `pymupdf.mupdf_version`.
    - `pymupdf.pymupdf_date`.

**Changes in version 1.24.5 (2024-05-30)**

- Fixed issues:

  - **Fixed** [3479](https://github.com/pymupdf/PyMuPDF/issues/3479): regression: fill\_textbox: IndexError: pop from empty list
  - **Fixed** [3488](https://github.com/pymupdf/PyMuPDF/issues/3488): set\_toc method error
- Other:

  - Some more fixes to use MuPDF floating formatting.
  - Removed/disabled some unnecessary diagnostics.
  - Fixed utils.do\_links() crash.
  - Experimental new functions `pymupdf.apply_pages()` and `pymupdf.get_text()`.
  - Addresses wrong label generation for label styles “a” and “A”.

**Changes in version 1.24.4 (2024-05-16)**

> - **Fixed** [3418](https://github.com/pymupdf/PyMuPDF/issues/3418): Re-introduced bug, text align add\_redact\_annot
> - **Fixed** [3472](https://github.com/pymupdf/PyMuPDF/issues/3472): insert\_pdf gives SystemError

- Other:

  - Fixed sysinstall test failing to remove all of prior installation before
    new install.
  - Fixed `utils.do_links()` crash.
  - Correct [TextPage](textpage.html#textpage) creation Code.
  - Unified various diagnostics.
  - Fix bug in `page_merge()`.

**Changes in version 1.24.3 (2024-05-09)**

- The Python module is now called `pymupdf`. `fitz` is still supported for
  backwards compatibility.
- Use MuPDF-1.24.2.
- Fixed issues:

  - **Fixed** [3357](https://github.com/pymupdf/PyMuPDF/issues/3357): PyMuPDF==1.24.0 will hanging when using page.get\_text(“text”)
  - **Fixed** [3376](https://github.com/pymupdf/PyMuPDF/issues/3376): Redacting results are not as expected in 1.24.x.
  - **Fixed** [3379](https://github.com/pymupdf/PyMuPDF/issues/3379): Documentation mismatch for get\_text\_blocks return value order.
  - **Fixed** [3381](https://github.com/pymupdf/PyMuPDF/issues/3381): Contents stream contains floats in scientific notation
  - **Fixed** [3402](https://github.com/pymupdf/PyMuPDF/issues/3402): Cannot add Widgets containing inter-field-calculation JavaScript
  - **Fixed** [3414](https://github.com/pymupdf/PyMuPDF/issues/3414): missing attribute set\_dpi()
  - **Fixed** [3430](https://github.com/pymupdf/PyMuPDF/issues/3430): page.get\_text() cause process freeze with certain pdf on v1.24.2
- Other:

  - New/modified methods:

    - [`Page.remove_rotation()`](page.html#Page.remove_rotation "Page.remove_rotation"): new, set page rotation to zero while keeping appearance.
  - Fixed some problems when checking for PDF properties.
  - Fixed pip builds from sdist
    (see discussion [3360](https://github.com/pymupdf/PyMuPDF/discussions/3360):
    Alpine linux docker build failing “No matching distribution found for pymupdfb==1.24.1”).

**Changes in version 1.24.2 (2024-04-17)**

- Removed obsolete classic implementation from releases
  (previously available as module `fitz_old`).
- Fixed issues:

  - **Fixed** [3331](https://github.com/pymupdf/PyMuPDF/issues/3331): Document.pages() is incorrectly type-hinted
  - **Fixed** [3354](https://github.com/pymupdf/PyMuPDF/issues/3354): PyMuPDF==1.24.1: AttributeError: property ‘metadata’ of ‘Document’ object has no setter
- Other:

  - New/modified methods:

    - [`Document.bake()`](document.html#Document.bake "Document.bake"): new, make annotations / fields permanent content.
    - [`Page.cluster_drawings()`](page.html#Page.cluster_drawings "Page.cluster_drawings"): new, identifies drawing items
      (i.e. vector graphics or line-art)
      that belong together based on their geometrical vicinity.
    - [`Page.apply_redactions()`](page.html#Page.apply_redactions "Page.apply_redactions"): added new parameter [`text`](xml-class.html#Xml.text "Xml.text").
    - [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts"): use MuPDF’s `pdf_subset_fonts()` instead of PyMuPDF code.
  - The [Document](document.html#document) class now supports page numbers specified as slices.
  - Avoid causing MuPDF warnings.

**Changes in version 1.24.1 (2024-04-02)**

- Fixed issues:

  - **Fixed** [3278](https://github.com/pymupdf/PyMuPDF/issues/3278): apply\_redactions moves some unredacted text
  - **Fixed** [3301](https://github.com/pymupdf/PyMuPDF/issues/3301): Be more permissive when classifying links as kind LINK\_URI
  - **Fixed** [3306](https://github.com/pymupdf/PyMuPDF/issues/3306): Text containing capital ‘ET’ not appearing as annotation
- Other:

  - Use MuPDF-1.24.1.
  - Support ObjStm Compression.
    Methods [`Document.save()`](document.html#Document.save "Document.save"), [`Document.ez_save()`](document.html#Document.ez_save "Document.ez_save") and `Document.write()`
    now support new parameters `use_objstm`, compression\_effort` and
    `preserve_metadata`.

**Changes in version 1.24.0 (2024-03-21)**

- Fixed issues:

  - **Fixed** [3281](https://github.com/pymupdf/PyMuPDF/issues/3281): Preparing metadata (pyproject.toml) did not run successfully
  - **Fixed** [3279](https://github.com/pymupdf/PyMuPDF/issues/3279): PyMuPDF no longer builds in Alpine Linux
  - **Fixed** [3257](https://github.com/pymupdf/PyMuPDF/issues/3257): apply\_redactions() deleting text outside of annotated box
  - **Fixed** [3216](https://github.com/pymupdf/PyMuPDF/issues/3216): AttributeError: ‘Annot’ object has no attribute ‘\_\_del\_\_’
  - **Fixed** [3207](https://github.com/pymupdf/PyMuPDF/issues/3207): get\_drawings’s items is missing line from h path operator
  - **Fixed** [3201](https://github.com/pymupdf/PyMuPDF/issues/3201): Memory leaks when merging PDFs
  - **Fixed** [3197](https://github.com/pymupdf/PyMuPDF/issues/3197): page.get\_text() returns hexadecimal text for some characters
  - **Fixed** [3196](https://github.com/pymupdf/PyMuPDF/issues/3196): Remove text not working in 1.23.25 version vs 1.20.2
  - **Fixed** [3172](https://github.com/pymupdf/PyMuPDF/issues/3172): PDF’s 45º lines disappearing in png conversion
  - **Fixed** [3135](https://github.com/pymupdf/PyMuPDF/issues/3135): Do not log warnings to stdout
  - **Fixed** [3125](https://github.com/pymupdf/PyMuPDF/issues/3125): get\_pixmap method stuck on one page and runs forever
  - **Fixed** [2964](https://github.com/pymupdf/PyMuPDF/issues/2964): There is an issue with the image generated by the page.get\_pixmap() function
- Other:

  - Use MuPDF-1.24.0.
  - Add support for redacting vector graphics.
  - Several fixes for table module

    - Add new method for outputting the table as a markdown string.
    - Address errors in computing the table header object:

      We now allow None as the cell value, because this will be resolved where
      needed (e.g. in the pandas DataFrame).

      We previously tried to enforce rect-like tuples in all header cell
      bboxes, however this fails for tables with all-None columns. This fix
      enables this and constructs an empty string in the corresponding cell
      string.

      We now correctly include start / stop points of lines in the bbox of the
      clustered graphic. We previously joined the line’s rectangle - which had
      no effect because this is always empty.
  - Improved exception text if we fail to open document.
  - Fixed build with new libclang 18.

**Changes in version 1.23.26 (2024-02-29)**

- Fixed issues:

  - **Fixed** [3199](https://github.com/pymupdf/PyMuPDF/issues/3199): Add entry\_points to setuptools configuration to provide command-line console scripts
  - **Fixed** [3209](https://github.com/pymupdf/PyMuPDF/issues/3209): Empty vertices in ink annotation
- Other:

  - Improvements to table detection:

    - Improved check for empty tables, fixes bugs when determining table headers.
    - Improved computation of enveloping vector graphic rectangles.
    - Ignore more meaningless “pseudo” tables
  - Install command-line ‘pymupdf’ command that runs fitz/\_\_main\_\_.py.
  - Don’t overwrite MuPDF’s config.h when building on non-Windows.
  - Fix [Story](story-class.html#story) constructor’s [Archive](archive-class.html#archive) arg to match docs - now accepts a single [Archive](archive-class.html#archive) constructor arg.
  - Do not include MuPDF source in sdist; will be downloaded automatically when building.

**Changes in version 1.23.25 (2024-02-20)**

- Fixed issues:

  - **Fixed** [3182](https://github.com/pymupdf/PyMuPDF/issues/3182): Pixmap.invert\_irect argument type error
  - **Fixed** [3186](https://github.com/pymupdf/PyMuPDF/issues/3186): extractText() extracts broken text from pdf
  - **Fixed** [3191](https://github.com/pymupdf/PyMuPDF/issues/3191): Error on .find\_tables()
- Other:

  - When building, be able to specify python-config directly, with environment
    variable `PIPCL_PYTHON_CONFIG`.

**Changes in version 1.23.24 (2024-02-19)**

- Fixed issues:

  - **Fixed** [3148](https://github.com/pymupdf/PyMuPDF/issues/3148): Table extraction - vertical text not handled correctly
  - **Fixed** [3179](https://github.com/pymupdf/PyMuPDF/issues/3179): Table Detection: Incorrect Separation of Vector Graphics Clusters
  - **Fixed** [3180](https://github.com/pymupdf/PyMuPDF/issues/3180): Cannot show optional content group: AttributeError: module ‘fitz.mupdf’ has no attribute ‘pdf\_array\_push\_drop’
- Other:

  - Be able to test system install using `sudo pip install` instead of a venv.

**Changes in version 1.23.23 (2024-02-18)**

- Fixed issues:

  - **Fixed** [3126](https://github.com/pymupdf/PyMuPDF/issues/3126): Initialising Archive with a pathlib.Path fails.
  - **Fixed** [3131](https://github.com/pymupdf/PyMuPDF/issues/3131): Calling the next attribute of an Annot raises a “No attribute .parent” warning
  - **Fixed** [3134](https://github.com/pymupdf/PyMuPDF/issues/3134): Using an IRect as clip parameter in Page.get\_pixmap no longer works since 1.23.9
  - **Fixed** [3140](https://github.com/pymupdf/PyMuPDF/issues/3140): PDF document stays in use after closing
  - **Fixed** [3150](https://github.com/pymupdf/PyMuPDF/issues/3150): doc.select() hangs on this doc.
  - **Fixed** [3163](https://github.com/pymupdf/PyMuPDF/issues/3163): AssertionError on using fitz.IRect
  - **Fixed** [3177](https://github.com/pymupdf/PyMuPDF/issues/3177): fitz.Pixmap(None, pix) Unrecognised args for constructing Pixmap
- Other:

  - Improved `` Document.select() by using new MuPDF function
    `pdf_rearrange_pages() ``. This is a more complete (and faster)
    implementation of what needs to be done here in that not only pages will
    be rearranged, but also consequential changes will be made to the table
    of contents, links to removed pages and affected entries in the Optional
    Content definitions.
  - [`TextWriter.appendv()`](textwriter.html#TextWriter.appendv "TextWriter.appendv"): added `small_caps` arg.
  - Fixed some valgrind errors with MuPDF master.
  - Fixed `Document.insert_image()` when build with MuPDF master.

**Changes in version 1.23.22 (2024-02-12)**

- Fixed issues:

  - **Fixed** [3143](https://github.com/pymupdf/PyMuPDF/issues/3143): Difference in decoding of OCGs names between doc.get\_ocgs() and page.get\_drawings()
  - **Fixed** [3139](https://github.com/pymupdf/PyMuPDF/issues/3139): Pixmap resizing needs positional arg “clip” - even if None.
- Other:

  - Removed the use of MuPDF function `fz_image_size()` from PyMuPDF.

**Changes in version 1.23.21 (2024-02-01)**

- Fixed issues:
- Other:

  - Fixed bug in set\_xml\_metadata(), PR [3112](https://github.com/pymupdf/PyMuPDF/pull/3112): Fix pdf\_add\_stream metadata error
  - Fixed lack of `.parent` member in [TextPage](textpage.html#textpage) from [`Annot.get_textpage()`](annot.html#Annot.get_textpage "Annot.get_textpage").
  - Fixed bug in [`Page.add_widget()`](page.html#Page.add_widget "Page.add_widget").

**Changes in version 1.23.20 (2024-01-29)**

- Bug fixes:

  - **Fixed** [3100](https://github.com/pymupdf/PyMuPDF/issues/3100): Wrong internal property accessed in get\_xml\_metadata
- Other:

  - Significantly improved speed of [`Document.get_toc()`](document.html#Document.get_toc "Document.get_toc").

**Changes in version 1.23.19 (2024-01-25)**

- Bug fixes:

  - **Fixed** [3087](https://github.com/pymupdf/PyMuPDF/issues/3087): Exception in insert\_image with mask specified
  - **Fixed** [3094](https://github.com/pymupdf/PyMuPDF/issues/3094): TypeError: ‘<’ not supported between instances of ‘FzLocation’ and ‘int’ in doc.delete\_pages
- Other:

  - When finding tables:

    - Allow addition of user-defined “virtual” vector graphics when finding tables.
    - Confirm that the enveloping bboxes of vector graphics are inside the clip rectangle.
    - Avoid slow finding of rectangle intersections.
  - Added [`Font.bbox`](font.html#Font.bbox "Font.bbox") property.

**Changes in version 1.23.18 (2024-01-23)**

- Bug fixes:

  - **Fixed** [3081](https://github.com/pymupdf/PyMuPDF/issues/3081): doc.close() not closing the document
- Other:

  - Reduced size of sdist to fit on pypi.org (by reducing size of two test files).
  - Fix [`Annot.file_info()`](annot.html#Annot.file_info "Annot.file_info") if no `Desc` item.

**Changes in version 1.23.17 (2024-01-22)**

- Bug fixes:

  - **Fixed** [3062](https://github.com/pymupdf/PyMuPDF/issues/3062): page\_rotation\_reset does not return page to original rotation
  - **Fixed** [3070](https://github.com/pymupdf/PyMuPDF/issues/3070): update\_link(): AttributeError: ‘Page’ object has no attribute ‘super’
- Other:

  - Fixed bug in [`Page.links()`](page.html#Page.links "Page.links") (PR #3075).
  - Fixed bug in [`Page.get_bboxlog()`](functions.html#Page.get_bboxlog "Page.get_bboxlog") with layers.
  - Add support for timeouts in scripts/ and tests/run\_compound.py.

**Changes in version 1.23.16 (2024-01-18)**

- Bug fixes:

  - **Fixed** [3058](https://github.com/pymupdf/PyMuPDF/issues/3058): Pixmap created from CMYK JPEG delivers RGB format
- Other:

  - In table detection strategy “lines\_strict”, exclude fill-only vector graphics.
  - Fixed sysinstall test failure.
  - In documentation, update feature matrix with item about text writing.

**Changes in version 1.23.15 (2024-01-16)**

- Bug fixes:

  - **Fixed** [3050](https://github.com/pymupdf/PyMuPDF/issues/3050): python3.9 pix.set\_pixel has something wrong in c.append( ord(i))
- Other:

  - Improved docs for Page.find\_tables().

**Changes in version 1.23.14 (2024-01-15)**

- Bug fixes:

  - **Fixed** [3038](https://github.com/pymupdf/PyMuPDF/issues/3038): JM\_pixmap\_from\_display\_list > Assertion Error : Checking for wrong type
  - **Fixed** [3039](https://github.com/pymupdf/PyMuPDF/issues/3039): Issue with doc.close() not closing the document in PyMuPDF
- Other:

  - Ensure valid “re” rectangles in [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") with derotated pages.

**Changes in version 1.23.13 (2024-01-15)**

- Bug fixes:

  - **Fixed** [2979](https://github.com/pymupdf/PyMuPDF/issues/2979): list index out of range in to\_pandas()
  - **Fixed** [3001](https://github.com/pymupdf/PyMuPDF/issues/3001): Calling find\_tables() on one document alters the bounding boxes of a subsequent document
- Other:

  - Fixed [`Rect.height`](rect.html#Rect.height "Rect.height") and [`Rect.width`](rect.html#Rect.width "Rect.width") to never return negative values.
  - Fixed `TextPage.extractIMGINFO()`’s returned `dictkey_yres` value.

**Changes in version 1.23.12 (2024-01-12)**

- - **Fixed** [3027](https://github.com/pymupdf/PyMuPDF/issues/3027): Page.get\_text throws Attribute Error for ‘parent’

**Changes in version 1.23.11 (2024-01-12)**

- Fixed some Pixmap construction bugs.
- Fixed Pixmap.yres().

**Changes in version 1.23.10 (2024-01-12)**

- Bug fixes:

  - **Fixed** [3020](https://github.com/pymupdf/PyMuPDF/issues/3020): Can’t resize a PixMap
- Other:

  - Fixed Page.delete\_image().

**Changes in version 1.23.9 (2024-01-11)**

- Default to new “rebased” implementation.

  - The old “classic” implementation is available with `import fitz_old as fitz`.
  - For more information about why we are changing to the rebased implementation,
    see: <https://github.com/pymupdf/PyMuPDF/discussions/2680>
- Use MuPDF-1.23.9.
- Bug fixes (rebased implementation only):

  - **Fixed** [2911](https://github.com/pymupdf/PyMuPDF/issues/2911): Page.derotation\_matrix returns a tuple instead of a Matrix with rebased implementation
  - **Fixed** [2919](https://github.com/pymupdf/PyMuPDF/issues/2919): Rebased version: KeyError in resolve\_names when merging pdfs
  - **Fixed** [2922](https://github.com/pymupdf/PyMuPDF/issues/2922): New feature that allows inserting named-destination links doesn’t work
  - **Fixed** [2943](https://github.com/pymupdf/PyMuPDF/issues/2943): ZeroDivisionError: float division by zero when use apply\_redactions()
  - **Fixed** [2950](https://github.com/pymupdf/PyMuPDF/issues/2950): Shelling out to pip during tests is problematic
  - **Fixed** [2954](https://github.com/pymupdf/PyMuPDF/issues/2954): Replacement unicode character in text extraction
  - **Fixed** [2957](https://github.com/pymupdf/PyMuPDF/issues/2957): apply\_redactions() moving text
  - **Fixed** [2961](https://github.com/pymupdf/PyMuPDF/issues/2961): Passing a string as a page number raises IndexError instead of TypeError.
  - **Fixed** [2969](https://github.com/pymupdf/PyMuPDF/issues/2969): annot.next throws AttributeError
  - **Fixed** [2978](https://github.com/pymupdf/PyMuPDF/issues/2978): 1.23.9rc1: module ‘fitz.mupdf’ has no attribute ‘fz\_copy\_pixmap\_rect’
  - **Fixed** [2907](https://github.com/pymupdf/PyMuPDF/issues/2907): segfault trying to call clean\_contents on certain pdfs with python 3.12
  - **Fixed** [2905](https://github.com/pymupdf/PyMuPDF/issues/2905): SystemError: <built-in function TextPage\_extractIMGINFO> returned a result with an exception set
  - **Fixed** [2742](https://github.com/pymupdf/PyMuPDF/issues/2742): Segmentation Fault when inserting three (but not two) copies of the same source page into one destination page
- Other:

  - Add optional setting of opacity to [`Page.insert_htmlbox()`](page.html#Page.insert_htmlbox "Page.insert_htmlbox").
  - Fixed issue with add\_redact\_annot() mentioned in #2934.
  - Fixed [`Page.rotation()`](page.html#Page.rotation "Page.rotation") to return 0 for non-PDF documents instead of raising an exception.
  - Fixed internal quad detection to cope with any Python sequence.
  - Fixed rebased `fitz.pymupdf_version_tuple` - was previously set to mupdf version.
  - Improved support for Linux system installs, including adding regular testing on Github.
  - Add missing `flake8` to `scripts/gh_release.py:test_packages`.
  - Use newly public functions in MuPDF-1.23.8.
  - Improved `scripts/test.py` to help investigation of MuPDF issues.

**Changes in version 1.23.8 (2023-12-19)**

- Bug fixes (rebased implementation only):

  - **Fixed** [2634](https://github.com/pymupdf/PyMuPDF/issues/2634): get\_toc and set\_toc do not behave consistently for rotated pages
  - **Fixed** [2861](https://github.com/pymupdf/PyMuPDF/issues/2861): AttributeError in getLinkDict during PDF Merge
  - **Fixed** [2871](https://github.com/pymupdf/PyMuPDF/issues/2871): KeyError in getLinkDict during PDF merge
  - **Fixed** [2886](https://github.com/pymupdf/PyMuPDF/issues/2886): Error in Skeleton for Named Link Destinations
- Bug fixes (rebased and classic implementations):

  - **Fixed** [2885](https://github.com/pymupdf/PyMuPDF/issues/2885): pymupdf find tables too slow
- Other:

  - Rebased implementation:

    - [`Page.insert_htmlbox()`](page.html#Page.insert_htmlbox "Page.insert_htmlbox"): new, much more powerful alternative to [`Page.insert_textbox()`](page.html#Page.insert_textbox "Page.insert_textbox") or [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox"), using [Story](story-class.html#story).
    - `Story.fit*()`: new methods for fitting a Story into an expanded rect.
    - [`Story.write_with_links()`](story-class.html#Story.write_with_links "Story.write_with_links"): add support for external links.
    - `Document.language()`: fixed to use MuPDF’s new `mupdf.fz_string_from_text_language2()`.
    - [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts") - fixed.
    - Fixed internal `Archive._add_treeitem()` method.
    - Fixed `fitz_new.__doc__` to contain PyMuPDF and Python version information, and OS name.
    - Removed use of `(*args, **kwargs)` in API, we now specify keyword args explicitly.
    - Work with new MuPDF Python exception classes.
  - Fixed bug where [`button_states()`](widget.html#Widget.button_states "Widget.button_states") returns None when `/AP` points to an indirect object.
  - Fixed pillow test to not ignore all errors, and install pillow when testing.
  - Added test for `fitz.css_for_pymupdf_font()` (uses package `pymupdf-fonts`).
  - Simplified Github Actions test specifications.
  - Updated `tests/README.md`.

**Changes in version 1.23.7 (2023-11-30)**

- Bug fixes in rebased implementation, not fixed in classic implementation:

  - **Fixed** [2232](https://github.com/pymupdf/PyMuPDF/issues/2232): Geometry helper classes should support keyword arguments
  - **Fixed** [2788](https://github.com/pymupdf/PyMuPDF/issues/2788): Problem with get\_toc in pymupdf 1.23.6
  - **Fixed** [2791](https://github.com/pymupdf/PyMuPDF/issues/2791): Experiencing small memory leak in save()
- Bug fixes (rebased and classic implementations):

  - **Fixed** [2736](https://github.com/pymupdf/PyMuPDF/issues/2736): Failure when set cropbox with mediabox negative value
  - **Fixed** [2749](https://github.com/pymupdf/PyMuPDF/issues/2749): RuntimeError: cycle in structure tree
  - **Fixed** [2753](https://github.com/pymupdf/PyMuPDF/issues/2753): Story.write\_with\_links will ignore everything after the first “page break” in the HTML.
  - **Fixed** [2812](https://github.com/pymupdf/PyMuPDF/issues/2812): find\_tables on landscape page generates reversed text
  - **Fixed** [2829](https://github.com/pymupdf/PyMuPDF/issues/2829): [cannot create /Annot for kind] is still printed despite #2345 is closed.
  - **Fixed** [2841](https://github.com/pymupdf/PyMuPDF/issues/2841): Unexpected KeyError when using scrub with fitz\_new
- Use MuPDF-1.23.7.
- Other:

  - Rebased implementation:

    - Added flake8 code checking to test suite, and made various fixes.
    - Disable diagnostics during Document constructor to match classic implementation.
  - Additional fix to [2553](https://github.com/pymupdf/PyMuPDF/issues/2553): Invalid characters in versions >= 1.22
  - Fixed [MuPDF Bug 707324](https://bugs.ghostscript.com/show_bug.cgi?id=707324): Story: HTML table row background color repeated incorrectly
  - Added `scripts/test.py`, for simple build+test of PyMuPDF git checkout.
  - Added `fitz.pymupdf_version_tuple`, e.g. `(1, 23, 6)`.
  - Restored mistakenly-reverted fix for [2345](https://github.com/pymupdf/PyMuPDF/issues/2345): Turn off print statements in utils.py
  - Include any trailing `... repeated <N> times...` text in warnings returned by [`mupdf_warnings()`](tools.html#Tools.mupdf_warnings "Tools.mupdf_warnings") (rebased only).

**Changes in version 1.23.6 (2023-11-06)**

- Bug fixes:

  - **Fixed** [2553](https://github.com/pymupdf/PyMuPDF/issues/2553): Invalid characters in versions >= 1.22
  - **Fixed** [2608](https://github.com/pymupdf/PyMuPDF/issues/2608): Incorrect utf32 text extraction (high & low surrogates are split)
  - **Fixed** [2710](https://github.com/pymupdf/PyMuPDF/issues/2710): page.rect and text location wrong / differing from older version
  - **Fixed** [2774](https://github.com/pymupdf/PyMuPDF/issues/2774): wrong encoding for “?” character when sort=True
  - **Fixed** [2775](https://github.com/pymupdf/PyMuPDF/issues/2775): fitz\_new does not work with python3.10 or earlier
  - **Fixed** [2777](https://github.com/pymupdf/PyMuPDF/issues/2777): With fitz\_new, wrong type for Page.mediabox
- Other:

  - Use MuPDF-1.23.5.
  - Added Document.resolve\_names() (rebased implementation only).

**Changes in version 1.23.5 (2023-10-11)**

- Bug fixes:

  - **Fixed** [2341](https://github.com/pymupdf/PyMuPDF/issues/2341): Handling negative values in the zoom section for LINK\_GOTO in linkDest
  - **Fixed** [2522](https://github.com/pymupdf/PyMuPDF/issues/2522): Typo in set\_layer() - NameError: name ‘f’ is not defined
  - **Fixed** [2548](https://github.com/pymupdf/PyMuPDF/issues/2548): Fitz freezes on some PDFs when calling the fitz.Page.get\_text\_blocks method.
  - **Fixed** [2596](https://github.com/pymupdf/PyMuPDF/issues/2596): save(garbage=3) breaks get\_pixmap() with side effect
  - **Fixed** [2635](https://github.com/pymupdf/PyMuPDF/issues/2635): “clean=True” makes objects invisible in the pdf
  - **Fixed** [2637](https://github.com/pymupdf/PyMuPDF/issues/2637): Page.insert\_textbox incorrectly handles the last word if it starts a new line
  - **Fixed** [2699](https://github.com/pymupdf/PyMuPDF/issues/2699): extract paragraph with below table
  - **Fixed** [2703](https://github.com/pymupdf/PyMuPDF/issues/2703): Wrong fontsize calculation in corner cases (“page.get\_texttrace()”)
  - **Fixed** [2710](https://github.com/pymupdf/PyMuPDF/issues/2710): page.rect and text location wrong / differing from older version
  - **Fixed** [2723](https://github.com/pymupdf/PyMuPDF/issues/2723): When will a Python 3.12 wheel be available?
  - **Fixed** [2730](https://github.com/pymupdf/PyMuPDF/issues/2730): persistent get\_text() formatting
- Other:

  - Use MuPDF-1.23.4.
  - Fix optimisation flags with system installs.
  - Fixed the problem that the clip parameter does not take effect during table recognition
  - Support Pillow mode “RGBa”
  - Support extra word delimiters
  - Support checking valid PDF name objects

**Changes in version 1.23.4 (2023-09-26)**

- Improved build instructions.
- Fixed Tesseract in rebased implementation.
- Improvements to build/install with system MuPDF.
- Fixed Pyodide builds.
- Fixed rebased bug in \_insert\_image().
- Bug fixes:

  - **Fixed** [2556](https://github.com/pymupdf/PyMuPDF/issues/2556): Segmentation fault at calling get\_cdrawings(extended=True)
  - **Fixed** [2637](https://github.com/pymupdf/PyMuPDF/issues/2637): Page.insert\_textbox incorrectly handles the last word if it starts a new line
  - **Fixed** [2683](https://github.com/pymupdf/PyMuPDF/issues/2683): Windows sdist build failure - non-quoting of path and using UNIX which command
  - **Fixed** [2691](https://github.com/pymupdf/PyMuPDF/issues/2691): Page.get\_textpage\_ocr() bug in rebased fitz\_new version
  - **Fixed** [2692](https://github.com/pymupdf/PyMuPDF/issues/2692): Page.get\_pixmap(clip=Rect()) bug in rebased fitz\_new version

**Changes in version 1.23.3 (2023-08-31)**

- Fixed use of Tesseract for OCR.

**Changes in version 1.23.2 (2023-08-28)**

- **Fixed** [#2613](https://github.com/pymupdf/PyMuPDF/issues/2613): release 1.23.0 not MacOS-arm64 compatible

**Changes in version 1.23.1 (2023-08-24)**

- Updated README and package summary description.
- Fixed a problem on some Linux installations with Python-3.10
  (and possibly earlier versions) where `import fitz` failed with
  `ImportError: libcrypt.so.2: cannot open shared object file: No such
  file or directory`.
- Fixed `incompatible architecture` error on MacOS arm64.
- Fixed installation warning from Poetry about missing entry in wheels’
  RECORD files.

**Changes in version 1.23.0 (2023-08-22)**

- Add method [`find_tables()`](page.html#Page.find_tables "Page.find_tables") to the [Page](page.html#page) object.

  This allows locating tables on any supported document page, and
  extracting table content by cell.
- New “rebased” implementation of PyMuPDF.

  The rebased implementation is available as Python module
  `fitz_new`. It can be used as a drop-in replacement with `import
  fitz_new as fitz`.
- Python-independent MuPDF libraries are now in a second wheel called
  `PyMuPDFb` that will be automatically installed by pip.

  This is to save space on pypi.org - a full release only needs one
  `PyMuPDFb` wheel for each OS.
- Bug fixes:

  - **Fixed** [#2542](https://github.com/pymupdf/PyMuPDF/issues/2542): fitz.utils.scrub AttributeError Annot object has no attribute fileUpd inside
  - **Fixed** [#2533](https://github.com/pymupdf/PyMuPDF/issues/2533): get\_texttrace returned a incorrect character bbox
  - **Fixed** [#2537](https://github.com/pymupdf/PyMuPDF/issues/2537): Validation when setting a grouped RadioButton throws a RuntimeError: path to ‘V’ has indirects
- Other changes:

  - Dropped support for Python-3.7.
  - Fix for wrong page / annot `/Contents` cleaning.

    We need to set `pdf_filter_options::no_update` to zero.
  - Added new function get\_tessdata().
  - Cope with problem `/Annot` arrays.

    When copying page annotations in method Document.insert\_pdf we
    previously did not check the validity of members of the `/Annots`
    array. For faulty members (like null or non-dictionary items) this
    could cause unnecessary exceptions. This fix implements more checks
    and skips such array items.
  - Additional annotation type checks.

    We did not previously check for annotation type when getting /
    setting annotation border properties. This is now checked in
    accordance with MuPDF.
  - Increase fault tolerance.

    Avoid exceptions in method [`insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf") when source pages contains
    invalid items in the `/Annots` array.
  - Return empty border dict for applicable annots.

    We previously were returning a non-empty border dictionary even for
    non-applicable annotation types. We now return the empty dictionary
    `{}` in these cases. This requires some corresponding changes in the
    annotation `.update()` method, namely for dashes and border width.
  - Restrict [`set_rect`](annot.html#Annot.set_rect "Annot.set_rect") to applicable annot types.

    We were insufficiently excluding non-applicable annotation types
    from [`set_rect()`](annot.html#Annot.set_rect "Annot.set_rect") method. We now let MuPDF catch unsupported
    annotations and return `False` in these cases.
  - Wrong fontsize computation in `page.get_texttrace()`.

    When computing the font size we were using the final text
    transformation matrix, where we should have taken `span->trm`
    instead. This is corrected here.
  - Updates to cope with changes to latest MuPDF.

    `pdf_lookup_anchor()` has been removed.
  - Update fill\_textbox to better respect rect.width

    The function norm\_words in fill\_textbox had a bug in its last
    loop, appending n+1 characters when actually measuring width of n
    characters. It led to a bug in fill\_texbox when you tried to write
    a single word mostly composed of “wide” letters (M,m, W, w…),
    causing the written text to exceed the given rect.

    The fix was just to replace n+1 by n.
  - Add [`script_focus`](widget.html#Widget.script_focus "Widget.script_focus") and [`script_blur`](widget.html#Widget.script_blur "Widget.script_blur") options to widget.

**Changes in version 1.22.5 (2023-06-21)**

- This release uses `MuPDF-1.22.2`.
- Bug fixes:

  - **Fixed** [#2365](https://github.com/pymupdf/PyMuPDF/issues/2365): Incorrect dictionary values for type “fs” drawings.
  - **Fixed** [#2391](https://github.com/pymupdf/PyMuPDF/issues/2391): Check box automatically uncheck when we update same checkbox more than 1 times.
  - **Fixed** [#2400](https://github.com/pymupdf/PyMuPDF/issues/2400): Gaps within text of same line not filled with spaces.
  - **Fixed** [#2404](https://github.com/pymupdf/PyMuPDF/issues/2404): Blacklining an image in PDF won’t remove underlying content in version 1.22.X.
  - **Fixed** [#2430](https://github.com/pymupdf/PyMuPDF/issues/2430): Incorrectly reducing ref count of Py\_None.
  - **Fixed** [#2450](https://github.com/pymupdf/PyMuPDF/issues/2450): Empty fill color and fill opacity for paths with fill and stroke operations with 1.22.\*
  - **Fixed** [#2462](https://github.com/pymupdf/PyMuPDF/issues/2462): Error at “get\_drawing(extended=True )”
  - **Fixed** [#2468](https://github.com/pymupdf/PyMuPDF/issues/2468): Decode error when trying to get drawings
  - **Fixed** [#2710](https://github.com/pymupdf/PyMuPDF/issues/2710): page.rect and text location wrong / differing from older version
  - **Fixed** [#2723](https://github.com/pymupdf/PyMuPDF/issues/2723): When will a Python 3.12 wheel be available?
- New features:

  - **Changed** Annotations now support “cloudy” borders.
    The [`Annot.border`](annot.html#Annot.border "Annot.border") property has the new item `clouds`,
    and method [`Annot.set_border()`](annot.html#Annot.set_border "Annot.set_border") supports the corresponding `clouds` argument.
  - **Changed** Radio button widgets in the same RB group
    are now consistently updated **if the group is defined in the standard way**.
  - **Added** Support for the `/Locked` key in PDF Optional Content.
    This array inside the catalog entry `/OCProperties` can now be extracted and set.
  - **Added** Support for new parameter `tessdata` in OCR functions.
    New function [`get_tessdata()`](functions.html#get_tessdata "get_tessdata") locates the language support folder if Tesseract is installed.

**Changes in version 1.22.3 (2023-05-10)**

- This release uses `MuPDF-1.22.0`.
- Bug fixes:

  - **Fixed** [#2333](https://github.com/pymupdf/PyMuPDF/issues/2333): Unable to set any of button radio group in form

**Changes in version 1.22.2 (2023-04-26)**

- This release uses `MuPDF-1.22.0`.
- Bug fixes:

  - **Fixed** [#2369](https://github.com/pymupdf/PyMuPDF/issues/2369): Image extraction bugs with newer versions

**Changes in version 1.22.1 (2023-04-18)**

- This release uses `MuPDF-1.22.0`.
- Bug fixes:

  - **Fixed** [#2345](https://github.com/pymupdf/PyMuPDF/issues/2345): Turn off print statements in utils.py
  - **Fixed** [#2348](https://github.com/pymupdf/PyMuPDF/issues/2348): extract\_image returns an extension “flate” instead of “png”
  - **Fixed** [#2350](https://github.com/pymupdf/PyMuPDF/issues/2350): Can not make widget (checkbox) to read-only by adding flags PDF\_FIELD\_IS\_READ\_ONLY
  - **Fixed** [#2355](https://github.com/pymupdf/PyMuPDF/issues/2355): 1.22.0 error when using get\_toc (AttributeError: ‘SwigPyObject’ object has no attribute)

**Changes in version 1.22.0 (2023-04-14)**

- This release uses `MuPDF-1.22.0`.
- Behavioural changes:

  - Text extraction now includes glyphs that overlap with clip rect; previously
    they were included only if they were entirely contained within the clip
    rect.
- Bug fixes:

  - **Fixed** [#1763](https://github.com/pymupdf/PyMuPDF/issues/1763): Interactive(smartform) form PDF calculation not working in pymupdf
  - **Fixed** [#1995](https://github.com/pymupdf/PyMuPDF/issues/1995): RuntimeError: image is too high for a long paged pdf file when trying
  - **Fixed** [#2093](https://github.com/pymupdf/PyMuPDF/issues/2093): Image in pdf changes color after applying redactions
  - **Fixed** [#2108](https://github.com/pymupdf/PyMuPDF/issues/2108): Redaction removing more text than expected
  - **Fixed** [#2141](https://github.com/pymupdf/PyMuPDF/issues/2141): Failed to read JPX header when trying to get blocks
  - **Fixed** [#2144](https://github.com/pymupdf/PyMuPDF/issues/2144): Replace image throws an error
  - **Fixed** [#2146](https://github.com/pymupdf/PyMuPDF/issues/2146): Wrong Handling of Reference Count of “None” Object
  - **Fixed** [#2161](https://github.com/pymupdf/PyMuPDF/issues/2161): Support adding images as pages directly
  - **Fixed** [#2168](https://github.com/pymupdf/PyMuPDF/issues/2168): `page.add_highlight_annot(start=pointa, stop=pointb)` not working
  - **Fixed** [#2173](https://github.com/pymupdf/PyMuPDF/issues/2173): Double free of `Colorspace` used in `Pixmap`
  - **Fixed** [#2179](https://github.com/pymupdf/PyMuPDF/issues/2179): Incorrect documentation for `pixmap.tint_with()`
  - **Fixed** [#2208](https://github.com/pymupdf/PyMuPDF/issues/2208): Pushbutton widget appears as check box
  - **Fixed** [#2210](https://github.com/pymupdf/PyMuPDF/issues/2210): `apply_redactions()` move pdf text to right after redaction
  - **Fixed** [#2220](https://github.com/pymupdf/PyMuPDF/issues/2220): `Page.delete_image()` | object has no attribute `is_image`
  - **Fixed** [#2228](https://github.com/pymupdf/PyMuPDF/issues/2228): open some pdf cost too much time
  - **Fixed** [#2238](https://github.com/pymupdf/PyMuPDF/issues/2238): Bug - can not extract data from file in the newest version 1.21.1
  - **Fixed** [#2242](https://github.com/pymupdf/PyMuPDF/issues/2242): Python quits silently in `Story.element_positions()` if callback function prototype is wrong
  - **Fixed** [#2246](https://github.com/pymupdf/PyMuPDF/issues/2246): TextWriter write text in a wrong position
  - **Fixed** [#2248](https://github.com/pymupdf/PyMuPDF/issues/2248): After redacting the content, the position of the remaining text changes
  - **Fixed** [#2250](https://github.com/pymupdf/PyMuPDF/issues/2250): docs: unclear or broken link in page.rst
  - **Fixed** [#2251](https://github.com/pymupdf/PyMuPDF/issues/2251): mupdf\_display\_errors does not apply to Pixmap when loading broken image
  - **Fixed** [#2270](https://github.com/pymupdf/PyMuPDF/issues/2270): `Annot.get_text("words")` - doesn’t return the first line of words
  - **Fixed** [#2275](https://github.com/pymupdf/PyMuPDF/issues/2275): insert\_image: document that rotations are counterclockwise
  - **Fixed** [#2278](https://github.com/pymupdf/PyMuPDF/issues/2278): Can not make widget (checkbox) to read-only by adding flags PDF\_FIELD\_IS\_READ\_ONLY
  - **Fixed** [#2290](https://github.com/pymupdf/PyMuPDF/issues/2290): Different image format/data from Page.get\_text(“dict”) and Fitz.get\_page\_images()
  - **Fixed** [#2293](https://github.com/pymupdf/PyMuPDF/issues/2293): 68 failed tests when installing from sdist on my box
  - **Fixed** [#2300](https://github.com/pymupdf/PyMuPDF/issues/2300): Too much recursion in tree (parents), makes program terminate
  - **Fixed** [#2322](https://github.com/pymupdf/PyMuPDF/issues/2322): add\_highlight\_annot using clip generates “A Number is Out of Range” error in PDF
- Other:

  - Add key “/AS (Yes)” to the underlying annot object of a selected button form field.
  - Remove unused `Document` methods `has_xref_streams()` and
    `has_old_style_xrefs()` as MuPDF equivalents have been removed.
  - Add new `Document` methods and properties for getting/setting
    `/PageMode`, `/PageLayout` and `/MarkInfo`.
  - New `Document` property `version_count`, which contains the number of
    incremental saves plus one.
  - New `Document` property `is_fast_webaccess` which tells whether the
    document is linearized.
  - `DocumentWriter` is now a context manager.
  - Add support for `Pixmap` JPEG output.
  - Add support for drawing rectangles with rounded corners.
  - `get_drawings()`: added optional `extended` arg.
  - Fixed issue where trace devices’ state was not being initialised
    correctly; data returned from things like `fitz.Page.get_texttrace()`
    might be slightly altered, e.g. `linewidth` values.
  - Output warning to `stderr` if it looks like we are being used with
    current directory containing an invalid `fitz/` directory, because
    this can break import of `fitz` module. For example this happens
    if one attempts to use `fitz` when current directory is a PyMuPDF
    checkout.
- Documentation:

  - General rework:

    - Introduces a new home page and new table of contents.
    - Structural update to include new About section.
    - Comparison & performance graphing.
    - Includes performance methodology in appendix.
    - Updates conf.py to understand single back-ticks as code.
    - Converts double back-ticks to single back-ticks.
    - Removes redundant files.
  - Improve `insert_file()` documentation.
  - `get_bboxlog()`: added optional `layers` to `get_bboxlog()`.
  - `Page.get_texttrace()`: add new dictionary key `layer`, name of Optional Content Group.
  - Mention use of Python venv in installation documentation.
  - Added missing fix for #2057 to release 1.21.1’s changelog.
  - Fixes many links to the PyMuPDF-Utilities repo scripts.
  - Avoid duplication of `changes.txt` and `docs/changes.rst`.
- Build

  - Added `pyproject.toml` file to improve builds using pip etc.

**Changes in Version 1.21.1 (2022-12-13)**

- This release uses `MuPDF-1.21.1`.
- Bug fixes:

  - **Fixed** [#2110](https://github.com/pymupdf/PyMuPDF/issues/2110): Fully embedded font is extracted only partially if it occupies more than one object
  - **Fixed** [#2094](https://github.com/pymupdf/PyMuPDF/issues/2094): Rectangle Detection Logic
  - **Fixed** [#2088](https://github.com/pymupdf/PyMuPDF/issues/2088): Destination point not set for named links in toc
  - **Fixed** [#2087](https://github.com/pymupdf/PyMuPDF/issues/2087): Image with Filter “[/FlateDecode/JPXDecode]” not extracted
  - **Fixed** [#2086](https://github.com/pymupdf/PyMuPDF/issues/2086): Document.save() owner\_pw & user\_pw has buffer overflow bug
  - **Fixed** [#2076](https://github.com/pymupdf/PyMuPDF/issues/2076): Segfault in fitz.py
  - **Fixed** [#2057](https://github.com/pymupdf/PyMuPDF/issues/2057): Document.save garbage parameter not working in PyMuPDF 1.21.0
  - **Fixed** [#2051](https://github.com/pymupdf/PyMuPDF/issues/2051): Missing DPI Parameter
  - **Fixed** [#2048](https://github.com/pymupdf/PyMuPDF/issues/2048): Invalid size of TextPage and bbox with newest version 1.21.0
  - **Fixed** [#2045](https://github.com/pymupdf/PyMuPDF/issues/2045): SystemError: <built-in function Page\_get\_texttrace> returned a result with an error set
  - **Fixed** [#2039](https://github.com/pymupdf/PyMuPDF/issues/2039): 1.21.0 fails to build against system libmupdf
  - **Fixed** [#2036](https://github.com/pymupdf/PyMuPDF/issues/2036): Archive::Archive defined twice
- Other

  - Swallow “&zoom=nan” in link uri strings.
  - Add new Page utility methods `Page.replace_image()` and `Page.delete_image()`.
- Documentation:

  - [#2040](https://github.com/pymupdf/PyMuPDF/issues/2040): Added note about test failure with non-default build of MuPDF, to `tests/README.md`.
  - [#2037](https://github.com/pymupdf/PyMuPDF/issues/2037): In `docs/installation.rst`, mention incompatibility with chocolatey.org on Windows.
  - [#2061](https://github.com/pymupdf/PyMuPDF/issues/2061): Fixed description of `Annot.file_info`.
  - [#2065](https://github.com/pymupdf/PyMuPDF/issues/2065): Show how to insert internal PDF link.
  - Improved description of building from source without an sdist.
  - Added information about running tests.
  - [#2084](https://github.com/pymupdf/PyMuPDF/issues/2084): Fixed broken link to PyMuPDF-Utilities.

**Changes in Version 1.21.0 (2022-11-8)**

- This release uses `MuPDF-1.21.0`.
- New feature: Stories.
- Added wheels for Python-3.11.
- Bug fixes:

  - **Fixed** [#1701](https://github.com/pymupdf/PyMuPDF/issues/1701): Broken custom image insertion.
  - **Fixed** [#1854](https://github.com/pymupdf/PyMuPDF/issues/1854): [`Document.delete_pages()`](document.html#Document.delete_pages "Document.delete_pages") declines keyword arguments.
  - **Fixed** [#1868](https://github.com/pymupdf/PyMuPDF/issues/1868): Access Violation Error at `page.apply_redactions()`.
  - **Fixed** [#1909](https://github.com/pymupdf/PyMuPDF/issues/1909): Adding text with `fontname="Helvetica"` can silently fail.
  - **Fixed** [#1913](https://github.com/pymupdf/PyMuPDF/issues/1913): [`draw_rect()`](page.html#Page.draw_rect "Page.draw_rect"): does not respect width if color is not specified.
  - **Fixed** [#1917](https://github.com/pymupdf/PyMuPDF/issues/1917): [`subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts"): make it possible to silence the stdout.
  - **Fixed** [#1936](https://github.com/pymupdf/PyMuPDF/issues/1936): Rectangle detection can be incorrect producing wrong output.
  - **Fixed** [#1945](https://github.com/pymupdf/PyMuPDF/issues/1945): Segmentation fault when saving with `clean=True`.
  - **Fixed** [#1965](https://github.com/pymupdf/PyMuPDF/issues/1965): [`pdfocr_save()`](pixmap.html#Pixmap.pdfocr_save "Pixmap.pdfocr_save") Hard Crash.
  - **Fixed** [#1971](https://github.com/pymupdf/PyMuPDF/issues/1971): Segmentation fault when using [`get_drawings()`](page.html#Page.get_drawings "Page.get_drawings").
  - **Fixed** [#1946](https://github.com/pymupdf/PyMuPDF/issues/1946): `block_no` and `block_type` switched in [`get_text()`](annot.html#Annot.get_text "Annot.get_text") docs.
  - **Fixed** [#2013](https://github.com/pymupdf/PyMuPDF/issues/2013): AttributeError: ‘Widget’ object has no attribute ‘\_annot’ in delete widget.
- Misc changes to core code:

  - Fixed various compiler warnings and a sequence-point bug.
  - Added support for Memento builds.
  - Fixed leaks detected by Memento in test suite.
  - Fixed handling of exceptions in set\_name() and set\_rect().
  - Allow build with latest MuPDF, for regular testing of PyMuPDF master.
  - Cope with new MuPDF exceptions when setting rect for some Annot types.
  - Reduced cosmetic differences between MuPDF’s config.h and PyMuPDF’s \_config.h.
  - Cope with various changes to MuPDF API.
- Other:

  - Fixed various broken links and typos in docs.
  - Mention install of `swig-python` on MacOS for #875.
  - Added (untested) wheels for macos-arm64.

**Changes in Version 1.20.2**

- This release uses `MuPDF-1.20.3`.
- **Fixed** [#1787](https://github.com/pymupdf/PyMuPDF/issues/1787).
  Fix linking issues on Unix systems.
- **Fixed** [#1824](https://github.com/pymupdf/PyMuPDF/issues/1824).
  SegFault when applying redactions overlapping a transparent image. (Fixed
  in `MuPDF-1.20.3`.)
- Improvements to documentation:

  - Improved information about building from source in `docs/installation.rst`.
  - Clarified memory allocation setting ``` JM_MEMORY` in ``docs/tools.rst ```.
  - Fixed link to PDF Reference manual in `docs/app3.rst`.
  - Fixed building of html documentation on OpenBSD.
  - Moved old `docs/faq.rst` into separate `docs/recipes-*` files.
- Removed some unused files and directories:

  - `installation/`
  - `docs/wheelnames.txt`

**Changes in Version 1.20.1**

- **Fixed** [#1724](https://github.com/pymupdf/PyMuPDF/issues/1724).
  Fix for building on FreeBSD.
- **Fixed** [#1771](https://github.com/pymupdf/PyMuPDF/issues/1771).
  [`linkDest()`](linkdest.html#linkDest "linkDest") had a broken call to `re.match()`, introduced in 1.20.0.
- **Fixed** [#1751](https://github.com/pymupdf/PyMuPDF/issues/1751).
  [`get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") and [`get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings") previously always returned with `closePath=False`.
- **Fixed** [#1645](https://github.com/pymupdf/PyMuPDF/issues/1645).
  Default FreeText annotation text color is now black.
- Improvements to sphinx-generated documentation:

  - Use readthedocs theme with enhancements.
  - Renamed the `.txt` files to have `.rst` suffixes.

---

**Changes in Version 1.20.0**

This release uses `MuPDF-1.20.0`, released 2022-06-15.

- Cope with new MuPDF link uri format, changed from `#<int>,<int>,<int>` to `#page=<int>&zoom=<float>,<float>,<float>`.

> - In `tests/test_insertpdf.py`, use new reference output `joined-1.20.pdf`. We also check that new output values are approximately the same as the old ones.

- **Fixed** [#1738](https://github.com/pymupdf/PyMuPDF/issues/1738). Leak of `pdf_graft_map`.
  Also fixed a SEGV issue that this seemed to expose, caused by incorrect freeing of underlying fz\_document.
- **Fixed** [#1733](https://github.com/pymupdf/PyMuPDF/issues/1733). Fixed ownership of `Annotation.get_pixmap()`.

Changes to build/release process:

- If pip builds from source because an appropriate wheel is not available, we no longer require MuPDF to be pre-installed. Instead the required MuPDF source is embedded in the sdist and automatically built into PyMuPDF.
- Various changes to `setup.py` to download the required MuPDF release as required. See comments at start of setup.py for details.
- Added `.github/workflows/build_wheels.yml` to control building of wheels on Github.

---

**Changes in Version 1.19.6**

- **Fixed** [#1620](https://github.com/pymupdf/PyMuPDF/issues/1620). The [TextPage](textpage.html#textpage) created by [`Page.get_textpage()`](page.html#Page.get_textpage "Page.get_textpage") will now be freed correctly (removed memory leak).
- **Fixed** [#1601](https://github.com/pymupdf/PyMuPDF/issues/1601). Document open errors should now be more concise and easier to interpret. In the course of this, two PyMuPDF-specific Python exceptions have been **added:**

  > - `EmptyFileError` – raised when trying to create a [Document](document.html#document) (`fitz.open()`) from an empty file or zero-length memory.
  > - `FileDataError` – raised when MuPDF encounters irrecoverable document structure issues.
- **Added** [`Page.load_widget()`](page.html#Page.load_widget "Page.load_widget") given a PDF field’s xref.
- **Added** Dictionary [`pdfcolor`](functions.html#pdfcolor "pdfcolor") which provide the about 500 colors defined as PDF color values with the lower case color name as key.
- **Added** algebra functionality to the [Quad](quad.html#quad) class. These objects can now also be added and subtracted among themselves, and be multiplied by numbers and matrices.
- **Added** new constants defining the default text extraction flags for more comfortable handling. Their naming convention is like [`TEXTFLAGS_WORDS`](vars.html#TEXTFLAGS_WORDS "TEXTFLAGS_WORDS") for `page.get_text("words")`. See [Text Extraction Flags Defaults](app1.html#text-extraction-flags).
- **Changed** [`Page.annots()`](page.html#Page.annots "Page.annots") and [`Page.widgets()`](page.html#Page.widgets "Page.widgets") to detect and prevent reloading the page (illegally) inside the iterator loops via [`Document.reload_page()`](document.html#Document.reload_page "Document.reload_page"). Doing this brings down the interpreter. Documented clean ways to do annotation and widget mass updates within properly designed loops.
- **Changed** several internal utility functions to become standalone (“SWIG inline”) as opposed to be part of the [Tools](tools.html#tools) class. This, among other things, increases the performance of geometry object creation.
- **Changed** [`Document.update_stream()`](document.html#Document.update_stream "Document.update_stream") to always accept stream updates - whether or not the dictionary object behind the xref already is a stream. Thus the former `new` parameter is now ignored and will be removed in v1.20.0.

---

**Changes in Version 1.19.5**

- **Fixed** [#1518](https://github.com/pymupdf/PyMuPDF/issues/1518). A limited “fix”: in some cases, rectangles and quadrupels were not correctly encoded to support re-drawing by [Shape](shape.html#shape).
- **Fixed** [#1521](https://github.com/pymupdf/PyMuPDF/issues/1521). This had the same ultimate reason behind issue #1510.
- **Fixed** [#1513](https://github.com/pymupdf/PyMuPDF/issues/1513). Some Optional Content functions did not support non-ASCII characters.
- **Fixed** [#1510](https://github.com/pymupdf/PyMuPDF/issues/1510). Support more soft-mask image subtypes.
- **Fixed** [#1507](https://github.com/pymupdf/PyMuPDF/issues/1507). Immunize against items in the outlines chain, that are `"null"` objects.
- **Fixed** re-opened [#1417](https://github.com/pymupdf/PyMuPDF/issues/1417). (“too many open files”). This was due to insufficient calls to MuPDF’s `fz_drop_document()`. This also fixes [#1550](https://github.com/pymupdf/PyMuPDF/issues/1550).
- **Fixed** several undocumented issues in relation to incorrectly setting the text span origin [`point_like`](glossary.html#point_like "point_like").
- **Fixed** undocumented error computing the character bbox in method [`Page.get_texttrace()`](functions.html#Page.get_texttrace "Page.get_texttrace") when text is **flipped** (as opposed to just rotated).
- **Added** items to the dictionary returned by `image_properties()`: `orientation` and `transform` report the natural image orientation (EXIF data).
- **Added** method [`Document.xref_copy()`](document.html#Document.xref_copy "Document.xref_copy"). It will make a given target PDF object an exact copy of a source object.

---

**Changes in Version 1.19.4**

- **Fixed** [#1505](https://github.com/pymupdf/PyMuPDF/issues/1505). Immunize against circular outline items.
- **Fixed** [#1484](https://github.com/pymupdf/PyMuPDF/issues/1484). Correct CropBox coordinates are now returned in all situations.
- **Fixed** [#1479](https://github.com/pymupdf/PyMuPDF/issues/1479).
- **Fixed** [#1474](https://github.com/pymupdf/PyMuPDF/issues/1474). TextPage objects are now properly deleted again.
- **Added** [Page](page.html#page) methods and attributes for PDF `/ArtBox`, `/BleedBox`, `/TrimBox`.
- **Added** global attribute `TESSDATA_PREFIX` for easy checking of OCR support.
- **Changed** [`Document.xref_set_key()`](document.html#Document.xref_set_key "Document.xref_set_key") such that dictionary keys will physically be removed if set to value `"null"`.
- **Changed** [`Document.extract_font()`](document.html#Document.extract_font "Document.extract_font") to optionally return a dictionary (instead of a tuple).

---

**Changes in Version 1.19.3**

This patch version implements minor improvements for [Pixmap](pixmap.html#pixmap) and also some important fixes.

- **Fixed** [#1351](https://github.com/pymupdf/PyMuPDF/discussions/1351). Reverted code that introduced the memory growth in v1.18.15.
- **Fixed** [#1417](https://github.com/pymupdf/PyMuPDF/discussions/1417). Developed circumvention for growth of open file handles using [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf").
- **Fixed** [#1418](https://github.com/pymupdf/PyMuPDF/discussions/1418). Developed circumvention for memory growth using [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf").
- **Fixed** [#1430](https://github.com/pymupdf/PyMuPDF/discussions/1430). Developed circumvention for mass pixmap generations of document pages.
- **Fixed** [#1433](https://github.com/pymupdf/PyMuPDF/discussions/1433). Solves a bbox error for some Type 3 font in PyMuPDF text processing.
- **Added** [`Pixmap.color_topusage()`](pixmap.html#Pixmap.color_topusage "Pixmap.color_topusage") to determine the share of the most frequently used color. Solves [#1397](https://github.com/pymupdf/PyMuPDF/discussions/1397).
- **Added** [`Pixmap.warp()`](pixmap.html#Pixmap.warp "Pixmap.warp") which makes a new pixmap from a given arbitrary convex quad inside the pixmap.
- **Added** [`Annot.irt_xref`](annot.html#Annot.irt_xref "Annot.irt_xref") and [`Annot.set_irt_xref()`](annot.html#Annot.set_irt_xref "Annot.set_irt_xref") to inquire or set the `/IRT` (“In Response To”) property of an annotation. Implements [#1450](https://github.com/pymupdf/PyMuPDF/discussions/1450).
- **Added** [`Rect.torect()`](rect.html#Rect.torect "Rect.torect") and [`IRect.torect()`](irect.html#IRect.torect "IRect.torect") which compute a matrix that transforms to a given other rectangle.
- **Changed** [`Pixmap.color_count()`](pixmap.html#Pixmap.color_count "Pixmap.color_count") to also return the count of each color.
- **Changed** [`Page.get_texttrace()`](functions.html#Page.get_texttrace "Page.get_texttrace") to also return correct span and character bboxes if `span["dir"] != (1, 0)`.

---

**Changes in Version 1.19.2**

This patch version implements minor improvements for [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") and also some important fixes.

- **Fixed** [#1388](https://github.com/pymupdf/PyMuPDF/discussions/1388). Fixed intermittent memory corruption when insert or updating annotations.
- **Fixed** [#1375](https://github.com/pymupdf/PyMuPDF/discussions/1375). Inconsistencies between line numbers as returned by the “words” and the “dict” options of [`Page.get_text()`](page.html#Page.get_text "Page.get_text") have been corrected.
- **Fixed** [#1364](https://github.com/pymupdf/PyMuPDF/issues/1342). The check for being a `"rawdict"` span in [`recover_span_quad()`](functions.html#recover_span_quad "recover_span_quad") now works correctly.
- **Fixed** [#1342](https://github.com/pymupdf/PyMuPDF/issues/1364). Corrected the check for rectangle infiniteness in [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page").
- **Changed** [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings"), [`Page.get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings") to return an indicator on the area orientation covered by a rectangle. This implements [#1355](https://github.com/pymupdf/PyMuPDF/issues/1355). Also, the recognition rate for rectangles and quads has been significantly improved.
- **Changed** all text search and extraction methods to set the new `flags` option `TEXT_MEDIABOX_CLIP` to ON by default. That bit causes the automatic suppression of all characters that are completely outside a page’s mediabox (in as far as that notion is supported for a document type). This eliminates the need for using `clip=page.rect` or similar for omitting text outside the visible area.
- **Added** parameter `"dpi"` to [`Page.get_pixmap()`](page.html#Page.get_pixmap "Page.get_pixmap") and [`Annot.get_pixmap()`](annot.html#Annot.get_pixmap "Annot.get_pixmap"). When given, parameter `"matrix"` is ignored, and a [Pixmap](pixmap.html#pixmap) with the desired dots per inch is created.
- **Added** attributes [`Pixmap.is_monochrome`](pixmap.html#Pixmap.is_monochrome "Pixmap.is_monochrome") and [`Pixmap.is_unicolor`](pixmap.html#Pixmap.is_unicolor "Pixmap.is_unicolor") allowing fast checks of pixmap properties. Addresses [#1397](https://github.com/pymupdf/PyMuPDF/discussions/1397).
- **Added** method [`Pixmap.color_count()`](pixmap.html#Pixmap.color_count "Pixmap.color_count") to determine the unique colors in the pixmap.
- **Added** boolean parameter `"compress"` to PDF document method [`Document.update_stream()`](document.html#Document.update_stream "Document.update_stream"). Addresses / enables solution for [#1408](https://github.com/pymupdf/PyMuPDF/discussions/1408).

---

**Changes in Version 1.19.1**

This is the first patch version to support MuPDF v1.19.0. Apart from one bug fix, it includes important improvements for OCR support and the option to **sort extracted text** to the standard reading order “from top-left to bottom-right”.

- **Fixed** [#1328](https://github.com/pymupdf/PyMuPDF/issues/1328). “words” text extraction again returns correct `(x0, y0)` coordinates.
- **Changed** [`Page.get_textpage_ocr()`](page.html#Page.get_textpage_ocr "Page.get_textpage_ocr"): it now supports parameter `dpi` to control OCR quality. It is also possible to choose whether the **full page** should be OCRed or **only the images displayed** by the page.
- **Changed** [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") and [`Page.get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings") to automatically convert colors to RGB color tuples. Implements [#1332](https://github.com/pymupdf/PyMuPDF/discussions/1332). Similar change was applied to [`Page.get_texttrace()`](functions.html#Page.get_texttrace "Page.get_texttrace").
- **Changed** [`Page.get_text()`](page.html#Page.get_text "Page.get_text") to support a parameter `sort`. If set to `True` the output is conveniently sorted.

---

**Changes in Version 1.19.0**

This is the first version supporting MuPDF 1.19.\*, published 2021-10-05. It introduces many new features compared to the previous version 1.18.\*.

PyMuPDF has now picked up integrated Tesseract OCR support, which was already present in MuPDF v1.18.0.

- Supported images can be OCRed via their [Pixmap](pixmap.html#pixmap) which results in a 1-page PDF with a text layer.
- All supported document pages (i.e. not only PDFs), can be OCRed using specialized text extraction methods. The result is a mixture of standard and OCR text (depending on which part of the page was deemed to require OCRing) that can be searched and extracted without restrictions.
- All this requires an independent installation of Tesseract. MuPDF actually (only) needs the location of Tesseract’s `"tessdata"` folder, where its language support data are stored. This location must be available as environment variable `TESSDATA_PREFIX`.

A new MuPDF feature is **journalling PDF updates**, which is also supported by this PyMuPDF version. Changes may be logged, rolled back or replayed, allowing to implement a whole new level of control over PDF document integrity – similar to functions present in modern database systems.

A third feature (unrelated to the new MuPDF version) includes the ability to detect when page **objects cover or hide each other**. It is now e.g. possible to see that text is covered by a drawing or an image.

- **Changed** terminology and meaning of important geometry concepts: Rectangles are now characterized as *finite*, *valid* or *empty*, while the definitions of these terms have also changed. Rectangles specifically are now thought of being “open”: not all corners and sides are considered part of the rectangle. Please do read the [Rect](rect.html#rect) section for details.
- **Added** new parameter `"no_new_id"` to [`Document.save()`](document.html#Document.save "Document.save") / [`Document.tobytes()`](document.html#Document.tobytes "Document.tobytes") methods. Use it to suppress updating the second item of the document `/ID` which in PDF indicates that the original file has been updated. If the PDF has no `/ID` at all yet, then no new one will be created either.
- **Added** a **journalling facility** for PDF updates. This allows logging changes, undoing or redoing them, or saving the journal for later use. Refer to [`Document.journal_enable()`](document.html#Document.journal_enable "Document.journal_enable") and friends.
- **Added** new [Pixmap](pixmap.html#pixmap) methods [`Pixmap.pdfocr_save()`](pixmap.html#Pixmap.pdfocr_save "Pixmap.pdfocr_save") and [`Pixmap.pdfocr_tobytes()`](pixmap.html#Pixmap.pdfocr_tobytes "Pixmap.pdfocr_tobytes"), which generate a 1-page PDF containing the pixmap as PNG image with OCR text layer.
- **Added** [`Page.get_textpage_ocr()`](page.html#Page.get_textpage_ocr "Page.get_textpage_ocr") which executes optical character recognition for the page, then extracts the results and stores them together with “normal” page content in a [TextPage](textpage.html#textpage). Use or reuse this object in subsequent text extractions and text searches to avoid multiple efforts. The existing text search and text extraction methods have been extended to support a separately created textpage – see next item.
- **Added** a new parameter `textpage` to text extraction and text search methods. This allows reuse of a previously created [TextPage](textpage.html#textpage) and thus achieves significant runtime benefits – which is especially important for the new OCR features. But “normal” text extractions can definitely also benefit.
- **Added** [`Page.get_texttrace()`](functions.html#Page.get_texttrace "Page.get_texttrace"), a technical method delivering low-level text character properties. It was present before as a private method, but the author felt it now is mature enough to be officially available. It specifically includes a “sequence number” which indicates the page appearance build operation that painted the text.
- **Added** [`Page.get_bboxlog()`](functions.html#Page.get_bboxlog "Page.get_bboxlog") which delivers the list of rectangles of page objects like text, images or drawings. Its significance lies in its sequence: rectangles intersecting areas with a lower index are covering or hiding them.
- **Changed** methods [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") and [`Page.get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings") to include a “sequence number” indicating the page appearance build operation that created the drawing.
- **Fixed** [#1311](https://github.com/pymupdf/PyMuPDF/issues/1311). Field values in comboboxes should now be handled correctly.
- **Fixed** [#1290](https://github.com/pymupdf/PyMuPDF/issues/1290). Error was caused by incorrect rectangle emptiness check, which is fixed due to new geometry logic of this version.
- **Fixed** [#1286](https://github.com/pymupdf/PyMuPDF/issues/1286). Text alignment for redact annotations is working again.
- **Fixed** [#1287](https://github.com/pymupdf/PyMuPDF/issues/1287). Infinite loop issue for non-Windows systems when applying some redactions has been resolved.
- **Fixed** [#1284](https://github.com/pymupdf/PyMuPDF/issues/1284). Text layout destruction after applying redactions in some cases has been resolved.

---

**Changes in Version 1.18.18 / 1.18.19**

- **Fixed** issue [#1266](https://github.com/pymupdf/PyMuPDF/issues/1266). Failure to set [`Pixmap.samples`](pixmap.html#Pixmap.samples "Pixmap.samples") in important cases, was hotfixed in a new version 1.18.19.
- **Fixed** issue [#1257](https://github.com/pymupdf/PyMuPDF/issues/1257). Removing the read-only flag from PDF fields is now possible.
- **Fixed** issue [#1252](https://github.com/pymupdf/PyMuPDF/issues/1252). Now correctly specifying the `zoom` value for PDF link annotations.
- **Fixed** issue [#1244](https://github.com/pymupdf/PyMuPDF/issues/1244). Now correctly computing the transform matrix in `Page.get_image__bbox()`.
- **Fixed** issue [#1241](https://github.com/pymupdf/PyMuPDF/issues/1241). Prevent returning artifact characters in [`Page.get_textbox()`](page.html#Page.get_textbox "Page.get_textbox"), which happened in certain constellations.
- **Fixed** issue [#1234](https://github.com/pymupdf/PyMuPDF/issues/1234). Avoid creating infinite rectangles in corner cases – [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings"), [`Page.get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings").
- **Added** test data and test scripts to the source PyPI source distribution.

---

**Changes in Version 1.18.17**

Focus of this version are major performance improvements of selected functions.

- **Fixed** issue [#1199](https://github.com/pymupdf/PyMuPDF/issues/1199). Using a non-existing page number in [`Document.get_page_images()`](document.html#Document.get_page_images "Document.get_page_images") and friends will no longer lead to segfaults.
- **Changed** [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings") to now differentiate between “stroke”, “fill” and combined paths. Paths containing more than one rectangle (i.e. “re” items) are now supported. Extracting “clipped” paths is now available as an option.
- **Added** [`Page.get_cdrawings()`](page.html#Page.get_cdrawings "Page.get_cdrawings"), performance-optimized version of [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings").
- **Added** [`Pixmap.samples_mv`](pixmap.html#Pixmap.samples_mv "Pixmap.samples_mv"), *memoryview* of a pixmap’s pixel area. Does not copy and thus always accesses the current state of that area.
- **Added** [`Pixmap.samples_ptr`](pixmap.html#Pixmap.samples_ptr "Pixmap.samples_ptr"), Python “pointer” to a pixmap’s pixel area. Allows much faster creation (factor 800+) of Qt images.

---

**Changes in Version 1.18.16**

- **Fixed** issue [#1184](https://github.com/pymupdf/PyMuPDF/issues/1184). Existing PDF widget fonts in a PDF are now accepted (i.e. not forcedly changed to a Base-14 font).
- **Fixed** issue [#1154](https://github.com/pymupdf/PyMuPDF/issues/1154). Text search hits should now be correct when `clip` is specified.
- **Fixed** issue [#1152](https://github.com/pymupdf/PyMuPDF/issues/1152).
- **Fixed** issue [#1146](https://github.com/pymupdf/PyMuPDF/issues/1146).
- **Added** [`Link.flags`](link.html#Link.flags "Link.flags") and [`Link.set_flags()`](link.html#Link.set_flags "Link.set_flags") to the [Link](link.html#link) class. Implements enhancement requests [#1187](https://github.com/pymupdf/PyMuPDF/issues/1187).
- **Added** option to *simulate* [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox") output for predicting the number of lines, that a given text would occupy in the textbox.
- **Added** text output support as subcommand `gettext` to the `fitz` CLI module. Most importantly, original **physical text layout** reproduction is now supported.

---

**Changes in Version 1.18.15**

- **Fixed** issue [#1088](https://github.com/pymupdf/PyMuPDF/issues/1088). Removing an annotation’s fill color should now work again both ways, using the `fill_color=[]` argument in [`Annot.update()`](annot.html#Annot.update "Annot.update") as well as `fill=[]` in [`Annot.set_colors()`](annot.html#Annot.set_colors "Annot.set_colors").
- **Fixed** issue [#1081](https://github.com/pymupdf/PyMuPDF/issues/1081). [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts"): fixed an error which created wrong character widths for some fonts.
- **Fixed** issue [#1078](https://github.com/pymupdf/PyMuPDF/issues/1078). [`Page.get_text()`](page.html#Page.get_text "Page.get_text") and other methods related to text extraction: changed the default value of the [TextPage](textpage.html#textpage) `flags` parameter. All whitespace and `ligatures` are now preserved.
- **Fixed** issue [#1085](https://github.com/pymupdf/PyMuPDF/issues/1085). The old *snake\_cased* alias of `fitz.detTextlength` is now defined correctly.
- **Changed** [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts") will now correctly prefix font subsets with an appropriate six letter uppercase tag, complying with the PDF specification.
- **Added** new method [`Widget.button_states()`](widget.html#Widget.button_states "Widget.button_states") which returns the possible values that a button-type field can have when being set to “on” or “off”.
- **Added** support of text with **Small Capital** letters to the [Font](font.html#font) and [TextWriter](textwriter.html#textwriter) classes. This is reflected by an additional bool parameter `small_caps` in various of their methods.

---

**Changes in Version 1.18.14**

- **Finished** implementing new, “snake\_cased” names for methods and properties, that were “camelCased” and awkward in many aspects. At the end of this documentation, there is section [Deprecated Names](znames.html#deprecated) with more background and a mapping of old to new names.
- **Fixed** issue [#1053](https://github.com/pymupdf/PyMuPDF/issues/1053). [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image"): when given, include image mask in the hash computation.
- **Fixed** issue [#1043](https://github.com/pymupdf/PyMuPDF/issues/1043). Added `Pixmap.getPNGdata` to the aliases of [`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes").
- **Fixed** an internal error when computing the enveloping rectangle of drawn paths as returned by [`Page.get_drawings()`](page.html#Page.get_drawings "Page.get_drawings").
- **Fixed** an internal error occasionally causing loops when outputting text via [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox").
- **Added** [`Font.char_lengths()`](font.html#Font.char_lengths "Font.char_lengths"), which returns a tuple of character widths of a string.
- **Added** more ways to specify pages in [`Document.delete_pages()`](document.html#Document.delete_pages "Document.delete_pages"). Now a sequence (list, tuple or range) can be specified, and the Python `del` statement can be used. In the latter case, Python `slices` are also accepted.
- **Changed** [`Document.del_toc_item()`](document.html#Document.del_toc_item "Document.del_toc_item"), which disables a single item of the TOC: previously, the title text was removed. Instead, now the complete item will be shown grayed-out by supporting viewers.

---

**Changes in Version 1.18.13**

- **Fixed** issue [#1014](https://github.com/pymupdf/PyMuPDF/issues/1014).
- **Fixed** an internal memory leak when computing image bboxes – [`Page.get_image_bbox()`](page.html#Page.get_image_bbox "Page.get_image_bbox").
- **Added** support for low-level access and modification of the PDF trailer. Applies to [`Document.xref_get_keys()`](document.html#Document.xref_get_keys "Document.xref_get_keys"), [`Document.xref_get_key()`](document.html#Document.xref_get_key "Document.xref_get_key"), and [`Document.xref_set_key()`](document.html#Document.xref_set_key "Document.xref_set_key").
- **Added** documentation for maintaining private entries in PDF metadata.
- **Added** documentation for handling transparent image insertions, [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image").
- **Added** [`Page.get_image_rects()`](page.html#Page.get_image_rects "Page.get_image_rects"), an improved version of [`Page.get_image_bbox()`](page.html#Page.get_image_bbox "Page.get_image_bbox").
- **Changed** [`Document.delete_pages()`](document.html#Document.delete_pages "Document.delete_pages") to support various ways of specifying pages to delete. Implements [#1042](https://github.com/pymupdf/PyMuPDF/issues/1042).
- **Changed** [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image") to also accept the xref of an existing image in the file. This allows “copying” images between pages, and extremely fast multiple insertions.
- **Changed** [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image") to also accept the integer parameter `alpha`. To be used for performance improvements.
- **Changed** [`Pixmap.set_alpha()`](pixmap.html#Pixmap.set_alpha "Pixmap.set_alpha") to support new parameters for pre-multiplying colors with their alpha values and setting a specific color to fully transparent (e.g. white).
- **Changed** [`Document.embfile_add()`](document.html#Document.embfile_add "Document.embfile_add") to automatically set creation and modification date-time. Correspondingly, [`Document.embfile_upd()`](document.html#Document.embfile_upd "Document.embfile_upd") automatically maintains modification date-time (`/ModDate` PDF key), and [`Document.embfile_info()`](document.html#Document.embfile_info "Document.embfile_info") correspondingly reports these data. In addition, the embedded file’s associated “collection item” is included via its [`xref`](glossary.html#xref "xref"). This supports the development of PDF portfolio applications.

---

**Changes in Version 1.18.11 / 1.18.12**

- **Fixed** issue [#972](https://github.com/pymupdf/PyMuPDF/issues/972). Improved layout of source distribution material.
- **Fixed** issue [#962](https://github.com/pymupdf/PyMuPDF/issues/962). Stabilized Linux distribution detection for generating PyMuPDF from sources.
- **Added:** [`Page.get_xobjects()`](page.html#Page.get_xobjects "Page.get_xobjects") delivers the result of [`Document.get_page_xobjects()`](document.html#Document.get_page_xobjects "Document.get_page_xobjects").
- **Added:** [`Page.get_image_info()`](page.html#Page.get_image_info "Page.get_image_info") delivers meta information for all images shown on the page.
- **Added:** [`Tools.mupdf_display_warnings()`](tools.html#Tools.mupdf_display_warnings "Tools.mupdf_display_warnings") allows setting on / off the display of MuPDF-generated warnings. The default is off.
- **Added:** [`Document.ez_save()`](document.html#Document.ez_save "Document.ez_save") convenience alias of [`Document.save()`](document.html#Document.save "Document.save") with some different defaults.
- **Changed:** Image extractions of document pages now also contain the image’s **transformation matrix**. This concerns [`Page.get_image_bbox()`](page.html#Page.get_image_bbox "Page.get_image_bbox") and the DICT, JSON, RAWDICT, and RAWJSON variants of [`Page.get_text()`](page.html#Page.get_text "Page.get_text").

---

**Changes in Version 1.18.10**

- **Fixed** issue [#941](https://github.com/pymupdf/PyMuPDF/issues/941). Added old aliases for [`DisplayList.get_pixmap()`](displaylist.html#DisplayList.get_pixmap "DisplayList.get_pixmap") and [`DisplayList.get_textpage()`](displaylist.html#DisplayList.get_textpage "DisplayList.get_textpage").
- **Fixed** issue [#929](https://github.com/pymupdf/PyMuPDF/issues/929). Stabilized removal of JavaScript objects with [`Document.scrub()`](document.html#Document.scrub "Document.scrub").
- **Fixed** issue [#927](https://github.com/pymupdf/PyMuPDF/issues/927). Removed a loop in the reworked [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox").
- **Changed** [`Document.xref_get_keys()`](document.html#Document.xref_get_keys "Document.xref_get_keys") and [`Document.xref_get_key()`](document.html#Document.xref_get_key "Document.xref_get_key") to also allow accessing the PDF trailer dictionary. This can be done by using `-1` as the xref number argument.
- **Added** a number of functions for reconstructing the quads for text lines, spans and characters extracted by [`Page.get_text()`](page.html#Page.get_text "Page.get_text") options “dict” and “rawdict”. See [`recover_quad()`](functions.html#recover_quad "recover_quad") and friends.
- **Added** [`Tools.unset_quad_corrections()`](tools.html#Tools.unset_quad_corrections "Tools.unset_quad_corrections") to suppress character quad corrections (occasionally required for erroneous fonts).

---

**Changes in Version 1.18.9**

- **Fixed** issue [#888](https://github.com/pymupdf/PyMuPDF/issues/888). Removed ambiguous statements concerning PyMuPDF’s license, which is now clearly stated to be GNU AGPL V3.
- **Fixed** issue [#895](https://github.com/pymupdf/PyMuPDF/issues/895).
- **Fixed** issue [#896](https://github.com/pymupdf/PyMuPDF/issues/896). Since v1.17.6 PyMuPDF suppresses the font subset tags and only reports the base fontname in text extraction outputs “dict” / “json” / “rawdict” / “rawjson”. Now a new global parameter can request the old behaviour, [`Tools.set_subset_fontnames()`](tools.html#Tools.set_subset_fontnames "Tools.set_subset_fontnames").
- **Fixed** issue [#885](https://github.com/pymupdf/PyMuPDF/issues/885). Pixmap creation now also works with filenames given as `pathlib.Paths`.
- **Changed** [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts"): Text is **not rewritten** any more and should therefore **retain all its original properties** – like being hidden or being controlled by Optional Content mechanisms.
- **Changed** [TextWriter](textwriter.html#textwriter) output to also accept text in right to left mode (Arabian, Hebrew): [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox"), [`TextWriter.append()`](textwriter.html#TextWriter.append "TextWriter.append"). These methods now accept a new boolean parameter `right_to_left`, which is *False* by default. Implements [#897](https://github.com/pymupdf/PyMuPDF/issues/897).
- **Changed** [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox") to return all lines of text, that did not fit in the given rectangle. Also changed the default of the `warn` parameter to no longer print a warning message in overflow situations.
- **Added** a utility function [`recover_quad()`](functions.html#recover_quad "recover_quad"), which computes the quadrilateral of a span. This function can be used for correctly marking text extracted with the “dict” or “rawdict” options of [`Page.get_text()`](page.html#Page.get_text "Page.get_text").

---

**Changes in Version 1.18.8**

This is a bug fix version only. We are publishing early because of the potentially widely used functions.

- **Fixed** issue [#881](https://github.com/pymupdf/PyMuPDF/issues/881). Fixed a memory leak in [`Page.insert_image()`](page.html#Page.insert_image "Page.insert_image") when inserting images from files or memory.
- **Fixed** issue [#878](https://github.com/pymupdf/PyMuPDF/issues/878). `pathlib.Path` objects should now correctly handle file path hierarchies.

---

**Changes in Version 1.18.7**

- **Added** an experimental [`Document.subset_fonts()`](document.html#Document.subset_fonts "Document.subset_fonts") which reduces the size of eligible fonts based on their use by text in the PDF. Implements [#855](https://github.com/pymupdf/PyMuPDF/discussions/855).
- **Implemented** request [#870](https://github.com/pymupdf/PyMuPDF/pull/870): [`Document.convert_to_pdf()`](document.html#Document.convert_to_pdf "Document.convert_to_pdf") now also supports PDF documents.
- **Renamed** `Document.write` to [`Document.tobytes()`](document.html#Document.tobytes "Document.tobytes") for greater clarity. But the deprecated name remains available for some time.
- **Implemented** request [#843](https://github.com/pymupdf/PyMuPDF/Discussions/843): [`Document.tobytes()`](document.html#Document.tobytes "Document.tobytes") now supports linearized PDF output. [`Document.save()`](document.html#Document.save "Document.save") now also supports writing to Python **file objects**. In addition, the open function now also supports Python file objects.
- **Fixed** issue [#844](https://github.com/pymupdf/PyMuPDF/issues/844).
- **Fixed** issue [#838](https://github.com/pymupdf/PyMuPDF/issues/838).
- **Fixed** issue [#823](https://github.com/pymupdf/PyMuPDF/issues/823). More logic for better support of OCRed text output (Tesseract, ABBYY).
- **Fixed** issue [#818](https://github.com/pymupdf/PyMuPDF/issues/818).
- **Fixed** issue [#814](https://github.com/pymupdf/PyMuPDF/issues/814).
- **Added** [`Document.get_page_labels()`](document.html#Document.get_page_labels "Document.get_page_labels") which returns a list of page label definitions of a PDF.
- **Added** [`Document.has_annots()`](document.html#Document.has_annots "Document.has_annots") and [`Document.has_links()`](document.html#Document.has_links "Document.has_links") to check whether these object types are present anywhere in a PDF.
- **Added** expert low-level functions to simplify inquiry and modification of PDF object sources: [`Document.xref_get_keys()`](document.html#Document.xref_get_keys "Document.xref_get_keys") lists the keys of object [`xref`](glossary.html#xref "xref"), [`Document.xref_get_key()`](document.html#Document.xref_get_key "Document.xref_get_key") returns type and content of a key, and [`Document.xref_set_key()`](document.html#Document.xref_set_key "Document.xref_set_key") modifies the key’s value.
- **Added** parameter `thumbnails` to [`Document.scrub()`](document.html#Document.scrub "Document.scrub") to also allow removing page thumbnail images.
- **Improved** documentation for how to add valid text marker annotations for non-horizontal text.

We continued the process of renaming methods and properties from *“mixedCase”* to *“snake\_case”*. Documentation usually mentions the new names only, but old, deprecated names remain available for some time.

---

**Changes in Version 1.18.6**

- **Fixed** issue [#812](https://github.com/pymupdf/PyMuPDF/issues/812).
- **Fixed** issue [#793](https://github.com/pymupdf/PyMuPDF/issues/793). Invalid document metadata previously prevented opening some documents at all. This error has been removed.
- **Fixed** issue [#792](https://github.com/pymupdf/PyMuPDF/issues/792). Text search and text extraction will make no rectangle containment checks at all if the default `clip=None` is used.
- **Fixed** issue [#785](https://github.com/pymupdf/PyMuPDF/issues/785).
- **Fixed** issue [#780](https://github.com/pymupdf/PyMuPDF/issues/780). Corrected a parameter check error.
- **Fixed** issue [#779](https://github.com/pymupdf/PyMuPDF/issues/779). Fixed typo
- **Added** an option to set the desired line height for text boxes. Implements [#804](https://github.com/pymupdf/PyMuPDF/issues/804).
- **Changed** text position retrieval to better cope with Tesseract’s glyphless font. Implements [#803](https://github.com/pymupdf/PyMuPDF/issues/803).
- **Added** an option to choose the prefix of new annotations, fields and links for providing unique annotation ids. Implements request [#807](https://github.com/pymupdf/PyMuPDF/issues/807).
- **Added** getting and setting color and text properties for Table of Contents items for PDFs. Implements [#779](https://github.com/pymupdf/PyMuPDF/issues/779).
- **Added** PDF page label handling: [`Page.get_label()`](page.html#Page.get_label "Page.get_label") returns the page label, [`Document.get_page_numbers()`](document.html#Document.get_page_numbers "Document.get_page_numbers") return all page numbers having a specified label, and [`Document.set_page_labels()`](document.html#Document.set_page_labels "Document.set_page_labels") adds or updates a PDF’s page label definition.

Note

This version introduces **Python type hinting**. The goal is to provide each parameter and the return value of all functions and methods with type information. This still is work in progress although the majority of functions has already been handled.

---

**Changes in Version 1.18.5**

Apart from several fixes, this version also focusses on several minor, but important feature improvements. Among the latter is a more precise computation of proper line heights and insertion points for writing / inserting text. As opposed to using font-agnostic constants, these values are now taken from the font’s properties.

Also note that this is the first version which does no longer provide pregenerated wheels for Python versions older than 3.6. PIP also discontinues support for these by end of this year 2020.

- **Fixed** issue [#771](https://github.com/pymupdf/PyMuPDF/issues/771). By using “small glyph heights” option, the full page text can be extracted.
- **Fixed** issue [#768](https://github.com/pymupdf/PyMuPDF/issues/768).
- **Fixed** issue [#750](https://github.com/pymupdf/PyMuPDF/issues/750).
- **Fixed** issue [#739](https://github.com/pymupdf/PyMuPDF/issues/739). The “dict”, “rawdict” and corresponding JSON output variants now have two new *span* keys: `"ascender"` and `"descender"`. These floats represent special font properties which can be used to compute bboxes of spans or characters of **exactly fontsize height** (as opposed to the default line height). An example algorithm is shown in section “Span Dictionary” [here](https://pymupdf.readthedocs.io/en/latest/textpage.html#dictionary-structure-of-extractdict-and-extractrawdict). Also improved the detection and correction of ill-specified ascender / descender values encountered in some fonts.
- **Added** a new, experimental [`Tools.set_small_glyph_heights()`](tools.html#Tools.set_small_glyph_heights "Tools.set_small_glyph_heights") – also in response to issue [#739](https://github.com/pymupdf/PyMuPDF/issues/739). This method sets or unsets a global parameter to **always compute bboxes with fontsize height**. If “on”, text searching and all text extractions will returned rectangles, bboxes and quads with a smaller height.
- **Fixed** issue [#728](https://github.com/pymupdf/PyMuPDF/issues/728).
- **Changed** fill color logic of ‘Polyline’ annotations: this parameter now only pertains to line end symbols – the annotation itself can no longer have a fill color. Also addresses issue [#727](https://github.com/pymupdf/PyMuPDF/issues/727).
- **Changed** `Page.getImageBbox()` to also compute the bbox if the image is contained in an XObject.
- **Changed** `Shape.insertTextbox()`, resp. `Page.insertTextbox()`, resp. `TextWriter.fillTextbox()` to respect font’s properties “ascender” / “descender” when computing line height and insertion point. This should no longer lead to line overlaps for multi-line output. These methods used to ignore font specifics and used constant values instead.

---

**Changes in Version 1.18.4**

This version adds several features to support PDF Optional Content. Among other things, this includes OCMDs (Optional Content Membership Dictionaries) with the full scope of *“visibility expressions”* (PDF key `/VE`), text insertions (including the [TextWriter](textwriter.html#textwriter) class) and drawings.

- **Fixed** issue [#727](https://github.com/pymupdf/PyMuPDF/issues/727). Freetext annotations now support an uncolored rectangle when `fill_color=None`.
- **Fixed** issue [#726](https://github.com/pymupdf/PyMuPDF/issues/726). UTF-8 encoding errors are now handled for HTML / XML `Page.getText()` output.
- **Fixed** issue [#724](https://github.com/pymupdf/PyMuPDF/issues/724). Empty values are no longer stored in the PDF /Info metadata dictionary.
- **Added** new methods [`Document.set_oc()`](document.html#Document.set_oc "Document.set_oc") and [`Document.get_oc()`](document.html#Document.get_oc "Document.get_oc") to set or get optional content references for **existing** image and form XObjects. These methods are similar to the same-named methods of [Annot](annot.html#annot).
- **Added** [`Document.set_ocmd()`](document.html#Document.set_ocmd "Document.set_ocmd"), [`Document.get_ocmd()`](document.html#Document.get_ocmd "Document.get_ocmd") for handling OCMDs.
- **Added** **Optional Content** support for text insertion and drawing.
- **Added** new method `Page.deleteWidget()`, which deletes a form field from a page. This is analogous to deleting annotations.
- **Added** support for Popup annotations. This includes defining the Popup rectangle and setting the Popup to open or closed. Methods / attributes [`Annot.set_popup()`](annot.html#Annot.set_popup "Annot.set_popup"), [`Annot.set_open()`](annot.html#Annot.set_open "Annot.set_open"), [`Annot.has_popup`](annot.html#Annot.has_popup "Annot.has_popup"), [`Annot.is_open`](annot.html#Annot.is_open "Annot.is_open"), [`Annot.popup_rect`](annot.html#Annot.popup_rect "Annot.popup_rect"), [`Annot.popup_xref`](annot.html#Annot.popup_xref "Annot.popup_xref").

Other changes:

- The **naming of methods and attributes** in PyMuPDF is far from being satisfactory: we have *CamelCases*, *mixedCases* and *lower\_case\_with\_underscores* all over the place. With the [Annot](annot.html#annot) as the first candidate, we have started an activity to clean this up step by step, converting to lower case with underscores for methods and attributes while keeping UPPERCASE for the constants.

  > - Old names will remain available to prevent code breaks, but they will no longer be mentioned in the documentation.
  > - New methods and attributes of all classes will be named according to the new standard.

---

**Changes in Version 1.18.3**

As a major new feature, this version introduces support for PDF’s **Optional Content** concept.

- **Fixed** issue [#714](https://github.com/pymupdf/PyMuPDF/issues/714).
- **Fixed** issue [#711](https://github.com/pymupdf/PyMuPDF/issues/711).
- **Fixed** issue [#707](https://github.com/pymupdf/PyMuPDF/issues/707): if a PDF user password, but no owner password is supplied nor present, then the user password is also used as the owner password.
- **Fixed** `expand` and `deflate` parameters of methods [`Document.save()`](document.html#Document.save "Document.save") and `Document.write()`. Individual image and font compression should now finally work. Addresses issue [#713](https://github.com/pymupdf/PyMuPDF/issues/713).
- **Added** a support of PDF optional content. This includes several new [Document](document.html#document) methods for inquiring and setting optional content status and adding optional content configurations and groups. In addition, images, form XObjects and annotations now can be bound to optional content specifications. **Resolved** issue [#709](https://github.com/pymupdf/PyMuPDF/issues/709).

---

**Changes in Version 1.18.2**

This version contains some interesting improvements for text searching: any number of search hits is now returned and the **hit\_max** parameter was removed. The new **clip** parameter in addition allows to restrict the search area. Searching now detects hyphenations at line breaks and accordingly finds hyphenated words.

- **Fixed** issue [#575](https://github.com/pymupdf/PyMuPDF/issues/575): if using `quads=False` in text searching, then overlapping rectangles on the same line are joined. Previously, parts of the search string, which belonged to different “marked content” items, each generated their own rectangle – just as if occurring on separate lines.
- **Added** `Document.isRepaired`, which is true if the PDF was repaired on open.
- **Added** `Document.setXmlMetadata()` which either updates or creates PDF XML metadata. Implements issue [#691](https://github.com/pymupdf/PyMuPDF/issues/691).
- **Added** `Document.getXmlMetadata()` returns PDF XML metadata.
- **Changed** creation of PDF documents: they will now always carry a PDF identification (`/ID` field) in the document trailer. Implements issue [#691](https://github.com/pymupdf/PyMuPDF/issues/691).
- **Changed** `Page.searchFor()`: a new parameter `clip` is accepted to restrict the search to this rectangle. Correspondingly, the attribute [`TextPage.rect`](textpage.html#TextPage.rect "TextPage.rect") is now respected by [`TextPage.search()`](textpage.html#TextPage.search "TextPage.search").
- **Changed** parameter `hit_max` in `Page.searchFor()` and [`TextPage.search()`](textpage.html#TextPage.search "TextPage.search") is now obsolete: methods will return all hits.
- **Changed** character **selection criteria** in `Page.getText()`: a character is now considered to be part of a `clip` if its bbox is fully contained. Before this, a non-empty intersection was sufficient.
- **Changed** [`Document.scrub()`](document.html#Document.scrub "Document.scrub") to support a new option `redact_images`. This addresses issue [#697](https://github.com/pymupdf/PyMuPDF/issues/697).

---

**Changes in Version 1.18.1**

- **Fixed** issue [#692](https://github.com/pymupdf/PyMuPDF/issues/692). PyMuPDF now detects and recovers from more cyclic resource dependencies in PDF pages and for the first time reports them in the MuPDF warnings store.
- **Fixed** issue [#686](https://github.com/pymupdf/PyMuPDF/issues/686).
- **Added** opacity options for the [Shape](shape.html#shape) class: Stroke and fill colors can now be set to some transparency value. This means that all [Page](page.html#page) draw methods, methods `Page.insertText()`, `Page.insertTextbox()`, [`Shape.finish()`](shape.html#Shape.finish "Shape.finish"), `Shape.insertText()`, and `Shape.insertTextbox()` support two new parameters: *stroke\_opacity* and *fill\_opacity*.
- **Added** new parameter `mask` to `Page.insertImage()` for optionally providing an external image mask. Resolves issue [#685](https://github.com/pymupdf/PyMuPDF/issues/685).
- **Added** `Annot.soundGet()` for extracting the sound of an audio annotation.

---

**Changes in Version 1.18.0**

This is the first PyMuPDF version supporting MuPDF v1.18. The focus here is on extending PyMuPDF’s own functionality – apart from bug fixing. Subsequent PyMuPDF patches may address features new in MuPDF.

- **Fixed** issue [#519](https://github.com/pymupdf/PyMuPDF/issues/519). This upstream bug occurred occasionally for some pages only and seems to be fixed now: page layout should no longer be ruined in these cases.
- **Fixed** issue [#675](https://github.com/pymupdf/PyMuPDF/issues/675).

  - Unsuccessful storage allocations should now always lead to exceptions (circumvention of an upstream bug intermittently crashing the interpreter).
  - [Pixmap](pixmap.html#pixmap) size is now based on `size_t` instead of `int` in C and should be correct even for extremely large pixmaps.
- **Fixed** issue [#668](https://github.com/pymupdf/PyMuPDF/issues/668). Specification of dashes for PDF drawing insertion should now correctly reflect the PDF spec.
- **Fixed** issue [#669](https://github.com/pymupdf/PyMuPDF/issues/669). A major source of memory leakage in `Page.insert_pdf()` has been removed.
- **Added** keyword *“images”* to [`Page.apply_redactions()`](page.html#Page.apply_redactions "Page.apply_redactions") for fine-controlling the handling of images.
- **Added** `Annot.getText()` and `Annot.getTextbox()`, which offer the same functionality as the [Page](page.html#page) versions.
- **Added** key *“number”* to the block dictionaries of `Page.getText()` / `Annot.getText()` for options “dict” and “rawdict”.
- **Added** [`glyph_name_to_unicode()`](functions.html#glyph_name_to_unicode "glyph_name_to_unicode") and [`unicode_to_glyph_name()`](functions.html#unicode_to_glyph_name "unicode_to_glyph_name"). Both functions do not really connect to a specific font and are now independently available, too. The data are now based on the [Adobe Glyph List](https://github.com/adobe-type-tools/agl-aglfn/blob/master/glyphlist.txt).
- **Added** convenience functions [`adobe_glyph_names()`](functions.html#adobe_glyph_names "adobe_glyph_names") and [`adobe_glyph_unicodes()`](functions.html#adobe_glyph_unicodes "adobe_glyph_unicodes") which return the respective available data.
- **Added** `Page.getDrawings()` which returns details of drawing operations on a document page. Works for all document types.
- Improved performance of [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf"). Multiple object copies are now also suppressed across multiple separate insertions from the same source. This saves time, memory and target file size. Previously this mechanism was only active within each single method execution. The feature can also be suppressed with the new method bool parameter *final=1*, which is the default.
- For PNG images created from pixmaps, the resolution (dpi) is now automatically set from the respective [`Pixmap.xres`](pixmap.html#Pixmap.xres "Pixmap.xres") and [`Pixmap.yres`](pixmap.html#Pixmap.yres "Pixmap.yres") values.

---

**Changes in Version 1.17.7**

- **Fixed** issue [#651](https://github.com/pymupdf/PyMuPDF/issues/651). An upstream bug causing interpreter crashes in corner case redaction processings was fixed by backporting MuPDF changes from their development repo.
- **Fixed** issue [#645](https://github.com/pymupdf/PyMuPDF/issues/645). Pixmap top-left coordinates can be set (again) by their own method, [`Pixmap.set_origin()`](pixmap.html#Pixmap.set_origin "Pixmap.set_origin").
- **Fixed** issue [#622](https://github.com/pymupdf/PyMuPDF/issues/622). `Page.insertImage()` again accepts a [`rect_like`](glossary.html#rect_like "rect_like") parameter.
- **Added** several new methods to improve and speed-up table of contents (TOC) handling. Among other things, TOC items can now changed or deleted individually – without always replacing the complete TOC. Furthermore, access to some PDF page attributes is now possible without first **loading** the page. This has a very significant impact on the performance of TOC manipulation.
- **Added** an option to [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf") which allows displaying progress messages. Addresses [#640](https://github.com/pymupdf/PyMuPDF/issues/640).
- **Added** `Page.getTextbox()` which extracts text contained in a rectangle. In many cases, this should obsolete writing your own script for this type of thing.
- **Added** new `clip` parameter to `Page.getText()` to simplify and speed up text extraction of page sub areas.
- **Added** [`TextWriter.appendv()`](textwriter.html#TextWriter.appendv "TextWriter.appendv") to add text in **vertical write mode**. Addresses issue [#653](https://github.com/pymupdf/PyMuPDF/issues/653)

---

**Changes in Version 1.17.6**

- **Fixed** issue [#605](https://github.com/pymupdf/PyMuPDF/issues/605)
- **Fixed** issue [#600](https://github.com/pymupdf/PyMuPDF/issues/600) – text should now be correctly positioned also for pages with a CropBox smaller than MediaBox.
- **Added** text span dictionary key `origin` which contains the lower left coordinate of the first character in that span.
- **Added** attribute [`Font.buffer`](font.html#Font.buffer "Font.buffer"), a *bytes* copy of the font file.
- **Added** parameter *sanitize* to `Page.cleanContents()`. Allows switching of sanitization, so only syntax cleaning will be done.

---

**Changes in Version 1.17.5**

- **Fixed** issue [#561](https://github.com/pymupdf/PyMuPDF/issues/561) – second go: certain [TextWriter](textwriter.html#textwriter) usages with many alternating fonts did not work correctly.
- **Fixed** issue [#566](https://github.com/pymupdf/PyMuPDF/issues/566).
- **Fixed** issue [#568](https://github.com/pymupdf/PyMuPDF/issues/568).
- **Fixed** – opacity is now correctly taken from the [TextWriter](textwriter.html#textwriter) object, if not given in `TextWriter.writeText()`.
- **Added** a new global attribute [`fitz_fontdescriptors`](functions.html#fitz_fontdescriptors "fitz_fontdescriptors"). Contains information about usable fonts from repository [pymupdf-fonts](https://github.com/pymupdf/pymupdf-fonts).
- **Added** [`Font.valid_codepoints()`](font.html#Font.valid_codepoints "Font.valid_codepoints") which returns an array of unicode codepoints for which the font has a glyph.
- **Added** option `text_as_path` to `Page.getSVGimage()`. this implements [#580](https://github.com/pymupdf/PyMuPDF/issues/580). Generates much smaller SVG files with parseable text if set to *False*.

---

**Changes in Version 1.17.4**

- **Fixed** issue [#561](https://github.com/pymupdf/PyMuPDF/issues/561). Handling of more than 10 [Font](font.html#font) objects on one page should now work correctly.
- **Fixed** issue [#562](https://github.com/pymupdf/PyMuPDF/issues/562). Annotation pixmaps are no longer derived from the page pixmap, thus avoiding unintended inclusion of page content.
- **Fixed** issue [#559](https://github.com/pymupdf/PyMuPDF/issues/559). This **MuPDF** bug is being temporarily fixed with a pre-version of MuPDF’s next release.
- **Added** utility function `repair_mono_font()` for correcting displayed character spacing for some mono-spaced fonts.
- **Added** utility method [`Document.need_appearances()`](document.html#Document.need_appearances "Document.need_appearances") for fine-controlling Form PDF behavior. Addresses issue [#563](https://github.com/pymupdf/PyMuPDF/issues/563).
- **Added** utility function [`sRGB_to_pdf()`](functions.html#sRGB_to_pdf "sRGB_to_pdf") to recover the PDF color triple for a given color integer in sRGB format.
- **Added** utility function [`sRGB_to_rgb()`](functions.html#sRGB_to_rgb "sRGB_to_rgb") to recover the (R, G, B) color triple for a given color integer in sRGB format.
- **Added** utility function [`make_table()`](functions.html#make_table "make_table") which delivers table cells for a given rectangle and desired numbers of columns and rows.
- **Added** support for optional fonts in repository [pymupdf-fonts](https://github.com/pymupdf/pymupdf-fonts).

---

**Changes in Version 1.17.3**

- **Fixed** an undocumented issue, which prevented fully cleaning a PDF page when using `Page.cleanContents()`.
- **Fixed** issue [#540](https://github.com/pymupdf/PyMuPDF/issues/540). Text extraction for EPUB should again work correctly.
- **Fixed** issue [#548](https://github.com/pymupdf/PyMuPDF/issues/548). Documentation now includes `LINK_NAMED`.
- **Added** new parameter to control start of text in `TextWriter.fillTextbox()`. Implements [#549](https://github.com/pymupdf/PyMuPDF/issues/549).
- **Changed** documentation of [`Page.add_redact_annot()`](page.html#Page.add_redact_annot "Page.add_redact_annot") to explain the usage of non-builtin fonts.

---

**Changes in Version 1.17.2**

- **Fixed** issue [#533](https://github.com/pymupdf/PyMuPDF/issues/533).
- **Added** options to modify ‘Redact’ annotation appearance. Implements [#535](https://github.com/pymupdf/PyMuPDF/issues/535).

---

**Changes in Version 1.17.1**

- **Fixed** issue [#520](https://github.com/pymupdf/PyMuPDF/issues/520).
- **Fixed** issue [#525](https://github.com/pymupdf/PyMuPDF/issues/525). Vertices for ‘Ink’ annots should now be correct.
- **Fixed** issue [#524](https://github.com/pymupdf/PyMuPDF/issues/524). It is now possible to query and set rotation for applicable annotation types.

Also significantly improved inline documentation for better support of interactive help.

---

**Changes in Version 1.17.0**

This version is based on MuPDF v1.17. Following are highlights of new and changed features:

- **Added** extended language support for annotations and widgets: a mixture of Latin, Greece, Russian, Chinese, Japanese and Korean characters can now be used in ‘FreeText’ annotations and text widgets. No special arrangement is required to use it.
- Faster page access is implemented for documents supporting a “chapter” structure. This applies to EPUB documents currently. This comes with several new [Document](document.html#document) methods and changes for `Document.loadPage()` and the “indexed” page access *doc[n]*: In addition to specifying a page number as before, a tuple *(chapter, pno)* can be specified to identify the desired page.
- **Changed:** Improved support of redaction annotations: images overlapped by redactions are **permanently modified** by erasing the overlap areas. Also links are removed if overlapped by redactions. This is now fully in sync with PDF specifications.

Other changes:

- **Changed** `TextWriter.writeText()` to support the *“morph”* parameter.
- **Added** methods [`Rect.morph()`](rect.html#Rect.morph "Rect.morph"), [`IRect.morph()`](irect.html#IRect.morph "IRect.morph"), and [`Quad.morph()`](quad.html#Quad.morph "Quad.morph"), which return a new [Quad](quad.html#quad).
- **Changed** [`Page.add_freetext_annot()`](page.html#Page.add_freetext_annot "Page.add_freetext_annot") to support text alignment via a new *“align”* parameter.
- **Fixed** issue [#508](https://github.com/pymupdf/PyMuPDF/issues/508). Improved image rectangle calculation to hopefully deliver correct values in most if not all cases.
- **Fixed** issue [#502](https://github.com/pymupdf/PyMuPDF/issues/502).
- **Fixed** issue [#500](https://github.com/pymupdf/PyMuPDF/issues/500). `Document.convertToPDF()` should no longer cause memory leaks.
- **Fixed** issue [#496](https://github.com/pymupdf/PyMuPDF/issues/496). Annotations and widgets / fields are now added or modified using the coordinates of the **unrotated page**. This behavior is now in sync with other methods modifying PDF pages.
- **Added** `Page.rotationMatrix` and `Page.derotationMatrix` to support coordinate transformations between the rotated and the original versions of a PDF page.

Potential code breaking changes:

- The private method `Page._getTransformation()` has been removed. Use the public `Page.transformationMattrix` instead.

---

**Changes in Version 1.16.18**

This version introduces several new features around PDF text output. The motivation is to simplify this task, while at the same time offering extending features.

One major achievement is using MuPDF’s capabilities to dynamically choosing fallback fonts whenever a character cannot be found in the current one. This seamlessly works for Base-14 fonts in combination with CJK fonts (China, Japan, Korea). So a text may contain **any combination of characters** from the Latin, Greek, Russian, Chinese, Japanese and Korean languages.

- **Fixed** issue [#493](https://github.com/pymupdf/PyMuPDF/issues/493). `Pixmap(doc, xref)` should now again correctly resemble the loaded image object.
- **Fixed** issue [#488](https://github.com/pymupdf/PyMuPDF/issues/488). Widget names are now modifiable.
- **Added** new class [Font](font.html#font) which represents a font.
- **Added** new class [TextWriter](textwriter.html#textwriter) which serves as a container for text to be written on a page.
- **Added** `Page.writeText()` to write one or more [TextWriter](textwriter.html#textwriter) objects to the page.

---

**Changes in Version 1.16.17**

- **Fixed** issue [#479](https://github.com/pymupdf/PyMuPDF/issues/479). PyMuPDF should now more correctly report image resolutions. This applies to both, images (either from images files or extracted from PDF documents) and pixmaps created from images.
- **Added** [`Pixmap.set_dpi()`](pixmap.html#Pixmap.set_dpi "Pixmap.set_dpi") which sets the image resolution in x and y directions.

---

**Changes in Version 1.16.16**

- **Fixed** issue [#477](https://github.com/pymupdf/PyMuPDF/issues/477).
- **Fixed** issue [#476](https://github.com/pymupdf/PyMuPDF/issues/476).
- **Changed** annotation line end symbol coloring and fixed an error coloring the interior of ‘Polyline’ /’Polygon’ annotations.

---

**Changes in Version 1.16.14**

- **Changed** text marker annotations to accept parameters beyond just quadrilaterals such that now **text lines between two given points can be marked**.
- **Added** [`Document.scrub()`](document.html#Document.scrub "Document.scrub") which **removes potentially sensitive data** from a PDF. Implements [#453](https://github.com/pymupdf/PyMuPDF/issues/453).
- **Added** `Annot.blendMode()` which returns the **blend mode** of annotations.
- **Added** `Annot.setBlendMode()` to set the annotation’s blend mode. This resolves issue [#416](https://github.com/pymupdf/PyMuPDF/issues/416).
- **Changed** [`Annot.update()`](annot.html#Annot.update "Annot.update") to accept additional parameters for setting blend mode and opacity.
- **Added** advanced graphics features to **control the anti-aliasing values**, [`Tools.set_aa_level()`](tools.html#Tools.set_aa_level "Tools.set_aa_level"). Resolves [#467](https://github.com/pymupdf/PyMuPDF/issues/467)
- **Fixed** issue [#474](https://github.com/pymupdf/PyMuPDF/issues/474).
- **Fixed** issue [#466](https://github.com/pymupdf/PyMuPDF/issues/466).

---

**Changes in Version 1.16.13**

- **Added** `Document.getPageXObjectList()` which returns a list of **Form XObjects** of the page.
- **Added** `Page.setMediaBox()` for changing the physical PDF page size.
- **Added** [Page](page.html#page) methods which have been internal before: `Page.cleanContents()` (= `Page._cleanContents()`), `Page.getContents()` (= `Page._getContents()`), `Page.getTransformation()` (= `Page._getTransformation()`).

---

**Changes in Version 1.16.12**

- **Fixed** issue [#447](https://github.com/pymupdf/PyMuPDF/issues/447)
- **Fixed** issue [#461](https://github.com/pymupdf/PyMuPDF/issues/461).
- **Fixed** issue [#397](https://github.com/pymupdf/PyMuPDF/issues/397).
- **Fixed** issue [#463](https://github.com/pymupdf/PyMuPDF/issues/463).
- **Added** JavaScript support to PDF form fields, thereby fixing [#454](https://github.com/pymupdf/PyMuPDF/issues/454).
- **Added** a new annotation method [`Annot.delete_responses()`](annot.html#Annot.delete_responses "Annot.delete_responses"), which removes ‘Popup’ and response annotations referring to the current one. Mainly serves data protection purposes.
- **Added** a new form field method [`Widget.reset()`](widget.html#Widget.reset "Widget.reset"), which resets the field value to its default.
- **Changed** and extended handling of redactions: images and XObjects are removed if *contained* in a redaction rectangle. Any partial only overlaps will just be covered by the redaction background color. Now an *overlay* text can be specified to be inserted in the rectangle area to **take the place the deleted original** text. This resolves [#434](https://github.com/pymupdf/PyMuPDF/issues/434).

---

**Changes in Version 1.16.11**

- **Added** Support for redaction annotations via method [`Page.add_redact_annot()`](page.html#Page.add_redact_annot "Page.add_redact_annot") and [`Page.apply_redactions()`](page.html#Page.apply_redactions "Page.apply_redactions").
- **Fixed** issue #426 (“PolygonAnnotation in 1.16.10 version”).
- **Fixed** documentation only issues [#443](https://github.com/pymupdf/PyMuPDF/issues/443) and [#444](https://github.com/pymupdf/PyMuPDF/issues/444).

---

**Changes in Version 1.16.10**

- **Fixed** issue #421 (“annot.set\_rect(rect) has no effect on text Annotation”)
- **Fixed** issue #417 (“Strange behavior for page.deleteAnnot on 1.16.9 compare to 1.13.20”)
- **Fixed** issue #415 (“Annot.setOpacity throws mupdf warnings”)
- **Changed** all “add annotation / widget” methods to store a unique name in the */NM* PDF key.
- **Changed** `Annot.setInfo()` to also accept direct parameters in addition to a dictionary.
- **Changed** [`Annot.info`](annot.html#Annot.info "Annot.info") to now also show the annotation’s unique id (*/NM* PDF key) if present.
- **Added** [`Page.annot_names()`](page.html#Page.annot_names "Page.annot_names") which returns a list of all annotation names (*/NM* keys).
- **Added** [`Page.load_annot()`](page.html#Page.load_annot "Page.load_annot") which loads an annotation given its unique id (*/NM* key).
- **Added** [`Document.reload_page()`](document.html#Document.reload_page "Document.reload_page") which provides a new copy of a page after finishing any pending updates to it.

---

**Changes in Version 1.16.9**

- **Fixed** #412 (“Feature Request: Allow controlling whether TOC entries should be collapsed”)
- **Fixed** #411 (“Seg Fault with page.firstWidget”)
- **Fixed** #407 (“Annot.setOpacity trouble”)
- **Changed** methods `Annot.setBorder()`, `Annot.setColors()`, `Link.setBorder()`, and `Link.setColors()` to also accept direct parameters, and not just cumbersome dictionaries.

---

**Changes in Version 1.16.8**

- **Added** several new methods to the [Document](document.html#document) class, which make dealing with PDF low-level structures easier. I also decided to provide them as “normal” methods (as opposed to private ones starting with an underscore “\_”). These are `Document.xrefObject()`, `Document.xrefStream()`, `Document.xrefStreamRaw()`, `Document.PDFTrailer()`, `Document.PDFCatalog()`, `Document.metadataXML()`, `Document.updateObject()`, `Document.updateStream()`.
- **Added** `Tools.mupdf_disply_errors()` which sets the display of mupdf errors on *sys.stderr*.
- **Added** a commandline facility. This a major new feature: you can now invoke several utility functions via *“python -m fitz …”*. It should obsolete the need for many of the most trivial scripts. Please refer to [Command line interface](module.html#module).

---

**Changes in Version 1.16.7**

Minor changes to better synchronize the binary image streams of [TextPage](textpage.html#textpage) image blocks and `Document.extractImage()` images.

- **Fixed** issue #394 (“PyMuPDF Segfaults when using TOOLS.mupdf\_warnings()”).
- **Changed** redirection of MuPDF error messages: apart from writing them to Python *sys.stderr*, they are now also stored with the MuPDF warnings.
- **Changed** [`Tools.mupdf_warnings()`](tools.html#Tools.mupdf_warnings "Tools.mupdf_warnings") to automatically empty the store (if not deactivated via a parameter).
- **Changed** `Page.getImageBbox()` to return an **infinite rectangle** if the image could not be located on the page – instead of raising an exception.

---

**Changes in Version 1.16.6**

- **Fixed** issue #390 (“Incomplete deletion of annotations”).
- **Changed** `Page.searchFor()` / `Document.searchPageFor()` to also support the *flags* parameter, which controls the data included in a [TextPage](textpage.html#textpage).
- **Changed** `Document.getPageImageList()`, `Document.getPageFontList()` and their [Page](page.html#page) counterparts to support a new parameter *full*. If true, the returned items will contain the [`xref`](glossary.html#xref "xref") of the *Form XObject* where the font or image is referenced.

---

**Changes in Version 1.16.5**

More performance improvements for text extraction.

- **Fixed** second part of issue #381 (see item in v1.16.4).
- **Added** `Page.getTextPage()`, so it is no longer required to create an intermediate display list for text extractions. Page level wrappers for text extraction and text searching are now based on this, which should improve performance by ca. 5%.

---

**Changes in Version 1.16.4**

- **Fixed** issue #381 (“TextPage.extractDICT … failed … after upgrading … to 1.16.3”)
- **Added** method [`Document.pages()`](document.html#Document.pages "Document.pages") which delivers a generator iterator over a page range.
- **Added** method [`Page.links()`](page.html#Page.links "Page.links") which delivers a generator iterator over the links of a page.
- **Added** method [`Page.annots()`](page.html#Page.annots "Page.annots") which delivers a generator iterator over the annotations of a page.
- **Added** method [`Page.widgets()`](page.html#Page.widgets "Page.widgets") which delivers a generator iterator over the form fields of a page.
- **Changed** [`Document.is_form_pdf`](document.html#Document.is_form_pdf "Document.is_form_pdf") to now contain the number of widgets, and *False* if not a PDF or this number is zero.

---

**Changes in Version 1.16.3**

Minor changes compared to version 1.16.2. The code of the “dict” and “rawdict” variants of `Page.getText()` has been ported to C which has greatly improved their performance. This improvement is mostly noticeable with text-oriented documents, where they now should execute almost two times faster.

- **Fixed** issue #369 (“mupdf: cmsCreateTransform failed”) by removing ICC colorspace support.
- **Changed** `Page.getText()` to accept additional keywords “blocks” and “words”. These will deliver the results of `Page.getTextBlocks()` and `Page.getTextWords()`, respectively. So all text extraction methods are now available via a uniform API. Correspondingly, there are now new methods [`TextPage.extractBLOCKS()`](textpage.html#TextPage.extractBLOCKS "TextPage.extractBLOCKS") and `TextPage.extractWords()`.
- **Changed** `Page.getText()` to default bit indicator *TEXT\_INHIBIT\_SPACES* to **off**. Insertion of additional spaces is **not suppressed** by default.

---

**Changes in Version 1.16.2**

- **Changed** text extraction methods of [Page](page.html#page) to allow detail control of the amount of extracted data.
- **Added** [`planish_line()`](functions.html#planish_line "planish_line") which maps a given line (defined as a pair of points) to the x-axis.
- **Fixed** an issue (w/o Github number) which brought down the interpreter when encountering certain non-UTF-8 encodable characters while using `Page.getText()` with the “dict” option.
- **Fixed** issue #362 (“Memory Leak with getText(‘rawDICT’)”).

---

**Changes in Version 1.16.1**

- **Added** property [`Quad.is_convex`](quad.html#Quad.is_convex "Quad.is_convex") which checks whether a line is contained in the quad if it connects two points of it.
- **Changed** [`Document.insert_pdf()`](document.html#Document.insert_pdf "Document.insert_pdf") to now allow dropping or including links and annotations independently during the copy. Fixes issue #352 (“Corrupt PDF data and …”), which seemed to intermittently occur when using the method for some problematic PDF files.
- **Fixed** a bug which, in matrix division using the syntax *“m1/m2”*, caused matrix *“m1”* to be **replaced** by the result instead of delivering a new matrix.
- **Fixed** issue #354 (“SyntaxWarning with Python 3.8”). We now always use *“==”* for literals (instead of the *“is”* Python keyword).
- **Fixed** issue #353 (“mupdf version check”), to no longer refuse the import when there are only patch level deviations from MuPDF.

---

**Changes in Version 1.16.0**

This major new version of MuPDF comes with several nice new or changed features. Some of them imply programming API changes, however. This is a synopsis of what has changed:

- PDF document encryption and decryption is now **fully supported**. This includes setting **permissions**, **passwords** (user and owner passwords) and the desired encryption method.
- In response to the new encryption features, PyMuPDF returns an integer (ie. a combination of bits) for document permissions, and no longer a dictionary.
- Redirection of MuPDF errors and warnings is now natively supported. PyMuPDF redirects error messages from MuPDF to *sys.stderr* and no longer buffers them. Warnings continue to be buffered and will not be displayed. Functions exist to access and reset the warnings buffer.
- Annotations are now **only supported for PDF**.
- Annotations and widgets (form fields) are now **separate object chains** on a page (although widgets technically still **are** PDF annotations). This means, that you will **never encounter widgets** when using `Page.firstAnnot` or [`Annot.next()`](annot.html#Annot.next "Annot.next"). You must use `Page.firstWidget` and [`Widget.next()`](widget.html#Widget.next "Widget.next") to access form fields.
- As part of MuPDF’s changes regarding widgets, only the following four fonts are supported, when **adding** or **changing** form fields: **Courier, Helvetica, Times-Roman** and **ZapfDingBats**.

List of change details:

- **Added** [`Document.can_save_incrementally()`](document.html#Document.can_save_incrementally "Document.can_save_incrementally") which checks conditions that are preventing use of option *incremental=True* of [`Document.save()`](document.html#Document.save "Document.save").
- **Added** `Page.firstWidget` which points to the first field on a page.
- **Added** `Page.getImageBbox()` which returns the rectangle occupied by an image shown on the page.
- **Added** `Annot.setName()` which lets you change the (icon) name field.
- **Added** outputting the text color in `Page.getText()`: the *“dict”*, *“rawdict”* and *“xml”* options now also show the color in sRGB format.
- **Changed** [`Document.permissions`](document.html#Document.permissions "Document.permissions") to now contain an integer of bool indicators – was a dictionary before.
- **Changed** [`Document.save()`](document.html#Document.save "Document.save"), `Document.write()`, which now fully support password-based decryption and encryption of PDF files.
- **Changed the names of all Python constants** related to annotations and widgets. Please make sure to consult the **Constants and Enumerations** chapter if your script is dealing with these two classes. This decision goes back to the dropped support for non-PDF annotations. The **old names** (starting with “ANNOT\_\*” or “WIDGET\_\*”) will be available as deprecated synonyms.
- **Changed** font support for widgets: only *Cour* (Courier), *Helv* (Helvetica, default), *TiRo* (Times-Roman) and *ZaDb* (ZapfDingBats) are accepted when **adding or changing** form fields. Only the plain versions are possible – not their italic or bold variations. **Reading** widgets, however will show its original font.
- **Changed** the name of the warnings buffer to [`Tools.mupdf_warnings()`](tools.html#Tools.mupdf_warnings "Tools.mupdf_warnings") and the function to empty this buffer is now called [`Tools.reset_mupdf_warnings()`](tools.html#Tools.reset_mupdf_warnings "Tools.reset_mupdf_warnings").
- **Changed** `Page.getPixmap()`, [`Document.get_page_pixmap()`](document.html#Document.get_page_pixmap "Document.get_page_pixmap"): a new bool argument *annots* can now be used to **suppress the rendering of annotations** on the page.
- **Changed** [`Page.add_file_annot()`](page.html#Page.add_file_annot "Page.add_file_annot") and [`Page.add_text_annot()`](page.html#Page.add_text_annot "Page.add_text_annot") to enable setting an icon.
- **Removed** widget-related methods and attributes from the [Annot](annot.html#annot) object.
- **Removed** [Document](document.html#document) attributes *openErrCode*, *openErrMsg*, and [Tools](tools.html#tools) attributes / methods *stderr*, *reset\_stderr*, *stdout*, and *reset\_stdout*.
- **Removed** **thirdparty zlib** dependency in PyMuPDF: there are now compression functions available in MuPDF. Source installers of PyMuPDF may now omit this extra installation step.

**No version published for MuPDF v1.15.0**

---

**Changes in Version 1.14.20 / 1.14.21**

- **Changed** text marker annotations to support multiple rectangles / quadrilaterals. This fixes issue #341 (“Question : How to addhighlight so that a string spread across more than a line is covered by one highlight?”) and similar (#285).
- **Fixed** issue #331 (“Importing PyMuPDF changes warning filtering behaviour globally”).

---

**Changes in Version 1.14.19**

- **Fixed** issue #319 (“InsertText function error when use custom font”).
- **Added** new method [`Document.get_sigflags()`](document.html#Document.get_sigflags "Document.get_sigflags") which returns information on whether a PDF is signed. Resolves issue #326 (“How to detect signature in a form pdf?”).

---

**Changes in Version 1.14.17**

- **Added** `Document.fullcopyPage()` to make full page copies within a PDF (not just copied references as `Document.copyPage()` does).
- **Changed** `Page.getPixmap()`, [`Document.get_page_pixmap()`](document.html#Document.get_page_pixmap "Document.get_page_pixmap") now use *alpha=False* as default.
- **Changed** text extraction: the span dictionary now (again) contains its rectangle under the *bbox* key.
- **Changed** `Document.movePage()` and `Document.copyPage()` to use direct functions instead of wrapping [`Document.select()`](document.html#Document.select "Document.select") – similar to [`Document.delete_page()`](document.html#Document.delete_page "Document.delete_page") in v1.14.16.

---

**Changes in Version 1.14.16**

- **Changed** [Document](document.html#document) methods around PDF */EmbeddedFiles* to no longer use MuPDF’s “portfolio” functions. That support will be dropped in MuPDF v1.15 – therefore another solution was required.
- **Changed** `Document.embfile_Count()` to be a function (was an attribute).
- **Added** new method `Document.embfile_Names()` which returns a list of names of embedded files.
- **Changed** [`Document.delete_page()`](document.html#Document.delete_page "Document.delete_page") and [`Document.delete_pages()`](document.html#Document.delete_pages "Document.delete_pages") to internally no longer use [`Document.select()`](document.html#Document.select "Document.select"), but instead use functions to perform the deletion directly. As it has turned out, the [`Document.select()`](document.html#Document.select "Document.select") method yields invalid outline trees (tables of content) for very complex PDFs and sophisticated use of annotations.

---

**Changes in Version 1.14.15**

- **Fixed** issues #301 (“Line cap and Line join”), #300 (“How to draw a shape without outlines”) and #298 (“utils.updateRect exception”). These bugs pertain to drawing shapes with PyMuPDF. Drawing shapes without any border is fully supported. Line cap styles and line line join style are now differentiated and support all possible PDF values (0, 1, 2) instead of just being a bool. The previous parameter *roundCap* is deprecated in favor of *lineCap* and *lineJoin* and will be deleted in the next release.
- **Fixed** issue #290 (“Memory Leak with getText(‘rawDICT’)”). This bug caused memory not being (completely) freed after invoking the “dict”, “rawdict” and “json” versions of `Page.getText()`.

---

**Changes in Version 1.14.14**

- **Added** new low-level function `ImageProperties()` to determine a number of characteristics for an image.
- **Added** new low-level function [`Document.is_stream()`](functions.html#Document.is_stream "Document.is_stream"), which checks whether an object is of stream type.
- **Changed** low-level functions `Document._getXrefString()` and `Document._getTrailerString()` now by default return object definitions in a formatted form which makes parsing easy.

---

**Changes in Version 1.14.13**

- **Changed** methods working with binary input: while ever supporting bytes and bytearray objects, they now also accept *io.BytesIO* input, using their *getvalue()* method. This pertains to document creation, embedded files, FileAttachment annotations, pixmap creation and others. Fixes issue #274 (“Segfault when using BytesIO as a stream for insertImage”).
- **Fixed** issue #278 (“Is insertImage(keep\_proportion=True) broken?”). Images are now correctly presented when keeping aspect ratio.

---

**Changes in Version 1.14.12**

- **Changed** the draw methods of [Page](page.html#page) and [Shape](shape.html#shape) to support not only RGB, but also GRAY and CMYK colorspaces. This solves issue #270 (“Is there a way to use CMYK color to draw shapes?”). This change also applies to text insertion methods of [Shape](shape.html#shape), resp. [Page](page.html#page).
- **Fixed** issue #269 (“AttributeError in Document.insert\_page()”), which occurred when using [`Document.insert_page()`](document.html#Document.insert_page "Document.insert_page") with text insertion.

---

**Changes in Version 1.14.11**

- **Changed** [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") to always position the source rectangle centered in the target. This method now also supports **rotation by arbitrary angles**. The argument *reuse\_xref* has been deprecated: prevention of duplicates is now **handled internally**.
- **Changed** `Page.insertImage()` to support rotated display of the image and keeping the aspect ratio. Only rotations by multiples of 90 degrees are supported here.
- **Fixed** issue #265 (“TypeError: insertText() got an unexpected keyword argument ‘idx’”). This issue only occurred when using [`Document.insert_page()`](document.html#Document.insert_page "Document.insert_page") with also inserting text.

---

**Changes in Version 1.14.10**

- **Changed** [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") to support rotation of the source rectangle. Fixes #261 (“Cannot rotate inserted pages”).
- **Fixed** a bug in `Page.insertImage()` which prevented insertion of multiple images provided as streams.

---

**Changes in Version 1.14.9**

- **Added** new low-level method `Document._getTrailerString()`, which returns the trailer object of a PDF. This is much like `Document._getXrefString()` except that the PDF trailer has no / needs no [`xref`](glossary.html#xref "xref") to identify it.
- **Added** new parameters for text insertion methods. You can now set stroke and fill colors of glyphs (text characters) independently, as well as the thickness of the glyph border. A new parameter *render\_mode* controls the use of these colors, and whether the text should be visible at all.
- **Fixed** issue #258 (“Copying image streams to new PDF without size increase”): For JPX images embedded in a PDF, `Document.extractImage()` will now return them in their original format. Previously, the MuPDF base library was used, which returns them in PNG format (entailing a massive size increase).
- **Fixed** issue #259 (“Morphing text to fit inside rect”). Clarified use of [`get_text_length()`](functions.html#get_text_length "get_text_length") and removed extra line breaks for long words.

---

**Changes in Version 1.14.8**

- **Added** [`Pixmap.set_rect()`](pixmap.html#Pixmap.set_rect "Pixmap.set_rect") to change the pixel values in a rectangle. This is also an alternative to setting the color of a complete pixmap ([`Pixmap.clear_with()`](pixmap.html#Pixmap.clear_with "Pixmap.clear_with")).
- **Fixed** an image extraction issue with JBIG2 (monochrome) encoded PDF images. The issue occurred in `Page.getText()` (parameters “dict” and “rawdict”) and in `Document.extractImage()` methods.
- **Fixed** an issue with not correctly clearing a non-alpha [Pixmap](pixmap.html#pixmap) ([`Pixmap.clear_with()`](pixmap.html#Pixmap.clear_with "Pixmap.clear_with")).
- **Fixed** an issue with not correctly inverting colors of a non-alpha [Pixmap](pixmap.html#pixmap) ([`Pixmap.invert_irect()`](pixmap.html#Pixmap.invert_irect "Pixmap.invert_irect")).

---

**Changes in Version 1.14.7**

- **Added** [`Pixmap.set_pixel()`](pixmap.html#Pixmap.set_pixel "Pixmap.set_pixel") to change one pixel value.
- **Added** documentation for image conversion in the [FAQ](faq.html#faq).
- **Added** new function [`get_text_length()`](functions.html#get_text_length "get_text_length") to determine the string length for a given font.
- **Added** Postscript image output (changed [`Pixmap.save()`](pixmap.html#Pixmap.save "Pixmap.save") and [`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes")).
- **Changed** [`Pixmap.save()`](pixmap.html#Pixmap.save "Pixmap.save") and [`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes") to ensure valid combinations of colorspace, alpha and output format.
- **Changed** [`Pixmap.save()`](pixmap.html#Pixmap.save "Pixmap.save"): the desired format is now inferred from the filename.
- **Changed** FreeText annotations can now have a transparent background - see [`Annot.update()`](annot.html#Annot.update "Annot.update").

---

**Changes in Version 1.14.5**

- **Changed:** [Shape](shape.html#shape) methods now strictly use the transformation matrix of the [Page](page.html#page) – instead of “manually” calculating locations.
- **Added** method [`Pixmap.pixel()`](pixmap.html#Pixmap.pixel "Pixmap.pixel") which returns the pixel value (a list) for given pixel coordinates.
- **Added** method [`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes") which returns a bytes object representing the pixmap in a variety of formats. Previously, this could be done for PNG outputs only ([`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes")).
- **Changed:** output of methods [`Pixmap.save()`](pixmap.html#Pixmap.save "Pixmap.save") and (the new) [`Pixmap.tobytes()`](pixmap.html#Pixmap.tobytes "Pixmap.tobytes") may now also be PSD (Adobe Photoshop Document).
- **Added** method `Shape.drawQuad()` which draws a [Quad](quad.html#quad). This actually is a shorthand for a `Shape.drawPolyline()` with the edges of the quad.
- **Changed** method `Shape.drawOval()`: the argument can now be **either** a rectangle ([`rect_like`](glossary.html#rect_like "rect_like")) **or** a quadrilateral ([`quad_like`](glossary.html#quad_like "quad_like")).

---

**Changes in Version 1.14.4**

- **Fixes** issue #239 “Annotation coordinate consistency”.

---

**Changes in Version 1.14.3**

This patch version contains minor bug fixes and CJK font output support.

- **Added** support for the four CJK fonts as PyMuPDF generated text output. This pertains to methods `Page.insertFont()`, `Shape.insertText()`, `Shape.insertTextbox()`, and corresponding [Page](page.html#page) methods. The new fonts are available under “reserved” fontnames “china-t” (traditional Chinese), “china-s” (simplified Chinese), “japan” (Japanese), and “korea” (Korean).
- **Added** full support for the built-in fonts ‘Symbol’ and ‘Zapfdingbats’.
- **Changed:** The 14 standard fonts can now each be referenced by a 4-letter abbreviation.

---

**Changes in Version 1.14.1**

This patch version contains minor performance improvements.

- **Added** support for [Document](document.html#document) filenames given as *pathlib* object by using the Python *str()* function.

---

**Changes in Version 1.14.0**

To support MuPDF v1.14.0, massive changes were required in PyMuPDF – most of them purely technical, with little visibility to developers. But there are also quite a lot of interesting new and improved features. Following are the details:

- **Added** “ink” annotation.
- **Added** “rubber stamp” annotation.
- **Added** “squiggly” text marker annotation.
- **Added** new class [Quad](quad.html#quad) (quadrilateral or tetragon) – which represents a general four-sided shape in the plane. The special subtype of rectangular, non-empty tetragons is used in text marker annotations and as returned objects in text search methods.
- **Added** a new option “decrypt” to [`Document.save()`](document.html#Document.save "Document.save") and `Document.write()`. Now you can **keep encryption** when saving a password protected PDF.
- **Added** suppression and redirection of unsolicited messages issued by the underlying C-library MuPDF. Consult [Diagnostics](app3.html#redirectmessages) for details.
- **Changed:** Changes to annotations now **always require** [`Annot.update()`](annot.html#Annot.update "Annot.update") to become effective.
- **Changed** free text annotations to support the full Latin character set and range of appearance options.
- **Changed** text searching, `Page.searchFor()`, to optionally return [Quad](quad.html#quad) instead [Rect](rect.html#rect) objects surrounding each search hit.
- **Changed** plain text output: we now add a *n* to each line if it does not itself end with this character.
- **Fixed** issue 211 (“Something wrong in the doc”).
- **Fixed** issue 213 (“Rewritten outline is displayed only by mupdf-based applications”).
- **Fixed** issue 214 (“PDF decryption GONE!”).
- **Fixed** issue 215 (“Formatting of links added with pyMuPDF”).
- **Fixed** issue 217 (“extraction through json is failing for my pdf”).

Behind the curtain, we have changed the implementation of geometry objects: they now purely exist in Python and no longer have “shadow” twins on the C-level (in MuPDF). This has improved processing speed in that area by more than a factor of two.

Because of the same reason, most methods involving geometry parameters now also accept the corresponding Python sequence. For example, in method *“page.show\_pdf\_page(rect, …)”* parameter *rect* may now be any [`rect_like`](glossary.html#rect_like "rect_like") sequence.

We also invested considerable effort to further extend and improve the [FAQ](faq.html#faq) chapter.

---

**Changes in Version 1.13.19**

This version contains some technical / performance improvements and bug fixes.

- **Changed** memory management: for Python 3 builds, Python memory management is exclusively used across all C-level code (i.e. no more native *malloc()* in MuPDF code or PyMuPDF interface code). This leads to improved memory usage profiles and also some runtime improvements: we have seen > 2% shorter runtimes for text extractions and pixmap creations (on Windows machines only to date).
- **Fixed** an error occurring in Python 2.7, which crashed the interpreter when using [`TextPage.extractRAWDICT()`](textpage.html#TextPage.extractRAWDICT "TextPage.extractRAWDICT") (= *Page.getText(“rawdict”)*).
- **Fixed** an error occurring in Python 2.7, when creating link destinations.
- **Extended** the [FAQ](faq.html#faq) chapter with more examples.

---

**Changes in Version 1.13.18**

- **Added** method [`TextPage.extractRAWDICT()`](textpage.html#TextPage.extractRAWDICT "TextPage.extractRAWDICT"), and a corresponding new string parameter “rawdict” to method `Page.getText()`. It extracts text and images from a page in Python *dict* form like [`TextPage.extractDICT()`](textpage.html#TextPage.extractDICT "TextPage.extractDICT"), but with the detail level of [`TextPage.extractXML()`](textpage.html#TextPage.extractXML "TextPage.extractXML"), which is position information down to each single character.

---

**Changes in Version 1.13.17**

- **Fixed** an error that intermittently caused an exception in [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page"), when pages from many different source PDFs were shown.
- **Changed** method `Document.extractImage()` to now return more meta information about the extracted image. Also, its performance has been greatly improved. Several demo scripts have been changed to make use of this method.
- **Changed** method `Document._getXrefStream()` to now return *None* if the object is no stream and no longer raise an exception if otherwise.
- **Added** method `Document._deleteObject()` which deletes a PDF object identified by its [`xref`](glossary.html#xref "xref"). Only to be used by the experienced PDF expert.
- **Added** a method [`paper_rect()`](functions.html#paper_rect "paper_rect") which returns a [Rect](rect.html#rect) for a supplied paper format string. Example: *fitz.paper\_rect(“letter”) = fitz.Rect(0.0, 0.0, 612.0, 792.0)*.
- **Added** a [FAQ](faq.html#faq) chapter to this document.

---

**Changes in Version 1.13.16**

- **Added** support for correctly setting transparency (opacity) for certain annotation types.
- **Added** a tool property ([`Tools.fitz_config`](tools.html#Tools.fitz_config "Tools.fitz_config")) showing the configuration of this PyMuPDF version.
- **Fixed** issue #193 (‘insertText(overlay=False) gives “cannot resize a buffer with shared storage” error’) by avoiding read-only buffers.

---

**Changes in Version 1.13.15**

- **Fixed** issue #189 (“cannot find builtin CJK font”), so we are supporting builtin CJK fonts now (CJK = China, Japan, Korea). This should lead to correctly generated pixmaps for documents using these languages. This change has consequences for our binary file size: it will now range between 8 and 10 MB, depending on the OS.
- **Fixed** issue #191 (“Jupyter notebook kernel dies after ca. 40 pages”), which occurred when modifying the contents of an annotation.

---

**Changes in Version 1.13.14**

This patch version contains several improvements, mainly for annotations.

- **Changed** `Annot.lineEnds` is now a list of two integers representing the line end symbols. Previously was a *dict* of strings.
- **Added** support of line end symbols for applicable annotations. PyMuPDF now can generate these annotations including the line end symbols.
- **Added** `Annot.setLineEnds()` adds line end symbols to applicable annotation types (‘Line’, ‘PolyLine’, ‘Polygon’).
- **Changed** technical implementation of `Page.insertImage()` and [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page"): they now create there own contents objects, thereby avoiding changes of potentially large streams with consequential compression / decompression efforts and high change volumes with incremental updates.

---

**Changes in Version 1.13.13**

This patch version contains several improvements for embedded files and file attachment annotations.

- **Added** `Document.embfile_Upd()` which allows changing **file content and metadata** of an embedded file. It supersedes the old method `Document.embfile_SetInfo()` (which will be deleted in a future version). Content is automatically compressed and metadata may be unicode.
- **Changed** `Document.embfile_Add()` to now automatically compress file content. Accompanying metadata can now be unicode (had to be ASCII in the past).
- **Changed** `Document.embfile_Del()` to now automatically delete **all entries** having the supplied identifying name. The return code is now an integer count of the removed entries (was *None* previously).
- **Changed** embedded file methods to now also accept or show the PDF unicode filename as additional parameter *ufilename*.
- **Added** [`Page.add_file_annot()`](page.html#Page.add_file_annot "Page.add_file_annot") which adds a new file attachment annotation.
- **Changed** `Annot.fileUpd()` (file attachment annot) to now also accept the PDF unicode *ufilename* parameter. The description parameter *desc* correctly works with unicode. Furthermore, **all** parameters are optional, so metadata may be changed without also replacing the file content.
- **Changed** `Annot.fileInfo()` (file attachment annot) to now also show the PDF unicode filename as parameter *ufilename*.
- **Fixed** issue #180 (“page.getText(output=’dict’) return invalid bbox”) to now also work for vertical text.
- **Fixed** issue #185 (“Can’t render the annotations created by PyMuPDF”). The issue’s cause was the minimalistic MuPDF approach when creating annotations. Several annotation types have no */AP* (“appearance”) object when created by MuPDF functions. MuPDF, SumatraPDF and hence also PyMuPDF cannot render annotations without such an object. This fix now ensures, that an appearance object is always created together with the annotation itself. We still do not support line end styles.

---

**Changes in Version 1.13.12**

- **Fixed** issue #180 (“page.getText(output=’dict’) return invalid bbox”). Note that this is a circumvention of an MuPDF error, which generates zero-height character rectangles in some cases. When this happens, this fix ensures a bbox height of at least fontsize.
- **Changed** for ListBox and ComboBox widgets, the attribute list of selectable values has been renamed to [`Widget.choice_values`](widget.html#Widget.choice_values "Widget.choice_values").
- **Changed** when adding widgets, any missing of the [PDF Base 14 Fonts](app3.html#base-14-fonts) is automatically added to the PDF. Widget text fonts can now also be chosen from existing widget fonts. Any specified field values are now honored and lead to a field with a preset value.
- **Added** `Annot.updateWidget()` which allows changing existing form fields – including the field value.

---

**Changes in Version 1.13.11**

While the preceding patch subversions only contained various fixes, this version again introduces major new features:

- **Added** basic support for PDF widget annotations. You can now add PDF form fields of types Text, CheckBox, ListBox and ComboBox. Where necessary, the PDF is transformed to a Form PDF with the first added widget.
- **Fixed** issues #176 (“wrong file embedding”), #177 (“segment fault when invoking page.getText()”)and #179 (“Segmentation fault using page.getLinks() on encrypted PDF”).

---

**Changes in Version 1.13.7**

- **Added** support of variable page sizes for reflowable documents (e-books, HTML, etc.): new parameters *rect* and *fontsize* in [Document](document.html#document) creation (open), and as a separate method [`Document.layout()`](document.html#Document.layout "Document.layout").
- **Added** [Annot](annot.html#annot) creation of many annotations types: sticky notes, free text, circle, rectangle, line, polygon, polyline and text markers.
- **Added** support of annotation transparency ([`Annot.opacity`](annot.html#Annot.opacity "Annot.opacity"), `Annot.setOpacity()`).
- **Changed** [`Annot.vertices`](annot.html#Annot.vertices "Annot.vertices"): point coordinates are now grouped as pairs of floats (no longer as separate floats).
- **Changed** annotation colors dictionary: the two keys are now named *“stroke”* (formerly *“common”*) and *“fill”*.
- **Added** `Document.isDirty` which is *True* if a PDF has been changed in this session. Reset to *False* on each [`Document.save()`](document.html#Document.save "Document.save") or `Document.write()`.

---

**Changes in Version 1.13.6**

- Fix #173: for memory-resident documents, ensure the stream object will not be garbage-collected by Python before document is closed.

---

**Changes in Version 1.13.5**

- New low-level method `Page._setContents()` defines an object given by its [`xref`](glossary.html#xref "xref") to serve as the [`contents`](glossary.html#contents "contents") object.
- Changed and extended PDF form field support: the attribute *widget\_text* has been renamed to `Annot.widget_value`. Values of all form field types (except signatures) are now supported. A new attribute `Annot.widget_choices` contains the selectable values of listboxes and comboboxes. All these attributes now contain *None* if no value is present.

---

**Changes in Version 1.13.4**

- `Document.convertToPDF()` now supports page ranges, reverted page sequences and page rotation. If the document already is a PDF, an exception is raised.
- Fixed a bug (introduced with v1.13.0) that prevented `Page.insertImage()` for transparent images.

---

**Changes in Version 1.13.3**

Introduces a way to convert **any MuPDF supported document** to a PDF. If you ever wanted PDF versions of your XPS, EPUB, CBZ or FB2 files – here is a way to do this.

- `Document.convertToPDF()` returns a Python *bytes* object in PDF format. Can be opened like normal in PyMuPDF, or be written to disk with the *“.pdf”* extension.

---

**Changes in Version 1.13.2**

The major enhancement is PDF form field support. Form fields are annotations of type *(19, ‘Widget’)*. There is a new document method to check whether a PDF is a form. The [Annot](annot.html#annot) class has new properties describing field details.

- [`Document.is_form_pdf`](document.html#Document.is_form_pdf "Document.is_form_pdf") is true if object type */AcroForm* and at least one form field exists.
- `Annot.widget_type`, `Annot.widget_text` and `Annot.widget_name` contain the details of a form field (i.e. a “Widget” annotation).

---

**Changes in Version 1.13.1**

- [`TextPage.extractDICT()`](textpage.html#TextPage.extractDICT "TextPage.extractDICT") is a new method to extract the contents of a document page (text and images). All document types are supported as with the other [TextPage](textpage.html#textpage) *extract\*()* methods. The returned object is a dictionary of nested lists and other dictionaries, and **exactly equal** to the JSON-deserialization of the old [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON "TextPage.extractJSON"). The difference is that the result is created directly – no JSON module is used. Because the user needs no JSON module to interpret the information, it should be easier to use, and also have a better performance, because it contains images in their original **binary format** – they need not be base64-decoded.
- `Page.getText()` correspondingly supports the new parameter value *“dict”* to invoke the above method.
- [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON "TextPage.extractJSON") (resp. *Page.getText(“json”)*) is still supported for convenience, but its use is expected to decline.

---

**Changes in Version 1.13.0**

This version is based on MuPDF v1.13.0. This release is “primarily a bug fix release”.

In PyMuPDF, we are also doing some bug fixes while introducing minor enhancements. There only very minimal changes to the user’s API.

- [Document](document.html#document) construction is more flexible: the new *filetype* parameter allows setting the document type. If specified, any extension in the filename will be ignored. More completely addresses [issue #156](https://github.com/pymupdf/PyMuPDF/issues/156). As part of this, the documentation has been reworked.
- Changes to [Pixmap](pixmap.html#pixmap) constructors:
  :   - Colorspace conversion no longer allows dropping the alpha channel: source and target **alpha will now always be the same**. We have seen exceptions and even interpreter crashes when using *alpha = 0*.
      - As a replacement, the simple pixmap copy lets you choose the target alpha.
- [`Document.save()`](document.html#Document.save "Document.save") again offers the full garbage collection range 0 thru 4. Because of a bug in [`xref`](glossary.html#xref "xref") maintenance, we had to temporarily enforce *garbage > 1*. Finally resolves [issue #148](https://github.com/pymupdf/PyMuPDF/issues/148).
- [`Document.save()`](document.html#Document.save "Document.save") now offers to “prettify” PDF source via an additional argument.
- `Page.insertImage()` has the additional *stream* -parameter, specifying a memory area holding an image.
- Issue with garbled PNGs on Linux systems has been resolved ([“Problem writing PNG” #133)](https://github.com/pymupdf/PyMuPDF/issues/133).

---

**Changes in Version 1.12.4**

This is an extension of 1.12.3.

- Fix of [issue #147](https://github.com/pymupdf/PyMuPDF/issues/147): methods `Document.getPageFontlist()` and `Document.getPageImagelist()` now also show fonts and images contained in [`resources`](glossary.html#resources "resources") nested via “Form XObjects”.
- Temporary fix of [issue #148](https://github.com/pymupdf/PyMuPDF/issues/148): Saving to new PDF files will now automatically use *garbage = 2* if a lower value is given. Final fix is to be expected with MuPDF’s next version. At that point we will remove this circumvention.
- Preventive fix of illegally using stencil / image mask pixmaps in some methods.
- Method `Document.getPageFontlist()` now includes the encoding name for each font in the list.
- Method `Document.getPageImagelist()` now includes the decode method name for each image in the list.

---

**Changes in Version 1.12.3**

This is an extension of 1.12.2.

- Many functions now return *None* instead of *0*, if the result has no other meaning than just indicating successful execution ([`Document.close()`](document.html#Document.close "Document.close"), [`Document.save()`](document.html#Document.save "Document.save"), [`Document.select()`](document.html#Document.select "Document.select"), [`Pixmap.save()`](pixmap.html#Pixmap.save "Pixmap.save") and many others).

---

**Changes in Version 1.12.2**

This is an extension of 1.12.1.

- Method [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") now accepts the new *clip* argument. This specifies an area of the source page to which the display should be restricted.
- New `Page.CropBox` and `Page.MediaBox` have been included for convenience.

---

**Changes in Version 1.12.1**

This is an extension of version 1.12.0.

- New method [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page") displays another’s PDF page. This is a **vector** image and therefore remains precise across zooming. Both involved documents must be PDF.
- New method `Page.getSVGimage()` creates an SVG image from the page. In contrast to the raster image of a pixmap, this is a vector image format. The return is a unicode text string, which can be saved in a *.svg* file.
- Method `Page.getTextBlocks()` now accepts an additional bool parameter “images”. If set to true (default is false), image blocks (metadata only) are included in the produced list and thus allow detecting areas with rendered images.
- Minor bug fixes.
- “text” result of `Page.getText()` concatenates all lines within a block using a single space character. MuPDF’s original uses “\n” instead, producing a rather ragged output.
- New properties of [Page](page.html#page) objects `Page.MediaBoxSize` and `Page.CropBoxPosition` provide more information about a page’s dimensions. For non-PDF files (and for most PDF files, too) these will be equal to `Page.rect.bottom_right`, resp. `Page.rect.top_left`. For example, class [Shape](shape.html#shape) makes use of them to correctly position its items.

---

**Changes in Version 1.12.0**

This version is based on and requires MuPDF v1.12.0. The new MuPDF version contains quite a number of changes – most of them around text extraction. Some of the changes impact the programmer’s API.

- `Outline.saveText()` and `Outline.saveXML()` have been deleted without replacement. You probably haven’t used them much anyway. But if you are looking for a replacement: the output of [`Document.get_toc()`](document.html#Document.get_toc "Document.get_toc") can easily be used to produce something equivalent.
- Class *TextSheet* does no longer exist.
- Text “spans” (one of the hierarchy levels of [TextPage](textpage.html#textpage)) no longer contain positioning information (i.e. no “bbox” key). Instead, spans now provide the font information for its text. This impacts our JSON output variant.
- HTML output has improved very much: it now creates valid documents which can be displayed by browsers to produce a similar view as the original document.
- There is a new output format XHTML, which provides text and images in a browser-readable format. The difference to HTML output is, that no effort is made to reproduce the original layout.
- All output formats of `Page.getText()` now support creating complete, valid documents, by wrapping them with appropriate header and trailer information. If you are interested in using the HTML output, please make sure to read [Controlling Quality of HTML Output](app1.html#htmlquality).
- To support finding text positions, we have added special methods that don’t need detours like [`TextPage.extractJSON()`](textpage.html#TextPage.extractJSON "TextPage.extractJSON") or [`TextPage.extractXML()`](textpage.html#TextPage.extractXML "TextPage.extractXML"): use `Page.getTextBlocks()` or resp. `Page.getTextWords()` to create lists of text blocks or resp. words, which are accompanied by their rectangles. This should be much faster than the standard text extraction methods and also avoids using additional packages for interpreting their output.

---

**Changes in Version 1.11.2**

This is an extension of v1.11.1.

- New `Page.insertFont()` creates a PDF */Font* object and returns its object number.
- New `Document.extractFont()` extracts the content of an embedded font given its object number.
- Methods **FontList(…)** items no longer contain the PDF generation number. This value never had any significance. Instead, the font file extension is included (e.g. “pfa” for a “PostScript Font for ASCII”), which is more valuable information.
- Fonts other than “simple fonts” (Type1) are now also supported.
- New options to change [Pixmap](pixmap.html#pixmap) size:

  > - Method [`Pixmap.shrink()`](pixmap.html#Pixmap.shrink "Pixmap.shrink") reduces the pixmap proportionally in place.
  > - A new [Pixmap](pixmap.html#pixmap) copy constructor allows scaling via setting target width and height.

---

**Changes in Version 1.11.1**

This is an extension of v1.11.0.

- New class *Shape*. It facilitates and extends the creation of image shapes on PDF pages. It contains multiple methods for creating elementary shapes like lines, rectangles or circles, which can be combined into more complex ones and be given common properties like line width or colors. Combined shapes are handled as a unit and e.g. be “morphed” together. The class can accumulate multiple complex shapes and put them all in the page’s foreground or background – thus also reducing the number of updates to the page’s [`contents`](glossary.html#contents "contents") object.
- All *Page* draw methods now use the new *Shape* class.
- Text insertion methods *insertText()* and *insertTextBox()* now support morphing in addition to text rotation. They have become part of the *Shape* class and thus allow text to be freely combined with graphics.
- A new *Pixmap* constructor allows creating pixmap copies with an added alpha channel. A new method also allows directly manipulating alpha values.
- Binary algebraic operations with geometry objects (matrices, rectangles and points) now generally also support lists or tuples as the second operand. You can add a tuple *(x, y)* of numbers to a [Point](point.html#point). In this context, such sequences are called “[`point_like`](glossary.html#point_like "point_like")” (resp. [`matrix_like`](glossary.html#matrix_like "matrix_like"), [`rect_like`](glossary.html#rect_like "rect_like")).
- Geometry objects now fully support in-place operators. For example, *p /= m* replaces point p with *p \* 1/m* for a number, or *p \* ~m* for a [`matrix_like`](glossary.html#matrix_like "matrix_like") object *m*. Similarly, if *r* is a rectangle, then *r |= (3, 4)* is the new rectangle that also includes *fitz.Point(3, 4)*, and *r &= (1, 2, 3, 4)* is its intersection with *fitz.Rect(1, 2, 3, 4)*.

---

**Changes in Version 1.11.0**

This version is based on and requires MuPDF v1.11.

Though MuPDF has declared it as being mostly a bug fix version, one major new feature is indeed contained: support of embedded files – also called portfolios or collections. We have extended PyMuPDF functionality to embrace this up to an extent just a little beyond the *mutool* utility as follows.

- The *Document* class now support embedded files with several new methods and one new property:

  > - *embfile\_Info()* returns metadata information about an entry in the list of embedded files. This is more than *mutool* currently provides: it shows all the information that was used to embed the file (not just the entry’s name).
  > - *embfile\_Get()* retrieves the (decompressed) content of an entry into a *bytes* buffer.
  > - *embfile\_Add(…)* inserts new content into the PDF portfolio. We (in contrast to *mutool*) **restrict** this to entries with a **new name** (no duplicate names allowed).
  > - *embfile\_Del(…)* deletes an entry from the portfolio (function not offered in MuPDF).
  > - *embfile\_SetInfo()* – changes filename or description of an embedded file.
  > - *embfile\_Count* – contains the number of embedded files.
- Several enhancements deal with streamlining geometry objects. These are not connected to the new MuPDF version and most of them are also reflected in PyMuPDF v1.10.0. Among them are new properties to identify the corners of rectangles by name (e.g. *Rect.bottom\_right*) and new methods to deal with set-theoretic questions like *Rect.contains(x)* or *IRect.intersects(x)*. Special effort focussed on supporting more “Pythonic” language constructs: *if x in rect …* is equivalent to *rect.contains(x)*.
- The [Rect](rect.html#rect) chapter now has more background on empty amd infinite rectangles and how we handle them. The handling itself was also updated for more consistency in this area.
- We have started basic support for **generation** of PDF content:

  > - *Document.insert\_page()* adds a new page into a PDF, optionally containing some text.
  > - *Page.insertImage()* places a new image on a PDF page.
  > - *Page.insertText()* puts new text on an existing page
- For **FileAttachment** annotations, content and name of the attached file can extracted and changed.

---

**Changes in Version 1.10.0**

**MuPDF v1.10 Impact**

MuPDF version 1.10 has a significant impact on our bindings. Some of the changes also affect the API – in other words, **you** as a PyMuPDF user.

- Link destination information has been reduced. Several properties of the *linkDest* class no longer contain valuable information. In fact, this class as a whole has been deleted from MuPDF’s library and we in PyMuPDF only maintain it to provide compatibility to existing code.
- In an effort to minimize memory requirements, several improvements have been built into MuPDF v1.10:

  > - A new *config.h* file can be used to de-select unwanted features in the C base code. Using this feature we have been able to reduce the size of our binary *\_fitz.o* / *\_fitz.pyd* by about 50% (from 9 MB to 4.5 MB). When UPX-ing this, the size goes even further down to a very handy 2.3 MB.
  > - The alpha (transparency) channel for pixmaps is now optional. Letting alpha default to *False* significantly reduces pixmap sizes (by 20% – CMYK, 25% – RGB, 50% – GRAY). Many *Pixmap* constructors therefore now accept an *alpha* boolean to control inclusion of this channel. Other pixmap constructors (e.g. those for file and image input) create pixmaps with no alpha altogether. On the downside, save methods for pixmaps no longer accept a *savealpha* option: this channel will always be saved when present. To minimize code breaks, we have left this parameter in the call patterns – it will just be ignored.
- *DisplayList* and *TextPage* class constructors now **require the mediabox** of the page they are referring to (i.e. the *page.bound()* rectangle). There is no way to construct this information from other sources, therefore a source code change cannot be avoided in these cases. We assume however, that not many users are actually employing these rather low level classes explicitly. So the impact of that change should be minor.

**Other Changes compared to Version 1.9.3**

- The new [Document](document.html#document) method *write()* writes an opened PDF to memory (as opposed to a file, like *save()* does).
- An annotation can now be scaled and moved around on its page. This is done by modifying its rectangle.
- Annotations can now be deleted. [Page](page.html#page) contains the new method *deleteAnnot()*.
- Various annotation attributes can now be modified, e.g. content, dates, title (= author), border, colors.
- Method *Document.insert\_pdf()* now also copies annotations of source pages.
- The *Pages* class has been deleted. As documents can now be accessed with page numbers as indices (like *doc[n] = doc.loadPage(n)*), and document object can be used as iterators, the benefit of this class was too low to maintain it. See the following comments.
- *loadPage(n)* / *doc[n]* now accept arbitrary integers to specify a page number, as long as *n < pageCount*. So, e.g. *doc[-500]* is always valid and will load page *(-500) % pageCount*.
- A document can now also be used as an iterator like this: *for page in doc: …<do something with “page”> …*. This will yield all pages of *doc* as *page*.
- The [Pixmap](pixmap.html#pixmap) method *getSize()* has been replaced with property *size*. As before *Pixmap.size == len(Pixmap)* is true.
- In response to transparency (alpha) being optional, several new parameters and properties have been added to [Pixmap](pixmap.html#pixmap) and [Colorspace](colorspace.html#colorspace) classes to support determining their characteristics.
- The [Page](page.html#page) class now contains new properties *firstAnnot* and *firstLink* to provide starting points to the respective class chains, where *firstLink* is just a mnemonic synonym to method *loadLinks()* which continues to exist. Similarly, the new property *rect* is a synonym for method *bound()*, which also continues to exist.
- [Pixmap](pixmap.html#pixmap) methods *samplesRGB()* and *samplesAlpha()* have been deleted because pixmaps can now be created without transparency.
- [Rect](rect.html#rect) now has a property *irect* which is a synonym of method *round()*. Likewise, [IRect](irect.html#irect) now has property *rect* to deliver a [Rect](rect.html#rect) which has the same coordinates as floats values.
- Document has the new method *searchPageFor()* to search for a text string. It works exactly like the corresponding *Page.searchFor()* with page number as additional parameter.

---

**Changes in Version 1.9.3**

This version is also based on MuPDF v1.9a. Changes compared to version 1.9.2:

- As a major enhancement, annotations are now supported in a similar way as links. Annotations can be displayed (as pixmaps) and their properties can be accessed.
- In addition to the document *select()* method, some simpler methods can now be used to manipulate a PDF:

  > - *copyPage()* copies a page within a document.
  > - *movePage()* is similar, but deletes the original.
  > - *delete\_page()* deletes a page
  > - *delete\_pages()* deletes a page range
- *rotation* or *setRotation()* access or change a PDF page’s rotation, respectively.
- Available but undocumented before, [IRect](irect.html#irect), [Rect](rect.html#rect), [Point](point.html#point) and [Matrix](matrix.html#matrix) support the *len()* method and their coordinate properties can be accessed via indices, e.g. *IRect.x1 == IRect[2]*.
- For convenience, documents now support simple indexing: *doc.loadPage(n) == doc[n]*. The index may however be in range *-pageCount < n < pageCount*, such that *doc[-1]* is the last page of the document.

---

**Changes in Version 1.9.2**

This version is also based on MuPDF v1.9a. Changes compared to version 1.9.1:

- *fitz.open()* (no parameters) creates a new empty **PDF** document, i.e. if saved afterwards, it must be given a *.pdf* extension.
- [Document](document.html#document) now accepts all of the following formats (*Document* and *open* are synonyms):

  - *open()*,
  - *open(filename)* (equivalent to *open(filename, None)*),
  - *open(filetype, area)* (equivalent to *open(filetype, stream = area)*).

  Type of memory area *stream* may be *bytes* or *bytearray*. Thus, e.g. *area = open(“file.pdf”, “rb”).read()* may be used directly (without first converting it to bytearray).
- New method *Document.insert\_pdf()* (PDFs only) inserts a range of pages from another PDF.
- *Document* objects doc now support the *len()* function: `len(doc) == doc.pageCount`.
- New method *Document.getPageImageList()* creates a list of images used on a page.
- New method *Document.getPageFontList()* creates a list of fonts referenced by a page.
- New pixmap constructor *fitz.Pixmap(doc, xref)* creates a pixmap based on an opened PDF document and an [`xref`](glossary.html#xref "xref") number of the image.
- New pixmap constructor *fitz.Pixmap(cspace, spix)* creates a pixmap as a copy of another one *spix* with the colorspace converted to *cspace*. This works for all colorspace combinations.
- Pixmap constructor *fitz.Pixmap(colorspace, width, height, samples)* now allows *samples* to also be *bytes*, not only *bytearray*.

---

**Changes in Version 1.9.1**

This version of PyMuPDF is based on MuPDF library source code version 1.9a published on April 21, 2016.

Please have a look at MuPDF’s website to see which changes and enhancements are contained herein.

Changes in version 1.9.1 compared to version 1.8.0 are the following:

- New methods *get\_area()* for both *fitz.Rect* and *fitz.IRect*
- Pixmaps can now be created directly from files using the new constructor *fitz.Pixmap(filename)*.
- The Pixmap constructor *fitz.Pixmap(image)* has been extended accordingly.
- *fitz.Rect* can now be created with all possible combinations of points and coordinates.
- PyMuPDF classes and methods now all contain \_\_doc\_\_ strings, most of them created by SWIG automatically. While the PyMuPDF documentation certainly is more detailed, this feature should help a lot when programming in Python-aware IDEs.
- A new document method of *getPermits()* returns the permissions associated with the current access to the document (print, edit, annotate, copy), as a Python dictionary.
- The identity matrix *fitz.Identity* is now **immutable**.
- The new document method *select(list)* removes all pages from a document that are not contained in the list. Pages can also be duplicated and re-arranged.
- Various improvements and new members in our demo and examples collections. Perhaps most prominently: *PDF\_display* now supports scrolling with the mouse wheel, and there is a new example program *wxTableExtract* which allows to graphically identify and extract table data in documents.
- *fitz.open()* is now an alias of *fitz.Document()*.
- New pixmap method *tobytes()* which will return a bytearray formatted as a PNG image of the pixmap.
- New pixmap method *samplesRGB()* providing a *samples* version with alpha bytes stripped off (RGB colorspaces only).
- New pixmap method *samplesAlpha()* providing the alpha bytes only of the *samples* area.
- New iterator *fitz.Pages(doc)* over a document’s set of pages.
- New matrix methods *invert()* (calculate inverted matrix), *concat()* (calculate matrix product), *pretranslate()* (perform a shift operation).
- New *IRect* methods *intersect()* (intersection with another rectangle), *translate()* (perform a shift operation).
- New *Rect* methods *intersect()* (intersection with another rectangle), *transform()* (transformation with a matrix), *include\_point()* (enlarge rectangle to also contain a point), *include\_rect()* (enlarge rectangle to also contain another one).
- Documented *Point.transform()* (transform a point with a matrix).
- *Matrix*, *IRect*, *Rect* and *Point* classes now support compact, algebraic formulations for manipulating such objects.
- Incremental saves for changes are possible now using the call pattern *doc.save(doc.name, incremental=True)*.
- A PDF’s metadata can now be deleted, set or changed by document method *set\_metadata()*. Supports incremental saves.
- A PDF’s bookmarks (or table of contents) can now be deleted, set or changed with the entries of a list using document method *set\_toc(list)*. Supports incremental saves.

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.