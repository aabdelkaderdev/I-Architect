<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.selectboxcolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L1010 "View st.SelectboxColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.SelectboxColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, options=None, format\_func=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. If this is None (default), Streamlit will enable editing wherever possible.  If a column has mixed types, it may become uneditable regardless of disabled. |
| required (bool or None) | Whether edited cells in the column need to have a value. If this is False (default), the user can submit empty values for this column. If this is True, an edited cell in this column can only be submitted if its value is not None, and a new row will only be submitted after the user fills in this column. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (str, int, float, bool, or None) | Specifies the default value in this column when a new row is added by the user. This defaults to None. |
| options (Iterable[str, int, float, bool] or None) | The options that can be selected during editing. If this is None (default), the options will be inferred from the underlying dataframe column if its dtype is "category". For more information, see [Pandas docs](https://pandas.pydata.org/docs/user_guide/categorical.html)). |
| format\_func (function or None) | Function to modify the display of the options. It receives the raw option defined in options as an argument and should output the label to be shown for that option. If this is None (default), the raw option is used as the label. |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        )
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-selectbox-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Checkbox column](/develop/api-reference/data/st.column_config/st.column_config.checkboxcolumn)[*arrow\_forward*Next: Multiselect column](/develop/api-reference/data/st.column_config/st.column_config.multiselectcolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI