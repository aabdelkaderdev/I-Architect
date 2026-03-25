<!-- Source: https://pymupdf.readthedocs.io/en/latest/irect.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# IRect

IRect is a rectangular bounding box, very similar to [Rect](rect.html#rect), except that all corner coordinates are integers. IRect is used to specify an area of pixels, e.g. to receive image data during rendering. Otherwise, e.g. considerations concerning emptiness and validity of rectangles also apply to this class. Methods and attributes have the same names, and in many cases are implemented by re-using the respective [Rect](rect.html#rect) counterparts.

| **Attribute / Method** | **Short Description** |
| --- | --- |
| [`IRect.contains()`](#IRect.contains "IRect.contains") | checks containment of another object |
| [`IRect.get_area()`](#IRect.get_area "IRect.get_area") | calculate rectangle area |
| [`IRect.intersect()`](#IRect.intersect "IRect.intersect") | common part with another rectangle |
| [`IRect.intersects()`](#IRect.intersects "IRect.intersects") | checks for non-empty intersection |
| [`IRect.morph()`](#IRect.morph "IRect.morph") | transform with a point and a matrix |
| [`IRect.torect()`](#IRect.torect "IRect.torect") | matrix that transforms to another rectangle |
| [`IRect.norm()`](#IRect.norm "IRect.norm") | the Euclidean norm |
| [`IRect.normalize()`](#IRect.normalize "IRect.normalize") | makes a rectangle finite |
| [`IRect.bottom_left`](#IRect.bottom_left "IRect.bottom_left") | bottom left point, synonym *bl* |
| [`IRect.bottom_right`](#IRect.bottom_right "IRect.bottom_right") | bottom right point, synonym *br* |
| [`IRect.height`](#IRect.height "IRect.height") | height of the rectangle |
| [`IRect.is_empty`](#IRect.is_empty "IRect.is_empty") | whether rectangle is empty |
| [`IRect.is_infinite`](#IRect.is_infinite "IRect.is_infinite") | whether rectangle is infinite |
| [`IRect.rect`](#IRect.rect "IRect.rect") | the [Rect](rect.html#rect) equivalent |
| [`IRect.top_left`](#IRect.top_left "IRect.top_left") | top left point, synonym *tl* |
| [`IRect.top_right`](#IRect.top_right "IRect.top_right") | top\_right point, synonym *tr* |
| [`IRect.quad`](#IRect.quad "IRect.quad") | [Quad](quad.html#quad) made from rectangle corners |
| [`IRect.width`](#IRect.width "IRect.width") | width of the rectangle |
| [`IRect.x0`](#IRect.x0 "IRect.x0") | X-coordinate of the top left corner |
| [`IRect.x1`](#IRect.x1 "IRect.x1") | X-coordinate of the bottom right corner |
| [`IRect.y0`](#IRect.y0 "IRect.y0") | Y-coordinate of the top left corner |
| [`IRect.y1`](#IRect.y1 "IRect.y1") | Y-coordinate of the bottom right corner |

**Class API**

*class* IRect
:   \_\_init\_\_(*self*)

    \_\_init\_\_(*self*, *x0*, *y0*, *x1*, *y1*)

    \_\_init\_\_(*self*, *irect*)

    \_\_init\_\_(*self*, *sequence*)
    :   Overloaded constructors. Also see examples below and those for the [Rect](rect.html#rect) class.

        If another irect is specified, a **new copy** will be made.

        If sequence is specified, it must be a Python sequence type of 4 numbers (see [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes)). Non-integer numbers will be truncated, non-numeric values will raise an exception.

        The other parameters mean integer coordinates.

    get\_area([*unit*])
    :   Calculates the area of the rectangle and, with no parameter, equals *abs(IRect)*. Like an empty rectangle, the area of an infinite rectangle is also zero.

        Parameters:
        :   **unit** (*str*) – Specify required unit: respective squares of “px” (pixels, default), “in” (inches), “cm” (centimeters), or “mm” (millimeters).

        Return type:
        :   float

    intersect(*ir*)
    :   The intersection (common rectangular area) of the current rectangle and *ir* is calculated and replaces the current rectangle. If either rectangle is empty, the result is also empty. If either rectangle is infinite, the other one is taken as the result – and hence also infinite if both rectangles were infinite.

        Parameters:
        :   **ir** (*rect\_like*) – Second rectangle.

    contains(*x*)
    :   Checks whether *x* is contained in the rectangle. It may be [`rect_like`](glossary.html#rect_like "rect_like"), [`point_like`](glossary.html#point_like "point_like") or a number. If *x* is an empty rectangle, this is always true. Conversely, if the rectangle is empty this is always `False`, if *x* is not an empty rectangle and not a number. If *x* is a number, it will be checked to be one of the four components. *x in irect* and *irect.contains(x)* are equivalent.

        Parameters:
        :   **x** ([IRect](#irect) or [Rect](rect.html#rect) or [Point](point.html#point) or `int`.) – the object to check.

        Return type:
        :   bool

    intersects(*r*)
    :   Checks whether the rectangle and the [`rect_like`](glossary.html#rect_like "rect_like") “r” contain a common non-empty [IRect](#irect). This will always be `False` if either is infinite or empty.

        Parameters:
        :   **r** (*rect\_like*) – the rectangle to check.

        Return type:
        :   bool

    torect(*rect*)
    :   - New in version 1.19.3

        Compute the matrix which transforms this rectangle to a given one. See [`Rect.torect()`](rect.html#Rect.torect "Rect.torect").

        Parameters:
        :   **rect** (*rect\_like*) – the target rectangle. Must not be empty or infinite.

        Return type:
        :   [Matrix](matrix.html#matrix)

        Returns:
        :   a matrix `mat` such that `self * mat = rect`. Can for example be used to transform between the page and the pixmap coordinates.

    morph(*fixpoint*, *matrix*)
    :   - New in version 1.17.0

        Return a new quad after applying a matrix to it using a fixed point.

        Parameters:
        :   - **fixpoint** (*point\_like*) – the fixed point.
            - **matrix** (*matrix\_like*) – the matrix.

        Returns:
        :   a new [Quad](quad.html#quad). This a wrapper of the same-named quad method. If infinite, the infinite quad is returned.

    norm()
    :   - New in version 1.16.0

        Return the Euclidean norm of the rectangle treated as a vector of four numbers.

    normalize()
    :   Make the rectangle finite. This is done by shuffling rectangle corners. After this, the bottom right corner will indeed be south-eastern to the top left one. See [Rect](rect.html#rect) for a more details.

    top\_left

    tl
    :   Equals *Point(x0, y0)*.

        Type:
        :   [Point](point.html#point)

    top\_right

    tr
    :   Equals *Point(x1, y0)*.

        Type:
        :   [Point](point.html#point)

    bottom\_left

    bl
    :   Equals *Point(x0, y1)*.

        Type:
        :   [Point](point.html#point)

    bottom\_right

    br
    :   Equals *Point(x1, y1)*.

        Type:
        :   [Point](point.html#point)

    rect
    :   The [Rect](rect.html#rect) with the same coordinates as floats.

        Type:
        :   [Rect](rect.html#rect)

    quad
    :   The quadrilateral *Quad(irect.tl, irect.tr, irect.bl, irect.br)*.

        Type:
        :   [Quad](quad.html#quad)

    width
    :   Contains the width of the bounding box. Equals *abs(x1 - x0)*.

        Type:
        :   int

    height
    :   Contains the height of the bounding box. Equals *abs(y1 - y0)*.

        Type:
        :   int

    x0
    :   X-coordinate of the left corners.

        Type:
        :   int

    y0
    :   Y-coordinate of the top corners.

        Type:
        :   int

    x1
    :   X-coordinate of the right corners.

        Type:
        :   int

    y1
    :   Y-coordinate of the bottom corners.

        Type:
        :   int

    is\_infinite
    :   `True` if rectangle is infinite, `False` otherwise.

        Type:
        :   bool

    is\_empty
    :   `True` if rectangle is empty, `False` otherwise.

        Type:
        :   bool

Note

- This class adheres to the Python sequence protocol, so components can be accessed via their index, too. Also refer to [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes).
- Rectangles can be used with arithmetic operators – see chapter [Operator Algebra for Geometry Objects](algebra.html#algebra).

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.