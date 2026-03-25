<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.numbercolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L439 "View st.NumberColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.NumberColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, format=None, min\_value=None, max\_value=None, step=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. If this is None (default), Streamlit will enable editing wherever possible.  If a column has mixed types, it may become uneditable regardless of disabled. |
| required (bool or None) | Whether edited cells in the column need to have a value. If this is False (default), the user can submit empty values for this column. If this is True, an edited cell in this column can only be submitted if its value is not None, and a new row will only be submitted after the user fills in this column. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (int, float, or None) | Specifies the default value in this column when a new row is added by the user. This defaults to None. |
| format (str, "plain", "localized", "percent", "dollar", "euro", "yen", "accounting", "compact", "scientific", "engineering", or None) | A format string controlling how numbers are displayed. This can be one of the following values:   - None (default): Streamlit infers the formatting from the data. - "plain": Show the full number without any formatting (e.g. "1234.567"). - "localized": Show the number in the default locale format (e.g. "1,234.567"). - "percent": Show the number as a percentage (e.g. "123456.70%"). - "dollar": Show the number as a dollar amount (e.g. "$1,234.57"). - "euro": Show the number as a euro amount (e.g. "€1,234.57"). - "yen": Show the number as a yen amount (e.g. "¥1,235"). - "accounting": Show the number in an accounting format (e.g. "1,234.00"). - "bytes": Show the number in a byte format (e.g. "1.2KB"). - "compact": Show the number in a compact format (e.g. "1.2K"). - "scientific": Show the number in scientific notation (e.g. "1.235E3"). - "engineering": Show the number in engineering notation (e.g. "1.235E3"). - printf-style format string: Format the number with a printf   specifier, like "%d" to show a signed integer (e.g. "1234") or   "%X" to show an unsigned hexadecimal integer (e.g. "4D2"). You   can also add prefixes and suffixes. To show British pounds, use   "£ %.2f" (e.g. "£ 1234.57"). Use , for thousand separators   (e.g. "%,d" yields "1,234"). For more information, see   [sprintf-js](https://github.com/alexei/sprintf.js?tab=readme-ov-file#format-specification).   Formatting from column\_config always takes precedence over formatting from pandas.Styler. The formatting does not impact the return value when used in st.data\_editor. |
| min\_value (int, float, or None) | The minimum value that can be entered. If this is None (default), there will be no minimum. |
| max\_value (int, float, or None) | The maximum value that can be entered. If this is None (default), there will be no maximum. |
| step (int, float, or None) | The precision of numbers that can be entered. If this None (default), integer columns will have a step of 1 and float columns will have unrestricted precision. In this case, some floats may display like integers. Setting step for float columns will ensure a consistent number of digits after the decimal are displayed.  If format is a predefined format like "dollar", step overrides the display precision. If format is a printf-style format string, step will not change the display precision. |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "price": [20, 950, 250, 500],
    }
)

st.data_editor(
    data_df,
    column_config={
        "price": st.column_config.NumberColumn(
            "Price (in USD)",
            help="The price of the product in USD",
            min_value=0,
            max_value=1000,
            step=1,
            format="$%d",
        )
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-number-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Text column](/develop/api-reference/data/st.column_config/st.column_config.textcolumn)[*arrow\_forward*Next: Checkbox column](/develop/api-reference/data/st.column_config/st.column_config.checkboxcolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI