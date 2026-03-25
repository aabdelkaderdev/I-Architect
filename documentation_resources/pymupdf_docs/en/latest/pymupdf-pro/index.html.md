<!-- Source: https://pymupdf.readthedocs.io/en/latest/pymupdf-pro/index.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# PyMuPDF Pro

PyMuPDF Pro is a set of *commercial extensions* for PyMuPDF.

Enhance PyMuPDF capability with **Office** document support & **RAG/LLM** integrations.

- Enables Office document handling, including `doc`, `docx`, `hwp`, `hwpx`, `ppt`, `pptx`, `xls`, `xlsx`, and others.
- Supports text and table extraction, document conversion and more.
- Includes the commercial version of PyMuPDF4LLM.

To enquire about obtaining a commercial license, then [use this contact page](https://artifex.com/contact/).

Note

A licensed version of PyMuPDF Pro also gives you a licensed version of PyMuPDF4LLM. If you are interested in using the PyMuPDF4LLM package you should install it separately.

## Platform support

Available for these platforms only:

- Windows x86\_64.
- Linux x86\_64 (glibc).
- MacOS x86\_64.
- MacOS arm64.

## Office file support

In addition to the [standard file types supported by PyMuPDF](../how-to-open-a-file.html#supported-file-types), PyMuPDF Pro supports:

| **DOC/DOCX** | **XLS/XLSX** | **PPT/PPTX** | **HWP/HWPX** |
| --- | --- | --- | --- |
|  |  |  |  |

## Usage

### Installation

Install via pip with:

```
pip install pymupdfpro
```

### Loading an **Office** document

Import PyMuPDF Pro and you can then reference **Office** documents directly, e.g.:

```
import pymupdf.pro
pymupdf.pro.unlock()
# PyMuPDF has now been extended with PyMuPDF Pro features, with some restrictions.
doc = pymupdf.open("my-office-doc.xls")
```

Note

All standard PyMuPDF functionality is exposed as expected - PyMuPDF Pro handles the extended **Office** file types

From then on you can work with document pages just as you would do normally, but with respect to the [restrictions](#pymupdfpro-restrictions).

### Converting an **Office** document to PDF

The following code snippet can convert your **Office** document to PDF format:

```
import pymupdf.pro
pymupdf.pro.unlock()

doc = pymupdf.open("my-office-doc.xlsx")

pdfdata = doc.convert_to_pdf()
with open('output.pdf', 'wb') as f:
    f.write(pdfdata)
```

### Restrictions

PyMuPDF Pro functionality is restricted without a license key as follows:

> **Only the first 3 pages of any document will be available.**

To unlock full functionality you should [obtain a trial key](https://pymupdf.pro/try-pro/).

## Trial keys

To obtain a license key [please fill out the form on this page](https://pymupdf.pro/try-pro/). You will then have the trial key emailled to the address you submitted.

### Using a key

Initialize PyMuPDF Pro with a key as follows:

```
import pymupdf.pro
pymupdf.pro.unlock(my_key)
# PyMuPDF has now been extended with PyMuPDF Pro features.
```

This will allow you to evaluate the product for a limited time. If you want to use PyMuPDF Pro after this time you should then [enquire about obtaining a commercial license](https://artifex.com/products/pymupdf-pro/).

## Fonts

By default `pymupdf.pro.unlock()` searches for all installed font directories.

This can be controlled with keyword-only args:

- `fontpath`: specific font directories, either as a list/tuple or `os.sep`-separated string.
  If None (the default), we use `os.environ['PYMUPDFPRO_FONT_PATH']` if set.
- `fontpath_auto`: Whether to append system font directories.
  If None (the default) we use true if `os.environ['PYMUPDFPRO_FONT_PATH_AUTO']` is ‘1’.
  If true we append all system font directories.

Function `pymupdf.pro.get_fontpath()` returns a tuple of all font directories used by `unlock()`.

Ready to try PyMuPDF Pro?

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.