<!-- Source: https://pymupdf.readthedocs.io/en/latest/about.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Features Comparison

## Feature Matrix

The following table illustrates how PyMuPDF compares with other typical solutions.

| Feature | PyMuPDF | pikepdf | PyPDF2 | pdfrw | pdfplumber / pdfminer |
| --- | --- | --- | --- | --- | --- |
| Supports Multiple Document Formats | PDF XPS EPUB MOBI FB2 CBZ SVG TXT Image   ---  DOCX XLSX PPTX HWPX See [note](#note) | PDF | PDF | PDF | PDF |
| Implementation | Python and C | Python and C++ | Python | Python | Python |
| Render Document Pages | All document types | No rendering | No rendering | No rendering | No rendering |
| Write Text to PDF Page | See: [Page.insert\_htmlbox](page.html#Page.insert_htmlbox)  or:  [Page.insert\_textbox](page.html#Page.insert_textbox )  or:  [TextWriter](textwriter.html) |  |  |  |  |
| Supports CJK characters |  |  |  |  |  |
| Extract Text | All document types |  | PDF only |  | PDF only |
| Extract Text as Markdown (.md) | All document types |  |  |  |  |
| Extract Tables | All document types |  |  |  | PDF only |
| Extract Vector Graphics | All document types |  |  |  | Limited |
| Draw Vector Graphics (PDF) |  |  |  |  |  |
| Based on Existing, Mature Library | MuPDF | QPDF |  |  |  |
| Automatic Repair of Damaged PDFs |  |  |  |  |  |
| Encrypted PDFs |  |  | Limited |  | Limited |
| Linerarized PDFs |  |  |  |  |  |
| Incremental Updates |  |  |  |  |  |
| Integrates with Jupyter and IPython Notebooks |  |  |  |  |  |
| Joining / Merging PDF with other Document Types | All document types | PDF only | PDF only | PDF only | PDF only |
| OCR API for Seamless Integration with Tesseract | All document types |  |  |  |  |
| Integrated Checkpoint / Restart Feature (PDF) |  |  |  |  |  |
| PDF Optional Content |  |  |  |  |  |
| PDF Embedded Files |  |  | Limited |  | Limited |
| PDF Redactions |  |  |  |  |  |
| PDF Annotations | Full |  | Limited |  |  |
| PDF Form Fields | Create, read, update |  | Limited, no creation |  |  |
| PDF Page Labels |  | Read-only |  |  |  |
| Support Font Sub-Setting |  |  |  |  |  |

  

---

Note

A note about **Office** document types (DOCX, XLXS, PPTX) and **Hangul** documents (HWPX). These documents can be loaded into PyMuPDF and you will receive a [Document](document.html#document) object.

There are some caveats:

- we convert the input to **HTML** to layout the content.
- because of this the original page separation has gone.

When saving out the result any faithful representation of the original layout cannot be expected.

Therefore input files are mostly in a form that’s useful for text extraction.

---

# PyMuPDF Product Suite

PyMuPDF is the standard version of the library, however there are a family of additional products each with different features and functionality.

**Additional products** in the PyMuPDF product suite are:

- PyMuPDF Pro adds support for Office document formats.
- PyMuPDF4LLM is optimized for large language model (LLM) applications, providing enhanced text extraction and processing capabilities.

> It focuses on layout analysis and semantic understanding, ideal for document conversion and formatting tasks with enhanced results.

Note

All of the products above depend on the same core product - PyMuPDF and therefore have full access to all of its features.
These additional products can be seen as optional extras to the enhance the core PyMuPDF library.

## PyMuPDF Products Comparison

The following table illustrates what features the products offer:

PyMuPDF Products Comparison

|  | PyMuPDF | PyMuPDF Pro | PyMuPDF4LLM |
| --- | --- | --- | --- |
| **Input Documents** | `PDF`, `XPS`, `EPUB`, `CBZ`, `MOBI`, `FB2`, `SVG`, `TXT`, Images (*standard document types*) | *as PyMuPDF* and: `DOC`/`DOCX`, `XLS`/`XLSX`, `PPT`/`PPTX`, `HWP`/`HWPX` | *as PyMuPDF* |
| **Output Documents** | Can convert any input document to `PDF`, `SVG` or Image | *as PyMuPDF* | *as PyMuPDF* and: Markdown (`MD`), `JSON` or `TXT` |
| **Page Analysis** | Basic page analysis to return document structure | *as PyMuPDF* | Advanced Page Analysis with trained data for enhanced results |
| **Data extraction** | Basic data extraction with structured layout information and bounding box data | *as PyMuPDF* | Advanced data extraction including layout analysis with semantic understanding and enhanced bounding box data |
| **Table extraction** | Basic table extraction as part of text extraction | *as PyMuPDF* | Advanced table extraction with cell structure, including support for merged cells and complex layouts |
| **Image extraction** | Basic image extraction | *as PyMuPDF* | Advanced detection and rendering of image areas on page saving them to disk or embedding in MD output |
| **Vector extraction** | Vector extraction and clustering | *as PyMuPDF* | Superior detection of “picture” areas |
| **Popular RAG Integrations** | Langchain, LlamaIndex | *as PyMuPDF* | *as PyMuPDF* and with some additional help methods for RAG workflows |
| **OCR** | On-demand invocation of built-in Tesseract for text detection on pages or images | *as PyMuPDF* | Automatic OCR based on page content analysis. OCR adapators for popular OCR engines available |

---

# Performance

To benchmark PyMuPDF performance against a range of tasks a test suite with a fixed set of [8 PDFs with a total of 7,031 pages](app4.html#appendix4-files-used) containing text & images is used to obtain performance timings.

Here are current results, grouped by task:

  

**Copying**
:   This refers to opening a document and then saving it to a new file. This test measures the speed of reading a PDF and re-writing as a new PDF. This process is also at the core of functions like merging / joining multiple documents. The numbers below therefore apply to PDF joining and merging.

    The results for all 7,031 pages are:

600

500

400

300

200

100

⏱

seconds

3.05

10.54

33.57

494.04

PyMuPDF

PDFrw

PikePDF

PyPDF2

*fastest*

←

←

*slowest*

  

**Text Extraction**
:   This refers to extracting simple, plain text from every page of the document and storing it in a text file.

    The results for all 7,031 pages are:

400

300

200

100

⏱

seconds

8.01

27.42

101.64

227.27

PyMuPDF

XPDF

PyPDF2

PDFMiner

*fastest*

←

←

*slowest*

  

**Rendering**
:   This refers to making an image (like PNG) from every page of a document at a given DPI resolution. This feature is the basis for displaying a document in a GUI window.

    The results for all 7,031 pages are:

1000

800

600

400

200

⏱

seconds

367.04

646

851.52

PyMuPDF

XPDF

PDF2JPG

*fastest*

←

*slowest*

  

Note

For more detail regarding the methodology for these performance timings see: [Performance Comparison Methodology](app4.html#appendix4).

# License and Copyright

PyMuPDF and MuPDF are now available under both, open-source AGPL and commercial license agreements. Please read the full text of the AGPL license agreement, available in the distribution material (file COPYING) and [on the GNU license page](https://www.gnu.org/licenses/agpl-3.0.html), to ensure that your use case complies with the guidelines of the license. If you determine you cannot meet the requirements of the AGPL, please contact [Artifex](https://artifex.com/contact/pymupdf-inquiry.php?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=inline-link) for more information regarding a commercial license.

Find out more about Licensing

Artifex is the exclusive commercial licensing agent for MuPDF.

Artifex, the Artifex logo, MuPDF, and the MuPDF logo are registered trademarks of Artifex Software Inc.

This documentation covers PyMuPDF 1.27.2.2.

The major and minor versions of PyMuPDF and MuPDF will always be the same. Only the third qualifier (patch level) may deviate from that of MuPDF.

Typically PyMuPDF is released more frequently than MuPDF so it will often be
the case that the patch level of PyMuPDF will be greater than the embedded
MuPDF.

For example PyMuPDF-1.24.5 contains MuPDF-1.24.2.

Also see [`pymupdf_version`](vars.html#pymupdf_version "pymupdf_version") and [`mupdf_version`](vars.html#mupdf_version "mupdf_version").

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.