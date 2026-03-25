<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.metric -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/metric.py#L98 "View st.metric source code on GitHub") | |
| --- | --- |
| st.metric(label, value, delta=None, delta\_color="normal", \*, help=None, label\_visibility="visible", border=False, width="stretch", height="content", chart\_data=None, chart\_type="line", delta\_arrow="auto", format=None, delta\_description=None) | |
| Parameters | |
| label (str) | The header or title for the metric. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| value (int, float, decimal.Decimal, str, or None) | Value of the metric. None is rendered as a long dash.  The value can optionally contain GitHub-flavored Markdown, subject to the same limitations described in the label parameter. |
| delta (int, float, decimal.Decimal, str, or None) | Amount or indicator of change in the metric. An arrow is shown next to the delta, oriented according to its sign:   - If the delta is None or an empty string, no arrow is shown. - If the delta is a negative number or starts with a minus sign,   the arrow points down and the delta is red. - Otherwise, the arrow points up and the delta is green.   You can modify the display, color, and orientation of the arrow using the delta\_color and delta\_arrow parameters.  The delta can optionally contain GitHub-flavored Markdown, subject to the same limitations described in the label parameter. |
| delta\_color (str) | The color of the delta and chart. This can be one of the following:   - "normal" (default): The color is red when the delta is   negative and green otherwise. - "inverse": The color is green when the delta is negative and   red otherwise. This is useful when a negative change is   considered good, like a decrease in cost. - "off": The color is gray regardless of the delta. - A named color from the basic palette: The chart and delta are the   specified color regardless of their value. This can be one of the   following: "red", "orange", "yellow", "green",   "blue", "violet", "gray"/"grey", or   "primary". |
| help (str or None) | A tooltip that gets displayed next to the metric label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| border (bool) | Whether to show a border around the metric container. If this is False (default), no border is shown. If this is True, a border is shown. |
| height ("content", "stretch", or int) | The height of the metric element. This can be one of the following:   - "content" (default): The height of the element matches the   height of its content. - "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. - An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. |
| width ("stretch", "content", or int) | The width of the metric element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| chart\_data (Iterable or None) | A sequence of numeric values to display as a sparkline chart. If this is None (default), no chart is displayed. The sequence can be anything supported by st.dataframe, including a list or set. If the sequence is dataframe-like, the first column will be used. Each value will be cast to float internally by default.  The chart uses the color of the delta indicator, which can be modified using the delta\_color parameter. |
| chart\_type ("line", "bar", or "area") | The type of sparkline chart to display. This can be one of the following:   - "line" (default): A simple sparkline. - "area": A sparkline with area shading. - "bar": A bar chart. |
| delta\_arrow ("auto", "up", "down", or "off") | Controls the direction of the delta indicator arrow. This can be one of the following strings:   - "auto" (default): The arrow direction follows the sign of   delta. - "up" or "down": The arrow is forced to point in the   specified direction. - "off": No arrow is shown, but the delta value remains   visible. |
| format (str or None) | A format string controlling how numbers are displayed for value and delta. The format is only applied if the value or delta is numeric. If the value or delta is a string with non-numeric characters, the format is ignored. The format can be one of the following values:   - None (default): No formatting is applied. - "plain": Show the full number without any formatting (e.g. "1234.567"). - "localized": Show the number in the default locale format (e.g. "1,234.567"). - "percent": Show the number as a percentage (e.g. "123456.70%"). - "dollar": Show the number as a dollar amount (e.g. "$1,234.57"). - "euro": Show the number as a euro amount (e.g. "€1,234.57"). - "yen": Show the number as a yen amount (e.g. "¥1,235"). - "accounting": Show the number in an accounting format (e.g. "1,234.00"). - "bytes": Show the number in a byte format (e.g. "1.2KB"). - "compact": Show the number in a compact format (e.g. "1.2K"). - "scientific": Show the number in scientific notation (e.g. "1.235E3"). - "engineering": Show the number in engineering notation (e.g. "1.235E3"). - printf-style format string: Format the number with a printf   specifier, like "%d" to show a signed integer (e.g. "1234") or   "%.2f" to show a float with 2 decimal places. Use , for   thousand separators (e.g. "%,d" yields "1,234"). |
| delta\_description (str or None) | A short description displayed next to the delta value, such as "month over month" or "vs. last quarter". If this is None (default), no description is shown. The description is displayed in a smaller, muted font style similar to st.caption. |

#### Examples

> **Example 1: Show a metric**
>
> ```
> import streamlit as st
>
> st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
> ```
>
> [Built with Streamlit 🎈](https://streamlit.io)
>
> [Fullscreen *open\_in\_new*](https://doc-metric-example1.streamlit.app//?utm_medium=oembed&)
>
> **Example 2: Create a row of metrics**
>
> st.metric looks especially nice in combination with st.columns.
>
> ```
> import streamlit as st
>
> col1, col2, col3 = st.columns(3)
> col1.metric("Temperature", "70 °F", "1.2 °F")
> col2.metric("Wind", "9 mph", "-8%")
> col3.metric("Humidity", "86%", "4%")
> ```
>
> [Built with Streamlit 🎈](https://streamlit.io)
>
> [Fullscreen *open\_in\_new*](https://doc-metric-example2.streamlit.app//?utm_medium=oembed&)
>
> **Example 3: Modify the delta indicator**
>
> The delta indicator color can also be inverted or turned off.
>
> ```
> import streamlit as st
>
> st.metric(
>     label="Gas price", value=4, delta=-0.5, delta_color="inverse"
> )
>
> st.metric(
>     label="Active developers",
>     value=123,
>     delta=123,
>     delta_color="off",
> )
> ```
>
> [Built with Streamlit 🎈](https://streamlit.io)
>
> [Fullscreen *open\_in\_new*](https://doc-metric-example3.streamlit.app//?utm_medium=oembed&)
>
> **Example 4: Create a grid of metric cards**
>
> Add borders to your metrics to create a dashboard look.
>
> ```
> import streamlit as st
>
> a, b = st.columns(2)
> c, d = st.columns(2)
>
> a.metric("Temperature", "30°F", "-9°F", border=True)
> b.metric("Wind", "4 mph", "2 mph", border=True)
>
> c.metric("Humidity", "77%", "5%", border=True)
> d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)
> ```
>
> [Built with Streamlit 🎈](https://streamlit.io)
>
> [Fullscreen *open\_in\_new*](https://doc-metric-example4.streamlit.app//?utm_medium=oembed&)
>
> **Example 5: Show sparklines**
>
> To show trends over time, add sparklines.
>
> ```
> import streamlit as st
> from numpy.random import default_rng as rng
>
> changes = list(rng(4).standard_normal(20))
> data = [sum(changes[:i]) for i in range(20)]
> delta = round(data[-1], 2)
>
> row = st.container(horizontal=True)
> with row:
>     st.metric(
>         "Line", 10, delta, chart_data=data, chart_type="line", border=True
>     )
>     st.metric(
>         "Area", 10, delta, chart_data=data, chart_type="area", border=True
>     )
>     st.metric(
>         "Bar", 10, delta, chart_data=data, chart_type="bar", border=True
>     )
> ```
>
> [Built with Streamlit 🎈](https://streamlit.io)
>
> [Fullscreen *open\_in\_new*](https://doc-metric-example5.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.table](/develop/api-reference/data/st.table)[*arrow\_forward*Next: st.json](/develop/api-reference/data/st.json)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI