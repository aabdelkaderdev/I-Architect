<!-- Source: https://pymupdf.readthedocs.io/en/latest/faq/index.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# FAQ

QI installed PyMuPDF but `import pymupdf` says "no module named pymupdf". What's wrong?+

This is the single most common installation issue. A few things to check:

First, make sure you installed `pymupdf` (not `pymypdf` or `mupdf`):

```
pip install pymupdf
```

Second, verify your IDE (PyCharm, VS Code, etc.) is using the same Python interpreter and virtual environment where you installed it. Try running `python -c "import pymupdf; print(pymupdf.__doc__)"` directly in a terminal to isolate IDE issues.

Third, there is a separate PyPI package literally named `fitz` that has nothing to do with PyMuPDF. These two packages cannot coexist in the same environment. If you installed both, uninstall `fitz` and reinstall `pymupdf`.

**Note:**`import fitz` still works as a legacy alias, but `import pymupdf` is the recommended import since version 1.24.0.

QHow do I install PyMuPDF on Apple Silicon (M1/M2/M3/M4/M5)?+

PyMuPDF now ships pre-built wheels for Apple Silicon. A simple `pip install pymupdf` should work.

```
pip install pymupdf
```

QWhen will PyMuPDF support the latest MuPDF version?+

PyMuPDF releases typically follow MuPDF releases by a few days. When a new MuPDF version is released, the PyMuPDF team updates bindings and pushes a new release within 1-2 days. Check the [changelog](https://pymupdf.readthedocs.io/en/latest/changes.html) for the latest version mapping.

QHow do I install PyMuPDF in a Docker container?+

Standard `pip install pymupdf` works in most Linux containers. For OCR support, you also need Tesseract language data files. A typical Dockerfile:

```
FROM python:3.11-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng
RUN pip install pymupdf
```

**Performance note:** OCR in Docker may be slower than on bare metal due to thread detection differences. Explicitly setting `OMP_THREAD_LIMIT` can help.

QWhat are the different text extraction modes and when should I use each?+

`page.get_text()` accepts several output format options:

`"text"` — Plain text. Good for simple extraction where layout doesn't matter.

`"blocks"` — Returns a list of text blocks with bounding boxes. Useful for identifying paragraphs.

`"words"` — Individual words with positions. Good for spatial analysis.

`"dict"` — Structured dictionary with blocks, lines, and spans including font information. Use this when you need font names, sizes, and colors.

`"rawdict"` — Like "dict" but with individual character-level positions. The most detailed but largest output. Use when you need exact character placement.

`"json"` / `"rawjson"` — Same as dict/rawdict but as JSON strings. Easier to save to a file for inspection.

**Tip:** If you want to inspect the output structure, use `"json"` or `"rawjson"` and save to a file rather than trying to dump a deeply nested dict to CSV.

QI can see text in the PDF but `get_text()` returns empty or garbled characters. Why?+

Several possible causes:

**Scanned PDF:** The page is an image, not real text. You need OCR. See the [OCR section](#ocr).

**Scrambled encoding:** Some PDF creators intentionally scramble character sequences as copy-protection. The text looks correct visually but the internal encoding is randomized. There is no reliable way to detect this programmatically. If you see lots of `U+FFFD` (replacement characters), this is likely the cause.

**Custom font encoding:** The font does not provide a back-translation to Unicode. If the font's internal `/ToUnicode` map is missing, the information simply cannot be recovered. OCR is your fallback here.

**Diagnostic:** Try `page.get_text("rawdict")` and inspect the character codes. If they're all `0xFFFD` or nonsensical, the encoding is broken at the PDF level, not a PyMuPDF issue.

QHow do I extract text from a specific rectangular area of a page?+

Use the `clip` parameter:

```
rect = pymupdf.Rect(100, 100, 400, 300)
text = page.get_text(clip=rect)

# With full detail:
data = page.get_text("rawdict", clip=rect)
```

This works with all output formats ("text", "dict", "rawdict", etc.).

QText extraction doesn't follow reading order. Columns are mixed up. How do I fix this?+

Text extraction order depends entirely on how the PDF was created. The internal order may not match visual reading order. Use `sort=True` to sort blocks by position (top-left to bottom-right):

```
text = page.get_text(sort=True)
```

For multi-column layouts, this helps but isn't perfect. You may need to identify column boundaries yourself using block bounding boxes and split text accordingly. There is no universal solution because PDF creators can store text in arbitrary order.

QHow do I extract only bold (or italic) text from a PDF?+

Use `"dict"` output and filter by span flags:

```
data = page.get_text("dict")
for block in data["blocks"]:
    if "lines" not in block:
        continue
    for line in block["lines"]:
        for span in line["spans"]:
            # flags: bit 0 = superscript, bit 1 = italic,
            # bit 2 = serif, bit 3 = monospace, bit 4 = bold
            if span["flags"] & (1 << 4):  # bold
                print(span["text"])
```

You can also check the font name. Bold fonts typically have "Bold", "Bd", or "Heavy" in their name.

QHow do I find and locate specific text on a page?+

Use `page.search_for()`:

```
areas = page.search_for("your search term")
for rect in areas:
    print(rect)  # pymupdf.Rect with coordinates
```

This returns a list of `Rect` objects showing where each occurrence appears. Note: regular expressions are not supported. If you need regex matching, first extract the full text with `get_text()`, find matches, then use `search_for()` to locate each match on the page.

**Performance note:** Adding `quads=True` is actually slightly faster than the default, because rects are internally converted from quads.

QCan I render specific spans from rawdict back onto a blank page?+

Yes, but it requires manual work. You need to: (1) extract the font(s) used in the spans, (2) write your own positioning code using the character-level data from `"rawdict"`, and (3) use `TextWriter` or `insert_text()` to place each character. This is an advanced use case where you're essentially re-rendering specific text elements.

QHow do I extract tables from a PDF into a pandas DataFrame?+

```
import pymupdf
import pandas as pd

doc = pymupdf.open("input.pdf")
page = doc[0]  # first page
tables = page.find_tables()

for table in tables:
    df = table.to_pandas()
    print(df)
```

The `find_tables()` method detects tables using vector graphics (lines and rectangles). No intermediate image conversion is involved.

Qfind\_tables() isn't detecting my table. What can I do?+

Table detection depends on how the table was constructed in the PDF. Common issues:

**No visible borders:** If the table has no drawn lines or rectangles, the detection may fail. Try the `strategy="text"` parameter for text-based detection.

**Background colors only:** Some tables use cell background colors without borders. These are harder to detect reliably.

PyMuPDF's table extraction is ported from pdfplumber (chosen over alternatives like tabula for its pure-Python implementation and better accuracy). For extremely unusual table structures, you may need to combine `get_text("dict")` with your own spatial logic.

QCan I extract a table, modify it, and write it back to the same location in the PDF?+

This has a very high probability of failure. You can extract and store table content, structure, and location, but writing it back only works if there are zero structural changes: no new cells, no removed cells, no cell size changes, no merged cells. Even then, there is no native "replace table" function. You would need to redact the original area and rebuild the table from scratch using text insertion and drawing commands.

QHow does OCR work in PyMuPDF? Does it use Tesseract?+

Yes. MuPDF contains the Tesseract C++ code directly (it's compiled in, not called as an external process). PyMuPDF calls MuPDF functions to invoke Tesseract. The only external requirement is Tesseract language data files (tessdata). Over 100 languages are supported.

There is no Python-level Tesseract dependency. Everything runs through the C/C++ layer.

QHow do I OCR an image file (not a PDF)?+

```
import pymupdf

pix = pymupdf.Pixmap("image.png")

# Remove alpha channel if present (required for OCR)
if pix.alpha:
    pix = pymupdf.Pixmap(pix, 0)

# Create a 1-page PDF with OCR text layer
doc = pymupdf.open("pdf", pix.pdfocr_tobytes())

# Now extract the text
text = doc[0].get_text()
```

**Common error:** If your image has a transparency (alpha) channel, OCR will fail. Always check and remove it with `pymupdf.Pixmap(pix, 0)` first.

QHow do I OCR a specific language (e.g., Ukrainian, Chinese)?+

Install the Tesseract language data file for your language, then specify it:

```
# For a full page OCR:
tp = page.get_textpage_ocr(language="ukr")  # Ukrainian
text = page.get_text(textpage=tp)

# For image-to-PDF OCR:
doc = pymupdf.open("pdf", pix.pdfocr_tobytes(language="chi_sim"))  # Chinese Simplified
```

Make sure the corresponding `.traineddata` file exists in your Tesseract data directory.

QOCR is very slow in my Docker container compared to running locally. Why?+

Tesseract uses OpenMP for parallelism. In Docker, thread detection may not work correctly, causing it to use fewer threads than available. Try setting `OMP_THREAD_LIMIT` environment variable explicitly. Also ensure your container has adequate CPU resources allocated.

QHow do I determine if a page needs OCR or already has extractable text?+

There's no silver bullet. A reasonable heuristic:

```
text = page.get_text().strip()
if not text or len(text) < 10:
    # Probably needs OCR
    tp = page.get_textpage_ocr()
    text = page.get_text(textpage=tp)
```

For scrambled text (copy-protection), you might get text that looks like random characters. Checking for high rates of `U+FFFD` replacement characters can help detect this. But detecting scrambled text reliably is fundamentally difficult.

QDoes PyMuPDF4LLM send my data to any external service or API?+

**No.** PyMuPDF4LLM is completely derived from PyMuPDF. There is no access to anything beyond your local machine. No calls to any AI, LLM, RAG, or cloud service. Everything works exactly the same when all internet access is blocked. It is fully GDPR-compatible in terms of data processing.

QHow do I get page-level metadata (like LlamaIndex documents) from PyMuPDF4LLM?+

Use the `page_chunks` option:

```
import pymupdf4llm

# Returns a list of page dictionaries (similar to LlamaIndex Document objects)
result = pymupdf4llm.to_markdown("input.pdf", page_chunks=True)

for page in result:
    print(page["metadata"])  # page number, etc.
    print(page["text"][:200])  # markdown content
```

QPyMuPDF4LLM merges my tables into plain text instead of markdown tables. Why?+

Table detection depends on the PDF structure. Some tables are defined in unusual ways (partial borders, background colors only on some cells, inconsistent cell structures). There's a limit to how creatively a table might have been defined.

Try adjusting table detection parameters. If the table structure is truly unconventional, you may need to fall back to `page.find_tables()` with custom parameters and handle table conversion to markdown separately.

QWhat is the licensing situation for PyMuPDF4LLM in a commercial product?+

PyMuPDF4LLM has the same license as PyMuPDF and MuPDF: either GNU AGPL or a commercial license from Artifex. If you're using it as part of a commercial product's data pipeline (even if it's just parsing PDFs for a RAG system), the AGPL obligations apply. Contact [Artifex](https://artifex.com/contact/) to evaluate your situation and discuss commercial licensing.

QCan I process multiple PDFs at once with PyMuPDF4LLM?+

The API processes one PDF at a time. For batch processing, loop over your files:

```
import pymupdf4llm
from pathlib import Path

for pdf in Path("./docs").glob("*.pdf"):
    md = pymupdf4llm.to_markdown(str(pdf), page_chunks=True)
    # process each result
```

QWhich AI frameworks use PyMuPDF for PDF parsing?+

LlamaIndex uses PyMuPDF. LangChain includes PyMuPDF as one of its PDF loader alternatives. Many RAG pipeline implementations in the ecosystem rely on PyMuPDF for the extraction layer.

QExtracted images have a black background where transparency should be. How do I preserve transparency?+

When extracting images, check for an SMask (soft mask). The `page.extract_image(xref)` result dictionary has an `"smask"` key. If its value is > 0, that's the xref of the transparency mask. You need to extract both and combine them:

```
img = page.extract_image(xref)
if img["smask"] > 0:
    mask_pix = pymupdf.Pixmap(doc, img["smask"])
    main_pix = pymupdf.Pixmap(doc, xref)
    # Combine image with its mask
    pix = pymupdf.Pixmap(main_pix, mask_pix)
else:
    pix = pymupdf.Pixmap(doc, xref)
```

QHow do I insert an image into a page?+

Use `page.insert_image()` with a target rectangle:

```
# Insert from file
rect = pymupdf.Rect(100, 100, 300, 250)
page.insert_image(rect, filename="logo.png")

# Use page.rect for full-page:
page.insert_image(page.rect, filename="background.jpg")
```

**Common mistake:** Don't pass the filename as a positional argument. Use `filename=` explicitly. The call pattern is `insert_image(rect, filename=None, pixmap=None, stream=None, ...)`.

QHow do I render a page to an image (screenshot)?+

```
page = doc[0]
pix = page.get_pixmap(dpi=150)  # default is 72 dpi
pix.save("page.png")

# Higher resolution:
pix = page.get_pixmap(dpi=300)
```

You can also use a `Matrix` for more control over scaling and rotation.

QCan I extract vector graphics (logos, diagrams) as images?+

Vector graphics (line art) cannot be extracted as images directly because they aren't images in the PDF. PyMuPDF can extract vector drawings as path data via `page.get_drawings()`, which returns elementary drawing commands (lines, curves, rectangles). To get a visual representation, render the relevant area to a Pixmap using a clip rectangle.

QWhat's the difference between `insert_text`, `insert_textbox`, and `insert_htmlbox`?+

`page.insert_text(point, text)` — Places text starting at a single point. No wrapping. You control exact position.

`page.insert_textbox(rect, text)` — Fills text into a rectangle with automatic line breaks. Returns a value indicating overflow (negative = text didn't fit).

`page.insert_htmlbox(rect, html)` — Like textbox but accepts HTML/CSS for rich formatting. Tremendously more flexible: supports mixed fonts, colors, alignment, etc. This is generally the recommended approach for complex text insertion.

QMy inserted text is white (invisible). How do I make it black?+

Black is the default color. If text appears white, you may be inserting on a dark background or there's a color space issue. Explicitly set color:

```
page.insert_text((100, 100), "Hello", color=pymupdf.pdfcolor["black"])

# Or using RGB tuple (0-1 range):
page.insert_text((100, 100), "Hello", color=(0, 0, 0))
```

QHow do I create a landscape page?+

```
# Use paper size with "-l" suffix for landscape
mediabox = pymupdf.paper_rect("a4-l")
page = doc.new_page(width=mediabox.width, height=mediabox.height)

# See all available paper sizes:
print(pymupdf.paper_sizes())
```

QHow do I set margins when inserting text on a new page?+

Create a fill rectangle with margins subtracted from the page rectangle:

```
page = doc.new_page()
left, top, right, bottom = 72, 72, 72, 72  # 1 inch margins
fill_rect = page.rect + (left, top, -right, -bottom)
page.insert_textbox(fill_rect, text, fontname="helv", fontsize=11)
```

QThe Euro sign (€) and other special characters show as "?" in my text. Why?+

The built-in Base-14 fonts (like "helv") only support characters up to Unicode 256. The Euro sign is at `0x80` in this range. Either replace `€` with `chr(0x80)` in your text, or use a proper Unicode font file:

```
page.insert_text((100, 100), "Price: 50€",
    fontfile="/path/to/arial.ttf",
    fontname="arial")
```

For CJK and extended characters, use the `pymupdf-fonts` package which includes FiraGO and CJK fallback fonts.

QHow do I dynamically fit text to a rectangle (auto font size)?+

Two approaches:

Option 1: Reduce font size until it fits:

```
fontsize = 20
while True:
    rc = page.insert_textbox(rect, text, fontsize=fontsize)
    if rc >= 0:  # positive = text fit
        break
    fontsize -= 0.5  # shrink and retry
```

Option 2: Use `insert_htmlbox()` which handles overflow more gracefully and gives you CSS-level control.

QHow do I add text on top of an image (with a background rectangle)?+

Draw the background rectangle first, then insert text on top:

```
shape = page.new_shape()
shape.draw_rect(rect)
shape.finish(fill=(1, 1, 0.8))  # light yellow fill
shape.commit()

page.insert_textbox(rect, text, fontsize=12)
```

Order matters: shapes drawn first appear behind text inserted later.

QDoes PyMuPDF support "cloudy" border style for annotations?+

No. The cloudy border effect (common in Adobe PDF annotations) is not implemented in MuPDF's C core, so it's not available through PyMuPDF either.

QHow do I redact (permanently remove) content from a PDF?+

```
# Step 1: Mark areas for redaction
rect = page.search_for("confidential")[0]
page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill

# Step 2: Apply redactions (permanently removes content)
page.apply_redactions()

doc.save("redacted.pdf")
```

After applying redactions, the original content is permanently removed from the PDF. This is a two-step process by design, so you can review before committing.

**Replacement text:** You can also insert replacement text during redaction, but the formatting options are limited. For more control, apply the redaction to clear the area, then use `insert_text()` or `insert_htmlbox()` in a separate step.

QCan I "flatten" annotations so they become part of the page content?+

MuPDF has work-in-progress support for this. If you flatten annotations, they become part of the page content stream and can no longer be edited, moved, or recognized as annotations by other PDF viewers. For form fields, this means they lose interactivity.

QHow do I add a highlight annotation to found text?+

```
quads = page.search_for("important text", quads=True)
for quad in quads:
    annot = page.add_highlight_annot(quad)
    annot.set_colors(stroke=(1, 1, 0))  # yellow
    annot.update()
```

Using `quads=True` gives more precise highlighting, especially for rotated or non-horizontal text.

QHow do I create a fillable form field (widget) in a PDF?+

```
import pymupdf

doc = pymupdf.open()
page = doc.new_page()

# Create a text input field
widget = pymupdf.Widget()
widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
widget.rect = pymupdf.Rect(50, 50, 250, 80)
widget.field_name = "name"
widget.field_value = "Enter name"

annot = page.add_widget(widget)
doc.save("form.pdf")
```

QHow do I create a date field widget?+

```
widget = pymupdf.Widget()
widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
widget.field_flags |= pymupdf.PDF_WIDGET_TX_FORMAT_DATE
widget.rect = pymupdf.Rect(20, 20, 160, 80)
widget.field_name = "Date"
widget.field_value = "12/12/2024"
annot = page.add_widget(widget)
```

QFonts in my form fields don't render correctly on mobile devices or non-Adobe readers.+

This is a common problem. PDF viewers that don't have the specified font will substitute or fail to render. The solution is to embed fonts in the PDF. Note that new form fields created by PyMuPDF have certain font restrictions. If you need specific fonts embedded, you may need to work at the xref level:

```
# After adding a widget:
annot = page.add_widget(widget)
xref = annot.xref  # use this to access low-level PDF objects
```

QWhat fonts are available by default without loading external font files?+

The PDF Base-14 fonts are always available:

`"helv"` (Helvetica), `"heit"` (Helvetica Italic), `"hebo"` (Helvetica Bold), `"hebi"` (Helvetica Bold Italic)

`"tiro"` (Times Roman), `"tiit"`, `"tibo"`, `"tibi"`

`"cour"` (Courier), `"coit"`, `"cobo"`, `"cobi"`

`"symb"` (Symbol), `"zadb"` (ZapfDingbats)

These only support characters up to about Unicode 256. For CJK, extended Latin, Arabic, etc., install `pymupdf-fonts` or provide your own font files.

QHow do I get the font name of extracted text?+

Use `"dict"` output format. Each span includes font information:

```
data = page.get_text("dict")
for block in data["blocks"]:
    if "lines" not in block:
        continue
    for line in block["lines"]:
        for span in line["spans"]:
            print(f"Font: {span['font']}, Size: {span['size']}")
```

QIs there a universal fallback font that can render any character?+

No single font covers everything including emojis. FiraGO (available in `pymupdf-fonts`) covers extended Latin and many scripts not in CJK. The CJK fallback font ("Droid Sans Fallback Regular") covers Chinese, Japanese, and Korean. But you cannot change or extend the fallback font chain. For maximum coverage, use a rich font like FiraGO as your primary and accept that some exotic characters may not render.

QHow do I extract specific pages from one PDF into a new PDF?+

```
src = pymupdf.open("input.pdf")
doc = pymupdf.open()  # new empty PDF
doc.insert_pdf(src, from_page=0, to_page=4)  # pages 1-5 (0-based)
doc.save("output.pdf")
```

QMy output PDF is the same size as the original even though I only extracted 2 pages from 20. Why?+

Different pages often share resources (fonts, images, etc.) that are referenced but not deduplicated on save. Use `ez_save()` instead of `save()`, or use save with garbage collection and deflation:

```
# Best option for size reduction:
doc.ez_save("output.pdf")

# Or with explicit options:
doc.save("output.pdf", garbage=4, deflate=True, clean=True)
```

`clean=True` can also help by cleaning content streams, but note this may increase file size for some PDFs (due to decompression of already-compressed streams).

QHow do I overlay one page on top of another (watermark / stamp)?+

Use `page.show_pdf_page()` to render a source page onto a target page:

```
src = pymupdf.open("watermark.pdf")
doc = pymupdf.open("document.pdf")

for page in doc:
    page.show_pdf_page(page.rect, src, 0)  # overlay page 0 of watermark

doc.save("stamped.pdf")
```

**Note:** `insert_pdf()` adds new pages. `show_pdf_page()` overlays content onto an existing page. These are different operations.

QWhat is the coordinate system in PyMuPDF? Where is (0,0)?+

The origin (0,0) is at the **top-left** of the page. X increases to the right, Y increases downward. This matches screen coordinates but differs from the PDF specification (which uses bottom-left origin). PyMuPDF handles the transformation internally.

An A4 page in portrait has dimensions approximately (0, 0, 595, 842) in points (1 point = 1/72 inch).

QWhat's the difference between `page.rect`, `page.mediabox`, and `page.cropbox`?+

`page.mediabox` — The physical page size as defined in the PDF. This is the largest boundary.

`page.cropbox` — The visible area when displayed. May be smaller than mediabox. This is what viewers typically show.

`page.rect` — The effective page rectangle considering rotation. Use this for most operations as it reflects what you actually see.

QWhat does bbox mean and what order are the coordinates?+

A bounding box (bbox) is defined as `(x0, y0, x1, y1)` where `(x0, y0)` is the top-left corner and `(x1, y1)` is the bottom-right corner. This forms a `pymupdf.Rect`:

```
rect = pymupdf.Rect(x0, y0, x1, y1)
print(rect.width)   # x1 - x0
print(rect.height)  # y1 - y0
print(rect.tl)      # top-left Point(x0, y0)
print(rect.br)      # bottom-right Point(x1, y1)
```

QHow do I check if a word/block is inside a given rectangle?+

Use rectangle containment or intersection:

```
region = pymupdf.Rect(100, 100, 400, 300)
word_rect = pymupdf.Rect(word[:4])  # first 4 elements of a "words" tuple

if word_rect in region:        # fully contained
    print("inside")
if word_rect.intersects(region):  # overlaps
    print("overlaps")
```

QHow do I handle very large PDFs without running out of memory?+

Close input/output documents at intervals to free resources. You can also shrink MuPDF's internal cache:

```
import pymupdf

# Process in batches
for i in range(0, total_pages, 50):
    src = pymupdf.open("huge.pdf")
    doc = pymupdf.open()
    doc.insert_pdf(src, from_page=i, to_page=min(i+49, total_pages-1))
    doc.save(f"batch_{i}.pdf")
    doc.close()
    src.close()
    pymupdf.TOOLS.store_shrink(100)  # free MuPDF cache
```

The major memory consumer is shared resources (fonts, images) that are referenced across pages. Batch processing with intermediate saves helps.

QCan I use multiprocessing with PyMuPDF?+

Yes, but each process needs its own document objects. Don't share `pymupdf.Document` objects across processes. A common pattern is to split work by page ranges, let each process open the file independently, and combine results afterward.

**Note:** Threading with GIL release was tested but found to have intolerable overhead. Multiprocessing is the better approach for parallelism.

QCan I use multithreading with PyMuPDF, perhaps with [free-threading Python](https://docs.python.org/3/howto/free-threading-python.html)?+

No, PyMuPDF does not support multithreaded use,
even with newer free-thread Python.

Making PyMuPDF work with threads is a tricky problem.
The underlying MuPDF library only provides partial thread safety so the results would not be as performant as might be naively assumed,
and the implementation would inevitably introduce and expose subtle bugs.

Any thread-safe implementation of PyMuPDF would also necessarily impose a single-threaded overhead.

The preferred approach is to [use multiple processes instead of multiple threads](../recipes-multiprocessing.html).
This gives most of what is generally required,
with simplicity and guaranteed correctness.

QHow do I convert HTML to PDF?+

Use the `Story` class:

```
import pymupdf

html = """
<h1>Hello World</h1>
<p>This is a <b>bold</b> paragraph.</p>
"""

story = pymupdf.Story(html)
writer = pymupdf.DocumentWriter("output.pdf")
mediabox = pymupdf.paper_rect("a4")

while True:
    device = writer.begin_page(mediabox)
    more, filled = story.place(mediabox + (36, 36, -36, -36))
    story.draw(device)
    writer.end_page()
    if not more:
        break

writer.close()
```

The Story class supports HTML and CSS for layout, including fonts, colors, and basic page flow.

QWhat document formats can PyMuPDF open?+

PDF, XPS, EPUB, MOBI, FB2, CBZ, SVG, and various image formats (PNG, JPEG, BMP, TIFF, etc.). All are opened with `pymupdf.open()`. For image formats, the result is a single-page document.