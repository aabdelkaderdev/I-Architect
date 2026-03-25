<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.progresscolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L2455 "View st.ProgressColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.ProgressColumn(label=None, \*, width=None, help=None, pinned=None, format=None, min\_value=None, max\_value=None, step=None, color=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| format (str, "plain", "localized", "percent", "dollar", "euro", "yen", "accounting", "compact", "scientific", "engineering", or None) | A format string controlling how the numbers are displayed. This can be one of the following values:   - None (default): Streamlit infers the formatting from the data. - "plain": Show the full number without any formatting (e.g. "1234.567"). - "localized": Show the number in the default locale format (e.g. "1,234.567"). - "percent": Show the number as a percentage (e.g. "123456.70%"). - "dollar": Show the number as a dollar amount (e.g. "$1,234.57"). - "euro": Show the number as a euro amount (e.g. "€1,234.57"). - "yen": Show the number as a yen amount (e.g. "¥1,235"). - "accounting": Show the number in an accounting format (e.g. "1,234.00"). - "bytes": Show the number in a byte format (e.g. "1.2KB"). - "compact": Show the number in a compact format (e.g. "1.2K"). - "scientific": Show the number in scientific notation (e.g. "1.235E3"). - "engineering": Show the number in engineering notation (e.g. "1.235E3"). - printf-style format string: Format the number with a printf   specifier, like "%d" to show a signed integer (e.g. "1234") or   "%X" to show an unsigned hexadecimal integer (e.g. "4D2"). You   can also add prefixes and suffixes. To show British pounds, use   "£ %.2f" (e.g. "£ 1234.57"). Use , for thousand separators   (e.g. "%,d" yields "1,234"). For more information, see   [sprintf-js](https://github.com/alexei/sprintf.js?tab=readme-ov-file#format-specification).   Number formatting from column\_config always takes precedence over number formatting from pandas.Styler. The number formatting does not impact the return value when used in st.data\_editor. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| min\_value (int, float, or None) | The minimum value of the progress bar. If this is None (default), the minimum will be 0. |
| max\_value (int, float, or None) | The maximum value of the progress bar. If this is None (default), the maximum will be 100 for integer values and 1.0 for float values. |
| step (int, float, or None) | The precision of numbers. If this is None (default), integer columns will have a step of 1 and float columns will have a step of 0.01. Setting step for float columns will ensure a consistent number of digits after the decimal are displayed. |
| color ("auto", "auto-inverse", str, or None) | The color to use for the chart. This can be one of the following:   - None (default): The primary color is used. - "auto": If the value is more than half, the bar is green; if the   value is less than half, the bar is red. - "auto-inverse": If the value is more than half, the bar is red;   if the value is less than half, the bar is green. - A single color value that is applied to all charts in the column.   In addition to the basic color palette (red, orange, yellow, green,   blue, violet, gray/grey, and primary), this supports hex codes like   "#483d8b". |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "sales": [200, 550, 1000, 80],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.ProgressColumn(
            "Sales volume",
            help="The sales volume in USD",
            format="$%f",
            min_value=0,
            max_value=1000,
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-progress-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Bar chart column](/develop/api-reference/data/st.column_config/st.column_config.barchartcolumn)[*arrow\_forward*Next: st.table](/develop/api-reference/data/st.table)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI