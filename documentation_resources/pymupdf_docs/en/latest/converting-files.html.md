<!-- Source: https://pymupdf.readthedocs.io/en/latest/converting-files.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Converting Files

## Files to PDF

[Document types supported by PyMuPDF](how-to-open-a-file.html#howtoopenafile) can easily be converted to PDF by using the [`Document.convert_to_pdf()`](document.html#Document.convert_to_pdf "Document.convert_to_pdf") method. This method returns a buffer of data which can then be utilized by PyMuPDF to create a new PDF.

**Example**

```
import pymupdf

xps = pymupdf.open("input.xps")
pdfbytes = xps.convert_to_pdf()
pdf = pymupdf.open("pdf", pdfbytes)
pdf.save("output.pdf")
```

## PDF to SVG

Technically, as SVG files cannot be multipage, we must export each page as an SVG.

To get an SVG representation of a page use the [`Page.get_svg_image()`](page.html#Page.get_svg_image "Page.get_svg_image") method.

**Example**

```
import pymupdf

doc = pymupdf.open("input.pdf")
page = doc[0]

# Convert page to SVG
svg_content = page.get_svg_image()

# Save to file
with open("output.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

doc.close()
```

## PDF to Markdown

By utlilizing the [PyMuPDF4LLM API](pymupdf4llm/api.html) we are able to convert PDF to a Markdown representation.

**Example**

```
import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("test.pdf")
print(md_text)

pathlib.Path("4llm-output.md").write_bytes(md_text.encode())
```

## PDF to DOCX

Use the [pdf2docx](https://pdf2docx.readthedocs.io/en/latest/) library which uses PyMuPDF to provide document conversion from PDF to **DOCX** format.

**Example**

```
from pdf2docx import Converter

pdf_file = 'input.pdf'
docx_file = 'output.docx'

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file) # all pages by default
cv.close()
```

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.