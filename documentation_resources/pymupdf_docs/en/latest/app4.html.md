<!-- Source: https://pymupdf.readthedocs.io/en/latest/app4.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Appendix 4: Performance Comparison Methodology

This article documents the approach to measure PyMuPDF’s performance and the tools and example files used to do comparisons.

The following three sections deal with different performance aspects:

- [Document Copying](#app4-copying) - This includes opening and parsing PDFs, then writing them to an output file. Because the same basic activities are also used for joining (merging) PDFs, the results also apply to these use cases.
- [Text Extraction](#app4-text-extraction) - This extracts plain text from PDFs and writes it to an output text file.
- [Page Rendering](#app4-page-rendering) - This converts PDF pages to image files looking identical to the pages. This ability is the basic prerequisite for using a tool in Python GUI scripts to scroll through documents. We have chosen a medium-quality (resolution 150 DPI) version.

Please note that in all cases the actual speed in dealing with PDF structures is not directly measured: instead, the timings also include the durations of writing files to the operating system’s file system. This cannot be avoided because tools other than PyMuPDF do not offer the option to e.g., separate the image **creation** step from the following step, which **writes** the image into a file.

So all timings documented include a common, OS-oriented base effort. Therefore, performance **differences per tool are actually larger** than the numbers suggest.

## Files used

A set of eight files is used for the performance testing. With each file we have the following information:

- **Name** of the file and download **link**.
- **Size** in bytes.
- Total number of **pages** in file.
- Total number of bookmarks (**Table of Contents** entries).
- Total number of **links**.
- **KB size** per page.
- **Textsize per page** is the amount text in the whole file in KB, divided by the number of pages.
- Any **notes** to generally describe the type of file.

| **Name** | **Size (bytes)** | **Pages** | **TOC size** | **Links** | **KB/page** | **Textsize/page** | **Notes** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `adobe.pdf` | 32,472,771 | 1,310 | 794 | 32,096 | 24 | 1,942 | linearized, many links / bookmarks |
| `artifex-website.pdf` | 31,570,732 | 47 | 46 | 2,035 | 656 | 3,538 | graphics oriented |
| `db-systems.pdf` | 29,326,355 | 1,241 | 0 | 0 | 23 | 2,142 |  |
| `fontforge.pdf` | 8,222,384 | 214 | 31 | 242 | 38 | 1,058 | mix of text & graphics |
| `pandas.pdf` | 10,585,962 | 3,071 | 536 | 16,554 | 3 | 1,539 | many pages |
| `pymupdf.pdf` | 6,805,176 | 478 | 276 | 5,277 | 14 | 1,937 | text oriented |
| `pythonbook.pdf` | 9,983,856 | 669 | 198 | 1,953 | 15 | 1,929 |  |
| `sample-50-MB-pdf-file.pdf` | 52,521,850 | 1 | 0 | 0 | 51,291 | 23,860 | single page, graphics oriented, large file size |

Note

**adobe.pdf** and **pymupdf.pdf** are clearly text oriented, **artifex-website.pdf** and **sample-50-MB-pdf-file.pdf** are graphics oriented. Other files are a mix of both.

## Tools used

In each section, the same fixed set of PDF files is being processed by a set of tools. The set of tools used per performance aspect however varies, depending on the supported tool features.

All tools are either platform independent, or at least can run on both, Windows and Unix / Linux.

| **Tool** | **Description** |
| --- | --- |
| PyMuPDF | The tool of this manual. |
| [PDFrw](https://pypi.org/project/pdfrw/) | A pure Python tool, being used by rst2pdf, has interface to ReportLab. |
| [PyPDF2](https://pypi.org/project/pypdf/) | A pure Python tool with a large function set. |
| [PDFMiner](https://pypi.org/project/pdfminer.six/) | A pure Python to extract text and other data from PDF. |
| [XPDF](https://www.xpdfreader.com/) | A command line utility with multiple functions. |
| [PikePDF](https://pypi.org/search/?q=pikepdf) | A Python package similar to PDFrw, but based on C++ library QPDF. |
| [PDF2JPG](https://pypi.org/project/pdf2jpg/) | A Python package specialized on rendering PDF pages to JPG images. |

## Copying / Joining / Merging

How fast is a PDF file read and its content parsed for further processing? The sheer parsing performance cannot directly be compared, because batch utilities always execute a requested task completely, in one go, front to end. PDFrw too, has a *lazy* strategy for parsing, meaning it only parses those parts of a document that are required in any moment.

To find an answer to the question, we therefore measure the time to copy a PDF file to an output file with each tool, and do nothing else.

These are the Python commands for how each tool is used:

PyMuPDF

```
import pymupdf
doc = pymupdf.open("input.pdf")
doc.save("output.pdf")
```

PDFrw

```
doc = PdfReader("input.pdf")
writer = PdfWriter()
writer.trailer = doc
writer.write("output.pdf")
```

PikePDF

```
from pikepdf import Pdf
doc = Pdf.open("input.pdf")
doc.save("output.pdf")
```

PyPDF2

```
pdfmerge = PyPDF2.PdfMerger()
pdfmerge.append("input.pdf")
pdfmerge.write("output.pdf")
pdfmerge.close()
```

**Observations**

These are our run time findings in **seconds** along with a base rate summary compared to PyMuPDF:

| **Name** | PyMuPDF | **PDFrw** | **PikePDF** | **PyPDF2** |
| --- | --- | --- | --- | --- |
| adobe.pdf | 1.75 | 5.15 | 22.37 | 374.05 |
| artifex-website.pdf | 0.26 | 0.38 | 1.41 | 2.81 |
| db-systems.pdf | 0.15 | 0.8 | 1.68 | 2.46 |
| fontforge.pdf | 0.09 | 0.14 | 0.28 | 1.1 |
| pandas.pdf | 0.38 | 2.21 | 2.73 | 70.3 |
| pymupdf.pdf | 0.11 | 0.56 | 0.83 | 6.05 |
| pythonbook.pdf | 0.19 | 1.2 | 1.34 | 37.19 |
| sample-50-MB-pdf-file.pdf | 0.12 | 0.1 | 2.93 | 0.08 |
| **Total** | **3.05** | **10.54** | **33.57** | **494.04** |
|  |  |  |  |  |
| **Rate compared to PyMuPDF** | 1.0 | 3.5 | 11.0 | 162 |

## Text Extraction

The following table shows plain text extraction durations. All tools have been used with their most basic functionality - i.e. no layout re-arrangements, etc.

**Observations**

These are our run time findings in **seconds** along with a base rate summary compared to PyMuPDF:

| **Name** | PyMuPDF | **XPDF** | **PyPDF2** | **PDFMiner** |
| --- | --- | --- | --- | --- |
| adobe.pdf | 2.01 | 6.19 | 22.2 | 49.15 |
| artifex-website.pdf | 0.18 | 0.3 | 1.1 | 4.06 |
| db-systems.pdf | 1.57 | 4.26 | 25.75 | 42.19 |
| fontforge.pdf | 0.24 | 0.47 | 2.69 | 4.2 |
| pandas.pdf | 2.41 | 10.54 | 25.38 | 76.56 |
| pymupdf.pdf | 0.49 | 2.34 | 6.44 | 13.55 |
| pythonbook.pdf | 0.84 | 2.88 | 9.28 | 24.27 |
| sample-50-MB-pdf-file.pdf | 0.27 | 0.44 | 8.8 | 13.29 |
| **Total** | **8.01** | **27.42** | **101.64** | **227.27** |
|  |  |  |  |  |
| **Rate compared to PyMuPDF** | 1.0 | 3.42 | 12.69 | 28.37 |

## Page Rendering

We have tested rendering speed of PyMuPDF against pdf2jpg and XPDF at a resolution of 150 DPI,

These are the Python commands for how each tool is used:

PyMuPDF

```
def ProcessFile(datei):
print "processing:", datei
doc=pymupdf.open(datei)
for p in pymupdf.Pages(doc):
    pix = p.get_pixmap(dpi=150)
    pix.save(f"t-{p.number}.png")
    pix = None
doc.close()
return
```

XPDF

```
pdftopng.exe -r 150 file.pdf ./
```

PDF2JPG

```
def ProcessFile(datei):
    print("processing:", datei)
    pdf2jpg.convert_pdf2jpg(datei, "images", pages="ALL", dpi=150)
    return
```

**Observations**

These are our run time findings in **seconds** along with a base rate summary compared to PyMuPDF:

| **Name** | PyMuPDF | **XPDF** | **PDF2JPG** |
| --- | --- | --- | --- |
| adobe.pdf | 51.33 | 98.16 | 75.71 |
| artifex-website.pdf | 26.35 | 51.28 | 54.11 |
| db-systems.pdf | 84.59 | 143.16 | 405.22 |
| fontforge.pdf | 12.23 | 22.18 | 20.14 |
| pandas.pdf | 138.74 | 241.67 | 202.06 |
| pymupdf.pdf | 22.35 | 39.11 | 33.38 |
| pythonbook.pdf | 30.44 | 49.12 | 55.68 |
| sample-50-MB-pdf-file.pdf | 1.01 | 1.32 | 5.22 |
| **Total** | **367.04** | **646** | **851.52** |
|  |  |  |  |
| **Rate compared to PyMuPDF** | 1.0 | 1.76 | 2.32 |

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.