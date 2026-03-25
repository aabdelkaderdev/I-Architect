<!-- Source: https://pymupdf.readthedocs.io/en/latest/point.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# Point

*Point* represents a point in the plane, defined by its x and y coordinates.

| **Attribute / Method** | **Description** |
| --- | --- |
| [`Point.distance_to()`](#Point.distance_to "Point.distance_to") | calculate distance to point or rect |
| [`Point.norm()`](#Point.norm "Point.norm") | the Euclidean norm |
| [`Point.transform()`](#Point.transform "Point.transform") | transform point with a matrix |
| [`Point.abs_unit`](#Point.abs_unit "Point.abs_unit") | same as unit, but positive coordinates |
| [`Point.unit`](#Point.unit "Point.unit") | point coordinates divided by *abs(point)* |
| [`Point.x`](#Point.x "Point.x") | the X-coordinate |
| [`Point.y`](#Point.y "Point.y") | the Y-coordinate |

**Class API**

*class* Point
:   \_\_init\_\_(*self*)

    \_\_init\_\_(*self*, *x*, *y*)

    \_\_init\_\_(*self*, *point*)

    \_\_init\_\_(*self*, *sequence*)
    :   > Overloaded constructors.
        >
        > Without parameters, *Point(0, 0)* will be created.
        >
        > With another point specified, a **new copy** will be created, “sequence” is a Python sequence of 2 numbers (see [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes)).

        Parameters:
        :   - **x** (*float*) – x coordinate of the point
            - **y** (*float*) – y coordinate of the point

    distance\_to(*x*[, *unit*])
    :   > Calculate the distance to *x*, which may be [`point_like`](glossary.html#point_like "point_like") or [`rect_like`](glossary.html#rect_like "rect_like"). The distance is given in units of either pixels (default), inches, centimeters or millimeters.

        Parameters:
        :   - **x** (*point\_like**,**rect\_like*) – to which to compute the distance.
            - **unit** (*str*) – the unit to be measured in. One of “px”, “in”, “cm”, “mm”.

        Return type:
        :   float

        Returns:
        :   the distance to *x*. If this is [`rect_like`](glossary.html#rect_like "rect_like"), then the distance

            - is the length of the shortest line connecting to one of the rectangle sides
            - is calculated to the **finite version** of it
            - is zero if it **contains** the point

    norm()
    :   - New in version 1.16.0

        Return the Euclidean norm (the length) of the point as a vector. Equals result of function *abs()*.

    transform(*m*)
    :   > Apply a matrix to the point and replace it with the result.

        Parameters:
        :   **m** (*matrix\_like*) – The matrix to be applied.

        Return type:
        :   [Point](#point)

    unit
    :   Result of dividing each coordinate by *norm(point)*, the distance of the point to (0,0). This is a vector of length 1 pointing in the same direction as the point does. Its x, resp. y values are equal to the cosine, resp. sine of the angle this vector (and the point itself) has with the x axis.

        Type:
        :   [Point](#point)

    abs\_unit
    :   Same as [`unit`](#Point.unit "Point.unit") above, replacing the coordinates with their absolute values.

        Type:
        :   [Point](#point)

    x
    :   The x coordinate

        Type:
        :   float

    y
    :   The y coordinate

        Type:
        :   float

Note

- This class adheres to the Python sequence protocol, so components can be accessed via their index, too. Also refer to [Using Python Sequences as Arguments in PyMuPDF](app3.html#sequencetypes).
- Rectangles can be used with arithmetic operators – see chapter [Operator Algebra for Geometry Objects](algebra.html#algebra).

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.