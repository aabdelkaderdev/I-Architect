<!-- Source: https://pymupdf.readthedocs.io/en/latest/font.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Font

- New in v1.16.18

This class represents a font as defined in MuPDF (`fz_font_s` structure). It is required for the new class [TextWriter](textwriter.html#textwriter) and the new [`Page.write_text()`](page.html#Page.write_text "Page.write_text"). Currently, it has no connection to how fonts are used in methods [`Page.insert_text()`](page.html#Page.insert_text "Page.insert_text") or [`Page.insert_textbox()`](page.html#Page.insert_textbox "Page.insert_textbox"), respectively.

A `Font` object also contains useful general information, like the font bbox, the number of defined glyphs, glyph names or the `bbox` of a single glyph.

| **Method / Attribute** | **Short Description** |
| --- | --- |
| [`glyph_advance()`](#Font.glyph_advance "Font.glyph_advance") | Width of a character |
| [`glyph_bbox()`](#Font.glyph_bbox "Font.glyph_bbox") | Glyph rectangle |
| [`glyph_name_to_unicode()`](#Font.glyph_name_to_unicode "Font.glyph_name_to_unicode") | Get unicode from glyph name |
| [`has_glyph()`](#Font.has_glyph "Font.has_glyph") | Return glyph id of unicode |
| [`text_length()`](#Font.text_length "Font.text_length") | Compute string length |
| [`char_lengths()`](#Font.char_lengths "Font.char_lengths") | Tuple of char widths of a string |
| [`unicode_to_glyph_name()`](#Font.unicode_to_glyph_name "Font.unicode_to_glyph_name") | Get glyph name of a unicode |
| [`valid_codepoints()`](#Font.valid_codepoints "Font.valid_codepoints") | Array of supported unicodes |
| [`ascender`](#Font.ascender "Font.ascender") | Font ascender |
| [`descender`](#Font.descender "Font.descender") | Font descender |
| [`bbox`](#Font.bbox "Font.bbox") | Font rectangle |
| [`buffer`](#Font.buffer "Font.buffer") | Copy of the font’s binary image |
| [`flags`](#Font.flags "Font.flags") | Collection of font properties |
| [`glyph_count`](#Font.glyph_count "Font.glyph_count") | Number of supported glyphs |
| [`name`](#Font.name "Font.name") | Name of font |
| [`is_bold`](#Font.is_bold "Font.is_bold") | `True` if bold |
| [`is_monospaced`](#Font.is_monospaced "Font.is_monospaced") | `True` if mono-spaced |
| [`is_serif`](#Font.is_serif "Font.is_serif") | `True` if serif, `False` if sans-serif |
| [`is_italic`](#Font.is_italic "Font.is_italic") | `True` if italic |

**Class API**

*class* Font
:   \_\_init\_\_(self, fontname=None, fontfile=None,

    fontbuffer=None, script=0, language=None, ordering=-1, is\_bold=0,

    is\_italic=0, is\_serif=0)
    :   Font constructor. The large number of parameters are used to locate font, which most closely resembles the requirements. Not all parameters are ever required – see the below pseudo code explaining the logic how the parameters are evaluated.

        Parameters:
        :   - **fontname** (*str*) –

              one of the [PDF Base 14 Fonts](app3.html#base-14-fonts) or CJK fontnames. Also possible are a select few other names like (watch the correct spelling): “Arial”, “Times”, “Times Roman”.

              *(Changed in v1.17.5)*

              If you have installed [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/), there are also new “reserved” fontnames available, which are listed in `fitz_fonts` and in the table further down.
            - **fontfile** (*str*) – the filename of a fontfile somewhere on your system [[1]](#f1).
            - **fontbuffer** (*bytes**,**bytearray**,**io.BytesIO*) – a fontfile loaded in memory [[1]](#f1).
            - **script** (*in*) – the number of a UCDN script. Currently supported in PyMuPDF are numbers 24, and 32 through 35.
            - **language** (*str*) – one of the values “zh-Hant” (traditional Chinese), “zh-Hans” (simplified Chinese), “ja” (Japanese) and “ko” (Korean). Otherwise, all ISO 639 codes from the subsets 1, 2, 3 and 5 are also possible, but are currently documentary only.
            - **ordering** (*int*) – an alternative selector for one of the CJK fonts.
            - **is\_bold** (*bool*) – look for a bold font.
            - **is\_italic** (*bool*) – look for an italic font.
            - **is\_serif** (*bool*) – look for a serifed font.

        Returns:
        :   a MuPDF font if successful. This is the overall sequence of checks to determine an appropriate font:

            | Argument | Action |
            | --- | --- |
            | fontfile? | Create font from file, exception if failure. |
            | fontbuffer? | Create font from buffer, exception if failure. |
            | ordering>=0 | Create universal font, always succeeds. |
            | fontname? | Create a Base-14 font, universal font, or font provided by [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/). See table below. |

        Note

        With the usual reserved names “helv”, “tiro”, etc., you will create fonts with the expected names “Helvetica”, “Times-Roman” and so on. **However**, and in contrast to [`Page.insert_font()`](page.html#Page.insert_font "Page.insert_font") and friends,

        > - a font file will **always** be embedded in your PDF,
        > - Greek and Cyrillic characters are supported without needing the *encoding* parameter.

        Using *ordering >= 0*, or fontnames “cjk”, “china-t”, “china-s”, “japan” or “korea” will **always create the same “universal”** font **“Droid Sans Fallback Regular”**. This font supports **all Chinese, Japanese, Korean and Latin characters**, including Greek and Cyrillic. This is a sans-serif font.

        Actually, you would rarely ever need another sans-serif font than **“Droid Sans Fallback Regular”**. **Except** that this font file is relatively large and adds about 1.65 MB (compressed) to your PDF file size. If you do not need CJK support, stick with specifying “helv”, “tiro” etc., and you will get away with about 35 KB compressed.

        If you **know** you have a mixture of CJK and Latin text, consider just using `Font("cjk")` because this supports everything and also significantly (by a factor of up to three) speeds up execution: MuPDF will always find any character in this single font and never needs to check fallbacks.

        But if you do use some other font, you will still automatically be able to also write CJK characters: MuPDF detects this situation and silently falls back to the universal font (which will then of course also be embedded in your PDF).

        *(New in v1.17.5)* Optionally, some new “reserved” fontname codes become available if you install [pymupdf-fonts](https://pypi.org/project/pymupdf-fonts/), `pip install pymupdf-fonts`. **“Fira Mono”** is a mono-spaced sans font set and **FiraGO** is another non-serifed “universal” font set which supports all Latin (including Cyrillic and Greek) plus Thai, Arabian, Hewbrew and Devanagari – but none of the CJK languages. The size of a FiraGO font is only a quarter of the “Droid Sans Fallback” size (compressed 400 KB vs. 1.65 MB) – **and** it provides the weights bold, italic, bold-italic – which the universal font doesn’t.

        **“Space Mono”** is another nice and small mono-spaced font from Google Fonts, which supports Latin Extended characters and comes with all 4 important weights.

        The following table maps a fontname code to the corresponding font. For the current content of the package please see its documentation:

        > | Code | Fontname | New in | Comment |
        > | --- | --- | --- | --- |
        > | figo | FiraGO Regular | v1.0.0 | narrower than Helvetica |
        > | figbo | FiraGO Bold | v1.0.0 |  |
        > | figit | FiraGO Italic | v1.0.0 |  |
        > | figbi | FiraGO Bold Italic | v1.0.0 |  |
        > | fimo | Fira Mono Regular | v1.0.0 |  |
        > | fimbo | Fira Mono Bold | v1.0.0 |  |
        > | spacemo | Space Mono Regular | v1.0.1 |  |
        > | spacembo | Space Mono Bold | v1.0.1 |  |
        > | spacemit | Space Mono Italic | v1.0.1 |  |
        > | spacembi | Space Mono Bold-Italic | v1.0.1 |  |
        > | math | Noto Sans Math Regular | v1.0.2 | math symbols |
        > | music | Noto Music Regular | v1.0.2 | musical symbols |
        > | symbol1 | Noto Sans Symbols Regular | v1.0.2 | replacement for “symb” |
        > | symbol2 | Noto Sans Symbols2 Regular | v1.0.2 | extended symbol set |
        > | notos | Noto Sans Regular | v1.0.3 | alternative to Helvetica |
        > | notosit | Noto Sans Italic | v1.0.3 |  |
        > | notosbo | Noto Sans Bold | v1.0.3 |  |
        > | notosbi | Noto Sans BoldItalic | v1.0.3 |  |

    has\_glyph(*chr*, *language=None*, *script=0*, *fallback=False*)
    :   Check whether the unicode `chr` exists in the font or (option) some fallback font. May be used to check whether any “TOFU” symbols will appear on output.

        Parameters:
        :   - **chr** (*int*) – the unicode of the character (i.e. `ord()`).
            - **language** (*str*) – the language – currently unused.
            - **script** (*int*) – the UCDN script number.
            - **fallback** (*bool*) – *(new in v1.17.5)* perform an extended search in fallback fonts or restrict to current font (default).

        Returns:
        :   *(changed in 1.17.7)* the glyph number. Zero indicates no glyph found.

    valid\_codepoints()
    :   - New in v1.17.5

        Return an array of unicodes supported by this font.

        Returns:
        :   an `array.array` [[2]](#f2) of length at most [`Font.glyph_count`](#Font.glyph_count "Font.glyph_count"). I.e. `chr()` of every item in this array has a glyph in the font without using fallbacks. This is an example display of the supported glyphs:

            ```
            >>> import pymupdf
            >>> font = pymupdf.Font("math")
            >>> vuc = font.valid_codepoints()
            >>> for i in vuc:
            >>>     print(f"{i:04X} {chr(i)} ({font.unicode_to_glyph_name(i)})")
            0000
            000D   (CR)
            0020   (space)
            0021 ! (exclam)
            0022 " (quotedbl)
            0023 # (numbersign)
            0024 $ (dollar)
            0025 % (percent)
            ...
            00AC ¬ (logicalnot)
            00B1 ± (plusminus)
            ...
            21D0 ⇐ (arrowdblleft)
            21D1 ⇑ (arrowdblup)
            21D2 ⇒ (arrowdblright)
            21D3 ⇓ (arrowdbldown)
            21D4 ⇔ (arrowdblboth)
            ...
            221E ∞ (infinity)
            ...
            ```

        Note

        This method only returns meaningful data for fonts having a CMAP (character map, charmap, the `/ToUnicode` PDF key). Otherwise, this array will have length 1 and contain zero only.

    glyph\_advance(*chr*, *language=None*, *script=0*, *wmode=0*)
    :   Calculate the “width” of the character’s glyph (visual representation).

        Parameters:
        :   - **chr** (*int*) – the unicode number of the character. Use `ord()`, not the character itself. Again, this should normally work even if a character is not supported by that font, because fallback fonts will be checked where necessary.
            - **wmode** (*int*) – write mode, `0` = horizontal, `1` = vertical.

        The other parameters are not in use currently.

        Returns:
        :   a float representing the glyph’s width relative to **fontsize 1**.

    glyph\_name\_to\_unicode(*name*)
    :   Return the unicode value for a given glyph name. Use it in conjunction with `chr()` if you want to output e.g. a certain symbol.

        Parameters:
        :   **name** (*str*) – The name of the glyph.

        Returns:
        :   The unicode integer, or 65533 = 0xFFFD if the name is unknown. Examples: `font.glyph_name_to_unicode("Sigma") = 931`, `font.glyph_name_to_unicode("sigma") = 963`. Refer to the [Adobe Glyph List](https://github.com/adobe-type-tools/agl-aglfn/blob/master/glyphlist.txt) publication for a list of glyph names and their unicode numbers. Example:

            ```
            >>> font = pymupdf.Font("helv")
            >>> font.has_glyph(font.glyph_name_to_unicode("infinity"))
            True
            ```

    glyph\_bbox(*chr*, *language=None*, *script=0*)
    :   The glyph rectangle relative to [`fontsize`](glossary.html#fontsize "fontsize") 1.

        Parameters:
        :   **chr** (*int*) – `ord()` of the character.

        Returns:
        :   a [Rect](rect.html#rect).

    unicode\_to\_glyph\_name(*ch*)
    :   Show the name of the character’s glyph.

        Parameters:
        :   **ch** (*int*) – the unicode number of the character. Use `ord()`, not the character itself.

        Returns:
        :   a string representing the glyph’s name. E.g. `font.glyph_name(ord("#")) = "numbersign"`. For an invalid code “.notfound” is returned.

            Note

            *(Changed in v1.18.0)* This method and [`Font.glyph_name_to_unicode()`](#Font.glyph_name_to_unicode "Font.glyph_name_to_unicode") no longer depend on a font and instead retrieve information from the **Adobe Glyph List**. Also available as `pymupdf.unicode_to_glyph_name()` and resp. `pymupdf.glyph_name_to_unicode()`.

    text\_length(*text*, *fontsize=11*)
    :   Calculate the length in points of a unicode string.

        Note

        There is a functional overlap with [`get_text_length()`](functions.html#get_text_length "get_text_length") for Base-14 fonts only.

        Parameters:
        :   - **text** (*str*) – a text string, UTF-8 encoded.
            - **fontsize** (*float*) – the [`fontsize`](glossary.html#fontsize "fontsize").

        Return type:
        :   float

        Returns:
        :   the length of the string in points when stored in the PDF. If a character is not contained in the font, it will automatically be looked up in a fallback font.

            Note

            This method was originally implemented in Python, based on calling [`Font.glyph_advance()`](#Font.glyph_advance "Font.glyph_advance"). For performance reasons, it has been rewritten in C for v1.18.14. To compute the width of a single character, you can now use either of the following without performance penalty:

            1. `font.glyph_advance(ord("Ä")) * fontsize`
            2. `font.text_length("Ä", fontsize=fontsize)`

            For multi-character strings, the method offers a huge performance advantage compared to the previous implementation: instead of about 0.5 microseconds for each character, only 12.5 nanoseconds are required for the second and subsequent ones.

    char\_lengths(*text*, *fontsize=11*)
    :   *New in v1.18.14*

        Sequence of character lengths in points of a unicode string.

        Parameters:
        :   - **text** (*str*) – a text string, UTF-8 encoded.
            - **fontsize** (*float*) – the [`fontsize`](glossary.html#fontsize "fontsize").

        Return type:
        :   tuple

        Returns:
        :   the lengths in points of the characters of a string when stored in the PDF. It works like [`Font.text_length()`](#Font.text_length "Font.text_length") broken down to single characters. This is a high speed method, used e.g. in [`TextWriter.fill_textbox()`](textwriter.html#TextWriter.fill_textbox "TextWriter.fill_textbox"). The following is true (allowing rounding errors): `font.text_length(text) == sum(font.char_lengths(text))`.

            ```
            >>> font = pymupdf.Font("helv")
            >>> text = "PyMuPDF"
            >>> font.text_length(text)
            50.115999937057495
            >>> pymupdf.get_text_length(text, fontname="helv")
            50.115999937057495
            >>> sum(font.char_lengths(text))
            50.115999937057495
            >>> pprint(font.char_lengths(text))
            (7.336999952793121,  # P
            5.5,                 # y
            9.163000047206879,   # M
            6.115999937057495,   # u
            7.336999952793121,   # P
            7.942000031471252,   # D
            6.721000015735626)   # F
            ```

    buffer
    :   - New in v1.17.6

        Copy of the binary font file content.

        Return type:
        :   bytes

    flags
    :   A dictionary with various font properties, each represented as bools. Example for Helvetica:

        ```
        >>> pprint(font.flags)
        {'bold': 0,
        'fake-bold': 0,
        'fake-italic': 0,
        'invalid-bbox': 0,
        'italic': 0,
        'mono': 0,
        'opentype': 0,
        'serif': 1,
        'stretch': 0,
        'substitute': 0}
        ```

        Return type:
        :   dict

    name
    :   Return type:
        :   str

        Name of the font. May be “” or “(null)”.

    bbox
    :   The font bbox. This is the maximum of its glyph bboxes.

        Return type:
        :   [Rect](rect.html#rect)

    glyph\_count
    :   Return type:
        :   int

        The number of glyphs defined in the font.

    ascender
    :   - New in v1.18.0

        The ascender value of the font, see [ascender typography](https://en.wikipedia.org/wiki/Ascender_(typography)) for details. Please note that there is a difference to the strict definition: our value includes everything above the baseline – not just the height difference between upper case “A” and and lower case “a”.

        Return type:
        :   float

    descender
    :   - New in v1.18.0

        The descender value of the font, see [descender typography](https://en.wikipedia.org/wiki/Descender) for details. This value always is negative and is the portion that some glyphs descend below the base line, for example “g” or “y”. As a consequence, the value `ascender - descender` is the total height, that every glyph of the font fits into. This is true at least for most fonts – as always, there are exceptions, especially for calligraphic fonts, etc.

        Return type:
        :   float

    is\_bold

    is\_italic

    is\_monospaced

    is\_serif
    :   A number of attributes with obvious meanings. Reflect some values of the [`Font.flags`](#Font.flags "Font.flags") dictionary.

        Return type:
        :   bool

Footnotes

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.