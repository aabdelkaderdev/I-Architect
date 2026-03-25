<!-- Source: https://pymupdf.readthedocs.io/en/latest/recipes-stories.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Stories

This document showcases some typical use cases for [Stories](tutorial.html#workingwithstories).

As mentioned in the [tutorial](tutorial.html#workingwithstories), stories may be created using up to three input sources: HTML, CSS and Archives – all of which are optional and which, respectively, can be provided programmatically.

The following examples will showcase combinations for using these inputs.

Note

Many of these recipe’s source code are included as examples in the `docs` folder.

## How to Add a Line of Text with Some Formatting

Here is the inevitable “Hello World” example. We will show two variants:

1. Create using existing HTML source [[1]](#f1), that may come from anywhere.
2. Create using the Python API.

---

Variant using an existing HTML source [[1]](#f1) – which in this case is defined as a constant in the script:

```
import pymupdf

HTML = """
<p style="font-family: sans-serif;color: blue">Hello World!</p>
"""

MEDIABOX = pymupdf.paper_rect("letter")  # output page format: Letter
WHERE = MEDIABOX + (36, 36, -36, -36)  # leave borders of 0.5 inches

story = pymupdf.Story(html=HTML)  # create story from HTML
writer = pymupdf.DocumentWriter("output.pdf")  # create the writer

more = 1  # will indicate end of input once it is set to 0

while more:  # loop outputting the story
    device = writer.begin_page(MEDIABOX)  # make new page
    more, _ = story.place(WHERE)  # layout into allowed rectangle
    story.draw(device)  # write on page
    writer.end_page()  # finish page

writer.close()  # close output file
```

Note

The above effect (sans-serif and blue text) could have been achieved by using a separate CSS source like so:

```
import pymupdf

CSS = """
body {
    font-family: sans-serif;
    color: blue;
}
"""

HTML = """
<p>Hello World!</p>
"""

# the story would then be created like this:
story = pymupdf.Story(html=HTML, user_css=CSS)
```

---

The Python API variant – everything is created programmatically:

```
import pymupdf

MEDIABOX = pymupdf.paper_rect("letter")
WHERE = MEDIABOX + (36, 36, -36, -36)

story = pymupdf.Story()  # create an empty story
body = story.body  # access the body of its DOM
with body.add_paragraph() as para:  # store desired content
    para.set_font("sans-serif").set_color("blue").add_text("Hello World!")

writer = pymupdf.DocumentWriter("output.pdf")

more = 1

while more:
    device = writer.begin_page(MEDIABOX)
    more, _ = story.place(WHERE)
    story.draw(device)
    writer.end_page()

writer.close()
```

Both variants will produce the same output PDF.

---

## How to use Images

Images can be referenced in the provided HTML source, or the reference to a desired image can also be stored via the Python API. In any case, this requires using an [Archive](archive-class.html#archive), which refers to the place where the image can be found.

Note

Images with the binary content embedded in the HTML source are **not supported** by stories.

We extend our “Hello World” example from above and display an image of our planet right after the text. Assuming the image has the name “world.jpg” and is present in the script’s folder, then this is the modified version of the above Python API variant:

```
import pymupdf

MEDIABOX = pymupdf.paper_rect("letter")
WHERE = MEDIABOX + (36, 36, -36, -36)

# create story, let it look at script folder for resources
story = pymupdf.Story(archive=".")
body = story.body  # access the body of its DOM

with body.add_paragraph() as para:
    # store desired content
    para.set_font("sans-serif").set_color("blue").add_text("Hello World!")

# another paragraph for our image:
with body.add_paragraph() as para:
    # store image in another paragraph
    para.add_image("world.jpg")

writer = pymupdf.DocumentWriter("output.pdf")

more = 1

while more:
    device = writer.begin_page(MEDIABOX)
    more, _ = story.place(WHERE)
    story.draw(device)
    writer.end_page()

writer.close()
```

---

## How to Read External HTML and CSS for a Story

These cases are fairly straightforward.

As a general recommendation, HTML and CSS sources should be **read as binary files** and decoded before using them in a story. The Python `pathlib.Path` provides convenient ways to do this:

```
import pathlib
import pymupdf

htmlpath = pathlib.Path("myhtml.html")
csspath = pathlib.Path("mycss.css")

HTML = htmlpath.read_bytes().decode()
CSS = csspath.read_bytes().decode()

story = pymupdf.Story(html=HTML, user_css=CSS)
```

---

## How to Output Database Content with Story Templates

This script demonstrates how to report SQL database content using an **HTML template**.

The example SQL database contains two tables:

1. Table “films” contains one row per film with the fields **“title”**, **“director”** and (release) **“year”**.
2. Table “actors” contains one row per actor and film title (fields (actor) **“name”** and (film) **“title”**).

The story DOM consists of a template for one film, which reports film data together with a list of casted actors.

**Files:**

- `docs/samples/filmfestival-sql.py`
- `docs/samples/filmfestival-sql.db`

See recipe

```
"""
This is a demo script for using PyMuPDF with its "Story" feature.

The following aspects are being covered here:

* The script produces a report of films that are stored in an SQL database
* The report format is provided as a HTML template

The SQL database contains two tables:
1. Table "films" which has the columns "title" (film title, str), "director"
   (str) and "year" (year of release, int).
2. Table "actors" which has the columns "name" (actor name, str) and "title"
   (the film title where the actor had been casted, str).

The script reads all content of the "films" table. For each film title it
reads all rows from table "actors" which took part in that film.

Comment 1
---------
To keep things easy and free from pesky technical detail, the relevant file
names inherit the name of this script:
- the database's filename is the script name with ".py" extension replaced
  by ".db".
- the output PDF similarly has script file name with extension ".pdf".

Comment 2
---------
The SQLITE database has been created using https://sqlitebrowser.org/, a free
multi-platform tool to maintain or manipulate SQLITE databases.
"""
import os
import sqlite3

import pymupdf

# ----------------------------------------------------------------------
# HTML template for the film report
# There are four placeholders coded as "id" attributes.
# One "id" allows locating the template part itself, the other three
# indicate where database text should be inserted.
# ----------------------------------------------------------------------
festival_template = (
    "<html><head><title>Just some arbitrary text</title></head>"
    '<body><h1 style="text-align:center">Hook Norton Film Festival</h1>'
    "<ol>"
    '<li id="filmtemplate">'
    '<b id="filmtitle"></b>'
    "<dl>"
    '<dt>Director<dd id="director">'
    '<dt>Release Year<dd id="filmyear">'
    '<dt>Cast<dd id="cast">'
    "</dl>"
    "</li>"
    "</ol>"
    "</body></html"
)

# -------------------------------------------------------------------
# define database access
# -------------------------------------------------------------------
dbfilename = __file__.replace(".py", ".db")  # the SQLITE database file name
assert os.path.isfile(dbfilename), f'{dbfilename}'
database = sqlite3.connect(dbfilename)  # open database
cursor_films = database.cursor()  # cursor for selecting the films
cursor_casts = database.cursor()  # cursor for selecting actors per film

# select statement for the films - let SQL also sort it for us
select_films = """SELECT title, director, year FROM films ORDER BY title"""

# select stament for actors, a skeleton: sub-select by film title
select_casts = """SELECT name FROM actors WHERE film = ? ORDER BY name"""
# -------------------------------------------------------------------
# define the HTML Story and fill it with database data
# -------------------------------------------------------------------
story = pymupdf.Story(festival_template)
body = story.body  # access the HTML body detail
template = body.find(None, "id", "filmtemplate")  # find the template part

# read the films from the database and put them all in one Python list
# NOTE: instead we might fetch rows one by one (advisable for large volumes)
cursor_films.execute(select_films)  # execute cursor, and ...
films = cursor_films.fetchall()  # read out what was found

for title, director, year in films:  # iterate through the films
    film = template.clone()  # clone template to report each film
    film.find(None, "id", "filmtitle").add_text(title)  # put title in templ
    film.find(None, "id", "director").add_text(director)  # put director
    film.find(None, "id", "filmyear").add_text(str(year))  # put year

    # the actors reside in their own table - find the ones for this film title
    cursor_casts.execute(select_casts, (title,))  # execute cursor
    casts = cursor_casts.fetchall()  # read actors for the film
    # each actor name appears in its own tuple, so extract it from there
    film.find(None, "id", "cast").add_text("\n".join([c[0] for c in casts]))
    body.append_child(film)

template.remove()  # remove the template

# -------------------------------------------------------------------
# generate the PDF
# -------------------------------------------------------------------
writer = pymupdf.DocumentWriter(__file__.replace(".py", ".pdf"), "compress")
mediabox = pymupdf.paper_rect("a4")  # use pages in ISO-A4 format
where = mediabox + (72, 36, -36, -72)  # leave page borders

more = 1  # end of output indicator

while more:
    dev = writer.begin_page(mediabox)  # make a new page
    more, filled = story.place(where)  # arrange content for this page
    story.draw(dev, None)  # write content to page
    writer.end_page()  # finish the page

writer.close()  # close the PDF
```

---

## How to Integrate with Existing PDFs

Because a [DocumentWriter](document-writer-class.html#documentwriter) can only write to a new file, stories cannot be placed on existing pages. This script demonstrates a circumvention of this restriction.

The basic idea is letting [DocumentWriter](document-writer-class.html#documentwriter) output to a PDF in memory. Once the story has finished, we re-open this memory PDF and put its pages to desired locations on **existing** pages via method [`Page.show_pdf_page()`](page.html#Page.show_pdf_page "Page.show_pdf_page").

**Files:**

- `docs/samples/showpdf-page.py`

See recipe

```
"""
Demo of Story class in PyMuPDF
-------------------------------

This script demonstrates how to the results of a pymupdf.Story output can be
placed in a rectangle of an existing (!) PDF page.

"""
import io
import os

import pymupdf

def make_pdf(fileptr, text, rect, font="sans-serif", archive=None):
    """Make a memory DocumentWriter from HTML text and a rect.

    Args:
        fileptr: a Python file object. For example an io.BytesIO().
        text: the text to output (HTML format)
        rect: the target rectangle. Will use its width / height as mediabox
        font: (str) font family name, default sans-serif
        archive: pymupdf.Archive parameter. To be used if e.g. images or special
                fonts should be used.
    Returns:
        The matrix to convert page rectangles of the created PDF back
        to rectangle coordinates in the parameter "rect".
        Normal use will expect to fit all the text in the given rect.
        However, if an overflow occurs, this function will output multiple
        pages, and the caller may decide to either accept or retry with
        changed parameters.
    """
    # use input rectangle as the page dimension
    mediabox = pymupdf.Rect(0, 0, rect.width, rect.height)
    # this matrix converts mediabox back to input rect
    matrix = mediabox.torect(rect)

    story = pymupdf.Story(text, archive=archive)
    body = story.body
    body.set_properties(font=font)
    writer = pymupdf.DocumentWriter(fileptr)
    while True:
        device = writer.begin_page(mediabox)
        more, _ = story.place(mediabox)
        story.draw(device)
        writer.end_page()
        if not more:
            break
    writer.close()
    return matrix

# -------------------------------------------------------------
# We want to put this in a given rectangle of an existing page
# -------------------------------------------------------------
HTML = """
<p>PyMuPDF is a great package! And it still improves significantly from one version to the next one!</p>
<p>It is a Python binding for <b>MuPDF</b>, a lightweight PDF, XPS, and E-book viewer, renderer, and toolkit.<br> Both are maintained and developed by Artifex Software, Inc.</p>
<p>Via MuPDF it can access files in PDF, XPS, OpenXPS, CBZ, EPUB, MOBI and FB2 (e-books) formats,<br> and it is known for its top
<b><i>performance</i></b> and <b><i>rendering quality.</p>"""

# Make a PDF page for demo purposes
root = os.path.abspath( f"{__file__}/..")
doc = pymupdf.open(f"{root}/mupdf-title.pdf")
page = doc[0]

WHERE = pymupdf.Rect(50, 100, 250, 500)  # target rectangle on existing page

fileptr = io.BytesIO()  # let DocumentWriter use this as its file

# -------------------------------------------------------------------
# call DocumentWriter and Story to fill our rectangle
matrix = make_pdf(fileptr, HTML, WHERE)
# -------------------------------------------------------------------
src = pymupdf.open("pdf", fileptr)  # open DocumentWriter output PDF
if src.page_count > 1:  # target rect was too small
    raise ValueError("target WHERE too small")

# its page 0 contains our result
page.show_pdf_page(WHERE, src, 0)

doc.ez_save(f"{root}/mupdf-title-after.pdf")
```

---

## How to Make Multi-Columned Layouts and Access Fonts from Package [pymupdf-fonts](https://github.com/pymupdf/pymupdf-fonts)

This script outputs an article (taken from Wikipedia) that contains text and multiple images and uses a 2-column page layout.

In addition, two “Ubuntu” font families from package [pymupdf-fonts](https://github.com/pymupdf/pymupdf-fonts) are used instead of defaulting to Base-14 fonts.

Yet another feature used here is that all data – the images and the article HTML – are jointly stored in a ZIP file.

**Files:**

- `docs/samples/quickfox.py`
- `docs/samples/quickfox.zip`

See recipe

```
"""
This is a demo script using PyMuPDF's Story class to output text as a PDF with
a two-column page layout.

The script demonstrates the following features:
* How to fill columns or table cells of complex page layouts
* How to embed images
* How to modify existing, given HTML sources for output (text indent, font size)
* How to use fonts defined in package "pymupdf-fonts"
* How to use ZIP files as Archive

--------------
The example is taken from the somewhat modified Wikipedia article
https://en.wikipedia.org/wiki/The_quick_brown_fox_jumps_over_the_lazy_dog.
--------------
"""

import io
import os
import zipfile
import pymupdf

thisdir = os.path.dirname(os.path.abspath(__file__))
myzip = zipfile.ZipFile(os.path.join(thisdir, "quickfox.zip"))
arch = pymupdf.Archive(myzip)

if pymupdf.fitz_fontdescriptors:
    # we want to use the Ubuntu fonts for sans-serif and for monospace
    CSS = pymupdf.css_for_pymupdf_font("ubuntu", archive=arch, name="sans-serif")
    CSS = pymupdf.css_for_pymupdf_font("ubuntm", CSS=CSS, archive=arch, name="monospace")
else:
    # No pymupdf-fonts available.
    CSS=""

docname = __file__.replace(".py", ".pdf")  # output PDF file name

HTML = myzip.read("quickfox.html").decode()

# make the Story object
story = pymupdf.Story(HTML, user_css=CSS, archive=arch)

# --------------------------------------------------------------
# modify the DOM somewhat
# --------------------------------------------------------------
body = story.body  # access HTML body
body.set_properties(font="sans-serif")  # and give it our font globally

# modify certain nodes
para = body.find("p", None, None)  # find relevant nodes (here: paragraphs)
while para != None:
    para.set_properties(  # method MUST be used for existing nodes
        indent=15,
        fontsize=13,
    )
    para = para.find_next("p", None, None)

# choose PDF page size
MEDIABOX = pymupdf.paper_rect("letter")
# text appears only within this subrectangle
WHERE = MEDIABOX + (36, 36, -36, -36)

# --------------------------------------------------------------
# define page layout within the WHERE rectangle
# --------------------------------------------------------------
COLS = 2  # layout: 2 cols 1 row
ROWS = 1
TABLE = pymupdf.make_table(WHERE, cols=COLS, rows=ROWS)
# fill the cells of each page in this sequence:
CELLS = [TABLE[i][j] for i in range(ROWS) for j in range(COLS)]

fileobject = io.BytesIO()  # let DocumentWriter write to memory
writer = pymupdf.DocumentWriter(fileobject)  # define the writer

more = 1
while more:  # loop until all input text has been written out
    dev = writer.begin_page(MEDIABOX)  # prepare a new output page
    for cell in CELLS:
        # content may be complete after any cell, ...
        if more:  # so check this status first
            more, _ = story.place(cell)
            story.draw(dev)
    writer.end_page()  # finish the PDF page

writer.close()  # close DocumentWriter output

# for housekeeping work re-open from memory
doc = pymupdf.open("pdf", fileobject)
doc.ez_save(docname)
```

---

## How to Make a Layout which Wraps Around a Predefined “no go area” Layout

This is a demo script using PyMuPDF’s Story class to output text as a PDF with
a two-column page layout.

The script demonstrates the following features:

- Layout text around images of an existing (“target”) PDF.
- Based on a few global parameters, areas on each page are identified, that
  can be used to receive text layouted by a Story.
- These global parameters are not stored anywhere in the target PDF and
  must therefore be provided in some way:

  - The width of the border(s) on each page.
  - The fontsize to use for text. This value determines whether the provided
    text will fit in the empty spaces of the (fixed) pages of target PDF. It
    cannot be predicted in any way. The script ends with an exception if
    target PDF has not enough pages, and prints a warning message if not all
    pages receive at least some text. In both cases, the FONTSIZE value
    can be changed (a float value).
  - Use of a 2-column page layout for the text.
- The layout creates a temporary (memory) PDF. Its produced page content
  (the text) is used to overlay the corresponding target page. If text
  requires more pages than are available in target PDF, an exception is raised.
  If not all target pages receive at least some text, a warning is printed.
- The script reads “image-no-go.pdf” in its own folder. This is the “target” PDF.
  It contains 2 pages with each 2 images (from the original article), which are
  positioned at places that create a broad overall test coverage. Otherwise the
  pages are empty.
- The script produces “quickfox-image-no-go.pdf” which contains the original pages
  and image positions, but with the original article text laid out around them.

**Files:**

- `docs/samples/quickfox-image-no-go.py`
- `docs/samples/quickfox-image-no-go.pdf`
- `docs/samples/quickfox.zip`

See recipe

```
"""
This is a demo script using PyMuPDF's Story class to output text as a PDF with
a two-column page layout.

The script demonstrates the following features:
* Layout text around images of an existing ("target") PDF.
* Based on a few global parameters, areas on each page are identified, that
  can be used to receive text layouted by a Story.
* These global parameters are not stored anywhere in the target PDF and
  must therefore be provided in some way.
  - The width of the border(s) on each page.
  - The fontsize to use for text. This value determines whether the provided
    text will fit in the empty spaces of the (fixed) pages of target PDF. It
    cannot be predicted in any way. The script ends with an exception if
    target PDF has not enough pages, and prints a warning message if not all
    pages receive at least some text. In both cases, the FONTSIZE value
    can be changed (a float value).
  - Use of a 2-column page layout for the text.
* The layout creates a temporary (memory) PDF. Its produced page content
  (the text) is used to overlay the corresponding target page. If text
  requires more pages than are available in target PDF, an exception is raised.
  If not all target pages receive at least some text, a warning is printed.
* The script reads "image-no-go.pdf" in its own folder. This is the "target" PDF.
  It contains 2 pages with each 2 images (from the original article), which are
  positioned at places that create a broad overall test coverage. Otherwise the
  pages are empty.
* The script produces "quickfox-image-no-go.pdf" which contains the original pages
  and image positions, but with the original article text laid out around them.

Note:
--------------
This script version uses just image positions to derive "No-Go areas" for
layouting the text. Other PDF objects types are detectable by PyMuPDF and may
be taken instead or in addition, without influencing the layouting.
The following are candidates for other such "No-Go areas". Each can be detected
and located by PyMuPDF:
* Annotations
* Drawings
* Existing text

--------------
The text and images are taken from the somewhat modified Wikipedia article
https://en.wikipedia.org/wiki/The_quick_brown_fox_jumps_over_the_lazy_dog.
--------------
"""

import io
import os
import zipfile
import pymupdf

thisdir = os.path.dirname(os.path.abspath(__file__))
myzip = zipfile.ZipFile(os.path.join(thisdir, "quickfox.zip"))

docname = os.path.join(thisdir, "image-no-go.pdf")  # "no go" input PDF file name
outname = os.path.join(thisdir, "quickfox-image-no-go.pdf")  # output PDF file name
BORDER = 36  # global parameter
FONTSIZE = 12.5  # global parameter
COLS = 2  # number of text columns, global parameter

def analyze_page(page):
    """Compute MediaBox and rectangles on page that are free to receive text.

    Notes:
        Assume a BORDER around the page, make 2 columns of the resulting
        sub-rectangle and extract the rectangles of all images on page.
        For demo purposes, the image rectangles are taken as "NO-GO areas"
        on the page when writing text with the Story.
        The function returns free areas for each of the columns.

    Returns:
        (page.number, mediabox, CELLS), where CELLS is a list of free cells.
    """
    prect = page.rect  # page rectangle - will be our MEDIABOX later
    where = prect + (BORDER, BORDER, -BORDER, -BORDER)
    TABLE = pymupdf.make_table(where, rows=1, cols=COLS)

    # extract rectangles covered by images on this page
    IMG_RECTS = sorted(  # image rects on page (sort top-left to bottom-right)
        [pymupdf.Rect(item["bbox"]) for item in page.get_image_info()],
        key=lambda b: (b.y1, b.x0),
    )

    def free_cells(column):
        """Return free areas in this column."""
        free_stripes = []  # y-value pairs wrapping a free area stripe
        # intersecting images: block complete intersecting column stripe
        col_imgs = [(b.y0, b.y1) for b in IMG_RECTS if abs(b & column) > 0]
        s_y0 = column.y0  # top y-value of column
        for y0, y1 in col_imgs:  # an image stripe
            if y0 > s_y0 + FONTSIZE:  # image starts below last free btm value
                free_stripes.append((s_y0, y0))  # store as free stripe
            s_y0 = y1  # start of next free stripe

        if s_y0 + FONTSIZE < column.y1:  # enough room to column bottom
            free_stripes.append((s_y0, column.y1))

        if free_stripes == []:  # covers "no image in this column"
            free_stripes.append((column.y0, column.y1))

        # make available cells of this column
        CELLS = [pymupdf.Rect(column.x0, y0, column.x1, y1) for (y0, y1) in free_stripes]
        return CELLS

    # collection of available Story rectangles on page
    CELLS = []
    for i in range(COLS):
        CELLS.extend(free_cells(TABLE[0][i]))

    return page.number, prect, CELLS

HTML = myzip.read("quickfox.html").decode()

# --------------------------------------------------------------
# Make the Story object
# --------------------------------------------------------------
story = pymupdf.Story(HTML)

# modify the DOM somewhat
body = story.body  # access HTML body
body.set_properties(font="sans-serif")  # and give it our font globally

# modify certain nodes
para = body.find("p", None, None)  # find relevant nodes (here: paragraphs)
while para != None:
    para.set_properties(  # method MUST be used for existing nodes
        indent=15,
        fontsize=FONTSIZE,
    )
    para = para.find_next("p", None, None)

# we remove all image references, because the target PDF already has them
img = body.find("img", None, None)
while img != None:
    next_img = img.find_next("img", None, None)
    img.remove()
    img = next_img

page_info = {}  # contains MEDIABOX and free CELLS per page
doc = pymupdf.open(docname)
for page in doc:
    pno, mediabox, cells = analyze_page(page)
    page_info[pno] = (mediabox, cells)
doc.close()  # close target PDF for now - re-open later

fileobject = io.BytesIO()  # let DocumentWriter write to memory
writer = pymupdf.DocumentWriter(fileobject)  # define output writer

more = 1  # stop if this ever becomes zero
pno = 0  # count output pages
while more:  # loop until all HTML text has been written
    try:
        MEDIABOX, CELLS = page_info[pno]
    except KeyError:  # too much text space required: reduce fontsize?
        raise ValueError("text does not fit on target PDF")
    dev = writer.begin_page(MEDIABOX)  # prepare a new output page
    for cell in CELLS:  # iterate over free cells on this page
        if not more:  # need to check this for every cell
            continue
        more, _ = story.place(cell)
        story.draw(dev)
    writer.end_page()  # finish the PDF page
    pno += 1

writer.close()  # close DocumentWriter output

# Re-open writer output, read its pages and overlay target pages with them.
# The generated pages have same dimension as their targets.
src = pymupdf.open("pdf", fileobject)
doc = pymupdf.open(doc.name)
for page in doc:  # overlay every target page with the prepared text
    if page.number >= src.page_count:
        print(f"Text only uses {src.page_count} target pages!")
        continue  # story did not need all target pages?

    # overlay target page
    page.show_pdf_page(page.rect, src, page.number)

    # DEBUG start --- draw the text rectangles
    # mb, cells = page_info[page.number]
    # for cell in cells:
    #     page.draw_rect(cell, color=(1, 0, 0))
    # DEBUG stop ---

doc.ez_save(outname)
```

---

## How to Output an HTML Table

Outputting HTML tables is supported as follows:

- Flat table layouts are supported (“rows x columns”), no support of the “colspan” / “rowspan” attributes.
- Table header tag *th* supports attribute “scope” with values “row” or “col”. Applicable text will be bold by default.
- Column widths are computed automatically based on column content. They cannot be directly set.
- Table **cells may contain images** which will be considered in the column width calculation magic.
- Row heights are computed automatically based on row content - leading to multi-line rows where needed.
- The potentially multiple lines of a table row will always be kept together on one page (respectively “where” rectangle) and not be split.
- Table header rows are only **shown on the first page / “where” rectangle.**
- The “style” attribute is ignored when given directly in HTML table elements. Styling for a table and its elements must happen separately, in CSS source or within the *style* tag.
- Styling for *tr* elements is not supported and ignored. Therefore, a table-wide grid or alternating row background colors are not supported. One of the following example scripts however shows an easy way to deal with this limitation.

**Files:**

- `docs/samples/table01.py` This script reflects basic features.

See recipe

```
"""
Demo script for basic HTML table support in Story objects

Outputs a table with three columns that fits on one Letter page.
The content of each row is filled via the Story's template mechanism.
Column widths and row heights are automatically computed by MuPDF.
Some styling via a CSS source is also demonstrated:

- The table header row has a gray background
- Each cell shows a border at its top
- The Story's body uses the sans-serif font family
- The text of one of the columns is set to blue

Dependencies
-------------
PyMuPDF v1.22.0 or later
"""
import pymupdf

table_text = (  # the content of each table row
    (
        "Length",
        "integer",
        """(Required) The number of bytes from the beginning of the line following the keyword stream to the last byte just before the keyword endstream. (There may be an additional EOL marker, preceding endstream, that is not included in the count and is not logically part of the stream data.) See “Stream Extent,” above, for further discussion.""",
    ),
    (
        "Filter",
        "name or array",
        """(Optional) The name of a filter to be applied in processing the stream data found between the keywords stream and endstream, or an array of such names. Multiple filters should be specified in the order in which they are to be applied.""",
    ),
    (
        "FFilter",
        "name or array",
        """(Optional; PDF 1.2) The name of a filter to be applied in processing the data found in the stream's external file, or an array of such names. The same rules apply as for Filter.""",
    ),
    (
        "FDecodeParms",
        "dictionary or array",
        """(Optional; PDF 1.2) A parameter dictionary, or an array of such dictionaries, used by the filters specified by FFilter. The same rules apply as for DecodeParms.""",
    ),
    (
        "DecodeParms",
        "dictionary or array",
        """(Optional) A parameter dictionary or an array of such dictionaries, used by the filters specified by Filter. If there is only one filter and that filter has parameters, DecodeParms must be set to the filter's parameter dictionary unless all the filter's parameters have their default values, in which case the DecodeParms entry may be omitted. If there are multiple filters and any of the filters has parameters set to nondefault values, DecodeParms must be an array with one entry for each filter: either the parameter dictionary for that filter, or the null object if that filter has no parameters (or if all of its parameters have their default values). If none of the filters have parameters, or if all their parameters have default values, the DecodeParms entry may be omitted. (See implementation note 7 in Appendix H.)""",
    ),
    (
        "DL",
        "integer",
        """(Optional; PDF 1.5) A non-negative integer representing the number of bytes in the decoded (defiltered) stream. It can be used to determine, for example, whether enough disk space is available to write a stream to a file.\nThis value should be considered a hint only; for some stream filters, it may not be possible to determine this value precisely.""",
    ),
    (
        "F",
        "file specification",
        """(Optional; PDF 1.2) The file containing the stream data. If this entry is present, the bytes between stream and endstream are ignored, the filters are specified by FFilter rather than Filter, and the filter parameters are specified by FDecodeParms rather than DecodeParms. However, the Length entry should still specify the number of those bytes. (Usually, there are no bytes and Length is 0.) (See implementation note 46 in Appendix H.)""",
    ),
)

# Only a minimal HTML source is required to provide the Story's working
HTML = """
<html>
<body><h2>TABLE 3.4 Entries common to all stream dictionaries</h2>
<table>
    <tr>
        <th>KEY</th><th>TYPE</th><th>VALUE</th>
    </tr>
    <tr id="row">
        <td id="col0"></td><td id="col1"></td><td id="col2"></td>
    </tr>
"""

"""
---------------------------------------------------------------------
Just for demo purposes, set:
- header cell background to gray
- text color in col1 to blue
- a border line at the top of all table cells
- all text to the sans-serif font
---------------------------------------------------------------------
"""
CSS = """th {
    background-color: #aaa;
}

td[id="col1"] {
    color: blue;
}

td, tr {
    border: 1px solid black;
    border-right-width: 0px;
    border-left-width: 0px;
    border-bottom-width: 0px;
}
body {
    font-family: sans-serif;
}
"""

story = pymupdf.Story(HTML, user_css=CSS)  # define the Story
body = story.body  # access the HTML <body> of it
template = body.find(None, "id", "row")  # find the template with name "row"
parent = template.parent  # access its parent i.e., the <table>

for col0, col1, col2 in table_text:
    row = template.clone()  # make a clone of the row template
    # add text to each cell in the duplicated row
    row.find(None, "id", "col0").add_text(col0)
    row.find(None, "id", "col1").add_text(col1)
    row.find(None, "id", "col2").add_text(col2)
    parent.append_child(row)  # add new row to <table>
template.remove()  # remove the template

# Story is ready - output it via a writer
writer = pymupdf.DocumentWriter(__file__.replace(".py", ".pdf"), "compress")
mediabox = pymupdf.paper_rect("letter")  # size of one output page
where = mediabox + (36, 36, -36, -36)  # use this sub-area for the content

more = True  # detects end of output
while more:
    dev = writer.begin_page(mediabox)  # start a page, returning a device
    more, filled = story.place(where)  # compute content fitting into "where"
    story.draw(dev)  # output it to the page
    writer.end_page()  # finalize the page
writer.close()  # close the output
```

- `docs/samples/national-capitals.py` Advanced script extending table output options using simple additional code:

  > - Multi-page output simulating **repeating header rows**
  > - Alternating table row background colors
  > - Table rows and columns delimited by gridlines
  > - Table rows dynamically generated / filled with data from an SQL database

See recipe

```
"""
Demo script using (Py-) MuPDF "Story" feature.

The following features are implemented:

* Use of Story "template" feature to provide row content
* Use database access (SQLITE) to fetch row content
* Use ElementPosition feature to locate cell positions on page
* Simulate feature "Table Header Repeat"
* Simulate feature "Cell Grid Lines"

"""
import io
import sqlite3
import sys

import pymupdf

"""
Table data. Used to populate a temporary SQL database, which will be processed by the script.
Its only purpose is to avoid carrying around a separate database file.
"""
# codespell:ignore-begin
table_data = """China;Beijing;21542000;1.5%;2018
Japan;Tokyo;13921000;11.2%;2019
DR Congo;Kinshasa;12691000;13.2%;2017
Russia;Moscow;12655050;8.7%;2021
Indonesia;Jakarta;10562088;3.9%;2020
Egypt;Cairo;10107125;9.3%;2022
South Korea;Seoul;9508451;18.3%;2022
Mexico;Mexico City;9209944;7.3%;2020
United Kingdom;London;9002488;13.4%;2020
Bangladesh;Dhaka;8906039;5.3%;2011
Peru;Lima;8852000;26.3%;2012
Iran;Tehran;8693706;9.9%;2016
Thailand;Bangkok;8305218;11.6%;2010
Vietnam;Hanoi;8053663;8.3%;2019
Iraq;Baghdad;7682136;17.6%;2021
Saudi Arabia;Riyadh;7676654;21.4%;2018
Hong Kong;Hong Kong;7291600;100%;2022
Colombia;Bogotá;7181469;13.9%;2011
Chile;Santiago;6310000;32.4%;2012
Turkey;Ankara;5747325;6.8%;2021
Singapore;Singapore;5453600;91.8%;2021
Afghanistan;Kabul;4601789;11.5%;2021
Kenya;Nairobi;4397073;8.3%;2019
Jordan;Amman;4061150;36.4%;2021
Algeria;Algiers;3915811;8.9%;2011
Germany;Berlin;3677472;4.4%;2021
Spain;Madrid;3305408;7.0%;2021
Ethiopia;Addis Ababa;3040740;2.5%;2012
Kuwait;Kuwait City;2989000;70.3%;2018
Guatemala;Guatemala City;2934841;16.7%;2020
South Africa;Pretoria;2921488;4.9%;2011
Ukraine;Kyiv;2920873;6.7%;2021
Argentina;Buenos Aires;2891082;6.4%;2010
North Korea;Pyongyang;2870000;11.1%;2016
Uzbekistan;Tashkent;2860600;8.4%;2022
Italy;Rome;2761632;4.7%;2022
Ecuador;Quito;2800388;15.7%;2020
Cameroon;Yaoundé;2765568;10.2%;2015
Zambia;Lusaka;2731696;14.0%;2020
Sudan;Khartoum;2682431;5.9%;2012
Brazil;Brasília;2648532;1.2%;2012
Taiwan;Taipei (de facto);2608332;10.9%;2020
Yemen;Sanaa;2575347;7.8%;2012
Angola;Luanda;2571861;7.5%;2020
Burkina Faso;Ouagadougou;2453496;11.1%;2019
Ghana;Accra;2388000;7.3%;2017
Somalia;Mogadishu;2388000;14.0%;2021
Azerbaijan;Baku;2303100;22.3%;2022
Cambodia;Phnom Penh;2281951;13.8%;2019
Venezuela;Caracas;2245744;8.0%;2016
France;Paris;2139907;3.3%;2022
Cuba;Havana;2132183;18.9%;2020
Zimbabwe;Harare;2123132;13.3%;2012
Syria;Damascus;2079000;9.7%;2019
Belarus;Minsk;1996553;20.8%;2022
Austria;Vienna;1962779;22.0%;2022
Poland;Warsaw;1863056;4.9%;2021
Philippines;Manila;1846513;1.6%;2020
Mali;Bamako;1809106;8.3%;2009
Malaysia;Kuala Lumpur;1782500;5.3%;2019
Romania;Bucharest;1716983;8.9%;2021
Hungary;Budapest;1706851;17.6%;2022
Congo;Brazzaville;1696392;29.1%;2015
Serbia;Belgrade;1688667;23.1%;2021
Uganda;Kampala;1680600;3.7%;2019
Guinea;Conakry;1660973;12.3%;2014
Mongolia;Ulaanbaatar;1466125;43.8%;2020
Honduras;Tegucigalpa;1444085;14.0%;2021
Senegal;Dakar;1438725;8.5%;2021
Niger;Niamey;1334984;5.3%;2020
Uruguay;Montevideo;1319108;38.5%;2011
Bulgaria;Sofia;1307439;19.0%;2021
Oman;Muscat;1294101;28.6%;2021
Czech Republic;Prague;1275406;12.1%;2022
Madagascar;Antananarivo;1275207;4.4%;2018
Kazakhstan;Astana;1239900;6.5%;2022
Nigeria;Abuja;1235880;0.6%;2011
Georgia;Tbilisi;1201769;32.0%;2022
Mauritania;Nouakchott;1195600;25.9%;2019
Qatar;Doha;1186023;44.1%;2020
Libya;Tripoli;1170000;17.4%;2019
Myanmar;Naypyidaw;1160242;2.2%;2014
Rwanda;Kigali;1132686;8.4%;2012
Mozambique;Maputo;1124988;3.5%;2020
Dominican Republic;Santo Domingo;1111838;10.0%;2010
Armenia;Yerevan;1096100;39.3%;2021
Kyrgyzstan;Bishkek;1074075;16.5%;2021
Sierra Leone;Freetown;1055964;12.5%;2015
Nicaragua;Managua;1055247;15.4%;2020
Canada;Ottawa;1017449;2.7%;2021
Pakistan;Islamabad;1014825;0.4%;2017
Liberia;Monrovia;1010970;19.5%;2008
United Arab Emirates;Abu Dhabi;1010092;10.8%;2020
Malawi;Lilongwe;989318;5.0%;2018
Haiti;Port-au-Prince;987310;8.6%;2015
Sweden;Stockholm;978770;9.4%;2021
Eritrea;Asmara;963000;26.6%;2020
Israel;Jerusalem;936425;10.5%;2019
Laos;Vientiane;927724;12.5%;2019
Chad;N'Djamena;916000;5.3%;2009
Netherlands;Amsterdam;905234;5.2%;2022
Central African Republic;Bangui;889231;16.3%;2020
Panama;Panama City;880691;20.2%;2013
Tajikistan;Dushanbe;863400;8.9%;2020
Nepal;Kathmandu;845767;2.8%;2021
Togo;Lomé;837437;9.7%;2010
Turkmenistan;Ashgabat;791000;12.5%;2017
Moldova;Chişinău;779300;25.5%;2019
Croatia;Zagreb;769944;19.0%;2021
Gabon;Libreville;703904;30.1%;2013
Norway;Oslo;697010;12.9%;2021
Macau;Macau;671900;97.9%;2022
United States;Washington D.C.;670050;0.2%;2021
Jamaica;Kingston;662491;23.4%;2019
Finland;Helsinki;658864;11.9%;2021
Tunisia;Tunis;638845;5.2%;2014
Denmark;Copenhagen;638117;10.9%;2021
Greece;Athens;637798;6.1%;2021
Latvia;Riga;605802;32.3%;2021
Djibouti;Djibouti (city);604013;54.6%;2012
Ireland;Dublin;588233;11.8%;2022
Morocco;Rabat;577827;1.6%;2014
Lithuania;Vilnius;576195;20.7%;2022
El Salvador;San Salvador;570459;9.0%;2019
Albania;Tirana;557422;19.5%;2011
North Macedonia;Skopje;544086;25.9%;2015
South Sudan;Juba;525953;4.9%;2017
Paraguay;Asunción;521559;7.8%;2020
Portugal;Lisbon;509614;5.0%;2020
Guinea-Bissau;Bissau;492004;23.9%;2015
Slovakia;Bratislava;440948;8.1%;2020
Estonia;Tallinn;438341;33.0%;2021
Australia;Canberra;431380;1.7%;2020
Namibia;Windhoek;431000;17.0%;2020
Tanzania;Dodoma;410956;0.6%;2012
Papua New Guinea;Port Moresby;364145;3.7%;2011
Ivory Coast;Yamoussoukro;361893;1.3%;2020
Lebanon;Beirut;361366;6.5%;2014
Bolivia;Sucre;360544;3.0%;2022
Puerto Rico (US);San Juan;342259;10.5%;2020
Costa Rica;San José;342188;6.6%;2018
Lesotho;Maseru;330760;14.5%;2016
Cyprus;Nicosia;326739;26.3%;2016
Equatorial Guinea;Malabo;297000;18.2%;2018
Slovenia;Ljubljana;285604;13.5%;2021
East Timor;Dili;277279;21.0%;2015
Bosnia and Herzegovina;Sarajevo;275524;8.4%;2013
Bahamas;Nassau;274400;67.3%;2016
Botswana;Gaborone;273602;10.6%;2020
Benin;Porto-Novo;264320;2.0%;2013
Suriname;Paramaribo;240924;39.3%;2012
India;New Delhi;249998;0.0%;2011
Sahrawi Arab Democratic Republic;Laayoune (claimed) - Tifariti (de facto);217732 - 3000;—;2014
New Zealand;Wellington;217000;4.2%;2021
Bahrain;Manama;200000;13.7%;2020
Kosovo;Pristina;198897;12.0%;2011
Montenegro;Podgorica;190488;30.3%;2020
Belgium;Brussels;187686;1.6%;2022
Cape Verde;Praia;159050;27.1%;2017
Mauritius;Port Louis;147066;11.3%;2018
Curaçao (Netherlands);Willemstad;136660;71.8%;2011
Burundi;Gitega;135467;1.1%;2020
Switzerland;Bern (de facto);134591;1.5%;2020
Transnistria;Tiraspol;133807;38.5%;2015
Maldives;Malé;133412;25.6%;2014
Iceland;Reykjavík;133262;36.0%;2021
Luxembourg;Luxembourg City;124509;19.5%;2021
Guyana;Georgetown;118363;14.7%;2012
Bhutan;Thimphu;114551;14.7%;2017
Comoros;Moroni;111326;13.5%;2016
Barbados;Bridgetown;110000;39.1%;2014
Sri Lanka;Sri Jayawardenepura Kotte;107925;0.5%;2012
Brunei;Bandar Seri Begawan;100700;22.6%;2007
Eswatini;Mbabane;94874;8.0%;2010
New Caledonia (France);Nouméa;94285;32.8%;2019
Fiji;Suva;93970;10.2%;2017
Solomon Islands;Honiara;92344;13.0%;2021
Republic of Artsakh;Stepanakert;75000;62.5%;2021
Gambia;Banjul;73000;2.8%;2013
São Tomé and Príncipe;São Tomé;71868;32.2%;2015
Kiribati;Tarawa;70480;54.7%;2020
Vanuatu;Port Vila;51437;16.1%;2016
Northern Mariana Islands (USA);Saipan;47565;96.1%;2017
Samoa;Apia;41611;19.0%;2021
Palestine;Ramallah (de facto);38998;0.8%;2017
Monaco;Monaco;38350;104.5%;2020
Jersey (UK);Saint Helier;37540;34.2%;2018
Trinidad and Tobago;Port of Spain;37074;2.4%;2011
Cayman Islands (UK);George Town;34399;50.5%;2021
Gibraltar (UK);Gibraltar;34003;104.1%;2020
Grenada;St. George's;33734;27.1%;2012
Aruba (Netherlands);Oranjestad;28294;26.6%;2010
Isle of Man (UK);Douglas;27938;33.2%;2011
Marshall Islands;Majuro;27797;66.1%;2011
Tonga;Nukuʻalofa;27600;26.0%;2022
Seychelles;Victoria;26450;24.8%;2010
French Polynesia (France);Papeete;26926;8.9%;2017
Andorra;Andorra la Vella;22873;28.9%;2022
Faroe Islands (Denmark);Tórshavn;22738;43.0%;2022
Antigua and Barbuda;St. John's;22219;23.8%;2011
Belize;Belmopan;20621;5.2%;2016
Saint Lucia;Castries;20000;11.1%;2013
Guernsey (UK);Saint Peter Port;18958;30.1%;2019
Greenland (Denmark);Nuuk;18800;33.4%;2021
Dominica;Roseau;14725;20.3%;2011
Saint Kitts and Nevis;Basseterre;14000;29.4%;2018
Saint Vincent and the Grenadines;Kingstown;12909;12.4%;2012
British Virgin Islands (UK);Road Town;12603;40.5%;2012
Åland (Finland);Mariehamn;11736;39.0%;2021
U.S. Virgin Islands (US);Charlotte Amalie;14477;14.5%;2020
Micronesia;Palikir;6647;5.9%;2010
Tuvalu;Funafuti;6320;56.4%;2017
Malta;Valletta;5827;1.1%;2019
Liechtenstein;Vaduz;5774;14.8%;2021
Saint Pierre and Miquelon (France);Saint-Pierre;5394;91.7%;2019
Cook Islands (NZ);Avarua;4906;28.9%;2016
San Marino;City of San Marino;4061;12.0%;2021
Turks and Caicos Islands (UK);Cockburn Town;3720;8.2%;2016
American Samoa (USA);Pago Pago;3656;8.1%;2010
Saint Martin (France);Marigot;3229;10.1%;2017
Saint Barthélemy (France);Gustavia;2615;24.1%;2010
Falkland Islands (UK);Stanley;2460;65.4%;2016
Svalbard (Norway);Longyearbyen;2417;82.2%;2020
Sint Maarten (Netherlands);Philipsburg;1894;4.3%;2011
Christmas Island (Australia);Flying Fish Cove;1599;86.8%;2016
Anguilla (UK);The Valley;1067;6.8%;2011
Guam (US);Hagåtña;1051;0.6%;2010
Wallis and Futuna (France);Mata Utu;1029;8.9%;2018
Bermuda (UK);Hamilton;854;1.3%;2016
Nauru;Yaren (de facto);747;6.0%;2011
Saint Helena (UK);Jamestown;629;11.6%;2016
Niue (NZ);Alofi;597;30.8%;2017
Tokelau (NZ);Atafu;541;29.3%;2016
Vatican City;Vatican City (city-state);453;100%;2019
Montserrat (UK);Brades (de facto) - Plymouth (de jure);449 - 0;-;2011
Norfolk Island (Australia);Kingston;341;-;2015
Palau;Ngerulmud;271;1.5%;2010
Cocos (Keeling) Islands (Australia);West Island;134;24.6%;2011
Pitcairn Islands (UK);Adamstown;40;100.0%;2021
South Georgia and the South Sandwich Islands (UK);King Edward Point;22;73.3%;2018"""
# codespell:ignore-end

# -------------------------------------------------------------------
# HTML template for the report. We define no table header <th> items
# because this is done in post processing.
# The actual template part is the table row, identified by id "row".
# The content of each cell will be filled using the respective id.
# -------------------------------------------------------------------
HTML = """
    <h1 style="text-align:center">World Capital Cities</h1>
    <p><i>Percent "%" is city population as a percentage of the country, as of "Year".</i>
    </p><p></p>
    <table>
    <tr id="row">
        <td id="country"></td>
        <td id="capital"></td>
        <td id="population"></td>
        <td id="percent"></td>
        <td id="year"></td>
    </tr>
    </table>
"""

# -------------------------------------------------------------------
# Sets font-family globally to sans-serif, and text-align to right
# for the numerical table columns.
# -------------------------------------------------------------------
CSS = """
body {
    font-family: sans-serif;
}
td[id="population"], td[id="percent"], td[id="year"] {
    text-align: right;
    padding-right: 2px;
}"""

# -------------------------------------------------------------------
# recorder function for cell positions
# -------------------------------------------------------------------
coords = {}  # stores cell gridline coordinates

def recorder(elpos):
    """We only record positions of table rows and cells.

    Information is stored in "coords" with page number as key.
    """
    global coords  # dictionary of row and cell coordinates per page
    if elpos.open_close != 2:  # only consider coordinates provided at "close"
        return
    if elpos.id not in ("row", "country", "capital", "population", "percent", "year"):
        return  # only look at row / cell content

    rect = pymupdf.Rect(elpos.rect)  # cell rectangle
    if rect.y1 > elpos.filled:  # ignore stuff below the filled rectangle
        return

    # per page, we store the floats top-most y, right-most x, column left
    # and row bottom borders.
    x, y, x1, y0 = coords.get(elpos.page, (set(), set(), 0, sys.maxsize))

    if elpos.id != "row":
        x.add(rect.x0)  # add cell left border coordinate
        if rect.x1 > x1:  # store right-most cell border on page
            x1 = rect.x1
    else:
        y.add(rect.y1)  # add row bottom border coordinate
        if rect.y0 < y0:  # store top-most cell border per page
            y0 = rect.y0

    coords[elpos.page] = (x, y, x1, y0)  # write back info per page
    return

# -------------------------------------------------------------------
# define database access: make an intermediate memory database for
# our demo purposes.
# -------------------------------------------------------------------
dbfilename = ":memory:"  # the SQLITE database file name
database = sqlite3.connect(dbfilename)  # open database
cursor = database.cursor()  # multi-purpose database cursor

# Define and fill the SQLITE database
cursor.execute(
    """CREATE TABLE capitals (Country text, Capital text, Population text, Percent text, Year text)"""
)

for value in table_data.splitlines():
    cursor.execute("INSERT INTO capitals VALUES (?,?,?,?,?)", value.split(";"))

# select statement for the rows - let SQL also sort it for us
select = """SELECT * FROM capitals ORDER BY "Country" """

# -------------------------------------------------------------------
# define the HTML Story and fill it with database data
# -------------------------------------------------------------------
story = pymupdf.Story(HTML, user_css=CSS)
body = story.body  # access the HTML body detail

template = body.find(None, "id", "row")  # find the template part
table = body.find("table", None, None)  # find start of table

# read the rows from the database and put them all in one Python list
# NOTE: instead, we might fetch rows one by one (advisable for large volumes)

cursor.execute(select)  # execute cursor, and ...
rows = cursor.fetchall()  # read out what was found
database.close()  # no longer needed

for country, capital, population, percent, year in rows:  # iterate through the row
    row = template.clone()  # clone the template to report each row
    row.find(None, "id", "country").add_text(country)
    row.find(None, "id", "capital").add_text(capital)
    row.find(None, "id", "population").add_text(population)
    row.find(None, "id", "percent").add_text(percent)
    row.find(None, "id", "year").add_text(year)

    table.append_child(row)

template.remove()  # remove the template

# -------------------------------------------------------------------
# generate the PDF and write it to memory
# -------------------------------------------------------------------
fp = io.BytesIO()
writer = pymupdf.DocumentWriter(fp)
mediabox = pymupdf.paper_rect("letter")  # use pages in Letter format
where = mediabox + (36, 36, -36, -72)  # leave page borders
more = True
page = 0
while more:
    dev = writer.begin_page(mediabox)  # make a new page
    if page > 0:  # leave room above the cells for inserting header row
        delta = (0, 20, 0, 0)
    else:
        delta = (0, 0, 0, 0)
    more, filled = story.place(where + delta)  # arrange content on this rectangle
    story.element_positions(recorder, {"page": page, "filled": where.y1})
    story.draw(dev)  # write content to page
    writer.end_page()  # finish the page
    page += 1
writer.close()  # close the PDF

# -------------------------------------------------------------------
# re-open memory PDF for inserting gridlines and header rows
# -------------------------------------------------------------------
doc = pymupdf.open("pdf", fp)
for page in doc:
    page.wrap_contents()  # ensure all "cm" commands are properly wrapped
    x, y, x1, y0 = coords[page.number]  # read coordinates of the page
    x = sorted(list(x)) + [x1]  # list of cell left-right borders
    y = [y0] + sorted(list(y))  # list of cell top-bottom borders
    shape = page.new_shape()  # make a canvas to draw upon

    for item in y:  # draw horizontal lines (one under each row)
        shape.draw_line((x[0] - 2, item), (x[-1] + 2, item))

    for i in range(len(y)):  # alternating row coloring
        if i % 2:
            rect = (x[0] - 2, y[i - 1], x[-1] + 2, y[i])
            shape.draw_rect(rect)

    for i in range(len(x)):  # draw vertical lines
        d = 2 if i == len(x) - 1 else -2
        shape.draw_line((x[i] + d, y[0]), (x[i] + d, y[-1]))

    # Write header row above table content
    y0 -= 5  # bottom coord for header row text
    shape.insert_text((x[0], y0), "Country", fontname="hebo", fontsize=12)
    shape.insert_text((x[1], y0), "Capital", fontname="hebo", fontsize=12)
    shape.insert_text((x[2], y0), "Population", fontname="hebo", fontsize=12)
    shape.insert_text((x[3], y0), "  %", fontname="hebo", fontsize=12)
    shape.insert_text((x[4], y0), "Year", fontname="hebo", fontsize=12)

    # Write page footer
    y0 = page.rect.height - 50  # top coordinate of footer bbox
    bbox = pymupdf.Rect(0, y0, page.rect.width, y0 + 20)  # footer bbox
    page.insert_textbox(
        bbox,
        f"World Capital Cities, Page {page.number+1} of {doc.page_count}",
        align=pymupdf.TEXT_ALIGN_CENTER,
    )
    shape.finish(width=0.3, color=0.5, fill=0.9)  # rectangles and gray lines
    shape.commit(overlay=False)  # put the drawings in background

doc.subset_fonts()
doc.save(__file__.replace(".py", ".pdf"), deflate=True, garbage=4, pretty=True)
doc.close()
```

---

## How to Create a Simple Grid Layout

By creating a sequence of [Story](story-class.html#story) objects within a grid created via the [make\_table](functions.html#functions-make-table) function a developer can create grid layouts as required.

**Files:**

- `docs/samples/simple-grid.py`

See recipe

```
import pymupdf

MEDIABOX = pymupdf.paper_rect("letter")  # output page format: Letter
GRIDSPACE = pymupdf.Rect(100, 100, 400, 400)
GRID = pymupdf.make_table(GRIDSPACE, rows=2, cols=2)
CELLS = [GRID[i][j] for i in range(2) for j in range(2)]
text_table = ("A", "B", "C", "D")
writer = pymupdf.DocumentWriter(__file__.replace(".py", ".pdf"))  # create the writer

device = writer.begin_page(MEDIABOX)  # make new page
for i, text in enumerate(text_table):
    story = pymupdf.Story(em=1)
    body = story.body
    with body.add_paragraph() as para:
        para.set_bgcolor("#ecc")
        para.set_pagebreak_after()  # fills whole cell with bgcolor
        para.set_align("center")
        para.set_fontsize(16)
        para.add_text(f"\n\n\n{text}")
    story.place(CELLS[i])
    story.draw(device)
    del story

writer.end_page()  # finish page

writer.close()  # close output file
```

---

## How to Generate a Table of Contents

This script lists the source code of all Python scripts that live in the script’s directory.

**Files:**

- `docs/samples/code-printer.py`

See recipe

```
"""
Demo script PyMuPDF Story class
-------------------------------

Read the Python sources in the script directory and create a PDF of all their
source codes.

The following features are included as a specialty:
1. HTML source for pymupdf.Story created via Python API exclusively
2. Separate Story objects for page headers and footers
3. Use of HTML "id" elements for identifying source start pages
4. Generate a Table of Contents pointing to source file starts. This
   - uses the new Stoy callback feature
   - uses Story also for making the TOC page(s)

"""
import io
import os
import time

import pymupdf

THISDIR = os.path.dirname(os.path.abspath(__file__))
TOC = []  # this will contain the TOC list items
CURRENT_ID = ""  # currently processed filename - stored by recorder func
MEDIABOX = pymupdf.paper_rect("a4-l")  # chosen page size
WHERE = MEDIABOX + (36, 50, -36, -36)  # sub rectangle for source content
# location of the header rectangle
HDR_WHERE = (36, 5, MEDIABOX.width - 36, 40)
# location of the footer rectangle
FTR_WHERE = (36, MEDIABOX.height - 36, MEDIABOX.width - 36, MEDIABOX.height)

def recorder(elpos):
    """Callback function invoked during story.place().
    This function generates / collects all TOC items and updates the value of
    CURRENT_ID - which is used to update the footer line of each page.
    """
    global TOC, CURRENT_ID
    if not elpos.open_close & 1:  # only consider "open" items
        return
    level = elpos.heading
    y0 = elpos.rect[1]  # top of written rectangle (use for TOC)
    if level > 0:  # this is a header (h1 - h6)
        pno = elpos.page + 1  # the page number
        TOC.append(
            (
                level,
                elpos.text,
                elpos.page + 1,
                y0,
            )
        )
        return

    CURRENT_ID = elpos.id if elpos.id else ""  # update for footer line
    return

def header_story(text):
    """Make the page header"""
    header = pymupdf.Story()
    hdr_body = header.body
    hdr_body.add_paragraph().set_properties(
        align=pymupdf.TEXT_ALIGN_CENTER,
        bgcolor="#eee",
        font="sans-serif",
        bold=True,
        fontsize=12,
        color="green",
    ).add_text(text)
    return header

def footer_story(text):
    """Make the page footer"""
    footer = pymupdf.Story()
    ftr_body = footer.body
    ftr_body.add_paragraph().set_properties(
        bgcolor="#eee",
        align=pymupdf.TEXT_ALIGN_CENTER,
        color="blue",
        fontsize=10,
        font="sans-serif",
    ).add_text(text)
    return footer

def code_printer(outfile):
    """Output the generated PDF to outfile."""
    global MAX_TITLE_LEN
    where = +WHERE
    writer = pymupdf.DocumentWriter(outfile, "")
    print_time = time.strftime("%Y-%m-%d %H:%M:%S (%z)")
    thispath = os.path.abspath(os.curdir)
    basename = os.path.basename(thispath)

    story = pymupdf.Story()
    body = story.body
    body.set_properties(font="sans-serif")

    text = f"Python sources in folder '{THISDIR}'"

    body.add_header(1).add_text(text)  # the only h1 item in the story

    files = os.listdir(THISDIR)  # list / select Python files in our directory
    i = 1
    for code_file in files:
        if not code_file.endswith(".py"):
            continue

        # read Python file source
        fileinput = open(os.path.join(THISDIR, code_file), "rb")
        text = fileinput.read().decode()
        fileinput.close()

        # make level 2 header
        hdr = body.add_header(2)
        if i > 1:
            hdr.set_pagebreak_before()
        hdr.add_text(f"{i}. Listing of file '{code_file}'")

        # Write the file code
        body.add_codeblock().set_bgcolor((240, 255, 210)).set_color("blue").set_id(
            code_file
        ).set_fontsize(10).add_text(text)

        # Indicate end of a source file
        body.add_paragraph().set_align(pymupdf.TEXT_ALIGN_CENTER).add_text(
            f"---------- End of File '{code_file}' ----------"
        )
        i += 1  # update file counter

    i = 0
    while True:
        i += 1
        device = writer.begin_page(MEDIABOX)
        # create Story objects for header, footer and the rest.
        header = header_story(f"Python Files in '{THISDIR}'")
        hdr_ok, _ = header.place(HDR_WHERE)
        if hdr_ok != 0:
            raise ValueError("header does not fit")
        header.draw(device, None)

        # --------------------------------------------------------------
        # Write the file content.
        # --------------------------------------------------------------
        more, filled = story.place(where)
        # Inform the callback function
        # Args:
        #   recorder: the Python function to call
        #   {}: dictionary containing anything - we pass the page number
        story.element_positions(recorder, {"page": i - 1})
        story.draw(device, None)

        # --------------------------------------------------------------
        # Make / write page footer.
        # We MUST have a paragraph b/o background color / alignment
        # --------------------------------------------------------------
        if CURRENT_ID:
            text = f"File '{CURRENT_ID}' printed at {print_time}{chr(160)*5}{'-'*10}{chr(160)*5}Page {i}"
        else:
            text = f"Printed at {print_time}{chr(160)*5}{'-'*10}{chr(160)*5}Page {i}"
        footer = footer_story(text)
        # write the page footer
        ftr_ok, _ = footer.place(FTR_WHERE)
        if ftr_ok != 0:
            raise ValueError("footer does not fit")
        footer.draw(device, None)

        writer.end_page()
        if more == 0:
            break
    writer.close()

if __name__ == "__main__" or os.environ.get('PYTEST_CURRENT_TEST'):
    fileptr1 = io.BytesIO()
    t0 = time.perf_counter()
    code_printer(fileptr1)  # make the PDF
    t1 = time.perf_counter()
    doc = pymupdf.open("pdf", fileptr1)
    old_count = doc.page_count
    # -----------------------------------------------------------------------------
    # Post-processing step to make / insert the toc
    # This also works using pymupdf.Story:
    # - make a new PDF in memory which contains pages with the TOC text
    # - add these TOC pages to the end of the original file
    # - search item text on the inserted pages and cover each with a PDF link
    # - move the TOC pages to the front of the document
    # -----------------------------------------------------------------------------
    story = pymupdf.Story()
    body = story.body
    body.add_header(1).set_font("sans-serif").add_text("Table of Contents")
    # prefix TOC with an entry pointing to this page
    TOC.insert(0, [1, "Table of Contents", old_count + 1, 36])

    for item in TOC[1:]:  # write the file name headers as TOC lines
        body.add_paragraph().set_font("sans-serif").add_text(
            item[1] + f" - ({item[2]})"
        )
    fileptr2 = io.BytesIO()  # put TOC pages to a separate PDF initially
    writer = pymupdf.DocumentWriter(fileptr2)
    i = 1
    more = 1
    while more:
        device = writer.begin_page(MEDIABOX)
        header = header_story(f"Python Files in '{THISDIR}'")
        # write the page header
        hdr_ok, _ = header.place(HDR_WHERE)
        header.draw(device, None)

        more, filled = story.place(WHERE)
        story.draw(device, None)

        footer = footer_story(f"TOC-{i}")  # separate page numbering scheme
        # write the page footer
        ftr_ok, _ = footer.place(FTR_WHERE)
        footer.draw(device, None)
        writer.end_page()
        i += 1

    writer.close()
    doc2 = pymupdf.open("pdf", fileptr2)  # open TOC pages as another PDF
    doc.insert_pdf(doc2)  # and append to the main PDF
    new_range = range(old_count, doc.page_count)  # the TOC page numbers
    pages = [doc[i] for i in new_range]  # these are the TOC pages within main PDF
    for item in TOC:  # search for TOC item text to get its rectangle
        for page in pages:
            rl = page.search_for(item[1], flags=pymupdf.TEXTFLAGS_SEARCH)
            if rl != []:  # this text must be on next page
                break
        else:
            assert 0, f'Cannot find {item[1]=} in {len(pages)=}.'
        rect = rl[0]  # rectangle of TOC item text
        link = {  # make a link from it
            "kind": pymupdf.LINK_GOTO,
            "from": rect,
            "to": pymupdf.Point(0, item[3]),
            "page": item[2] - 1,
        }
        page.insert_link(link)

    # insert the TOC in the main PDF
    doc.set_toc(TOC)
    # move all the TOC pages to the desired place (1st page here)
    for i in new_range:
        doc.move_page(doc.page_count - 1, 0)
    doc.ez_save(__file__.replace(".py", ".pdf"))
```

It features the following capabilities:

- Automatic generation of a Table of Contents (TOC) on separately numbered pages at the start of the document - using a specialized [Story](story-class.html#story).
- Use of 3 separate [Story](story-class.html#story) objects per page: header story, footer story and the story for printing the Python sources.

  > - The page **footer is automatically changed** to show the name of the current Python file.
- Use of [`Story.element_positions()`](story-class.html#Story.element_positions "Story.element_positions") to collect the data for the TOC and for the dynamic adjustment of page footers. This is an example of a **bidirectional communication** between the story output process and the script.
- The main PDF with the Python sources is being written to memory by its [DocumentWriter](document-writer-class.html#documentwriter). Another [Story](story-class.html#story) / [DocumentWriter](document-writer-class.html#documentwriter) pair is then used to create a (memory) PDF for the TOC pages. Finally, both these PDFs are joined and the result stored to disk.

---

## How to Display a List from JSON Data

This example takes some JSON data input which it uses to populate a [Story](story-class.html#story). It also contains some visual text formatting and shows how to add links.

**Files:**

- `docs/samples/json-example.py`

See recipe

```
import pymupdf
import json

my_json =  """
[
    {
         "name" :           "Five-storied Pagoda",
         "temple" :         "Rurikō-ji",
         "founded" :        "middle Muromachi period, 1442",
         "region" :         "Yamaguchi, Yamaguchi",
         "position" :       "34.190181,131.472917"
     },
     {
         "name" :           "Founder's Hall",
         "temple" :         "Eihō-ji",
         "founded" :        "early Muromachi period",
         "region" :         "Tajimi, Gifu",
         "position" :       "35.346144,137.129189"
     },
     {
         "name" :           "Fudōdō",
         "temple" :         "Kongōbu-ji",
         "founded" :        "early Kamakura period",
         "region" :         "Kōya, Wakayama",
         "position" :       "34.213103,135.580397"
     },
     {
         "name" :           "Goeidō",
         "temple" :         "Nishi Honganji",
         "founded" :        "Edo period, 1636",
         "region" :         "Kyoto",
         "position" :       "34.991394,135.751689"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Murō-ji",
         "founded" :        "early Heian period",
         "region" :         "Uda, Nara",
         "position" :       "34.536586819357986,136.0395548452301"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Fudō-in",
         "founded" :        "late Muromachi period, 1540",
         "region" :         "Hiroshima",
         "position" :       "34.427014,132.471117"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Ninna-ji",
         "founded" :        "Momoyama period, 1613",
         "region" :         "Kyoto",
         "position" :       "35.031078,135.713811"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Mii-dera",
         "founded" :        "Momoyama period, 1599",
         "region" :         "Ōtsu, Shiga",
         "position" :       "35.013403,135.852861"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Tōshōdai-ji",
         "founded" :        "Nara period, 8th century",
         "region" :         "Nara, Nara",
         "position" :       "34.675619,135.784842"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Tō-ji",
         "founded" :        "Momoyama period, 1603",
         "region" :         "Kyoto",
         "position" :       "34.980367,135.747686"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Tōdai-ji",
         "founded" :        "middle Edo period, 1705",
         "region" :         "Nara, Nara",
         "position" :       "34.688992,135.839822"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Hōryū-ji",
         "founded" :        "Asuka period, by 693",
         "region" :         "Ikaruga, Nara",
         "position" :       "34.614317,135.734458"
     },
     {
         "name" :           "Golden Hall",
         "temple" :         "Daigo-ji",
         "founded" :        "late Heian period",
         "region" :         "Kyoto",
         "position" :       "34.951481,135.821747"
     },
     {
         "name" :           "Keigū-in Main Hall",
         "temple" :         "Kōryū-ji",
         "founded" :        "early Kamakura period, before 1251",
         "region" :         "Kyoto",
         "position" :       "35.015028,135.705425"
     },
     {
         "name" :           "Konpon-chūdō",
         "temple" :         "Enryaku-ji",
         "founded" :        "early Edo period, 1640",
         "region" :         "Ōtsu, Shiga",
         "position" :       "35.070456,135.840942"
     },
     {
         "name" :           "Korō",
         "temple" :         "Tōshōdai-ji",
         "founded" :        "early Kamakura period, 1240",
         "region" :         "Nara, Nara",
         "position" :       "34.675847,135.785069"
     },
     {
         "name" :           "Kōfūzō",
         "temple" :         "Hōryū-ji",
         "founded" :        "early Heian period",
         "region" :         "Ikaruga, Nara",
         "position" :       "34.614439,135.735428"
     },
     {
         "name" :           "Large Lecture Hall",
         "temple" :         "Hōryū-ji",
         "founded" :        "middle Heian period, 990",
         "region" :         "Ikaruga, Nara",
         "position" :       "34.614783,135.734175"
     },
     {
         "name" :           "Lecture Hall",
         "temple" :         "Zuiryū-ji",
         "founded" :        "early Edo period, 1655",
         "region" :         "Takaoka, Toyama",
         "position" :       "36.735689,137.010019"
     },
     {
         "name" :           "Lecture Hall",
         "temple" :         "Tōshōdai-ji",
         "founded" :        "Nara period, 763",
         "region" :         "Nara, Nara",
         "position" :       "34.675933,135.784842"
     },
     {
         "name" :           "Lotus Flower Gate",
         "temple" :         "Tō-ji",
         "founded" :        "early Kamakura period",
         "region" :         "Kyoto",
         "position" :       "34.980678,135.746314"
     },
     {
         "name" :           "Main Hall",
         "temple" :         "Akishinodera",
         "founded" :        "early Kamakura period",
         "region" :         "Nara, Nara",
         "position" :       "34.703769,135.776189"
     }
]

"""

# the result is a Python dictionary:
my_dict = json.loads(my_json)

MEDIABOX = pymupdf.paper_rect("letter")  # output page format: Letter
WHERE = MEDIABOX + (36, 36, -36, -36)
writer = pymupdf.DocumentWriter("json-example.pdf")  # create the writer

story = pymupdf.Story()
body = story.body

for i, entry in enumerate(my_dict):

    for attribute, value in entry.items():
        para = body.add_paragraph()

        if attribute == "position":
            para.set_fontsize(10)
            para.add_link(f"www.google.com/maps/@{value},14z")
        else:
            para.add_span()
            para.set_color("#990000")
            para.set_fontsize(14)
            para.set_bold()
            para.add_text(f"{attribute} ")
            para.add_span()
            para.set_fontsize(18)
            para.add_text(f"{value}")

    body.add_horizontal_line()

# This while condition will check a value from the Story `place` method
# for whether all content for the story has been written (0), otherwise
# more content is waiting to be written (1)
more = 1
while more:
    device = writer.begin_page(MEDIABOX)  # make new page
    more, _ = story.place(WHERE)
    story.draw(device)
    writer.end_page()  # finish page

writer.close()  # close output file

del story
```

---

## Using the Alternative `Story.write*()` functions

The `Story.write*()` functions provide a different way to use the
[Story](story-class.html#story) functionality, removing the need for calling code to implement
a loop that calls [`Story.place()`](story-class.html#Story.place "Story.place") and [`Story.draw()`](story-class.html#Story.draw "Story.draw") etc, at the
expense of having to provide at least a `rectfn()` callback.

### How to do Basic Layout with [`Story.write()`](story-class.html#Story.write "Story.write")

This script lays out multiple copies of its own source code, into four
rectangles per page.

**Files:**

- `docs/samples/story-write.py`

See recipe

```
"""
Demo script for PyMuPDF's `Story.write()` method.

This is a way of laying out a story into a PDF document, that avoids the need
to write a loop that calls `story.place()` and `story.draw()`.

Instead just a single function call is required, albeit with a `rectfn()`
callback that returns the rectangles into which the story is placed.
"""

import html

import pymupdf

# Create html containing multiple copies of our own source code.
#
with open(__file__) as f:
    text = f.read()
text = html.escape(text)
html = f'''
<!DOCTYPE html>
<body>

<h1>Contents of {__file__}</h1>

<h2>Normal</h2>
<pre>
{text}
</pre>

<h2>Strong</h2>
<strong>
<pre>
{text}
</pre>
</strong>

<h2>Em</h2>
<em>
<pre>
{text}
</pre>
</em>

</body>
'''

def rectfn(rect_num, filled):
    '''
    We return four rectangles per page in this order:
    
        1 3
        2 4
    '''
    page_w = 800
    page_h = 600
    margin = 50
    rect_w = (page_w - 3*margin) / 2
    rect_h = (page_h - 3*margin) / 2
    
    if rect_num % 4 == 0:
        # New page.
        mediabox = pymupdf.Rect(0, 0, page_w, page_h)
    else:
        mediabox = None
    # Return one of four rects in turn.
    rect_x = margin + (rect_w+margin) * ((rect_num // 2) % 2)
    rect_y = margin + (rect_h+margin) * (rect_num % 2)
    rect = pymupdf.Rect(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)
    #print(f'rectfn(): rect_num={rect_num} filled={filled}. Returning: rect={rect}')
    return mediabox, rect, None

story = pymupdf.Story(html, em=8)

out_path = __file__.replace('.py', '.pdf')
writer = pymupdf.DocumentWriter(out_path)

story.write(writer, rectfn)
writer.close()
```

---

### How to do Iterative Layout for a Table of Contents with [`Story.write_stabilized()`](story-class.html#Story.write_stabilized "Story.write_stabilized")

This script creates html content dynamically, adding a contents section based
on ElementPosition items that have non-zero `.heading` values.

The contents section is at the start of the document, so modifications to the
contents can change page numbers in the rest of the document, which in turn can
cause page numbers in the contents section to be incorrect.

So the script uses [`Story.write_stabilized()`](story-class.html#Story.write_stabilized "Story.write_stabilized") to repeatedly lay things
out until things are stable.

**Files:**

- `docs/samples/story-write-stabilized.py`

See recipe

```
"""
Demo script for PyMuPDF's `pymupdf.Story.write_stabilized()`.

`pymupdf.Story.write_stabilized()` is similar to `pymupdf.Story.write()`,
except instead of taking a fixed html document, it does iterative layout
of dynamically-generated html content (provided by a callback) to a
`pymupdf.DocumentWriter`.

For example this allows one to add a dynamically-generated table of contents
section while ensuring that page numbers are patched up until stable.
"""

import textwrap

import pymupdf

def rectfn(rect_num, filled):
    '''
    We return one rect per page.
    '''
    rect = pymupdf.Rect(10, 20, 290, 380)
    mediabox = pymupdf.Rect(0, 0, 300, 400)
    #print(f'rectfn(): rect_num={rect_num} filled={filled}')
    return mediabox, rect, None

def contentfn(positions):
    '''
    Returns html content, with a table of contents derived from `positions`.
    '''
    ret = ''
    ret += textwrap.dedent('''
            <!DOCTYPE html>
            <body>
            <h2>Contents</h2>
            <ul>
            ''')
    
    # Create table of contents with links to all <h1..6> sections in the
    # document.
    for position in positions:
        if position.heading and (position.open_close & 1):
            text = position.text if position.text else ''
            if position.id:
                ret += f"    <li><a href=\"#{position.id}\">{text}</a>\n"
            else:
                ret += f"    <li>{text}\n"
            ret += f"        <ul>\n"
            ret += f"        <li>page={position.page_num}\n"
            ret += f"        <li>depth={position.depth}\n"
            ret += f"        <li>heading={position.heading}\n"
            ret += f"        <li>id={position.id!r}\n"
            ret += f"        <li>href={position.href!r}\n"
            ret += f"        <li>rect={position.rect}\n"
            ret += f"        <li>text={text!r}\n"
            ret += f"        <li>open_close={position.open_close}\n"
            ret += f"        </ul>\n"
    
    ret += '</ul>\n'
    
    # Main content.
    ret += textwrap.dedent(f'''
    
            <h1>First section</h1>
            <p>Contents of first section.
            
            <h1>Second section</h1>
            <p>Contents of second section.
            <h2>Second section first subsection</h2>
            
            <p>Contents of second section first subsection.
            
            <h1>Third section</h1>
            <p>Contents of third section.
            
            </body>
            ''')
    ret = ret.strip()
    with open(__file__.replace('.py', '.html'), 'w') as f:
        f.write(ret)
    return ret;

out_path = __file__.replace('.py', '.pdf')
writer = pymupdf.DocumentWriter(out_path)
pymupdf.Story.write_stabilized(writer, contentfn, rectfn)
writer.close()
```

---

### How to do Iterative Layout and Create PDF Links with `Story.write_stabilized_links()`

This script is similar to the one described in “How to use
[`Story.write_stabilized()`](story-class.html#Story.write_stabilized "Story.write_stabilized")” above, except that the generated PDF also
contains links that correspond to the internal links in the original html.

This is done by using `Story.write_stabilized_links()`; this is slightly
different from [`Story.write_stabilized()`](story-class.html#Story.write_stabilized "Story.write_stabilized"):

- It does not take a [DocumentWriter](document-writer-class.html#documentwriter) `writer` arg.
- It returns a PDF [Document](document.html#document) instance.

[The reasons for this are a little involved; for example a
[DocumentWriter](document-writer-class.html#documentwriter) is not necessarily a PDF writer, so doesn’t really work
in a PDF-specific API.]

**Files:**

- `docs/samples/story-write-stabilized-links.py`

See recipe

```
"""
Demo script for PyMuPDF's `pymupdf.Story.write_stabilized_with_links()`.

`pymupdf.Story.write_stabilized_links()` is similar to
`pymupdf.Story.write_stabilized()` except that it creates a PDF `pymupdf.Document`
that contains PDF links generated from all internal links in the original html.
"""

import textwrap

import pymupdf

def rectfn(rect_num, filled):
    '''
    We return one rect per page.
    '''
    rect = pymupdf.Rect(10, 20, 290, 380)
    mediabox = pymupdf.Rect(0, 0, 300, 400)
    #print(f'rectfn(): rect_num={rect_num} filled={filled}')
    return mediabox, rect, None

def contentfn(positions):
    '''
    Returns html content, with a table of contents derived from `positions`.
    '''
    ret = ''
    ret += textwrap.dedent('''
            <!DOCTYPE html>
            <body>
            <h2>Contents</h2>
            <ul>
            ''')
    
    # Create table of contents with links to all <h1..6> sections in the
    # document.
    for position in positions:
        if position.heading and (position.open_close & 1):
            text = position.text if position.text else ''
            if position.id:
                ret += f"    <li><a href=\"#{position.id}\">{text}</a>\n"
            else:
                ret += f"    <li>{text}\n"
            ret += f"        <ul>\n"
            ret += f"        <li>page={position.page_num}\n"
            ret += f"        <li>depth={position.depth}\n"
            ret += f"        <li>heading={position.heading}\n"
            ret += f"        <li>id={position.id!r}\n"
            ret += f"        <li>href={position.href!r}\n"
            ret += f"        <li>rect={position.rect}\n"
            ret += f"        <li>text={text!r}\n"
            ret += f"        <li>open_close={position.open_close}\n"
            ret += f"        </ul>\n"
    
    ret += '</ul>\n'
    
    # Main content.
    ret += textwrap.dedent(f'''
    
            <h1>First section</h1>
            <p>Contents of first section.
            <ul>
            <li>External <a href="https://artifex.com/">link to https://artifex.com/</a>.
            <li><a href="#idtest">Link to IDTEST</a>.
            <li><a href="#nametest">Link to NAMETEST</a>.
            </ul>
            
            <h1>Second section</h1>
            <p>Contents of second section.
            <h2>Second section first subsection</h2>
            
            <p>Contents of second section first subsection.
            <p id="idtest">IDTEST
            
            <h1>Third section</h1>
            <p>Contents of third section.
            <p><a name="nametest">NAMETEST</a>.
            
            </body>
            ''')
    ret = ret.strip()
    with open(__file__.replace('.py', '.html'), 'w') as f:
        f.write(ret)
    return ret;

out_path = __file__.replace('.py', '.pdf')
document = pymupdf.Story.write_stabilized_with_links(contentfn, rectfn)
document.save(out_path)
```

---

Footnotes

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.