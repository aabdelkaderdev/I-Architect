<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.linkcolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L733 "View st.LinkColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.LinkColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, max\_chars=None, validate=None, display\_text=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. If this is None (default), Streamlit will enable editing wherever possible.  If a column has mixed types, it may become uneditable regardless of disabled. |
| required (bool or None) | Whether edited cells in the column need to have a value. If this is False (default), the user can submit empty values for this column. If this is True, an edited cell in this column can only be submitted if its value is not None, and a new row will only be submitted after the user fills in this column. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (str or None) | Specifies the default value in this column when a new row is added by the user. This defaults to None. |
| max\_chars (int or None) | The maximum number of characters that can be entered. If this is None (default), there will be no maximum. |
| validate (str or None) | A JS-flavored regular expression (e.g. "^https://.+$") that edited values are validated against. If the user input is invalid, it will not be submitted. |
| display\_text (str or None) | The text that is displayed in the cell. This can be one of the following:   - None (default) to display the URL itself. - A string that is displayed in every cell, e.g. "Open link". - A Material icon that is displayed in every cell, e.g. ":material/open\_in\_new:". - A JS-flavored regular expression (detected by usage of parentheses)   to extract a part of the URL via a capture group. For example, use   "https://(.\*?)\.example\.com" to extract the display text   "foo" from the URL "https://foo.example.com".   For more complex cases, you may use [Pandas Styler's format](https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.format.html) function on the underlying dataframe. Note that this makes the app slow, doesn't work with editable columns, and might be removed in the future. Text formatting from column\_config always takes precedence over text formatting from pandas.Styler. |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "apps": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
        "creator": [
            "https://github.com/streamlit",
            "https://github.com/arnaudmiribel",
            "https://github.com/streamlit",
            "https://github.com/streamlit",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "apps": st.column_config.LinkColumn(
            "Trending apps",
            help="The top trending Streamlit apps",
            validate=r"^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text=r"https://(.*?)\.streamlit\.app"
        ),
        "creator": st.column_config.LinkColumn(
            "App Creator", display_text="Open profile"
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-link-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: List column](/develop/api-reference/data/st.column_config/st.column_config.listcolumn)[*arrow\_forward*Next: Image column](/develop/api-reference/data/st.column_config/st.column_config.imagecolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI