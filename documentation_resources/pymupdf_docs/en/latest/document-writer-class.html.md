<!-- Source: https://pymupdf.readthedocs.io/en/latest/document-writer-class.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# DocumentWriter

**This class is for PDF only.**

- New in v1.21.0

This class represents a utility which can output various [document types supported by PyMuPDF](how-to-open-a-file.html#supported-file-types).

In PyMuPDF only used for outputting PDF documents whose pages are populated by [Story](story-class.html#story) DOMs.

Using [DocumentWriter](#documentwriter) also for other document types might happen in the future.

| **Method / Attribute** | **Short Description** |
| --- | --- |
| [`DocumentWriter.begin_page()`](#DocumentWriter.begin_page "DocumentWriter.begin_page") | start a new output page |
| [`DocumentWriter.end_page()`](#DocumentWriter.end_page "DocumentWriter.end_page") | finish the current output page |
| [`DocumentWriter.close()`](#DocumentWriter.close "DocumentWriter.close") | flush pending output and close the file |

**Class API**

*class* DocumentWriter
:   \_\_init\_\_(*self*, *path*, *options=None*)
    :   Create a document writer object, passing a Python file pointer or a file path. Options to use when saving the file may also be passed.

        This class can also be used as a Python context manager.

        Parameters:
        :   - **path** –

              the output file. This may be a string file name, or any Python file pointer.

              Note

              By using a `io.BytesIO()` object as file pointer, a document writer can create a PDF in memory. Subsequently, this PDF can be re-opened for input and be further manipulated. This technique is used by several example scripts in [Stories recipes](recipes-stories.html#recipesstories).
            - **options** (*str*) – specify saving options for the output PDF. Typical are “compress” or “clean”. More possible values may be taken from help output of the `mutool convert` CLI utility.

    begin\_page(*mediabox*)
    :   Start a new output page of a given dimension.

        Parameters:
        :   **mediabox** (*rect\_like*) – a rectangle specifying the page size. After this method, output operations may write content to the page.

    end\_page()
    :   Finish a page. This flushes any pending data and appends the page to the output document.

    close()
    :   Close the output file. This method is required for writing any pending data.

    For usage examples consult the section of [Story](story-class.html#story).

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.